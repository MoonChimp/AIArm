"""
RunwayML API Integration
Provides AI video generation capabilities
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, Optional

class RunwayMLClient:
    """Client for RunwayML Gen-2/Gen-3 API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize RunwayML client

        Args:
            api_key: RunwayML API key (or set RUNWAYML_API_KEY env var)
        """
        import os
        self.api_key = api_key or os.getenv("RUNWAYML_API_KEY")
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_video_from_text(self, prompt: str, duration: int = 5, options: dict = None) -> Dict:
        """
        Generate video from text prompt using Gen-2/Gen-3

        Args:
            prompt: Text description of video
            duration: Video duration in seconds (max 10)
            options: Additional generation options

        Returns:
            Dict with status, task_id, and eventually video_url
        """
        options = options or {}

        payload = {
            "text_prompt": prompt,
            "duration": min(duration, 10),
            "ratio": options.get("ratio", "16:9"),
            "watermark": options.get("watermark", False)
        }

        try:
            print(f"[RunwayML] Submitting video generation request...")
            response = requests.post(
                f"{self.base_url}/text_to_video",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                task_id = data.get("id")

                print(f"[RunwayML] Task created: {task_id}")

                # Poll for completion
                return self._wait_for_completion(task_id)
            else:
                return {
                    "status": "error",
                    "message": f"RunwayML API error: {response.status_code} - {response.text}"
                }

        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Request timeout"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def generate_video_from_image(self, image_path: str, prompt: str, duration: int = 5) -> Dict:
        """
        Generate video from image + text prompt

        Args:
            image_path: Path to source image
            prompt: Text description for motion
            duration: Video duration in seconds

        Returns:
            Dict with status and video_url
        """
        try:
            # Upload image first
            with open(image_path, 'rb') as f:
                files = {'file': f}
                upload_response = requests.post(
                    f"{self.base_url}/uploads",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files
                )

            if upload_response.status_code != 200:
                return {"status": "error", "message": "Image upload failed"}

            image_id = upload_response.json().get("id")

            # Generate video
            payload = {
                "image_id": image_id,
                "text_prompt": prompt,
                "duration": min(duration, 10)
            }

            response = requests.post(
                f"{self.base_url}/image_to_video",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                task_id = response.json().get("id")
                return self._wait_for_completion(task_id)
            else:
                return {"status": "error", "message": response.text}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _wait_for_completion(self, task_id: str, max_wait: int = 300) -> Dict:
        """
        Poll task until completion

        Args:
            task_id: RunwayML task ID
            max_wait: Maximum wait time in seconds

        Returns:
            Dict with final status and video_url
        """
        start_time = time.time()

        while (time.time() - start_time) < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers=self.headers
                )

                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")

                    if status == "SUCCEEDED":
                        print(f"[RunwayML] Video generation complete!")
                        return {
                            "status": "success",
                            "video_url": data.get("output", {}).get("url"),
                            "task_id": task_id
                        }
                    elif status == "FAILED":
                        return {
                            "status": "error",
                            "message": data.get("error", "Generation failed")
                        }
                    else:
                        # Still processing
                        print(f"[RunwayML] Status: {status} - waiting...")
                        time.sleep(5)
                else:
                    return {"status": "error", "message": "Status check failed"}

            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "timeout", "message": "Video generation timeout"}

    def download_video(self, video_url: str, output_path: str) -> Dict:
        """
        Download generated video

        Args:
            video_url: URL from RunwayML
            output_path: Local path to save video

        Returns:
            Dict with status and filepath
        """
        try:
            print(f"[RunwayML] Downloading video...")
            response = requests.get(video_url, stream=True, timeout=120)

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"[RunwayML] Video saved to {output_path}")
                return {
                    "status": "success",
                    "filepath": str(output_path)
                }
            else:
                return {"status": "error", "message": "Download failed"}

        except Exception as e:
            return {"status": "error", "message": str(e)}


# Usage instructions
SETUP_INSTRUCTIONS = """
RunwayML Integration Setup
===========================

1. Get API Key:
   - Go to https://runwayml.com/
   - Sign up / Log in
   - Navigate to Settings > API Keys
   - Create new API key

2. Set Environment Variable:
   Windows:
   setx RUNWAYML_API_KEY "your-api-key-here"

   Linux/Mac:
   export RUNWAYML_API_KEY="your-api-key-here"

3. Restart Nexus after setting the key

Pricing (as of 2024):
- Gen-2: ~$0.05/second of video
- Gen-3: ~$0.10/second of video
- Credits purchased in packages

Features:
- Text-to-video generation
- Image-to-video animation
- Up to 10 seconds per generation
- Multiple aspect ratios
- High quality output
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)

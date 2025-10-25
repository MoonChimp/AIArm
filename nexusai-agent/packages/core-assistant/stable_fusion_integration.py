
import requests
import json
import base64
from typing import Optional, Dict, Any

class StableFusion:
    def __init__(self, api_key: str = None, host: str = "http://127.0.0.1:7860"):
        """Initialize Stable Fusion client
        Args:
            api_key (str, optional): API key if using hosted service
            host (str, optional): Host URL for local installation
        """
        self.api_key = api_key
        self.host = host
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        steps: int = 20,
        width: int = 512,
        height: int = 512,
        guidance_scale: float = 7.5,
        num_images: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Generate image(s) from prompt
        
        Args:
            prompt (str): Text prompt
            negative_prompt (str, optional): Things to avoid in generation
            steps (int, optional): Number of denoising steps
            width (int, optional): Image width
            height (int, optional): Image height
            guidance_scale (float, optional): How closely to follow prompt
            num_images (int, optional): Number of images to generate
            
        Returns:
            Optional[Dict[str, Any]]: Generation results or None if failed
        """
        endpoint = f"{self.host}/v1/generation"
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "width": width,
            "height": height,
            "guidance_scale": guidance_scale,
            "num_images": num_images
        }

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error generating images: {str(e)}")
            return None

    def get_models(self) -> Optional[Dict[str, Any]]:
        """Get available models
        
        Returns:
            Optional[Dict[str, Any]]: Model info or None if failed
        """
        try:
            response = requests.get(
                f"{self.host}/v1/models",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting models: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = StableFusion()
    
    # Example: Generate an image
    result = client.generate_image(
        prompt="A serene mountain landscape at sunset",
        steps=30,
        width=768,
        height=512
    )
    
    if result and "images" in result:
        # Save generated images
        for i, image_data in enumerate(result["images"]):
            with open(f"generated_image_{i}.png", "wb") as f:
                f.write(base64.b64decode(image_data))
            print(f"Saved image {i}")

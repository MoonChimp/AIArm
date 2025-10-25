#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Photo Generation Agent
Actually generates images using Stable Diffusion WebUI API
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import requests
import base64
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealPhotoAgent(Agent):
    """Agent that ACTUALLY generates images using Stable Diffusion"""

    def __init__(self):
        super().__init__(
            name="PhotoGeneration",
            description="Generates REAL images using Stable Diffusion WebUI",
            capabilities=[
                "Generate images from text prompts",
                "Control image size and quality",
                "Apply negative prompts",
                "Save images to disk",
                "Multiple styles and settings"
            ]
        )
        self.generation_history = []
        self.output_dir = Path("D:/AIArm/Generated/Images")
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.webui_url = "http://localhost:7860"
        self.default_negative = "blurry, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, deformed, ugly, low quality, worst quality, jpeg artifacts, signature, watermark, username, text, error, mutation, disfigured, out of frame, cropped, nsfw, adult content, inappropriate, smoking, drugs, violence, explicit"

    def process(self, prompt, context=None, options=None):
        """Generate an actual image"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[PhotoGeneration] Generating image: {prompt[:60]}...")

        # Check if WebUI is running
        if not self._check_webui():
            return {
                "status": "error",
                "message": "Stable Diffusion WebUI not running. Start it at http://localhost:7860"
            }

        try:
            # Generate the image
            result = self._generate_image(prompt, options)

            if result["status"] == "success":
                # Save the image
                image_data = result["image_data"]
                image_id = str(uuid.uuid4())[:8]
                filename = f"nexus_image_{image_id}.png"
                filepath = self.output_dir / filename

                # Decode and save
                img_bytes = base64.b64decode(image_data)
                with open(filepath, 'wb') as f:
                    f.write(img_bytes)

                print(f"[PhotoGeneration] Image saved to {filename}")

                # Log generation
                gen_entry = {
                    "timestamp": self.last_used,
                    "prompt": prompt,
                    "filepath": str(filepath),
                    "options": options
                }
                self.generation_history.append(gen_entry)

                return {
                    "status": "success",
                    "filepath": str(filepath),
                    "filename": filename,
                    "prompt": prompt,
                    "message": f"Image generated and saved to {filename}"
                }
            else:
                return result

        except Exception as e:
            print(f"[PhotoGeneration] Error: {e}")
            return {
                "status": "error",
                "message": f"Image generation failed: {str(e)}"
            }

    def _check_webui(self):
        """Check if Stable Diffusion WebUI is running"""
        try:
            response = requests.get(f"{self.webui_url}/sdapi/v1/progress", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _generate_image(self, prompt, options):
        """Generate image using SD WebUI API"""
        try:
            # Enhance prompt for better quality
            enhanced_prompt = self._enhance_prompt(prompt, options)

            # Build request payload with optimized settings
            payload = {
                "prompt": enhanced_prompt,
                "negative_prompt": options.get("negative_prompt", self.default_negative),
                "steps": options.get("steps", 40),  # More steps = better quality
                "width": options.get("width", 768),  # Higher resolution
                "height": options.get("height", 768),
                "cfg_scale": options.get("cfg_scale", 8.5),  # Better prompt adherence
                "sampler_name": options.get("sampler", "DPM++ 2M Karras"),
                "seed": options.get("seed", -1),
                "restore_faces": options.get("restore_faces", True),  # Fix faces
                "enable_hr": options.get("enable_hr", False),  # Hires fix
                "denoising_strength": options.get("denoising_strength", 0.4),
                "clip_skip": options.get("clip_skip", 2)
            }

            print(f"[PhotoGeneration] Requesting image from WebUI...")

            response = requests.post(
                f"{self.webui_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=120  # Image generation takes time
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("images") and len(data["images"]) > 0:
                    return {
                        "status": "success",
                        "image_data": data["images"][0]  # Base64 encoded
                    }
                else:
                    return {
                        "status": "error",
                        "message": "WebUI returned no images"
                    }
            else:
                return {
                    "status": "error",
                    "message": f"WebUI returned status {response.status_code}"
                }

        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "Image generation timeout (120s)"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _enhance_prompt(self, prompt, options):
        """Enhance prompt with quality boosters - FAST fallback if AI fails"""
        # Skip AI enhancement - go straight to manual for speed and reliability
        # The AI model times out too often

        # Don't double-enhance if user already included quality terms
        if any(term in prompt.lower() for term in ["masterpiece", "best quality", "highly detailed"]):
            return prompt

        # Add comprehensive quality boosters
        quality_prefix = "masterpiece, best quality, highly detailed, sharp focus, professional, 8k uhd"

        # Strong negative to avoid bad content
        negative_additions = ", safe for work, appropriate, family friendly"

        # Check if style requested
        style = options.get("style", "realistic")
        style_suffix = self._get_style_prompt(style)

        enhanced = f"{quality_prefix}, {prompt}, {style_suffix}"
        print(f"[PhotoGeneration] Enhanced prompt: {enhanced}")
        return enhanced

    def _ai_enhance_prompt(self, simple_prompt):
        """Use AI model to create optimized SD prompt"""
        try:
            print(f"[PhotoGeneration] Enhancing prompt with AI...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "brxce/stable-diffusion-prompt-generator:latest",
                    "prompt": simple_prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                enhanced_prompt = data.get("response", "").strip()
                print(f"[PhotoGeneration] AI-enhanced: {enhanced_prompt[:100]}...")
                return enhanced_prompt
            else:
                return None

        except Exception as e:
            print(f"[PhotoGeneration] AI enhancement failed: {e}")
            return None

    def _get_style_prompt(self, style):
        """Get style-specific prompt additions"""
        styles = {
            "realistic": "photorealistic, 8k uhd, dslr, soft lighting, high quality, film grain",
            "artistic": "artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski",
            "anime": "anime style, key visual, vibrant, studio anime, highly detailed",
            "cinematic": "cinematic lighting, dramatic, volumetric lighting, film still, professional color grading",
            "fantasy": "fantasy art, magical, ethereal, dreamlike, mystical atmosphere, enchanting",
            "portrait": "professional portrait, studio lighting, bokeh, shallow depth of field, 85mm lens",
            "landscape": "landscape photography, golden hour, epic vista, atmospheric, hdr",
            "digital_art": "digital art, trending on artstation, detailed, vibrant colors, concept art"
        }
        return styles.get(style, "")

    def generate_with_style(self, prompt, style="realistic"):
        """Generate image with a specific style"""
        return self.process(prompt, options={"style": style, "steps": 50, "enable_hr": True})

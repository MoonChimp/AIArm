#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stable Diffusion Integration
Connects the Photo Generation Agent to the Stable Diffusion WebUI API
"""

import sys
import os
import json
import requests
import base64
from pathlib import Path
from datetime import datetime
import traceback

class StableDiffusionConnector:
    """Connector to Stable Diffusion WebUI API"""
    
    def __init__(self, base_url="http://127.0.0.1:7860"):
        """Initialize the connector"""
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.save_dir = Path("D:/AIArm/InnerLife/Generated/Images")
        self.save_dir.mkdir(exist_ok=True, parents=True)
    
    def check_connection(self):
        """Check if Stable Diffusion WebUI is running"""
        try:
            response = requests.get(f"{self.api_url}/sd-models")
            if response.status_code == 200:
                return True, response.json()
            return False, {"error": f"API returned status code {response.status_code}"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def generate_image(self, prompt, negative_prompt="", steps=30, width=512, height=512, 
                        cfg_scale=7.0, sampler="Euler a", batch_size=1):
        """Generate an image using the SD WebUI API"""
        endpoint = f"{self.api_url}/txt2img"
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "width": width,
            "height": height,
            "cfg_scale": cfg_scale,
            "sampler_name": sampler,
            "batch_size": batch_size
        }
        
        try:
            print(f"Sending request to Stable Diffusion: {prompt[:50]}...")
            response = requests.post(endpoint, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save images
                file_paths = []
                for i, img_data in enumerate(data.get("images", [])):
                    # The API returns base64 encoded images
                    if "," in img_data:  # Format: data:image/png;base64,<data>
                        img_data = img_data.split(",", 1)[1]
                    
                    # Create a unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"sd_generated_{timestamp}_{i}.png"
                    file_path = self.save_dir / filename
                    
                    # Decode and save the image
                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(img_data))
                    
                    file_paths.append(str(file_path))
                
                result = {
                    "status": "success",
                    "message": f"Generated {len(file_paths)} image(s) with Stable Diffusion",
                    "file_paths": file_paths,
                    "info": data.get("info", {}),
                    "parameters": data.get("parameters", {})
                }
                
                print(f"Successfully generated {len(file_paths)} images")
                return result
            else:
                error_msg = f"API error: {response.status_code} - {response.text}"
                print(error_msg)
                return {
                    "status": "error",
                    "message": error_msg
                }
        
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return {
                "status": "error",
                "message": error_msg
            }
    
    def get_models(self):
        """Get available models from SD WebUI"""
        try:
            response = requests.get(f"{self.api_url}/sd-models")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error getting models: {e}")
            return []


class DallEConnector:
    """Connector to DALL-E API"""
    
    def __init__(self, dalle_dir="D:/DALL-E-master"):
        """Initialize the connector"""
        self.dalle_dir = Path(dalle_dir)
        self.save_dir = Path("D:/AIArm/InnerLife/Generated/Images")
        self.save_dir.mkdir(exist_ok=True, parents=True)
        
        # Add DALL-E directory to path for imports
        sys.path.append(str(self.dalle_dir))
    
    def check_installation(self):
        """Check if DALL-E is properly installed"""
        try:
            # Check if the main script exists
            main_script = self.dalle_dir / "generate.py"
            if not main_script.exists():
                return False, {"error": f"DALL-E main script not found at {main_script}"}
            
            # Try to import key modules
            # Note: This won't work directly as these modules would have to be properly installed
            # This is just a check for the files
            modules_to_check = ["dalle_pytorch", "clip"]
            for module in modules_to_check:
                module_dir = self.dalle_dir / module
                if not module_dir.exists() and not (self.dalle_dir / f"{module}.py").exists():
                    return False, {"error": f"Required module {module} not found in DALL-E directory"}
            
            return True, {"message": "DALL-E installation appears valid"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def generate_image(self, prompt, num_images=1):
        """Generate an image using DALL-E
        
        Note: This is a simplification. The actual implementation would depend
        on how the DALL-E installation is set up and how it's meant to be called.
        """
        try:
            # This would typically use subprocess to call the DALL-E script
            # For now, we'll create a mock implementation
            
            # Create a unique output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.save_dir / f"dalle_{timestamp}"
            output_dir.mkdir(exist_ok=True)
            
            # In a real implementation, this would call the DALL-E script
            # subprocess.run([
            #     "python", 
            #     str(self.dalle_dir / "generate.py"), 
            #     "--prompt", prompt,
            #     "--num_images", str(num_images),
            #     "--output_dir", str(output_dir)
            # ])
            
            # For the mock implementation, we'll just create a text file with the prompt
            prompt_file = output_dir / "prompt.txt"
            with open(prompt_file, "w") as f:
                f.write(f"DALL-E Generation Request\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Number of Images: {num_images}\n")
                f.write(f"Timestamp: {timestamp}\n")
            
            return {
                "status": "success",
                "message": f"DALL-E generation request created",
                "prompt_file": str(prompt_file),
                "output_dir": str(output_dir)
            }
            
        except Exception as e:
            error_msg = f"Error generating image with DALL-E: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return {
                "status": "error",
                "message": error_msg
            }


# For testing the connectors
if __name__ == "__main__":
    # Test Stable Diffusion connector
    print("Testing Stable Diffusion connector...")
    sd_connector = StableDiffusionConnector()
    sd_status, sd_info = sd_connector.check_connection()
    
    if sd_status:
        print("Stable Diffusion WebUI is running!")
        print("Available models:")
        models = sd_connector.get_models()
        for model in models:
            print(f"- {model['title']}")
        
        # Test image generation
        test_prompt = "A serene landscape with mountains and a lake, digital art"
        print(f"\nGenerating test image with prompt: {test_prompt}")
        result = sd_connector.generate_image(test_prompt)
        
        if result["status"] == "success":
            print("Image generated successfully!")
            print(f"Saved to: {result['file_paths']}")
        else:
            print(f"Failed to generate image: {result['message']}")
    else:
        print(f"Stable Diffusion WebUI is not running: {sd_info['error']}")
    
    # Test DALL-E connector
    print("\nTesting DALL-E connector...")
    dalle_connector = DallEConnector()
    dalle_status, dalle_info = dalle_connector.check_installation()
    
    if dalle_status:
        print("DALL-E installation appears valid!")
        
        # Test image generation
        test_prompt = "A futuristic cityscape with flying cars and tall buildings"
        print(f"\nGenerating test image with prompt: {test_prompt}")
        result = dalle_connector.generate_image(test_prompt)
        
        if result["status"] == "success":
            print("DALL-E generation request created!")
            print(f"Prompt file: {result['prompt_file']}")
            print(f"Output directory: {result['output_dir']}")
        else:
            print(f"Failed to generate image with DALL-E: {result['message']}")
    else:
        print(f"DALL-E installation check failed: {dalle_info['error']}")

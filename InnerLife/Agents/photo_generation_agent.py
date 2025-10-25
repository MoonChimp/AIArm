#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Photo Generation Agent
Enables Nexus to generate images based on descriptions
"""

import sys
import os
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class PhotoGenerationAgent(Agent):
    """Agent for photo generation capabilities"""
    
    def __init__(self):
        """Initialize the photo generation agent"""
        super().__init__(
            name="PhotoGeneration",
            description="Generates images based on text descriptions",
            capabilities=[
                "Create photorealistic images from text descriptions",
                "Generate artistic images in various styles",
                "Edit and modify existing images",
                "Create variations of existing images"
            ]
        )
        self.generation_history = []
        self.api_key = None
        self.save_dir = Path("D:/AIArm/InnerLife/Generated/Images")
        self.save_dir.mkdir(exist_ok=True, parents=True)
        
    def set_api_credentials(self, api_key):
        """Set API credentials for image generation service"""
        self.api_key = api_key
        return "API credentials set successfully"
    
    def process(self, prompt, context=None, options=None):
        """Process an image generation request"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}
        
        self.last_used = datetime.now().isoformat()
        
        # Set default options if none provided
        if options is None:
            options = {
                "size": "1024x1024",
                "quality": "standard",
                "style": "natural",
                "n": 1  # Number of images to generate
            }
        
        # Log the generation request
        generation_entry = {
            "prompt": prompt,
            "timestamp": self.last_used,
            "context": context,
            "options": options
        }
        self.generation_history.append(generation_entry)
        
        # Check if we have Stable Diffusion integration
        if SD_INTEGRATION_AVAILABLE:
            try:
                # Initialize Stable Diffusion connector
                sd_connector = StableDiffusionConnector()
                
                # Check if SD WebUI is running
                sd_status, sd_info = sd_connector.check_connection()
                
                if sd_status:
                    print("Using Stable Diffusion WebUI for image generation")
                    # Use SD WebUI for image generation
                    result = sd_connector.generate_image(
                        prompt=prompt,
                        negative_prompt=options.get("negative_prompt", ""),
                        steps=options.get("steps", 30),
                        width=int(options.get("size", "1024x1024").split("x")[0]),
                        height=int(options.get("size", "1024x1024").split("x")[1]),
                        cfg_scale=options.get("cfg_scale", 7.0),
                        sampler=options.get("sampler", "Euler a"),
                        batch_size=options.get("n", 1)
                    )
                    
                    generation_entry["result"] = result
                    return result
                else:
                    print(f"Stable Diffusion WebUI is not running: {sd_info.get('error')}")
                    print("Falling back to DALL-E")
                    
                    # Try DALL-E
                    dalle_connector = DallEConnector()
                    dalle_status, dalle_info = dalle_connector.check_installation()
                    
                    if dalle_status:
                        print("Using DALL-E for image generation")
                        # Use DALL-E for image generation
                        result = dalle_connector.generate_image(
                            prompt=prompt,
                            num_images=options.get("n", 1)
                        )
                        
                        generation_entry["result"] = result
                        return result
                    else:
                        print(f"DALL-E installation check failed: {dalle_info.get('error')}")
                        print("Falling back to simulation")
            except Exception as e:
                print(f"Error using image generation integrations: {e}")
                # Fall back to simulated generation
        
        # Simulate image generation for demonstration
        simulated_result = self._simulate_generation(prompt, options)
        generation_entry["result"] = {
            "status": simulated_result["status"],
            "file_paths": simulated_result.get("file_paths", [])
        }
        
        return simulated_result
    
    def _generate_with_api(self, prompt, options):
        """Generate image using an actual API"""
        # This is a placeholder for connecting to a real image generation API
        # In a real implementation, this would call an API like Stable Diffusion, DALL-E, etc.
        
        # Example using DALL-E API (OpenAI)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "prompt": prompt,
            "n": options.get("n", 1),
            "size": options.get("size", "1024x1024"),
            "quality": options.get("quality", "standard"),
            "style": options.get("style", "natural")
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result_data = response.json()
                file_paths = []
                
                # Save the generated images
                for i, image_data in enumerate(result_data.get("data", [])):
                    image_url = image_data.get("url")
                    if image_url:
                        # Download the image
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            # Create a unique filename
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"generated_{timestamp}_{i}.png"
                            file_path = self.save_dir / filename
                            
                            # Save the image
                            with open(file_path, "wb") as f:
                                f.write(img_response.content)
                            
                            file_paths.append(str(file_path))
                
                return {
                    "status": "success",
                    "message": f"Generated {len(file_paths)} image(s)",
                    "file_paths": file_paths,
                    "source": "api"
                }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code} - {response.text}",
                    "source": "api"
                }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating image: {str(e)}",
                "source": "api"
            }
    
    def _simulate_generation(self, prompt, options):
        """Simulate image generation for demonstration"""
        # This is a simplified simulation for demonstration purposes
        # In a real implementation, this would be replaced with actual image generation
        
        # Create a text file with the prompt as a placeholder for the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"simulated_{timestamp}.txt"
        file_path = self.save_dir / file_name
        
        with open(file_path, "w") as f:
            f.write(f"Simulated image generation for prompt: {prompt}\n")
            f.write(f"Options: {json.dumps(options, indent=2)}\n")
            f.write(f"Generated at: {timestamp}\n")
        
        return {
            "status": "success",
            "message": "Simulated image generation completed",
            "file_paths": [str(file_path)],
            "source": "simulation",
            "note": "This is a simulation. In a real implementation, an actual image would be generated."
        }
    
    def get_generation_history(self, limit=10):
        """Get recent generation history"""
        return self.generation_history[-limit:] if self.generation_history else []
    
    def clear_generation_history(self):
        """Clear generation history"""
        self.generation_history = []
        return "Generation history cleared"

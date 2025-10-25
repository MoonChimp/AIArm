#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm StableDiffusion Bridge
Connects the AIArm system directly to StableDiffusion WebUI API
"""

import sys
import os
import json
import traceback
import argparse
import requests
import io
import time
import base64
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SD_API_URL = "http://127.0.0.1:7860"
IMAGES_DIR = Path("D:/AIArm/Images")
IMAGES_DIR.mkdir(exist_ok=True, parents=True)

def check_sd_availability():
    """Check if StableDiffusion WebUI API is available"""
    try:
        response = requests.get(f"{SD_API_URL}/sdapi/v1/sd-models")
        if response.status_code == 200:
            models = response.json()
            model_names = [model.get("model_name") for model in models]
            return True, model_names
        else:
            return False, []
    except Exception as e:
        print(f"Error checking StableDiffusion availability: {e}")
        return False, []

def generate_image(prompt, options=None):
    """Generate an image using StableDiffusion WebUI API"""
    try:
        print(f"Generating image with prompt: {prompt}")
        
        # Default options
        default_options = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, deformed, distorted",
            "steps": 25,
            "cfg_scale": 7.5,
            "width": 768,
            "height": 768,
            "sampler_name": "DPM++ 2M Karras",
        }
        
        # Override with user options if provided
        if options and isinstance(options, dict):
            # Convert specific options from text to parameters
            if "quality" in options:
                quality = options["quality"].lower()
                if quality == "high":
                    default_options["steps"] = 30
                    default_options["cfg_scale"] = 8.0
                elif quality == "medium":
                    default_options["steps"] = 25
                    default_options["cfg_scale"] = 7.5
                elif quality == "low":
                    default_options["steps"] = 20
                    default_options["cfg_scale"] = 7.0
            
            # Apply style-specific adjustments
            if "style" in options:
                style = options["style"].lower()
                if style == "photorealistic":
                    if "negative_prompt" in default_options:
                        default_options["negative_prompt"] += ", cartoon, drawing, painting, anime, illustration"
                    prompt += ", photorealistic, highly detailed, 8k, photography"
                elif style == "anime":
                    prompt += ", anime style, illustration, digital art"
                elif style == "painting":
                    prompt += ", digital painting, detailed brushwork, artistic"
                elif style == "3d":
                    prompt += ", 3d render, octane render, highly detailed, volumetric lighting"
            
            # Override other direct parameters
            for key in ["width", "height", "steps", "cfg_scale", "sampler_name", "negative_prompt"]:
                if key in options:
                    default_options[key] = options[key]
            
            # Update the prompt with the processed one
            default_options["prompt"] = prompt
        
        print(f"Making API call to StableDiffusion with options: {json.dumps(default_options)}")
        
        # Make the API call
        response = requests.post(
            f"{SD_API_URL}/sdapi/v1/txt2img",
            json=default_options
        )
        
        if response.status_code != 200:
            print(f"Error from StableDiffusion API: {response.status_code} - {response.text}")
            return None, f"StableDiffusion API error: {response.status_code}"
        
        result = response.json()
        print(f"Received response with {len(result.get('images', []))} images")
        
        # Save the image
        if not result.get('images'):
            print("No images in the response")
            return None, "No images were generated"
            
        for i, image_data in enumerate(result["images"]):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"sd_generated_{timestamp}_{i}.png"
            image_path = IMAGES_DIR / image_filename
            
            # Check if the image data is in base64 format with a data URI prefix
            if ',' in image_data:
                print("Image data contains comma - splitting to get base64 content")
                image_data = image_data.split(",", 1)[1]
            
            # Decode and save image
            try:
                image_bytes = base64.b64decode(image_data)
                print(f"Decoded image size: {len(image_bytes)} bytes")
                
                # Save to main images directory
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Image saved to {image_path}")
                
                # Also create a copy in the static directory for web access
                static_images_dir = Path("D:/AIArm/WebInterface/static/images")
                static_images_dir.mkdir(exist_ok=True, parents=True)
                static_image_path = static_images_dir / image_filename
                
                # Copy the image
                with open(static_image_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Image saved to static directory: {static_image_path}")
                
                # Return the first image path
                if i == 0:
                    # Create a URL path for the image that can be accessed via the web server
                    image_url = f"/static/images/{image_filename}"
                    absolute_url = f"http://localhost:45678{image_url}"
                    print(f"Image URL: {absolute_url}")
                    return absolute_url, None
                    
            except Exception as e:
                print(f"Error processing image data: {e}")
                traceback.print_exc()
                return None, f"Error processing image data: {e}"
        
        return None, "No images were generated"
        
    except Exception as e:
        print(f"Error generating image: {e}")
        traceback.print_exc()
        return None, str(e)

def process_request(request_data):
    """Process a photo generation request"""
    try:
        # Extract request data
        if isinstance(request_data, str):
            try:
                # Try to parse as JSON
                data = json.loads(request_data)
            except json.JSONDecodeError:
                # Use the string as the prompt
                data = {"input": request_data}
        else:
            data = request_data
        
        # Get the prompt and options
        prompt = data.get("input", "")
        options = data.get("options", {})
        
        # Check if StableDiffusion is available
        available, models = check_sd_availability()
        if not available:
            return {
                "success": False,
                "status": "error",
                "error": "StableDiffusion WebUI API is not available",
                "result": "The image generation service is currently unavailable. Please ensure StableDiffusion WebUI is running with API enabled."
            }
        
        # Generate the image
        image_path, error = generate_image(prompt, options)
        
        if error:
            return {
                "success": False,
                "status": "error",
                "error": error,
                "result": f"Failed to generate image: {error}"
            }
        
        # Build the URL for the image
        image_url = f"http://localhost:45678{image_path}"
        
        return {
            "success": True,
            "status": "completed",
            "result": image_url,
            "image_url": image_url,
            "prompt": prompt
        }
        
    except Exception as e:
        print(f"Error processing request: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": f"Error processing photo generation request: {str(e)}"
        }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="AIArm StableDiffusion Bridge")
    parser.add_argument("--input", type=str, help="Input text to process (prompt or JSON)")
    parser.add_argument("--json", action="store_true", help="Indicate that input is provided as JSON")
    args = parser.parse_args()
    
    try:
        # Get the input
        if args.input:
            input_text = args.input
        else:
            # Read from stdin
            input_text = sys.stdin.read()
        
        # Process as JSON if flagged
        if args.json:
            try:
                input_json = json.loads(input_text)
                result = process_request(input_json)
            except json.JSONDecodeError:
                result = process_request(input_text)
        else:
            result = process_request(input_text)
        
        # Output the result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        error_result = {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": f"Error in StableDiffusion bridge: {str(e)}"
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
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
STATIC_IMAGES_DIR = Path("D:/AIArm/WebInterface/static/images")
STATIC_IMAGES_DIR.mkdir(exist_ok=True, parents=True)

def log_message(message, level="INFO"):
    """Log a message to the console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Print to console
    print(log_entry.strip())
    
    # Write to log file
    log_dir = Path("D:/AIArm/Logs")
    log_dir.mkdir(exist_ok=True, parents=True)
    log_file = log_dir / f"sd_bridge_{datetime.now().strftime('%Y%m%d')}.log"
    
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def check_sd_availability():
    """Check if StableDiffusion WebUI API is available"""
    log_message("Checking StableDiffusion WebUI availability")
    try:
        response = requests.get(f"{SD_API_URL}/sdapi/v1/sd-models")
        if response.status_code == 200:
            models = response.json()
            model_names = [model.get("model_name") for model in models]
            log_message(f"StableDiffusion WebUI is available with {len(model_names)} models")
            return True, model_names
        else:
            log_message(f"StableDiffusion WebUI returned status code {response.status_code}", "ERROR")
            return False, []
    except Exception as e:
        log_message(f"Error checking StableDiffusion availability: {e}", "ERROR")
        traceback.print_exc()
        return False, []

def generate_image(prompt, options=None):
    """Generate an image using StableDiffusion WebUI API"""
    try:
        log_message(f"Generating image with prompt: {prompt}")
        
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
        
        log_message(f"Making API call to StableDiffusion with options: {json.dumps(default_options)}")
        
        # Make the API call
        response = requests.post(
            f"{SD_API_URL}/sdapi/v1/txt2img",
            json=default_options
        )
        
        if response.status_code != 200:
            log_message(f"Error from StableDiffusion API: {response.status_code} - {response.text}", "ERROR")
            return None, f"StableDiffusion API error: {response.status_code}"
        
        result = response.json()
        log_message(f"Received response with {len(result.get('images', []))} images")
        
        # Save the image
        if not result.get('images'):
            log_message("No images in the response", "ERROR")
            return None, "No images were generated"
            
        for i, image_data in enumerate(result["images"]):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"sd_generated_{timestamp}_{i}.png"
            image_path = IMAGES_DIR / image_filename
            
            # Check if the image data is in base64 format with a data URI prefix
            if ',' in image_data:
                log_message("Image data contains comma - splitting to get base64 content")
                image_data = image_data.split(",", 1)[1]
            
            # Decode and save image
            try:
                image_bytes = base64.b64decode(image_data)
                log_message(f"Decoded image size: {len(image_bytes)} bytes")
                
                # Save to main images directory
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                log_message(f"Image saved to {image_path}")
                
                # Also create a copy in the static directory for web access
                static_image_path = STATIC_IMAGES_DIR / image_filename
                
                # Copy the image
                with open(static_image_path, "wb") as f:
                    f.write(image_bytes)
                log_message(f"Image saved to static directory: {static_image_path}")
                
                # Return the first image path
                if i == 0:
                    # Create a URL path for the image that can be accessed via the web server
                    image_url = f"/static/images/{image_filename}"
                    absolute_url = f"http://localhost:45678{image_url}"
                    log_message(f"Image URL: {absolute_url}")
                    return absolute_url, None
                    
            except Exception as e:
                log_message(f"Error processing image data: {e}", "ERROR")
                traceback.print_exc()
                return None, f"Error processing image data: {e}"
        
        return None, "No images were generated"
        
    except Exception as e:
        log_message(f"Error generating image: {e}", "ERROR")
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
        
        log_message(f"Processing request data: {json.dumps(data)}")
        
        # Check if this is an agent request
        if isinstance(data, dict) and "agent" in data and data.get("agent") == "PhotoGeneration":
            # Extract from agent request format
            action_data = data.get("data", {})
            prompt = action_data.get("input", "")
            options = action_data.get("options", {})
        else:
            # Extract direct format
            prompt = data.get("input", "")
            options = data.get("options", {})
        
        log_message(f"Extracted prompt: {prompt}")
        log_message(f"Extracted options: {json.dumps(options)}")
        
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
        image_url, error = generate_image(prompt, options)
        
        if error:
            log_message(f"Error generating image: {error}", "ERROR")
            return {
                "success": False,
                "status": "error",
                "error": error,
                "result": f"Failed to generate image: {error}"
            }
        
        # Return success response
        result = {
            "success": True,
            "status": "completed",
            "result": image_url,
            "image_url": image_url,
            "prompt": prompt,
            "response": f"Image generated successfully: {image_url}"
        }
        
        log_message(f"Returning successful result: {json.dumps(result)}")
        return result
        
    except Exception as e:
        log_message(f"Error processing request: {e}", "ERROR")
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
    parser.add_argument("--agent", type=str, default="PhotoGeneration", help="Agent to use for processing")
    parser.add_argument("--user", type=str, default="user", help="User ID for conversation tracking")
    parser.add_argument("--json", action="store_true", help="Indicate that input is provided as JSON")
    args = parser.parse_args()
    
    try:
        log_message("StableDiffusion Bridge starting")
        
        # Get the input
        if args.input:
            input_text = args.input
            log_message(f"Input provided via command line: {input_text[:100]}")
        else:
            # Read from stdin
            input_text = sys.stdin.read()
            log_message(f"Input provided via stdin: {input_text[:100]}")
        
        # Process as JSON if flagged
        if args.json:
            try:
                log_message("Processing input as JSON")
                input_json = json.loads(input_text)
                log_message(f"Parsed JSON: {json.dumps(input_json)}")
                result = process_request(input_json)
            except json.JSONDecodeError as e:
                log_message(f"JSON parsing error: {e}", "ERROR")
                result = process_request(input_text)
        else:
            result = process_request(input_text)
        
        # Output the result
        output = json.dumps(result, indent=2, ensure_ascii=False)
        log_message(f"Returning result: {output[:200]}")
        print(output)
        
    except Exception as e:
        log_message(f"Error in main: {e}", "ERROR")
        traceback.print_exc()
        
        error_result = {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": f"Error in StableDiffusion bridge: {str(e)}"
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
    
    log_message("StableDiffusion Bridge execution completed")

if __name__ == "__main__":
    main()
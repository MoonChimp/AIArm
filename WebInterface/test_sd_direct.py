#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
StableDiffusion Direct Test Script
Tests direct connection to StableDiffusion WebUI API with verbose logging
"""

import sys
import os
import json
import requests
import base64
import traceback
from pathlib import Path
from datetime import datetime

# Configuration
SD_API_URL = "http://127.0.0.1:7860"
IMAGES_DIR = Path("D:/AIArm/Images")
IMAGES_DIR.mkdir(exist_ok=True, parents=True)
STATIC_IMAGES_DIR = Path("D:/AIArm/WebInterface/static/images")
STATIC_IMAGES_DIR.mkdir(exist_ok=True, parents=True)

# Set up basic logging
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_sd_availability():
    """Check if StableDiffusion WebUI API is available"""
    log("Checking StableDiffusion WebUI availability...")
    try:
        response = requests.get(f"{SD_API_URL}/sdapi/v1/sd-models")
        if response.status_code == 200:
            models = response.json()
            log(f"✅ StableDiffusion WebUI is available")
            log(f"Available models: {[model.get('model_name') for model in models][:3]}...")
            return True, models
        else:
            log(f"❌ StableDiffusion WebUI returned status code {response.status_code}")
            log(f"Response: {response.text[:200]}...")
            return False, []
    except Exception as e:
        log(f"❌ Error checking StableDiffusion availability: {e}")
        traceback.print_exc()
        return False, []

def generate_test_image():
    """Generate a test image using StableDiffusion WebUI API"""
    log("Generating test image...")
    try:
        # Test prompt
        prompt = "A beautiful mountain landscape with a lake and forest, photorealistic, highly detailed"
        log(f"Using prompt: {prompt}")
        
        # Default options
        options = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, deformed, distorted",
            "steps": 25,
            "cfg_scale": 7.5,
            "width": 512,  # Using smaller dimensions for faster generation
            "height": 512,
            "sampler_name": "DPM++ 2M Karras",
        }
        
        log(f"Sending request to {SD_API_URL}/sdapi/v1/txt2img")
        log(f"Request options: {json.dumps(options)}")
        
        # Make the API call
        response = requests.post(
            f"{SD_API_URL}/sdapi/v1/txt2img",
            json=options
        )
        
        log(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            log(f"❌ Error from StableDiffusion API: {response.status_code}")
            log(f"Response: {response.text[:500]}...")
            return False
        
        # Parse the response
        result = response.json()
        log(f"Response received - contains {len(result.get('images', []))} images")
        
        # Save the image
        if not result.get('images'):
            log("❌ No images in response")
            return False
        
        for i, image_data in enumerate(result['images']):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"test_image_{timestamp}_{i}.png"
            image_path = IMAGES_DIR / image_filename
            static_image_path = STATIC_IMAGES_DIR / image_filename
            
            log(f"Processing image {i+1}/{len(result['images'])}")
            
            # Check if the image data is in base64 format
            if ',' in image_data:
                log("Image data contains comma - splitting to get base64 content")
                image_data = image_data.split(",", 1)[1]
            
            log(f"Decoding base64 data (length: {len(image_data)})")
            try:
                image_bytes = base64.b64decode(image_data)
                log(f"Decoded image size: {len(image_bytes)} bytes")
            except Exception as e:
                log(f"❌ Error decoding base64 data: {e}")
                traceback.print_exc()
                continue
            
            # Write to main images directory
            log(f"Saving image to {image_path}")
            try:
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                log(f"✅ Image saved to {image_path}")
            except Exception as e:
                log(f"❌ Error saving image to {image_path}: {e}")
                traceback.print_exc()
            
            # Also write to static directory for web access
            log(f"Saving image to static directory: {static_image_path}")
            try:
                with open(static_image_path, "wb") as f:
                    f.write(image_bytes)
                log(f"✅ Image saved to {static_image_path}")
            except Exception as e:
                log(f"❌ Error saving image to static directory: {e}")
                traceback.print_exc()
            
            # For the first image, print URL info
            if i == 0:
                image_url = f"http://localhost:45678/static/images/{image_filename}"
                log(f"✅ Image URL: {image_url}")
                return True
        
        return True
        
    except Exception as e:
        log(f"❌ Error generating test image: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function"""
    log("Starting StableDiffusion Direct Test")
    
    # Check if SD is available
    available, _ = check_sd_availability()
    if not available:
        log("❌ StableDiffusion WebUI is not available. Please make sure it's running with API enabled.")
        return
    
    # Generate a test image
    log("Running image generation test...")
    success = generate_test_image()
    
    if success:
        log("✅ Image generation test completed successfully!")
    else:
        log("❌ Image generation test failed.")

if __name__ == "__main__":
    main()
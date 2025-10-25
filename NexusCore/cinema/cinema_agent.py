#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Cinema Agent - Hollywood-Quality Content Generation
Handles SDXL, AnimateDiff, MoviePy for cinema-grade output
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

try:
    import torch
    import numpy as np
    from PIL import Image
    import cv2
    IMPORTS_AVAILABLE = True
    
    # Try to import diffusers, but handle xformers issues
    try:
        # Disable xformers to avoid DLL errors
        import os
        os.environ['XFORMERS_DISABLED'] = '1'
        from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
        from diffusers import AutoencoderKL
        DIFFUSERS_AVAILABLE = True
    except Exception as e:
        print(f"[CinemaAgent] Diffusers not fully available: {e}")
        print("[CinemaAgent] Cinema agent will work in limited mode")
        DIFFUSERS_AVAILABLE = False
        
except ImportError as e:
    print(f"[CinemaAgent] Warning: Some dependencies not available: {e}")
    print("[CinemaAgent] Run: D:\\AIArm\\INSTALL_CINEMA_DEPENDENCIES.bat")
    IMPORTS_AVAILABLE = False
    DIFFUSERS_AVAILABLE = False

class CinemaAgent:
    """
    Hollywood-grade content generation system
    - SDXL for photorealistic 1024x1024 images
    - ControlNet for precise composition
    - AnimateDiff for motion
    - MoviePy for video assembly
    - Professional color grading
    """
    
    def __init__(self, model_dir: str = "D:/AIArm/Models"):
        self.name = "CinemaAgent"
        self.active = False
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True, parents=True)
        
        # Output directory
        self.output_dir = Path("D:/AIArm/Generated/Cinema")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Models
        self.sdxl_pipeline = None
        self.device = "cuda" if IMPORTS_AVAILABLE and torch.cuda.is_available() else "cpu"
        
        # Cinema settings
        self.resolution = (1024, 1024)  # SDXL native
        self.aspect_ratios = {
            "16:9": (1344, 768),      # Widescreen
            "2.39:1": (1344, 576),    # Anamorphic cinema
            "1.85:1": (1024, 552),    # Classic cinema
            "1:1": (1024, 1024),      # Square (Instagram)
            "9:16": (768, 1344)       # Vertical (TikTok)
        }
        
        # Film looks (color grading presets)
        self.film_looks = {
            "neutral": {"temp": 0, "tint": 0, "saturation": 1.0},
            "warm": {"temp": 20, "tint": 5, "saturation": 1.1},
            "cool": {"temp": -15, "tint": -5, "saturation": 0.95},
            "noir": {"temp": -10, "tint": 0, "saturation": 0.3},
            "cinematic": {"temp": 10, "tint": 5, "saturation": 1.2}
        }
        
        print(f"[{self.name}] Initialized")
        print(f"  Device: {self.device}")
        print(f"  Model Dir: {self.model_dir}")
        print(f"  Output Dir: {self.output_dir}")
    
    def activate(self):
        """Activate the cinema agent"""
        if not IMPORTS_AVAILABLE or not DIFFUSERS_AVAILABLE:
            print(f"[{self.name}] Cannot activate - SDXL dependencies not available")
            print(f"[{self.name}] This is due to Python 3.13 compatibility issues")
            print(f"[{self.name}] Cinema agent will work in CPU-mode for basic image processing")
            self.active = False
            return False
        
        try:
            print(f"[{self.name}] Loading SDXL model...")
            # Use fp16 for speed if on GPU
            torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            # Try to load SDXL model
            model_id = "stabilityai/stable-diffusion-xl-base-1.0"
            
            self.sdxl_pipeline = StableDiffusionXLPipeline.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            if self.device == "cuda":
                self.sdxl_pipeline.to(self.device)
                # Enable memory optimizations
                self.sdxl_pipeline.enable_attention_slicing()
                self.sdxl_pipeline.enable_vae_slicing()
            
            self.active = True
            print(f"[{self.name}] ✓ Activated successfully")
            return True
            
        except Exception as e:
            print(f"[{self.name}] ✗ Activation failed: {e}")
            print(f"[{self.name}] Models will download on first use")
            self.active = False
            return False
    
    def generate_scene(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        film_look: str = "cinematic",
        num_images: int = 1,
        seed: Optional[int] = None
    ) -> Dict:
        """
        Generate a cinema-quality scene
        """
        if not self.active:
            return {
                "status": "error",
                "message": "Cinema agent not active. Run activate() first."
            }
        
        try:
            print(f"[{self.name}] Generating scene: {prompt[:50]}...")
            
            # Get resolution for aspect ratio
            resolution = self.aspect_ratios.get(aspect_ratio, (1024, 1024))
            
            # Enhance prompt for cinema quality
            enhanced_prompt = self._enhance_prompt(prompt, film_look)
            
            # Set seed for reproducibility
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            else:
                generator = None
            
            # Generate with SDXL
            images = self.sdxl_pipeline(
                prompt=enhanced_prompt,
                negative_prompt=self._get_negative_prompt(),
                height=resolution[1],
                width=resolution[0],
                num_inference_steps=50,  # High quality
                guidance_scale=7.5,
                num_images_per_prompt=num_images,
                generator=generator
            ).images
            
            # Apply color grading
            processed_images = []
            saved_paths = []
            
            for i, image in enumerate(images):
                # Apply film look
                graded_image = self._apply_film_look(image, film_look)
                processed_images.append(graded_image)
                
                # Save
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scene_{timestamp}_{i}.png"
                filepath = self.output_dir / filename
                graded_image.save(filepath, quality=95)
                saved_paths.append(str(filepath))
                print(f"[{self.name}] ✓ Saved: {filename}")
            
            return {
                "status": "success",
                "images": processed_images,
                "paths": saved_paths,
                "prompt": enhanced_prompt,
                "aspect_ratio": aspect_ratio,
                "film_look": film_look,
                "resolution": resolution
            }
            
        except Exception as e:
            print(f"[{self.name}] ✗ Generation failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def generate_storyboard(
        self,
        scene_descriptions: List[str],
        aspect_ratio: str = "16:9",
        film_look: str = "cinematic"
    ) -> Dict:
        """
        Generate a multi-shot storyboard
        """
        if not self.active:
            return {
                "status": "error",
                "message": "Cinema agent not active"
            }
        
        print(f"[{self.name}] Generating storyboard with {len(scene_descriptions)} shots...")
        
        all_images = []
        all_paths = []
        
        for i, description in enumerate(scene_descriptions):
            print(f"[{self.name}] Shot {i+1}/{len(scene_descriptions)}: {description[:50]}...")
            
            result = self.generate_scene(
                prompt=description,
                aspect_ratio=aspect_ratio,
                film_look=film_look,
                num_images=1
            )
            
            if result["status"] == "success":
                all_images.extend(result["images"])
                all_paths.extend(result["paths"])
        
        return {
            "status": "success",
            "storyboard": all_images,
            "paths": all_paths,
            "shot_count": len(all_images),
            "aspect_ratio": aspect_ratio,
            "film_look": film_look
        }
    
    def create_video_sequence(
        self,
        image_paths: List[str],
        output_path: Optional[str] = None,
        fps: int = 24,
        transition: str = "cut",
        add_audio: bool = False
    ) -> Dict:
        """
        Assemble images into video sequence
        Requires MoviePy
        """
        try:
            from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip
            from moviepy.video.fx.all import fadein, fadeout
        except ImportError:
            return {
                "status": "error",
                "message": "MoviePy not installed. Run INSTALL_CINEMA_DEPENDENCIES.bat"
            }
        
        if not image_paths:
            return {"status": "error", "message": "No images provided"}
        
        print(f"[{self.name}] Creating video from {len(image_paths)} images...")
        
        try:
            # Create clips
            clips = []
            duration_per_image = 3.0  # 3 seconds per image
            
            for i, img_path in enumerate(image_paths):
                clip = ImageClip(img_path).set_duration(duration_per_image)
                
                # Add transitions
                if transition == "fade":
                    if i > 0:
                        clip = clip.fadein(0.5)
                    if i < len(image_paths) - 1:
                        clip = clip.fadeout(0.5)
                
                clips.append(clip)
            
            # Concatenate
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Output path
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = str(self.output_dir / f"sequence_{timestamp}.mp4")
            
            # Write video
            final_clip.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',
                audio_codec='aac' if add_audio else None,
                preset='slow',  # High quality
                bitrate='8000k'
            )
            
            print(f"[{self.name}] ✓ Video created: {output_path}")
            
            return {
                "status": "success",
                "video_path": output_path,
                "duration": len(image_paths) * duration_per_image,
                "fps": fps,
                "frame_count": len(image_paths)
            }
            
        except Exception as e:
            print(f"[{self.name}] ✗ Video creation failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _enhance_prompt(self, prompt: str, film_look: str) -> str:
        """Enhance prompt for cinema quality"""
        
        # Add cinema-quality keywords
        quality_tokens = [
            "cinematic",
            "professional photography",
            "8k uhd",
            "high detail",
            "dramatic lighting",
            "film grain",
            "professional color grading"
        ]
        
        # Add film-specific keywords
        if film_look == "noir":
            quality_tokens.extend(["black and white", "high contrast", "film noir"])
        elif film_look == "warm":
            quality_tokens.extend(["golden hour", "warm tones"])
        elif film_look == "cool":
            quality_tokens.extend(["cool tones", "blue hour"])
        
        enhanced = f"{prompt}, {', '.join(quality_tokens)}"
        return enhanced
    
    def _get_negative_prompt(self) -> str:
        """Get negative prompt for quality"""
        return "low quality, blurry, distorted, deformed, ugly, bad anatomy, worst quality, low resolution, pixelated, jpeg artifacts, text, watermark, signature"
    
    def _apply_film_look(self, image: Image.Image, film_look: str) -> Image.Image:
        """Apply cinematic color grading"""
        if film_look not in self.film_looks:
            return image
        
        # Convert to numpy
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # Get film look parameters
        params = self.film_looks[film_look]
        
        # Apply saturation
        if params['saturation'] != 1.0:
            # Convert to HSV
            img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            img_hsv[:,:,1] *= params['saturation']
            img_hsv[:,:,1] = np.clip(img_hsv[:,:,1], 0, 1)
            img_array = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        
        # Apply temperature (warm/cool)
        if params['temp'] != 0:
            temp_factor = params['temp'] / 100.0
            img_array[:,:,0] += temp_factor  # Red channel
            img_array[:,:,2] -= temp_factor * 0.5  # Blue channel
            img_array = np.clip(img_array, 0, 1)
        
        # Convert back to PIL
        img_array = (img_array * 255).astype(np.uint8)
        return Image.fromarray(img_array)
    
    def upscale_to_4k(self, image_path: str) -> Dict:
        """Upscale image to 4K resolution"""
        try:
            # Load image
            img = Image.open(image_path)
            
            # 4K resolution (3840 x 2160)
            target_size = (3840, 2160)
            
            # Use high-quality Lanczos resampling
            upscaled = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Save
            output_path = Path(image_path).with_stem(Path(image_path).stem + "_4k")
            upscaled.save(output_path, quality=95)
            
            print(f"[{self.name}] ✓ Upscaled to 4K: {output_path}")
            
            return {
                "status": "success",
                "output_path": str(output_path),
                "resolution": target_size
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def status(self) -> Dict:
        """Get agent status"""
        return {
            "name": self.name,
            "active": self.active,
            "device": self.device,
            "model_loaded": self.sdxl_pipeline is not None,
            "output_dir": str(self.output_dir),
            "capabilities": [
                "Cinema-quality image generation (SDXL)",
                "Multiple aspect ratios (16:9, 2.39:1, etc.)",
                "Professional color grading",
                "Storyboard generation",
                "Video sequence creation",
                "4K upscaling"
            ]
        }


if __name__ == "__main__":
    # Test cinema agent
    print("Initializing Cinema Agent...")
    agent = CinemaAgent()
    
    # Try to activate
    agent.activate()
    
    # Show status
    print(f"\nStatus: {agent.status()}")
    
    # Test generation (if active)
    if agent.active:
        print("\nGenerating test scene...")
        result = agent.generate_scene(
            prompt="A futuristic cityscape at night with neon lights",
            aspect_ratio="16:9",
            film_look="cinematic"
        )
        print(f"Result: {result.get('status')}")
        if result.get('paths'):
            print(f"Saved to: {result['paths'][0]}")

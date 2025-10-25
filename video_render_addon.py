"""
Video rendering methods to add to RealVideoAgent
Add these methods to real_video_agent.py
"""

def _render_video_file(self, video_data, video_id, scenes):
    """Render actual MP4 video file"""
    import subprocess

    try:
        # Try multiple rendering methods
        methods = [
            self._render_with_ffmpeg_slideshow
        ]

        for method in methods:
            try:
                result = method(video_data, video_id, scenes)
                if result["status"] == "success":
                    return result
            except Exception as e:
                print(f"[VideoGeneration] Render method failed: {e}")
                continue

        # If all fail, create placeholder
        return self._create_video_placeholder(video_data, video_id)

    except Exception as e:
        return {
            "status": "error",
            "message": f"Video rendering failed: {str(e)}"
        }

def _render_with_ffmpeg_slideshow(self, video_data, video_id, scenes):
    """Create slideshow video using FFmpeg"""
    try:
        import subprocess
        from PIL import Image, ImageDraw, ImageFont

        print("[VideoGeneration] Using FFmpeg for slideshow...")

        # Create temporary directory for scene images
        temp_dir = self.output_dir / f"temp_{video_id}"
        temp_dir.mkdir(exist_ok=True)

        # Generate scene images
        if not scenes or len(scenes) == 0:
            # Create title scene
            img = Image.new('RGB', (1920, 1080), color=(20, 20, 40))
            draw = ImageDraw.Draw(img)
            draw.text((100, 400), video_data['concept'][:200], fill=(255, 255, 255))
            img_path = temp_dir / f"scene_000.png"
            img.save(img_path)
        else:
            for i, scene in enumerate(scenes):
                img = Image.new('RGB', (1920, 1080), color=(30, 30, 50))
                draw = ImageDraw.Draw(img)
                text = f"Scene {i+1}\n{scene.get('description', '')[:150]}"
                draw.text((100, 400), text, fill=(255, 255, 255))

                img_path = temp_dir / f"scene_{i:03d}.png"
                img.save(img_path)

        # Use FFmpeg to create video from images
        mp4_file = self.output_dir / f"nexus_video_{video_id}.mp4"

        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", "1/5",  # 5 seconds per image
            "-pattern_type", "glob",
            "-i", str(temp_dir / "scene_*.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(mp4_file)
        ], check=True, capture_output=True)

        # Clean up temp directory
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

        return {
            "status": "success",
            "filepath": str(mp4_file),
            "method": "ffmpeg"
        }

    except Exception as e:
        print(f"[VideoGeneration] FFmpeg error: {e}")
        raise

def _create_video_placeholder(self, video_data, video_id):
    """Create placeholder instructions for video generation"""
    try:
        print("[VideoGeneration] Creating video placeholder...")

        instructions_file = self.output_dir / f"nexus_video_{video_id}_VIDEO_INSTRUCTIONS.txt"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(f"Video Generation Instructions\n")
            f.write("="*60 + "\n\n")
            f.write("To generate video for this concept:\n\n")
            f.write("Option 1 - Install FFmpeg:\n")
            f.write("  1. Download from https://ffmpeg.org/download.html\n")
            f.write("  2. Add to PATH\n")
            f.write("  3. Run Nexus again\n\n")
            f.write("Option 2 - Use Runway ML or similar:\n")
            f.write("  1. Go to runwayml.com or pika.art\n")
            f.write(f"  2. Input concept: {video_data['concept']}\n")
            f.write("  3. Download MP4\n\n")
            f.write(f"Video Data:\n")
            f.write(f"  Type: {video_data['type']}\n")
            f.write(f"  Duration: {video_data['duration']}s\n")
            f.write(f"  Scenes: {len(video_data.get('scenes', []))}\n")

        return {
            "status": "partial",
            "filepath": str(instructions_file),
            "message": "Video rendering tools not available. Instructions saved."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

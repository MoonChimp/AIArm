#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Video Generation Agent
Generates video scripts, storyboards, and coordinates with image generation
for video creation
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import requests
import uuid
import subprocess
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

# Try to import RunwayML
try:
    from Agents.runway_ml_integration import RunwayMLClient
    RUNWAY_AVAILABLE = True
except:
    RUNWAY_AVAILABLE = False

class RealVideoAgent(Agent):
    """Agent for video concept generation and storyboarding"""

    def __init__(self):
        super().__init__(
            name="VideoGeneration",
            description="Generates video scripts, storyboards, and concepts",
            capabilities=[
                "Generate video scripts",
                "Create storyboards",
                "Plan scene compositions",
                "Coordinate with photo generation for frames",
                "Video concept development"
            ]
        )
        self.videos = []
        self.output_dir = Path("D:/AIArm/Generated/Videos")
        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Video generation settings
        self.use_video_rendering = True
        self.default_fps = 24
        self.default_resolution = (1920, 1080)

        # Initialize RunwayML if available
        self.runway_client = RunwayMLClient() if RUNWAY_AVAILABLE else None
        if self.runway_client and self.runway_client.api_key:
            print(f"[VideoGeneration] RunwayML integration enabled")
        else:
            print(f"[VideoGeneration] RunwayML not configured - using FFmpeg fallback")

    def process(self, concept, context=None, options=None):
        """Generate video concept and storyboard"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[VideoGeneration] Creating video concept: {concept[:60]}...")

        try:
            # Determine video type
            video_type = self._detect_video_type(concept)
            duration = options.get("duration", 30)  # seconds

            print(f"[VideoGeneration] Type: {video_type}, Duration: {duration}s")

            # Generate video script and storyboard
            result = self._generate_video_concept(concept, video_type, duration, options)

            if result["status"] == "success":
                # Save the video concept
                video_id = str(uuid.uuid4())[:8]
                filename = f"nexus_video_{video_id}.json"
                filepath = self.output_dir / filename

                video_data = {
                    "id": video_id,
                    "concept": concept,
                    "type": video_type,
                    "duration": duration,
                    "timestamp": self.last_used,
                    "script": result["script"],
                    "storyboard": result["storyboard"],
                    "scenes": result.get("scenes", [])
                }

                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(video_data, f, indent=2, ensure_ascii=False)

                # Also save human-readable version
                md_file = self.output_dir / f"nexus_video_{video_id}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Video Concept: {concept}\n\n")
                    f.write(f"**Type**: {video_type}\n")
                    f.write(f"**Duration**: {duration}s\n")
                    f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                    f.write("---\n\n")
                    f.write("## Script\n\n")
                    f.write(result["script"])
                    f.write("\n\n---\n\n")
                    f.write("## Storyboard\n\n")
                    f.write(result["storyboard"])

                print(f"[VideoGeneration] Video concept saved to {filename}")

                # STEP 3: Generate actual MP4 video file (if enabled)
                mp4_file = None
                if self.use_video_rendering and options.get("generate_video", True):
                    print(f"[VideoGeneration] Rendering MP4 video...")
                    video_result = self._render_video_file(video_data, video_id, result.get("scenes", []))
                    if video_result["status"] == "success":
                        mp4_file = video_result["filepath"]
                        print(f"[VideoGeneration] Video saved: {Path(mp4_file).name}")

                # Log video
                video_entry = {
                    "timestamp": self.last_used,
                    "concept": concept,
                    "type": video_type,
                    "filepath": str(filepath),
                    "video_file": str(mp4_file) if mp4_file else None
                }
                self.videos.append(video_entry)

                files_created = [filename, md_file.name]
                if mp4_file:
                    files_created.append(Path(mp4_file).name)

                return {
                    "status": "success",
                    "script": result["script"],
                    "storyboard": result["storyboard"],
                    "scenes": result.get("scenes", []),
                    "type": video_type,
                    "filepath": str(filepath),
                    "filename": filename,
                    "video_file": str(mp4_file) if mp4_file else None,
                    "message": f"✓ Video created: '{concept[:30]}...'\n\n📁 Files:\n" + "\n".join(f"   - {f}" for f in files_created)
                }
            else:
                return result

        except Exception as e:
            print(f"[VideoGeneration] Error: {e}")
            return {
                "status": "error",
                "message": f"Video generation failed: {str(e)}"
            }

    def _detect_video_type(self, concept):
        """Detect video type from concept"""
        concept_lower = concept.lower()

        types = {
            "tutorial": ["tutorial", "how to", "guide", "lesson"],
            "commercial": ["ad", "commercial", "advertisement", "promo"],
            "music_video": ["music video", "song", "music"],
            "documentary": ["documentary", "explain", "educational"],
            "animation": ["animation", "animated", "cartoon"],
            "narrative": ["story", "narrative", "film", "short film"]
        }

        for vtype, keywords in types.items():
            if any(keyword in concept_lower for keyword in keywords):
                return vtype

        return "general"

    def _generate_video_concept(self, concept, video_type, duration, options):
        """Generate video script and storyboard using Ollama"""
        try:
            prompt = self._build_video_prompt(concept, video_type, duration, options)

            model = options.get("model", "nexusai-visual-agent:latest")

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a video director and storyboard artist specializing in {video_type} videos. Create detailed scripts and visual storyboards."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "num_ctx": 8192
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")

                # Parse into script and storyboard
                script, storyboard, scenes = self._parse_video_content(content)

                return {
                    "status": "success",
                    "script": script,
                    "storyboard": storyboard,
                    "scenes": scenes
                }
            else:
                return {
                    "status": "error",
                    "message": f"Model returned status {response.status_code}"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _build_video_prompt(self, concept, video_type, duration, options):
        """Build prompt for video generation"""
        num_scenes = max(3, duration // 10)  # Roughly one scene per 10 seconds

        prompt = f"Create a detailed {video_type} video concept for: {concept}\n\n"
        prompt += f"Duration: {duration} seconds\n"
        prompt += f"Number of scenes: approximately {num_scenes}\n\n"
        prompt += "Provide:\n\n"
        prompt += "1. **SCRIPT**: Complete narration/dialogue\n\n"
        prompt += "2. **STORYBOARD**: Detailed visual description for each scene including:\n"
        prompt += "   - Scene number and duration\n"
        prompt += "   - Visual composition (camera angle, framing)\n"
        prompt += "   - Action/movement\n"
        prompt += "   - Key visual elements\n"
        prompt += "   - Transitions\n\n"
        prompt += "Format your response clearly with sections labeled SCRIPT and STORYBOARD."

        return prompt

    def _parse_video_content(self, content):
        """Parse generated content into script, storyboard, and scenes"""
        script = ""
        storyboard = ""
        scenes = []

        # Try to split by sections
        if "SCRIPT" in content.upper() and "STORYBOARD" in content.upper():
            parts = content.upper().split("STORYBOARD")
            script_part = parts[0].replace("SCRIPT", "").strip()
            storyboard_part = parts[1].strip() if len(parts) > 1 else ""

            # Get original case versions
            script_idx = content.upper().find("SCRIPT")
            storyboard_idx = content.upper().find("STORYBOARD")

            if script_idx >= 0 and storyboard_idx >= 0:
                script = content[script_idx + 6:storyboard_idx].strip()
                storyboard = content[storyboard_idx + 10:].strip()

        else:
            # If not clearly separated, use first half as script, second as storyboard
            mid = len(content) // 2
            script = content[:mid]
            storyboard = content[mid:]

        # Extract scenes from storyboard
        scene_lines = storyboard.split('\n')
        current_scene = None

        for line in scene_lines:
            if 'scene' in line.lower() and any(char.isdigit() for char in line):
                if current_scene:
                    scenes.append(current_scene)

                current_scene = {
                    "description": line.strip(),
                    "details": []
                }
            elif current_scene and line.strip():
                current_scene["details"].append(line.strip())

        if current_scene:
            scenes.append(current_scene)

        return script, storyboard, scenes

    def generate_scene_images(self, video_concept_file):
        """Generate images for each scene in the storyboard (requires PhotoGeneration agent)"""
        try:
            # Load video concept
            with open(video_concept_file, 'r', encoding='utf-8') as f:
                video_data = json.load(f)

            scenes = video_data.get("scenes", [])

            if not scenes:
                return {
                    "status": "error",
                    "message": "No scenes found in video concept"
                }

            # This would integrate with PhotoGeneration agent
            # For now, return scene prompts
            scene_prompts = []
            for i, scene in enumerate(scenes, 1):
                prompt = f"Scene {i}: {scene.get('description', '')}"
                scene_prompts.append(prompt)

            return {
                "status": "success",
                "scene_prompts": scene_prompts,
                "message": "Scene prompts generated. Use PhotoGeneration agent to create images."
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _render_video_file(self, video_data, video_id, scenes):
        """Render actual MP4 video file using FFmpeg"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            print("[VideoGeneration] Rendering video with FFmpeg...")
            
            # Create temp directory for frames
            temp_dir = self.output_dir / f"temp_{video_id}"
            temp_dir.mkdir(exist_ok=True)
            
            # Generate scene images
            if not scenes or len(scenes) == 0:
                # Create title frame
                img = Image.new('RGB', (1920, 1080), color=(20, 30, 50))
                draw = ImageDraw.Draw(img)
                draw.text((100, 500), video_data['concept'][:100], fill=(255, 255, 255))
                img.save(temp_dir / "scene_000.png")
            else:
                for i, scene in enumerate(scenes):
                    img = Image.new('RGB', (1920, 1080), color=(30, 40, 60))
                    draw = ImageDraw.Draw(img)
                    text = f"Scene {i+1}\n{scene.get('description', '')[:120]}"
                    draw.text((100, 500), text, fill=(255, 255, 255))
                    img.save(temp_dir / f"scene_{i:03d}.png")
            
            # Create video with FFmpeg (Windows-compatible pattern)
            mp4_file = self.output_dir / f"nexus_video_{video_id}.mp4"

            # Windows requires explicit file list instead of glob
            import glob
            scene_files = sorted(glob.glob(str(temp_dir / "scene_*.png")))

            if not scene_files:
                raise Exception("No scene files generated")

            # Create concat file for FFmpeg
            concat_file = temp_dir / "concat.txt"
            with open(concat_file, 'w') as f:
                for scene_file in scene_files:
                    # Each frame shown for 5 seconds
                    f.write(f"file '{scene_file}'\n")
                    f.write(f"duration 5\n")
                # Repeat last frame
                f.write(f"file '{scene_files[-1]}'\n")

            # Run FFmpeg with concat demuxer
            result = subprocess.run([
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1920:1080",
                str(mp4_file)
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"[VideoGeneration] FFmpeg error: {result.stderr}")
                raise Exception(f"FFmpeg failed: {result.stderr[:200]}")
            
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return {
                "status": "success",
                "filepath": str(mp4_file),
                "method": "ffmpeg"
            }
            
        except Exception as e:
            print(f"[VideoGeneration] Error: {e}")
            return {"status": "error", "message": str(e)}

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Music Generation Agent
Generates music using Ollama music models and saves MIDI/ABC notation
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import requests
import uuid
import re
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealMusicAgent(Agent):
    """Agent that creates complete songs with lyrics, melodies, and can generate audio"""

    def __init__(self):
        super().__init__(
            name="MusicGeneration",
            description="Creates complete songs with lyrics, melodies, chord progressions, and audio",
            capabilities=[
                "Generate complete songs with lyrics and music",
                "Create music in any style (rock, pop, hip-hop, country, etc.)",
                "Write lyrics based on themes and emotions",
                "Generate chord progressions and melodies",
                "Export to various formats (text, JSON, ABC notation)",
                "Prepare for audio synthesis",
                "Create music videos (integration with Video/Photo agents)"
            ]
        )
        self.compositions = []
        self.output_dir = Path("D:/AIArm/Generated/Music")
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.ollama_base = "http://localhost:11434"
        self.lyrics_model = "llama3:latest"  # For creative lyrics
        self.music_model = "llamusic/llamusic:3b"  # Music expert AI
        self.composer_model = "hemanth/classicalmusiccomposer:latest"  # For notation/composition

        # Audio generation settings
        self.use_audio_generation = True
        self.audio_api = "bark"  # Options: bark, musicgen, suno, elevenlabs

    def process(self, description, context=None, options=None):
        """Generate complete song with lyrics and music"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[MusicGeneration] Creating song: {description[:60]}...")

        # Check if this is a music video request
        if "music video" in description.lower() or "video for" in description.lower():
            return self._create_music_video(description, options)

        try:
            # Detect style and attributes
            style = self._detect_style(description)
            print(f"[MusicGeneration] Style: {style}")

            # Generate complete song
            song = self._generate_complete_song(description, style, options)

            if song["status"] == "success":
                # Save the song
                comp_id = str(uuid.uuid4())[:8]
                song_data = song["song_data"]

                # Save as JSON
                json_file = self.output_dir / f"nexus_song_{comp_id}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(song_data, f, indent=2, ensure_ascii=False)

                # Save as readable text
                txt_file = self.output_dir / f"nexus_song_{comp_id}.txt"
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(self._format_song_text(song_data))

                # Save ABC notation if generated
                abc_file = None
                if song_data.get("abc_notation"):
                    abc_file = self.output_dir / f"nexus_song_{comp_id}.abc"
                    with open(abc_file, 'w', encoding='utf-8') as f:
                        f.write(song_data["abc_notation"])

                print(f"[MusicGeneration] Song saved: {json_file.name}")

                # STEP 3: Generate actual MP3 audio file
                mp3_file = None
                if self.use_audio_generation and options.get("generate_audio", True):
                    print(f"[MusicGeneration] Generating MP3 audio...")
                    audio_result = self._generate_audio_file(song_data, comp_id)
                    if audio_result["status"] == "success":
                        mp3_file = audio_result["filepath"]
                        print(f"[MusicGeneration] Audio saved: {Path(mp3_file).name}")

                # Log composition
                self.compositions.append({
                    "timestamp": self.last_used,
                    "description": description,
                    "song_id": comp_id,
                    "style": style,
                    "filepath": str(json_file),
                    "audio_file": str(mp3_file) if mp3_file else None
                })

                files_created = [json_file.name, txt_file.name]
                if mp3_file:
                    files_created.append(Path(mp3_file).name)

                return {
                    "status": "success",
                    "song_id": comp_id,
                    "song_data": song_data,
                    "files": {
                        "json": str(json_file),
                        "text": str(txt_file),
                        "abc": str(abc_file) if abc_file else None,
                        "mp3": str(mp3_file) if mp3_file else None
                    },
                    "message": f"✓ Created '{song_data['title']}' - {style} song\n\n📁 Files:\n" + "\n".join(f"   - {f}" for f in files_created)
                }
            else:
                return song

        except Exception as e:
            print(f"[MusicGeneration] Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"Song generation failed: {str(e)}"
            }

    def _generate_complete_song(self, description, style, options):
        """Generate complete song with all components"""
        try:
            # Step 1: Generate lyrics
            print("[MusicGeneration] Generating lyrics...")
            lyrics_result = self._generate_lyrics(description, style)

            if lyrics_result["status"] != "success":
                return lyrics_result

            # Step 2: Generate musical structure
            print("[MusicGeneration] Creating musical structure...")
            music_structure = self._generate_music_structure(description, style, lyrics_result["lyrics"])

            # Build complete song data
            song_data = {
                "title": lyrics_result.get("title", self._extract_title(description)),
                "artist": "Nexus AI",
                "style": style,
                "description": description,
                "lyrics": lyrics_result["lyrics"],
                "structure": lyrics_result.get("structure", music_structure.get("structure")),
                "chords": music_structure.get("chords", []),
                "key": music_structure.get("key", "C"),
                "tempo": music_structure.get("tempo", 120),
                "time_signature": music_structure.get("time_signature", "4/4"),
                "instrumentation": music_structure.get("instrumentation", []),
                "melody_notes": music_structure.get("melody_notes"),
                "abc_notation": music_structure.get("abc_notation"),
                "created": datetime.now().isoformat()
            }

            return {
                "status": "success",
                "song_data": song_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Song generation failed: {str(e)}"
            }

    def _generate_lyrics(self, description, style):
        """Generate complete song lyrics"""
        try:
            prompt = f"""Write complete song lyrics for: {description}

Style: {style}

Requirements:
- Create a compelling title
- Include verse(s), chorus, and bridge
- Make lyrics emotionally resonant and meaningful
- Match the {style} style authentically
- Label each section clearly (Verse 1, Chorus, etc.)
- Write COMPLETE lyrics, not placeholders

Be creative and heartfelt."""

            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.lyrics_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a professional songwriter specializing in {style} music. Write authentic, complete lyrics with emotion and depth."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.9,
                        "num_ctx": 4096
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                lyrics_text = data.get("message", {}).get("content", "")

                # Extract title and structure
                title = self._extract_title_from_lyrics(lyrics_text) or self._extract_title(description)
                structure = self._parse_song_structure(lyrics_text)

                return {
                    "status": "success",
                    "lyrics": lyrics_text,
                    "title": title,
                    "structure": structure
                }
            else:
                return {
                    "status": "error",
                    "message": "Lyrics generation failed"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _generate_music_structure(self, description, style, lyrics):
        """Generate musical components (chords, melody, etc.)"""
        try:
            prompt = f"""Create musical structure for this {style} song:

Description: {description}

Lyrics preview:
{lyrics[:500]}...

Provide:
1. Chord progression (list of chords)
2. Key signature
3. Tempo (BPM)
4. Time signature
5. Instrumentation list
6. Melody suggestions (optional ABC notation)

Format as JSON."""

            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.music_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a music arranger. Provide structured musical data in JSON format."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.5
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")

                # Try to parse JSON
                music_data = self._extract_music_data(content, style)
                return music_data
            else:
                # Return defaults
                return self._get_default_music_structure(style)

        except Exception as e:
            print(f"[MusicGeneration] Music structure error: {e}")
            return self._get_default_music_structure(style)

    def _get_default_music_structure(self, style):
        """Get default musical structure for a style"""
        defaults = {
            "rock": {
                "chords": ["E", "A", "D", "G"],
                "key": "E",
                "tempo": 120,
                "time_signature": "4/4",
                "instrumentation": ["electric guitar", "bass", "drums", "vocals"]
            },
            "pop": {
                "chords": ["C", "G", "Am", "F"],
                "key": "C",
                "tempo": 110,
                "time_signature": "4/4",
                "instrumentation": ["piano", "synth", "drums", "vocals"]
            },
            "country": {
                "chords": ["G", "C", "D", "Em"],
                "key": "G",
                "tempo": 100,
                "time_signature": "4/4",
                "instrumentation": ["acoustic guitar", "fiddle", "steel guitar", "vocals"]
            }
        }

        return defaults.get(style, defaults["pop"])

    def _detect_style(self, description):
        """Detect music style from description"""
        description_lower = description.lower()

        styles = {
            "rock": ["rock", "linkin park", "alternative", "metal", "punk"],
            "pop": ["pop", "taylor swift", "ariana grande"],
            "country": ["country", "nashville", "western"],
            "hip-hop": ["hip hop", "rap", "hip-hop"],
            "r&b": ["r&b", "soul", "rhythm and blues"],
            "jazz": ["jazz", "swing", "bebop", "blues"],
            "electronic": ["electronic", "edm", "techno", "synth"],
            "classical": ["classical", "symphony", "orchestra", "baroque"],
            "folk": ["folk", "acoustic", "traditional"],
            "christian": ["christian", "worship", "gospel", "yeshua", "jesus", "god"]
        }

        for style, keywords in styles.items():
            if any(keyword in description_lower for keyword in keywords):
                return style

        return "pop"

    def _create_music_video(self, description, options):
        """Create a music video by coordinating with Video and Photo agents"""
        print("[MusicGeneration] Creating music video...")

        # First, check if we have a song file reference
        song_file = options.get("song_file")

        if not song_file:
            # Check if description mentions a recent song
            if self.compositions:
                # Use most recent song
                song_file = self.compositions[-1]["filepath"]
                print(f"[MusicGeneration] Using recent song: {song_file}")

        if not song_file or not Path(song_file).exists():
            return {
                "status": "error",
                "message": "No song found. Please create a song first, then request a music video."
            }

        # Load song data
        try:
            with open(song_file, 'r', encoding='utf-8') as f:
                song_data = json.load(f)

            # Create music video concept
            video_concept = f"""Music video for '{song_data['title']}' by {song_data['artist']}

Style: {song_data['style']}
Theme: {song_data['description']}

Lyrics preview:
{song_data['lyrics'][:300]}...

Create a compelling music video concept with:
- Visual theme matching the lyrics
- Scene-by-scene breakdown
- Visual effects and transitions
- Performance shots and narrative elements"""

            # Note: This would integrate with Video Agent
            # For now, return the concept
            return {
                "status": "success",
                "message": f"Music video concept created for '{song_data['title']}'",
                "song_file": song_file,
                "video_concept": video_concept,
                "next_step": "Use Video Agent to generate full storyboard and Photo Agent to create scene images"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Music video creation failed: {str(e)}"
            }

    def _extract_title(self, description):
        """Extract or generate title from description"""
        # Simple title extraction
        words = description.split()[:6]
        return " ".join(words).title()

    def _extract_title_from_lyrics(self, lyrics):
        """Try to extract title from lyrics text"""
        lines = lyrics.split('\n')
        for line in lines[:5]:
            if 'title:' in line.lower():
                return line.split(':', 1)[1].strip().strip('"\'')
            if line.startswith('#'):
                return line.strip('# \n')
        return None

    def _parse_song_structure(self, lyrics):
        """Parse song structure from lyrics"""
        structure = []
        lines = lyrics.split('\n')

        for line in lines:
            line_lower = line.lower().strip()
            if any(section in line_lower for section in ['verse', 'chorus', 'bridge', 'intro', 'outro', 'pre-chorus']):
                structure.append(line.strip())

        return structure

    def _extract_music_data(self, content, style):
        """Extract music data from AI response"""
        import json as json_lib

        try:
            # Try to parse JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json_lib.loads(json_match.group(0))
                return data
        except:
            pass

        # Fallback to defaults
        return self._get_default_music_structure(style)

    def _format_song_text(self, song_data):
        """Format song data as readable text"""
        text = f"{'='*60}\n"
        text += f"{song_data['title']}\n"
        text += f"Artist: {song_data['artist']}\n"
        text += f"Style: {song_data['style']}\n"
        text += f"{'='*60}\n\n"

        text += f"Key: {song_data['key']} | Tempo: {song_data['tempo']} BPM | Time: {song_data['time_signature']}\n"
        text += f"Chords: {', '.join(song_data.get('chords', []))}\n"
        text += f"Instrumentation: {', '.join(song_data.get('instrumentation', []))}\n\n"

        text += f"{'-'*60}\n"
        text += f"LYRICS\n"
        text += f"{'-'*60}\n\n"
        text += song_data['lyrics']
        text += f"\n\n{'='*60}\n"
        text += f"Generated: {song_data['created']}\n"

        return text

    def _generate_audio_file(self, song_data, comp_id):
        """Generate actual MP3 audio file from song data"""
        try:
            # Try multiple audio generation methods in order of preference
            methods = [
                self._generate_with_bark,
                self._generate_with_pyttsx3,
                self._generate_with_gtts
            ]

            for method in methods:
                try:
                    result = method(song_data, comp_id)
                    if result["status"] == "success":
                        return result
                except Exception as e:
                    print(f"[MusicGeneration] Audio method failed: {e}")
                    continue

            # If all methods fail, create a placeholder
            return self._create_audio_placeholder(song_data, comp_id)

        except Exception as e:
            return {
                "status": "error",
                "message": f"Audio generation failed: {str(e)}"
            }

    def _generate_with_bark(self, song_data, comp_id):
        """Generate audio using Bark (text-to-speech with singing)"""
        try:
            # Try to import bark
            from bark import SAMPLE_RATE, generate_audio, preload_models
            from scipy.io.wavfile import write as write_wav

            print("[MusicGeneration] Using Bark for audio generation...")

            # Preload models
            preload_models()

            # Generate audio from lyrics
            lyrics = song_data["lyrics"]
            audio_array = generate_audio(lyrics[:1000])  # Limit length

            # Save as WAV first
            wav_file = self.output_dir / f"nexus_song_{comp_id}.wav"
            write_wav(str(wav_file), SAMPLE_RATE, audio_array)

            # Convert to MP3 using FFmpeg
            mp3_file = self.output_dir / f"nexus_song_{comp_id}.mp3"
            subprocess.run([
                "ffmpeg", "-i", str(wav_file), "-y",
                "-codec:a", "libmp3lame", "-qscale:a", "2",
                str(mp3_file)
            ], check=True, capture_output=True)

            # Clean up WAV
            wav_file.unlink(missing_ok=True)

            return {
                "status": "success",
                "filepath": str(mp3_file),
                "method": "bark"
            }

        except ImportError:
            print("[MusicGeneration] Bark not installed")
            raise
        except Exception as e:
            print(f"[MusicGeneration] Bark error: {e}")
            raise

    def _generate_with_pyttsx3(self, song_data, comp_id):
        """Generate audio using pyttsx3 (offline TTS)"""
        try:
            import pyttsx3

            print("[MusicGeneration] Using pyttsx3 for audio generation...")

            engine = pyttsx3.init()

            # Set properties for better quality
            engine.setProperty('rate', song_data.get("tempo", 120))
            engine.setProperty('volume', 0.9)

            # Save to file
            wav_file = self.output_dir / f"nexus_song_{comp_id}.wav"
            engine.save_to_file(song_data["lyrics"], str(wav_file))
            engine.runAndWait()

            # Convert to MP3
            mp3_file = self.output_dir / f"nexus_song_{comp_id}.mp3"
            subprocess.run([
                "ffmpeg", "-i", str(wav_file), "-y",
                "-codec:a", "libmp3lame", "-qscale:a", "2",
                str(mp3_file)
            ], check=True, capture_output=True)

            # Clean up WAV
            wav_file.unlink(missing_ok=True)

            return {
                "status": "success",
                "filepath": str(mp3_file),
                "method": "pyttsx3"
            }

        except Exception as e:
            print(f"[MusicGeneration] pyttsx3 error: {e}")
            raise

    def _generate_with_gtts(self, song_data, comp_id):
        """Generate audio using gTTS (Google Text-to-Speech)"""
        try:
            from gtts import gTTS

            print("[MusicGeneration] Using gTTS for audio generation...")

            # Create TTS object
            tts = gTTS(text=song_data["lyrics"], lang='en', slow=False)

            # Save directly as MP3
            mp3_file = self.output_dir / f"nexus_song_{comp_id}.mp3"
            tts.save(str(mp3_file))

            return {
                "status": "success",
                "filepath": str(mp3_file),
                "method": "gtts"
            }

        except Exception as e:
            print(f"[MusicGeneration] gTTS error: {e}")
            raise

    def _create_audio_placeholder(self, song_data, comp_id):
        """Create a placeholder MP3 with instructions"""
        try:
            print("[MusicGeneration] Creating audio placeholder...")

            # Create a text file with audio generation instructions
            instructions_file = self.output_dir / f"nexus_song_{comp_id}_AUDIO_INSTRUCTIONS.txt"
            with open(instructions_file, 'w', encoding='utf-8') as f:
                f.write(f"Audio Generation Instructions for '{song_data['title']}'\n")
                f.write("="*60 + "\n\n")
                f.write("To generate audio for this song:\n\n")
                f.write("Option 1 - Suno AI (Recommended):\n")
                f.write(f"  1. Go to https://suno.ai\n")
                f.write(f"  2. Input: {song_data['description']}\n")
                f.write(f"  3. Style: {song_data['style']}\n")
                f.write(f"  4. Download as MP3\n\n")
                f.write("Option 2 - Local Tools:\n")
                f.write("  Install: pip install bark gTTS pyttsx3\n")
                f.write("  Then run Nexus again\n\n")
                f.write(f"Song Data:\n")
                f.write(f"  Title: {song_data['title']}\n")
                f.write(f"  Style: {song_data['style']}\n")
                f.write(f"  Tempo: {song_data['tempo']} BPM\n")
                f.write(f"  Key: {song_data['key']}\n")

            return {
                "status": "partial",
                "filepath": str(instructions_file),
                "message": "Audio generation tools not available. Instructions saved."
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _generate_music(self, description, model, style, options):
        """Generate music using Ollama music model"""
        try:
            prompt = self._build_music_prompt(description, style, options)

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a music composer. Generate music in ABC notation or describe musical elements clearly. Be creative and expressive."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.9,  # High creativity
                        "top_p": 0.95
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                composition = data.get("message", {}).get("content", "")

                return {
                    "status": "success",
                    "composition": composition
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

    def _build_music_prompt(self, description, style, options):
        """Build prompt for music generation"""
        prompt = f"Compose a {style} music piece based on this description: {description}\n\n"

        if options.get("abc_notation"):
            prompt += "Provide the composition in ABC music notation format.\n"
        else:
            prompt += "Describe the musical elements: melody, harmony, rhythm, instrumentation, and structure.\n"

        if options.get("length"):
            prompt += f"Length: {options['length']}\n"

        prompt += "\nBe creative and expressive in your composition."

        return prompt

    def _extract_abc(self, text):
        """Extract ABC notation from generated text"""
        # Look for ABC notation patterns
        abc_pattern = r'X:\s*\d+.*?(?=\n\n|\Z)'
        matches = re.findall(abc_pattern, text, re.DOTALL)

        if matches:
            return matches[0]

        # Alternative: Look for lines starting with standard ABC headers
        lines = text.split('\n')
        abc_lines = []
        in_abc = False

        for line in lines:
            if line.startswith('X:') or line.startswith('T:') or line.startswith('M:'):
                in_abc = True

            if in_abc:
                abc_lines.append(line)

                # Stop at double newline or non-ABC content
                if not line.strip() and abc_lines:
                    break

        if abc_lines:
            return '\n'.join(abc_lines)

        return None

    def generate_melody(self, description, key="C", time_signature="4/4"):
        """Generate a melody with specific musical parameters"""
        options = {
            "abc_notation": True,
            "key": key,
            "time_signature": time_signature
        }

        enhanced_desc = f"{description} in the key of {key} with {time_signature} time signature"

        return self.process(enhanced_desc, options=options)

    def generate_chord_progression(self, style, num_chords=4):
        """Generate a chord progression"""
        description = f"Create a {num_chords}-chord progression in {style} style"

        return self.process(description)

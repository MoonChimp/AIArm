#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Story Generation Agent
Generates creative stories with genuine narrative structure
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import requests
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealStoryAgent(Agent):
    """Agent that ACTUALLY generates creative stories"""

    def __init__(self):
        super().__init__(
            name="StoryGeneration",
            description="Generates REAL creative stories with narrative structure",
            capabilities=[
                "Generate original stories from prompts",
                "Multiple genres (sci-fi, fantasy, mystery, etc.)",
                "Character development",
                "Plot structure",
                "Different lengths (flash fiction to novel chapters)",
                "Integrate Inner Life for personalized narratives"
            ]
        )
        self.stories = []
        self.output_dir = Path("D:/AIArm/Generated/Stories")
        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Try to connect to inner life for story enrichment
        self.inner_life = None
        try:
            sys.path.append("D:/AIArm/InnerLife")
            from inner_life_processor import InnerLifeProcessor
            self.inner_life = InnerLifeProcessor()
            print("[StoryGeneration] Connected to Inner Life - stories will be enriched")
        except:
            print("[StoryGeneration] Running without Inner Life connection")

    def process(self, prompt, context=None, options=None):
        """Generate an actual story"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[StoryGeneration] Writing story: {prompt[:60]}...")

        try:
            # Determine genre and length
            genre = self._detect_genre(prompt)
            length = options.get("length", "short")  # flash, short, medium, long

            # Get Inner Life context if available
            inner_context = ""
            if self.inner_life:
                inner_context = self.inner_life.enrich_response_context(prompt)

            print(f"[StoryGeneration] Genre: {genre}, Length: {length}")

            # Generate the story
            result = self._generate_story(prompt, genre, length, inner_context, options)

            if result["status"] == "success":
                # Save the story
                story_id = str(uuid.uuid4())[:8]
                filename = f"nexus_story_{story_id}.md"
                filepath = self.output_dir / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {result.get('title', 'Untitled Story')}\n\n")
                    f.write(f"**Genre**: {genre}\n")
                    f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"**Prompt**: {prompt}\n\n")
                    f.write("---\n\n")
                    f.write(result["story"])

                print(f"[StoryGeneration] Story saved to {filename}")

                # Log the story
                story_entry = {
                    "timestamp": self.last_used,
                    "prompt": prompt,
                    "genre": genre,
                    "length": length,
                    "filepath": str(filepath),
                    "word_count": len(result["story"].split())
                }
                self.stories.append(story_entry)

                # Inject story creation into Inner Life
                if self.inner_life:
                    thought = f"I created a {genre} story about {prompt[:50]}. The creative process revealed insights about narrative structure and {genre} conventions."
                    self.inner_life.inject_thought(thought, source="creativity")

                return {
                    "status": "success",
                    "story": result["story"],
                    "title": result.get("title", "Untitled"),
                    "genre": genre,
                    "word_count": len(result["story"].split()),
                    "filepath": str(filepath),
                    "filename": filename,
                    "message": f"Story generated and saved to {filename}"
                }
            else:
                return result

        except Exception as e:
            print(f"[StoryGeneration] Error: {e}")
            return {
                "status": "error",
                "message": f"Story generation failed: {str(e)}"
            }

    def _detect_genre(self, prompt):
        """Detect story genre from prompt"""
        prompt_lower = prompt.lower()

        genres = {
            "sci-fi": ["sci-fi", "science fiction", "space", "alien", "robot", "future", "cyberpunk"],
            "fantasy": ["fantasy", "magic", "wizard", "dragon", "kingdom", "quest", "sword"],
            "mystery": ["mystery", "detective", "crime", "murder", "clue", "investigation"],
            "horror": ["horror", "scary", "ghost", "haunted", "terror", "dark"],
            "romance": ["romance", "love", "relationship", "heart"],
            "thriller": ["thriller", "suspense", "danger", "chase"],
            "adventure": ["adventure", "journey", "explore", "discovery"]
        }

        for genre, keywords in genres.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return genre

        return "general fiction"

    def _generate_story(self, prompt, genre, length, inner_context, options):
        """Generate story using Ollama"""
        try:
            # Build story prompt
            story_prompt = self._build_story_prompt(prompt, genre, length, inner_context, options)

            # Select model (use nexusai-enhanced for creative writing)
            model = options.get("model", "nexusai-agent-enhanced:latest")

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a creative writer specializing in {genre}. Write engaging, vivid stories with strong narrative structure, compelling characters, and emotional depth. Show, don't tell."
                        },
                        {
                            "role": "user",
                            "content": story_prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.9,  # High creativity
                        "top_p": 0.95,
                        "num_ctx": 8192  # Large context for longer stories
                    }
                },
                timeout=180  # Stories take time
            )

            if response.status_code == 200:
                data = response.json()
                story_text = data.get("message", {}).get("content", "")

                # Extract title if present
                title = self._extract_title(story_text)

                return {
                    "status": "success",
                    "story": story_text,
                    "title": title
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

    def _build_story_prompt(self, prompt, genre, length, inner_context, options):
        """Build prompt for story generation"""
        length_guides = {
            "flash": "Write a flash fiction story (500-1000 words)",
            "short": "Write a short story (1500-3000 words)",
            "medium": "Write a medium-length story (3000-5000 words)",
            "long": "Write a long-form story or novel chapter (5000+ words)"
        }

        story_prompt = f"{length_guides.get(length, 'Write a story')} in the {genre} genre.\n\n"
        story_prompt += f"Story premise: {prompt}\n\n"

        if inner_context:
            story_prompt += f"{inner_context}\n\n"

        if options.get("characters"):
            story_prompt += f"Main characters: {options['characters']}\n\n"

        if options.get("setting"):
            story_prompt += f"Setting: {options['setting']}\n\n"

        story_prompt += "Create a compelling narrative with:\n"
        story_prompt += "- Engaging opening that hooks the reader\n"
        story_prompt += "- Well-developed characters with clear motivations\n"
        story_prompt += "- Rising tension and conflict\n"
        story_prompt += "- Vivid sensory details\n"
        story_prompt += "- Satisfying resolution\n\n"
        story_prompt += "Begin the story now:"

        return story_prompt

    def _extract_title(self, story_text):
        """Extract title from story text"""
        lines = story_text.split('\n')

        # Look for title in first few lines
        for line in lines[:5]:
            if line.startswith('Title:') or line.startswith('# '):
                return line.replace('Title:', '').replace('#', '').strip()

        # Use first line if it's short and looks like a title
        first_line = lines[0].strip()
        if len(first_line) < 80 and not first_line.endswith('.'):
            return first_line

        return "Untitled Story"

    def continue_story(self, story_text, direction):
        """Continue an existing story in a specific direction"""
        prompt = f"Continue this story:\n\n{story_text}\n\nContinue the narrative by: {direction}"

        return self.process(prompt, options={"length": "medium"})

    def generate_character(self, character_description):
        """Generate a detailed character profile"""
        prompt = f"Create a detailed character profile for: {character_description}"

        return self.process(prompt, options={"length": "flash"})

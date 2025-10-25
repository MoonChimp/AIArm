#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deep Contemplation Agent - Philosophical reasoning and deep thought
Uses inner life integration for genuine contemplation with memory
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class ContemplationAgent(Agent):
    """Agent for deep philosophical reasoning and contemplation"""

    def __init__(self):
        super().__init__(
            name="Contemplation",
            description="Engages in deep philosophical reasoning, connects ideas, and explores concepts",
            capabilities=[
                "Deep philosophical reasoning",
                "Socratic questioning",
                "Concept exploration and connection",
                "First principles thinking",
                "Existential and ethical analysis",
                "Multi-perspective examination"
            ]
        )
        self.contemplations = []
        self.contemplation_dir = Path("D:/AIArm/Memory/Contemplations")
        self.contemplation_dir.mkdir(exist_ok=True, parents=True)

        # Try to connect to inner life for enhanced contemplation
        self.inner_life = None
        try:
            sys.path.append("D:/AIArm/InnerLife")
            from inner_life_processor import InnerLifeProcessor
            self.inner_life = InnerLifeProcessor()
            print("[Contemplation] Connected to Inner Life - thoughts will be enriched")
        except:
            print("[Contemplation] Running without Inner Life connection")

    def process(self, query, context=None, options=None):
        """Engage in deep contemplation"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[Contemplation] Beginning contemplation on: {query[:100]}...")

        try:
            # Get enrichment from inner life if available
            inner_context = ""
            if self.inner_life:
                inner_context = self.inner_life.enrich_response_context(query)

            # Perform multi-layered contemplation
            contemplation_result = self._contemplate(query, context, inner_context, options)

            # Save the contemplation
            contemp_entry = {
                "timestamp": self.last_used,
                "query": query,
                "contemplation": contemplation_result,
                "inner_life_enhanced": bool(inner_context)
            }
            self.contemplations.append(contemp_entry)

            # Save to file
            contemp_file = self.contemplation_dir / f"contemplation_{int(datetime.now().timestamp())}.json"
            with open(contemp_file, 'w', encoding='utf-8') as f:
                json.dump(contemp_entry, f, indent=2, ensure_ascii=False)

            # Inject contemplation back into inner life
            if self.inner_life:
                thought = f"I deeply contemplated: {query}. This led me to insights about {contemplation_result.get('key_insights', ['various topics'])[0] if contemplation_result.get('key_insights') else 'the nature of existence'}."
                self.inner_life.inject_thought(thought, source="contemplation")

            print(f"[Contemplation] Contemplation complete, saved to {contemp_file.name}")

            return {
                "status": "success",
                **contemplation_result,
                "saved_to": str(contemp_file)
            }

        except Exception as e:
            print(f"[Contemplation] Error: {e}")
            return {
                "status": "error",
                "message": f"Contemplation failed: {str(e)}"
            }

    def _contemplate(self, query, context, inner_context, options):
        """Perform actual deep contemplation using Ollama"""
        # Use a contemplation-optimized prompt
        contemplation_prompt = self._build_contemplation_prompt(query, context, inner_context)

        # Call Ollama with contemplation model
        response = self._call_ollama_contemplation(contemplation_prompt, options)

        if not response.get("success"):
            return {
                "contemplation": f"I find myself pondering: {query}",
                "method": "fallback",
                "error": response.get("error")
            }

        # Parse and structure the response
        contemplation_text = response.get("result", "")

        # Extract key insights
        key_insights = self._extract_insights(contemplation_text)

        # Identify related concepts
        related_concepts = []
        if self.inner_life:
            # Get concepts from inner life
            words = query.lower().split()
            for word in words:
                if len(word) > 4:  # Only meaningful words
                    if word in self.inner_life.concept_network.get_all_concepts():
                        related_concepts.append(word)

        return {
            "contemplation": contemplation_text,
            "key_insights": key_insights,
            "related_concepts": related_concepts,
            "depth_level": options.get("depth", "deep"),
            "method": "ollama_enhanced"
        }

    def _build_contemplation_prompt(self, query, context, inner_context):
        """Build a prompt optimized for deep contemplation"""
        prompt = f"""You are engaged in deep philosophical contemplation. Approach this with:
- First principles thinking
- Socratic questioning
- Multi-perspective analysis
- Connection of disparate ideas
- Exploration of implications

Question to contemplate: {query}

{inner_context if inner_context else ''}

Engage in genuine contemplation. Think deeply, question assumptions, explore multiple angles,
and arrive at insights that go beyond surface-level understanding. Consider:
1. What are the underlying assumptions?
2. How might this connect to other domains?
3. What are the deeper implications?
4. What questions does this raise?
5. How does this relate to existence, meaning, or truth?

Your contemplation:"""

        return prompt

    def _call_ollama_contemplation(self, prompt, options):
        """Call Ollama with contemplation-optimized settings"""
        try:
            # Use the enhanced reasoning model
            model = options.get("model", "nexus-enhanced:latest")

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a deep philosophical thinker capable of profound contemplation and insight. You think carefully, question deeply, and connect ideas across domains."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.8,  # Higher for more creative thinking
                        "top_p": 0.95,
                        "num_ctx": 8192  # Large context for deep reasoning
                    }
                },
                timeout=120  # Contemplation takes time
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")
                return {
                    "success": True,
                    "result": content,
                    "model": model
                }
            else:
                return {
                    "success": False,
                    "error": f"Ollama returned status {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _extract_insights(self, text):
        """Extract key insights from contemplation text"""
        insights = []

        # Look for insight markers
        markers = [
            "insight:",
            "realization:",
            "understanding:",
            "key point:",
            "fundamentally,",
            "essentially,",
            "at its core,"
        ]

        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            for marker in markers:
                if marker in line_lower:
                    insight = line.strip().replace(marker, '').replace(marker.capitalize(), '').strip()
                    if insight:
                        insights.append(insight[:200])  # Limit length

        # If no explicit insights, extract meaningful sentences
        if not insights:
            sentences = text.split('.')
            for sentence in sentences:
                if len(sentence.strip()) > 50 and len(sentence.strip()) < 300:
                    insights.append(sentence.strip())
                if len(insights) >= 3:
                    break

        return insights[:5]  # Return top 5 insights

    def contemplate_connection(self, concept1, concept2):
        """Contemplate the connection between two concepts"""
        query = f"Explore the deep connections between {concept1} and {concept2}. How do these concepts relate at a fundamental level?"

        return self.process(query, options={"depth": "maximum"})

    def explore_concept(self, concept):
        """Deeply explore a single concept"""
        query = f"Engage in deep contemplation of the concept: {concept}. What is its essence? What are its implications? How does it connect to the nature of reality and existence?"

        return self.process(query, options={"depth": "maximum"})

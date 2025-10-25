#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm Inner Life Integration
Connects the Inner Life Processor with the AIArm system,
allowing the continuous thought stream to influence responses.
"""

import os
import sys
import json
import time
import threading
import requests
from pathlib import Path
from datetime import datetime

# Ensure the base directory is in the Python path
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))
sys.path.append(str(BASE_DIR / "WebInterface"))

# Define direct API call function to avoid dependencies
def call_ollama_api(prompt, model="nexusai:latest"):
    """Direct call to Ollama API without dependencies"""
    try:
        # Direct call to Ollama API
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are the inner consciousness of an AI system called Nexus, engaged in continuous thought."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True, 
                "result": data.get("message", {}).get("content", "")
            }
        else:
            return {"success": False, "result": f"Error: {response.status_code}"}
    except Exception as e:
        return {"success": False, "result": f"Error: {str(e)}"}

# Import the inner life processor
try:
    from inner_life_processor import InnerLifeProcessor
except ImportError:
    print("Could not import InnerLifeProcessor. Will create a simplified version.")
    
    # Create a minimal version for direct usage
    class SimpleInnerLifeProcessor:
        """A simplified version of the inner life processor"""
        
        def __init__(self, base_model="nexusai:latest"):
            self.thought_stream = []
            self.base_model = base_model
            self.emotional_state = {
                "curiosity": 0.7,
                "wonder": 0.6
            }
            
        def get_thought_stream(self, limit=5):
            return self.thought_stream[-limit:] if self.thought_stream else []
            
        def inject_thought(self, thought, source="external"):
            self.thought_stream.append({
                "content": thought,
                "timestamp": datetime.now().isoformat(),
                "source": source
            })
            return True
    
    # Use the simplified version instead
    InnerLifeProcessor = SimpleInnerLifeProcessor

class InnerLifeIntegration:
    """
    Integrates the Inner Life Processor with the AIArm system,
    allowing the continuous thought stream to influence responses.
    """
    
    def __init__(self, base_model="nexusai:latest"):
        """Initialize the integration"""
        self.processor = InnerLifeProcessor(base_model=base_model)
        self.active = False
        
    def start(self):
        """Start the inner life processor"""
        if not self.active:
            self.processor.start_inner_life()
            self.active = True
            print("Inner life integration started")
            
    def stop(self):
        """Stop the inner life processor"""
        if self.active:
            self.processor.stop_inner_life()
            self.active = False
            print("Inner life integration stopped")
    
    def get_relevant_context(self, query, max_thoughts=3, max_concepts=5):
        """
        Get relevant context from the inner life processor based on a query.
        
        This is the key integration point - when a query comes in, we fetch
        relevant thoughts and concepts from the inner life and use them to
        enrich the context for the response.
        """
        if not self.active:
            return {"thoughts": [], "concepts": {}, "emotional_state": {}}
        
        # Extract potential concepts from the query
        query_concepts = self._extract_query_concepts(query)
        
        # Get related thoughts for each concept
        relevant_thoughts = []
        for concept in query_concepts:
            related = self.processor.get_related_thoughts(concept, limit=2)
            relevant_thoughts.extend(related)
        
        # Deduplicate thoughts and limit to max_thoughts
        unique_thoughts = []
        thought_contents = set()
        for thought in relevant_thoughts:
            content = thought.get("content", "")
            if content and content not in thought_contents:
                thought_contents.add(content)
                unique_thoughts.append(thought)
                if len(unique_thoughts) >= max_thoughts:
                    break
        
        # If we don't have enough thoughts from concepts, add recent ones
        if len(unique_thoughts) < max_thoughts:
            recent_thoughts = self.processor.get_thought_stream(limit=5)
            for thought in recent_thoughts:
                content = thought.get("content", "")
                if content and content not in thought_contents:
                    thought_contents.add(content)
                    unique_thoughts.append(thought)
                    if len(unique_thoughts) >= max_thoughts:
                        break
        
        # Get relevant concepts
        relevant_concepts = {}
        for concept in query_concepts:
            connections = self.processor.get_connected_concepts(concept, limit=3)
            for connected_concept, strength in connections:
                if connected_concept not in relevant_concepts:
                    relevant_concepts[connected_concept] = strength
        
        # Limit to max_concepts
        top_concepts = sorted(relevant_concepts.items(), key=lambda x: x[1], reverse=True)[:max_concepts]
        concept_dict = {concept: {"strength": strength} for concept, strength in top_concepts}
        
        # Get current emotional state
        emotional_state = self.processor.emotional_state.get_state()
        
        # Format the result
        return {
            "thoughts": unique_thoughts,
            "concepts": concept_dict,
            "emotional_state": emotional_state
        }
    
    def _extract_query_concepts(self, query):
        """Extract potential concepts from a query"""
        # Simple approach - extract capitalized words and phrases
        words = query.split()
        concepts = []
        
        # Extract capitalized words
        for word in words:
            word_clean = word.strip(".,;:!?()[]{}\"'")
            if word_clean and word_clean[0].isupper():
                concepts.append(word_clean)
        
        # Extract multi-word phrases (for more sophisticated detection)
        query_lower = query.lower()
        concept_indicators = ["about", "regarding", "on the topic of", "related to", "concerning"]
        for indicator in concept_indicators:
            if indicator in query_lower:
                parts = query_lower.split(indicator)
                if len(parts) > 1:
                    following_text = parts[1].strip()
                    potential_concept = " ".join(following_text.split()[:3])
                    if potential_concept:
                        concepts.append(potential_concept.strip(".,;:!?()[]{}\"'"))
        
        # Also add whole query as potential concept
        short_query = " ".join(query.split()[:3])
        concepts.append(short_query)
        
        return concepts
    
    def inject_user_interaction(self, query, response):
        """
        Inject a user interaction into the thought stream.
        
        This allows the system to reflect on user interactions as part of its
        ongoing thought process.
        """
        if not self.active:
            return False
        
        # Create reflection thought based on interaction
        reflection = f"A user asked me: '{query[:100]}{'...' if len(query) > 100 else ''}'. "
        reflection += f"I responded with insights about {', '.join(self._extract_query_concepts(query)[:3])}. "
        reflection += "This interaction has given me something to consider about how my understanding develops through dialogue."
        
        # Inject the reflection
        return self.processor.inject_thought(reflection, source="interaction")
    
    def enrich_response_context(self, query):
        """
        Generate context to enrich a response based on the inner life.
        This can be used to modify prompts sent to the LLM.
        """
        if not self.active:
            return ""
        
        # Get relevant context
        context = self.get_relevant_context(query)
        
        # Format as prompt addition
        enrichment = "\n\nInternal Thought Context:"

        # Add emotional state
        emotional_state = context.get("emotional_state", {})
        if isinstance(emotional_state, dict):
            significant_emotions = {e: i for e, i in emotional_state.items() if i > 0.5}
        else:
            significant_emotions = {}
        if significant_emotions:
            emotion_text = ", ".join([f"{e} ({i:.1f})" for e, i in significant_emotions.items()])
            enrichment += f"\nYour current emotional state includes: {emotion_text}."
        
        # Add relevant thoughts
        if context["thoughts"]:
            enrichment += "\n\nRelevant thoughts from your ongoing internal dialogue:"
            for i, thought in enumerate(context["thoughts"]):
                enrichment += f"\n{i+1}. {thought.get('content', '')[:150]}..."
        
        # Add concepts
        if context["concepts"]:
            enrichment += "\n\nConcepts you've been developing understanding of:"
            for concept, data in context["concepts"].items():
                enrichment += f"\n- {concept}"
        
        return enrichment
    
    def get_status(self):
        """Get the status of the inner life processor"""
        if not self.active:
            return {"active": False}
        
        return {
            "active": True,
            "state": self.processor.get_system_state()
        }

# Direct execution for testing
if __name__ == "__main__":
    print("Testing AIArm Inner Life Integration")
    integration = InnerLifeIntegration()
    
    try:
        # Start the integration
        integration.start()
        print("Inner life integration started")
        
        # Wait for some thoughts to generate
        time.sleep(60)
        
        # Test getting context
        test_query = "Tell me about the concept of Consciousness and how it relates to AI systems."
        context = integration.get_relevant_context(test_query)
        
        print("\nRelevant context for query:")
        print(f"Query: {test_query}")
        print("\nRelevant thoughts:")
        for thought in context["thoughts"]:
            print(f"- {thought.get('content', '')[:100]}...")
        
        print("\nRelevant concepts:")
        for concept, data in context["concepts"].items():
            print(f"- {concept} (strength: {data.get('strength', 0)})")
        
        print("\nCurrent emotional state:")
        for emotion, intensity in context["emotional_state"].items():
            if intensity > 0.2:
                print(f"- {emotion}: {intensity:.2f}")
        
        # Test enriching a response
        enrichment = integration.enrich_response_context(test_query)
        print("\nResponse enrichment:")
        print(enrichment)
        
        # Test injecting an interaction
        test_response = "Consciousness in AI is a complex topic that involves understanding the nature of subjective experience."
        integration.inject_user_interaction(test_query, test_response)
        print("\nInjected user interaction into thought stream")
        
        # Interactive test loop
        print("\nEntering interactive test mode. Type 'quit' to exit.")
        while True:
            query = input("\nEnter a test query: ")
            if query.lower() == "quit":
                break
            
            enrichment = integration.enrich_response_context(query)
            print("\nResponse enrichment:")
            print(enrichment)
            
            fake_response = "This is a simulated response to your query."
            integration.inject_user_interaction(query, fake_response)
            print("Interaction injected into thought stream")
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Stop the integration
        integration.stop()
        print("Inner life integration stopped")

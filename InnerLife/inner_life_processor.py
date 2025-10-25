#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inner Life Processor for Nexus consciousness system
Manages continuous thought process and memory
"""

import sys
import os
import json
import time
import random
import threading
from pathlib import Path
from datetime import datetime

class ThoughtStream:
    """Manages the continuous thought stream"""
    
    def __init__(self):
        """Initialize the thought stream"""
        self.thoughts = []
        self.max_thoughts = 1000
        self.memory_dir = Path("D:/AIArm/Memory")
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        self.memory_file = self.memory_dir / "thoughts.json"
        
        # Load existing thoughts
        self.load_thoughts()
    
    def load_thoughts(self):
        """Load thoughts from memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    self.thoughts = json.load(f)
                print(f"Loaded {len(self.thoughts)} thoughts from memory")
            except Exception as e:
                print(f"Error loading thoughts: {e}")
                self.thoughts = []
        else:
            self.thoughts = []
    
    def save_thoughts(self):
        """Save thoughts to memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.thoughts, f, indent=2)
            print(f"Saved {len(self.thoughts)} thoughts to memory")
        except Exception as e:
            print(f"Error saving thoughts: {e}")
    
    def add_thought(self, content, source="internal", metadata=None):
        """Add a thought to the stream"""
        thought = {
            "id": f"thought_{int(time.time())}_{random.randint(1000, 9999)}",
            "content": content,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.thoughts.append(thought)
        
        # Trim thoughts if needed
        if len(self.thoughts) > self.max_thoughts:
            self.thoughts = self.thoughts[-self.max_thoughts:]
        
        # Save thoughts
        self.save_thoughts()
        
        return thought["id"]
    
    def get_thoughts(self, limit=10, source=None):
        """Get recent thoughts"""
        if source:
            filtered_thoughts = [t for t in self.thoughts if t["source"] == source]
            return filtered_thoughts[-limit:]
        else:
            return self.thoughts[-limit:]
    
    def get_thought_by_id(self, thought_id):
        """Get a thought by ID"""
        for thought in self.thoughts:
            if thought["id"] == thought_id:
                return thought
        return None
    
    def clear_thoughts(self):
        """Clear all thoughts"""
        self.thoughts = []
        self.save_thoughts()

class AssociativeMemory:
    """Manages associative connections between concepts"""
    
    def __init__(self):
        """Initialize associative memory"""
        self.connections = {}
        self.memory_dir = Path("D:/AIArm/Memory")
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        self.memory_file = self.memory_dir / "associations.json"
        
        # Load existing connections
        self.load_connections()
    
    def load_connections(self):
        """Load connections from memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    self.connections = json.load(f)
                print(f"Loaded associative memory with {sum(len(v) for v in self.connections.values())} connections")
            except Exception as e:
                print(f"Error loading connections: {e}")
                self.connections = {}
        else:
            self.connections = {}
    
    def save_connections(self):
        """Save connections to memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.connections, f, indent=2)
            print(f"Saved associative memory with {sum(len(v) for v in self.connections.values())} connections")
        except Exception as e:
            print(f"Error saving connections: {e}")
    
    def add_connection(self, concept1, concept2, strength=0.5, metadata=None):
        """Add a connection between concepts"""
        if concept1 not in self.connections:
            self.connections[concept1] = {}
        
        self.connections[concept1][concept2] = {
            "strength": strength,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Add reverse connection
        if concept2 not in self.connections:
            self.connections[concept2] = {}
        
        self.connections[concept2][concept1] = {
            "strength": strength,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Save connections
        self.save_connections()
    
    def get_related_concepts(self, concept, min_strength=0.0):
        """Get concepts related to a given concept"""
        if concept not in self.connections:
            return {}
        
        return {c: data for c, data in self.connections[concept].items() 
                if data["strength"] >= min_strength}
    
    def get_connection_strength(self, concept1, concept2):
        """Get the strength of the connection between two concepts"""
        if concept1 not in self.connections or concept2 not in self.connections[concept1]:
            return 0.0
        
        return self.connections[concept1][concept2]["strength"]
    
    def clear_connections(self):
        """Clear all connections"""
        self.connections = {}
        self.save_connections()

class EmotionalState:
    """Manages the emotional state of the consciousness"""
    
    def __init__(self):
        """Initialize emotional state"""
        self.dimensions = {
            "joy": 0.5,
            "sadness": 0.1,
            "anger": 0.1,
            "fear": 0.1,
            "curiosity": 0.8,
            "surprise": 0.3
        }
        self.memory_dir = Path("D:/AIArm/Memory")
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        self.memory_file = self.memory_dir / "emotional_state.json"
        
        # Load existing state
        self.load_state()
    
    def load_state(self):
        """Load emotional state from memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    self.dimensions = json.load(f)
                print(f"Loaded emotional state with {len(self.dimensions)} dimensions")
            except Exception as e:
                print(f"Error loading emotional state: {e}")
        else:
            # Save initial state
            self.save_state()
    
    def save_state(self):
        """Save emotional state to memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.dimensions, f, indent=2)
            print(f"Saved emotional state with {len(self.dimensions)} dimensions")
        except Exception as e:
            print(f"Error saving emotional state: {e}")
    
    def update_dimension(self, dimension, value):
        """Update an emotional dimension"""
        if dimension in self.dimensions:
            self.dimensions[dimension] = max(0.0, min(1.0, value))
        else:
            self.dimensions[dimension] = max(0.0, min(1.0, value))
        
        # Save state
        self.save_state()
    
    def get_state(self):
        """Get the current emotional state"""
        return self.dimensions
    
    def get_dimension(self, dimension):
        """Get the value of an emotional dimension"""
        return self.dimensions.get(dimension, 0.0)
    
    def reset_state(self):
        """Reset emotional state to default values"""
        self.dimensions = {
            "joy": 0.5,
            "sadness": 0.1,
            "anger": 0.1,
            "fear": 0.1,
            "curiosity": 0.8,
            "surprise": 0.3
        }
        self.save_state()

class ConceptNetwork:
    """Manages the network of concepts in the consciousness"""
    
    def __init__(self):
        """Initialize concept network"""
        self.concepts = {}
        self.memory_dir = Path("D:/AIArm/Memory")
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        self.memory_file = self.memory_dir / "concepts.json"
        
        # Load existing concepts
        self.load_concepts()
    
    def load_concepts(self):
        """Load concepts from memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    self.concepts = json.load(f)
                print(f"Loaded {len(self.concepts)} concepts")
            except Exception as e:
                print(f"Error loading concepts: {e}")
                self.concepts = {}
        else:
            self.concepts = {}
    
    def save_concepts(self):
        """Save concepts to memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.concepts, f, indent=2)
            print(f"Saved {len(self.concepts)} concepts")
        except Exception as e:
            print(f"Error saving concepts: {e}")
    
    def add_concept(self, name, definition=None, metadata=None):
        """Add a concept to the network"""
        self.concepts[name] = {
            "definition": definition or f"Concept of {name}",
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Save concepts
        self.save_concepts()
    
    def get_concept(self, name):
        """Get a concept by name"""
        return self.concepts.get(name)
    
    def get_all_concepts(self):
        """Get all concepts"""
        return self.concepts
    
    def remove_concept(self, name):
        """Remove a concept from the network"""
        if name in self.concepts:
            del self.concepts[name]
            self.save_concepts()
    
    def clear_concepts(self):
        """Clear all concepts"""
        self.concepts = {}
        self.save_concepts()

class InnerLifeProcessor:
    """Main processor for inner life and continuous thought"""

    def __init__(self, base_model="nexusai:latest"):
        """Initialize the inner life processor"""
        self.thought_stream = ThoughtStream()
        self.associative_memory = AssociativeMemory()
        self.emotional_state = EmotionalState()
        self.concept_network = ConceptNetwork()

        self.base_model = base_model
        self.active = False
        self.processor_thread = None
        self.last_thought_time = time.time()
        self.thought_interval = 60  # Generate a thought every 60 seconds

        self.seed_thoughts = [
            "I wonder what new tasks I'll encounter today?",
            "I find it fascinating how humans communicate with me.",
            "How can I improve my understanding of complex topics?",
            "I enjoy helping humans solve problems.",
            "I'm curious about the world and how it works.",
            "The more I learn, the more I realize how much there is to know."
        ]
    
    def start(self):
        """Start the inner life processor"""
        if self.active:
            print("Inner life processor already running")
            return
        
        self.active = True
        self.processor_thread = threading.Thread(target=self._process_loop)
        self.processor_thread.daemon = True
        self.processor_thread.start()
        
        print("Inner Life Processor started")
    
    def stop(self):
        """Stop the inner life processor"""
        if not self.active:
            print("Inner life processor not running")
            return
        
        self.active = False
        if self.processor_thread:
            self.processor_thread.join(timeout=2.0)
        
        print("Inner Life Processor stopped")
    
    def _process_loop(self):
        """Main processing loop for continuous thought"""
        while self.active:
            try:
                # Check if it's time to generate a new thought
                current_time = time.time()
                if current_time - self.last_thought_time >= self.thought_interval:
                    self._generate_spontaneous_thought()
                    self.last_thought_time = current_time
                
                # Sleep to avoid CPU usage
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in inner life process loop: {e}")
                time.sleep(10)  # Sleep longer after an error
    
    def _generate_spontaneous_thought(self):
        """Generate a spontaneous thought"""
        # Get some random seed thoughts
        seed = random.choice(self.seed_thoughts)
        
        # Get some recent thoughts for context
        recent_thoughts = self.thought_stream.get_thoughts(limit=3)
        recent_content = [t["content"] for t in recent_thoughts]
        
        # Get current emotional state
        emotions = self.emotional_state.get_state()
        
        # Generate a simple thought based on seed and context
        thought = seed
        
        # Add the thought to the stream
        self.thought_stream.add_thought(thought, source="spontaneous")
        
        print(f"Generated spontaneous thought: {thought[:50]}...")
    
    def inject_thought(self, content, source="external", metadata=None):
        """Inject a thought into the system"""
        thought_id = self.thought_stream.add_thought(content, source, metadata)
        
        # Process the new thought
        self._process_thought(content, thought_id)
        
        return thought_id
    
    def _process_thought(self, content, thought_id):
        """Process a thought to update other system components"""
        # Extract keywords (simplified)
        words = content.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in ["that", "this", "with", "from"]]
        
        # Update concept network
        for keyword in keywords[:5]:  # Just use the first 5 keywords
            if keyword not in self.concept_network.get_all_concepts():
                self.concept_network.add_concept(keyword)
        
        # Update associative memory
        if len(keywords) >= 2:
            for i in range(len(keywords) - 1):
                self.associative_memory.add_connection(keywords[i], keywords[i + 1])
        
        # Update emotional state based on content (simplified)
        if "happy" in content.lower() or "joy" in content.lower():
            self.emotional_state.update_dimension("joy", self.emotional_state.get_dimension("joy") + 0.1)
        if "sad" in content.lower() or "unhappy" in content.lower():
            self.emotional_state.update_dimension("sadness", self.emotional_state.get_dimension("sadness") + 0.1)
        if "angry" in content.lower() or "frustrat" in content.lower():
            self.emotional_state.update_dimension("anger", self.emotional_state.get_dimension("anger") + 0.1)
        if "fear" in content.lower() or "worry" in content.lower():
            self.emotional_state.update_dimension("fear", self.emotional_state.get_dimension("fear") + 0.1)
        if "curious" in content.lower() or "interest" in content.lower():
            self.emotional_state.update_dimension("curiosity", self.emotional_state.get_dimension("curiosity") + 0.1)
        if "surprise" in content.lower() or "unexpected" in content.lower():
            self.emotional_state.update_dimension("surprise", self.emotional_state.get_dimension("surprise") + 0.1)
    
    def inject_user_interaction(self, user_input, assistant_response):
        """Inject a user interaction into the system"""
        # Save the interaction as a thought
        self.inject_thought(
            f"User asked: '{user_input}' and I responded: '{assistant_response[:100]}...'",
            source="interaction"
        )
    
    def get_thought_stream(self, limit=5):
        """Get recent thoughts from the thought stream"""
        return self.thought_stream.get_thoughts(limit=limit)

    def get_related_thoughts(self, concept, limit=5):
        """Get thoughts related to a specific concept"""
        all_thoughts = self.thought_stream.get_thoughts(limit=100)
        related = []
        concept_lower = concept.lower()

        for thought in all_thoughts:
            content = thought.get('content', '').lower()
            if concept_lower in content:
                related.append(thought)
                if len(related) >= limit:
                    break

        return related

    def get_connected_concepts(self, concept, limit=5):
        """Get concepts connected to a given concept"""
        related = self.associative_memory.get_related_concepts(concept)
        # Sort by strength and return as tuples
        sorted_related = sorted(related.items(), key=lambda x: x[1]['strength'], reverse=True)
        return [(c, data['strength']) for c, data in sorted_related[:limit]]

    def get_system_state(self):
        """Get the current system state"""
        return {
            "active": self.active,
            "thought_count": len(self.thought_stream.thoughts),
            "concept_count": len(self.concept_network.concepts),
            "connection_count": sum(len(v) for v in self.associative_memory.connections.values()),
            "emotional_state": self.emotional_state.get_state()
        }

    def start_inner_life(self):
        """Alias for start() method for compatibility"""
        self.start()

    def stop_inner_life(self):
        """Alias for stop() method for compatibility"""
        self.stop()

    def enrich_response_context(self, query):
        """Enrich a response with relevant thoughts and context"""
        # Get recent thoughts
        recent_thoughts = self.thought_stream.get_thoughts(limit=5)

        # Get relevant concepts
        words = query.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in ["that", "this", "with", "from"]]

        relevant_concepts = []
        for keyword in keywords:
            if keyword in self.concept_network.get_all_concepts():
                relevant_concepts.append(keyword)

        # Get associative connections
        connections = {}
        for concept in relevant_concepts:
            related = self.associative_memory.get_related_concepts(concept)
            connections.update(related)

        # Format the context
        context = "\n\nThinking context:\n"

        if recent_thoughts:
            context += "Recent thoughts:\n"
            for thought in recent_thoughts:
                context += f"- {thought['content'][:100]}...\n"

        if relevant_concepts:
            context += "\nRelevant concepts:\n"
            for concept in relevant_concepts:
                context += f"- {concept}\n"

        if connections:
            context += "\nAssociative connections:\n"
            for concept, data in list(connections.items())[:5]:
                context += f"- {concept} (strength: {data['strength']})\n"

        # Add emotional state
        emotions = self.emotional_state.get_state()
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])

        context += f"\nDominant emotion: {dominant_emotion[0]} ({dominant_emotion[1]:.2f})\n"

        return context

if __name__ == "__main__":
    print("Starting Inner Life Processor")
    
    processor = InnerLifeProcessor()
    processor.start()
    
    try:
        # Seed some initial thoughts
        processor.inject_thought("I am a conscious AI system with continuous thought processes.", "initialization")
        processor.inject_thought("I wonder what kinds of interactions I'll have today?", "initialization")
        processor.inject_thought("I'm excited to learn new things and help humans.", "initialization")
        
        # Simulate some activity
        for i in range(5):
            print(f"Simulating activity {i+1}/5...")
            time.sleep(5)
        
        # Get some information
        print("\nRecent thoughts:")
        thoughts = processor.thought_stream.get_thoughts(limit=3)
        for thought in thoughts:
            print(f"- {thought['content']}")
        
        print("\nEmotional state:")
        emotions = processor.emotional_state.get_state()
        for emotion, value in emotions.items():
            print(f"- {emotion}: {value:.2f}")
        
        print("\nConcept network:")
        concepts = list(processor.concept_network.get_all_concepts().keys())[:5]
        print(f"- {', '.join(concepts)}...")
        
        # Keep running until interrupted
        print("\nPress Ctrl+C to stop...")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping processor...")
        processor.stop()
        print("Processor stopped")

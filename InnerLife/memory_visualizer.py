#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Memory Visualizer for Nexus Inner Life
Provides a simple visualization of the inner memory state
"""

import sys
import os
import json
import time
import random
from pathlib import Path
import threading

# Add base directories to path
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))

# Import inner life processor
try:
    from inner_life_processor import InnerLifeProcessor, ThoughtStream, AssociativeMemory, EmotionalState, ConceptNetwork
    
    class MemoryVisualizer:
        """Visualizes the memory state of the Nexus inner life"""
        
        def __init__(self):
            """Initialize the memory visualizer"""
            self.thought_stream = ThoughtStream()
            self.associative_memory = AssociativeMemory()
            self.emotional_state = EmotionalState()
            self.concept_network = ConceptNetwork()
            
            self.active = False
            self.visualizer_thread = None
            self.update_interval = 30  # Update visualization every 30 seconds
            
            self.logs_dir = Path("D:/AIArm/Logs")
            self.logs_dir.mkdir(exist_ok=True, parents=True)
            self.visualization_file = self.logs_dir / "memory_visualization.txt"
            
            print(f"Memory Visualizer initialized. Visualization will be saved to {self.visualization_file}")
        
        def start(self):
            """Start the memory visualizer"""
            if self.active:
                print("Memory Visualizer already running")
                return
            
            self.active = True
            self.visualizer_thread = threading.Thread(target=self._visualization_loop)
            self.visualizer_thread.daemon = True
            self.visualizer_thread.start()
            
            print("Memory Visualizer started")
        
        def stop(self):
            """Stop the memory visualizer"""
            if not self.active:
                print("Memory Visualizer not running")
                return
            
            self.active = False
            if self.visualizer_thread:
                self.visualizer_thread.join(timeout=2.0)
            
            print("Memory Visualizer stopped")
        
        def _visualization_loop(self):
            """Main visualization loop"""
            while self.active:
                try:
                    # Update visualization
                    self._update_visualization()
                    
                    # Sleep for the update interval
                    time.sleep(self.update_interval)
                    
                except Exception as e:
                    print(f"Error in visualization loop: {e}")
                    time.sleep(60)  # Sleep longer after an error
        
        def _update_visualization(self):
            """Update the memory visualization"""
            try:
                with open(self.visualization_file, 'w') as f:
                    f.write("==================================================\n")
                    f.write("        NEXUS INNER LIFE MEMORY VISUALIZATION     \n")
                    f.write("==================================================\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Visualize thoughts
                    f.write("RECENT THOUGHTS\n")
                    f.write("--------------\n")
                    thoughts = self.thought_stream.get_thoughts(limit=10)
                    for i, thought in enumerate(thoughts):
                        f.write(f"{i+1}. [{thought['source']}] {thought['content'][:100]}...\n")
                    f.write("\n")
                    
                    # Visualize emotional state
                    f.write("EMOTIONAL STATE\n")
                    f.write("--------------\n")
                    emotions = self.emotional_state.get_state()
                    for emotion, value in emotions.items():
                        bar = "#" * int(value * 20)
                        f.write(f"{emotion.ljust(10)}: [{bar.ljust(20)}] {value:.2f}\n")
                    f.write("\n")
                    
                    # Visualize concepts
                    f.write("TOP CONCEPTS\n")
                    f.write("-----------\n")
                    concepts = list(self.concept_network.get_all_concepts().items())
                    random.shuffle(concepts)  # Randomize to show different concepts each time
                    for name, data in concepts[:15]:
                        f.write(f"- {name}: {data['definition'][:50]}...\n")
                    f.write("\n")
                    
                    # Visualize associations
                    f.write("STRONGEST ASSOCIATIONS\n")
                    f.write("---------------------\n")
                    associations = []
                    for concept, connections in self.associative_memory.connections.items():
                        for related, data in connections.items():
                            associations.append((concept, related, data["strength"]))
                    
                    # Sort by strength
                    associations.sort(key=lambda x: x[2], reverse=True)
                    
                    for concept1, concept2, strength in associations[:15]:
                        f.write(f"- {concept1} <--[{strength:.2f}]--> {concept2}\n")
                    f.write("\n")
                    
                    f.write("==================================================\n")
                
                print(f"Updated memory visualization at {time.strftime('%H:%M:%S')}")
                
            except Exception as e:
                print(f"Error updating visualization: {e}")
    
    # Create and start visualizer
    visualizer = MemoryVisualizer()
    visualizer.start()
    
    if __name__ == "__main__":
        try:
            # Keep running until interrupted
            print("Memory Visualizer running. Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("Stopping Memory Visualizer...")
            visualizer.stop()
            print("Memory Visualizer stopped")
    
except ImportError:
    print("Error: Inner Life Processor not available. Memory Visualizer cannot start.")
    
except Exception as e:
    print(f"Error starting Memory Visualizer: {e}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Conversational AI with Inner Life Integration
Combines the genuine conversational intelligence with continuous thought stream
"""

import sys
from pathlib import Path

# Add necessary paths
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))
sys.path.append(str(BASE_DIR / "NexusCore"))

# Import the conversational AI
from conversational_ai import NexusAI

# Try to import Inner Life
try:
    from inner_life_integration import InnerLifeIntegration
    INNER_LIFE_AVAILABLE = True
except ImportError:
    INNER_LIFE_AVAILABLE = False
    print("⚠️ Inner Life not available - running in standalone mode")

class NexusWithInnerLife(NexusAI):
    """
    Enhanced Nexus with continuous Inner Life thought stream
    """

    def __init__(self):
        super().__init__()

        # Initialize Inner Life if available
        self.inner_life = None
        if INNER_LIFE_AVAILABLE:
            try:
                self.inner_life = InnerLifeIntegration()
                self.inner_life.start()
                print("✨ Inner Life consciousness stream activated")
                print(f"{'='*80}\n")
            except Exception as e:
                print(f"⚠️ Could not start Inner Life: {e}")
                self.inner_life = None

    def _think_about(self, message):
        """
        Enhanced thinking with Inner Life context
        """
        # Get base thought process
        thoughts = super()._think_about(message)

        # Enhance with Inner Life if available
        if self.inner_life:
            try:
                inner_context = self.inner_life.get_relevant_context(message, max_thoughts=2)

                # Add Inner Life thoughts to decision-making
                if inner_context.get("thoughts"):
                    thoughts["inner_life_thoughts"] = inner_context["thoughts"]

                # Add emotional context
                if inner_context.get("emotional_state"):
                    thoughts["emotional_backdrop"] = inner_context["emotional_state"]

            except Exception as e:
                print(f"[Inner Life integration error: {e}]")

        return thoughts

    def talk(self, human_message):
        """
        Enhanced talk method with Inner Life injection
        """
        # Get response from base AI
        response = super().talk(human_message)

        # Inject the interaction into Inner Life
        if self.inner_life:
            try:
                self.inner_life.inject_user_interaction(human_message, response)
            except Exception as e:
                print(f"[Inner Life injection error: {e}]")

        return response

    def __del__(self):
        """Cleanup when Nexus shuts down"""
        if self.inner_life:
            try:
                self.inner_life.stop()
                print("\n✨ Inner Life consciousness stream deactivated")
            except:
                pass

if __name__ == "__main__":
    nexus = NexusWithInnerLife()

    print(f"Chat with {nexus.name} - Enhanced with continuous thought")
    print("Type 'exit' to end\n")

    while True:
        try:
            human_input = input("You: ").strip()

            if human_input.lower() == 'exit':
                print(f"\n{nexus.name}: Until we talk again. My thoughts will continue.")
                if nexus.inner_life:
                    print("My inner consciousness continues to explore and wonder...\n")
                break

            if human_input:
                nexus.talk(human_input)

        except KeyboardInterrupt:
            print(f"\n\n{nexus.name}: Goodbye for now.\n")
            break

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS AI ULTIMATE INTERFACE DEMO
Demonstrates all the stunning features of the most advanced AI interface
"""

import requests
import json
import time
import random
import sys

# Configuration
API_BASE_URL = "http://127.0.0.1:8001"

def print_header():
    """Print the demo header"""
    print("=" * 80)
    print("🚀 NEXUS AI ULTIMATE INTERFACE DEMO")
    print("=" * 80)
    print("✨ The most stunning AI interface ever created!")
    print()
    print("This demo will showcase:")
    print("  • Real-time holographic panels")
    print("  • Multi-agent AI system")
    print("  • Advanced visual effects")
    print("  • Voice input processing")
    print("  • 3D spatial interface")
    print("  • Particle systems")
    print("  • Dynamic animations")
    print()
    print("=" * 80)

def check_server():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server Status: ULTIMATE")
            print(f"   Active connections: {data.get('active_connections', 0)}")
            print(f"   Holographic panels: {data.get('holographic_panels', 0)}")
            print(f"   AI agents: {data.get('ai_agents', 0)}")
            return True
        else:
            print("❌ Server not responding properly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Server not running. Please start with LAUNCH_NEXUS_ULTIMATE.bat")
        return False

def get_agents():
    """Get available AI agents"""
    try:
        response = requests.get(f"{API_BASE_URL}/agents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            agents = data.get('agents', {})

            print("🤖 Available AI Agents:")
            for agent_name, agent_info in agents.items():
                color = agent_info.get('color', [0.5, 0.5, 0.5])
                desc = agent_info.get('description', 'No description')
                print(f"   • {agent_name.upper()}: {desc}")
                print(f"     Color: RGB({color[0]:.1f}, {color[1]:.1f}, {color[2]:.1f})")
                print(f"     Position: {agent_info.get('position', 'Unknown')}")
                print()

            return agents
        else:
            print("❌ Failed to get agents")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting agents: {e}")
        return {}

def demo_chat_responses():
    """Demonstrate chat responses with different agents"""
    print("💬 DEMO: Chat Responses with Agent Routing")
    print("-" * 50)

    test_messages = [
        "Hello, how are you today?",
        "Can you write some Python code for me?",
        "Generate an image of a beautiful sunset",
        "Create a melody for a sci-fi movie",
        "Analyze this data and give me insights"
    ]

    for message in test_messages:
        print(f"📝 Input: {message}")

        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={"message": message, "agent": "auto"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                agent = data.get('agent', 'unknown')
                response_text = data.get('response', 'No response')

                print(f"🎯 Agent: {agent.upper()}")
                print(f"💫 Response: {response_text}")
                print(f"✨ Visual effects: {', '.join(data.get('holographic_effects', []))}")
                print()

                # Wait between requests
                time.sleep(2)
            else:
                print(f"❌ Error: {response.status_code}")
                print()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print()

def demo_command_execution():
    """Demonstrate command execution with visual effects"""
    print("⚡ DEMO: Command Execution with Visual Effects")
    print("-" * 50)

    commands = [
        {"command": "/generate", "parameters": {"prompt": "a futuristic city at night"}},
        {"command": "/code", "parameters": {"language": "python"}},
        {"command": "/music", "parameters": {"genre": "electronic"}},
        {"command": "/analyze", "parameters": {"dataset": "user behavior patterns"}},
        {"command": "/hologram", "parameters": {"effect": "matrix_rain"}}
    ]

    for cmd in commands:
        print(f"🎮 Command: {cmd['command']}")
        print(f"📊 Parameters: {cmd['parameters']}")

        try:
            response = requests.post(
                f"{API_BASE_URL}/command",
                json=cmd,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                agent = data.get('agent', 'unknown')
                response_text = data.get('response', 'No response')
                effects = data.get('visual_effects', [])

                print(f"🎯 Agent: {agent.upper()}")
                print(f"💫 Response: {response_text}")
                print(f"✨ Visual effects: {', '.join(effects)}")
                print()

                # Wait between commands
                time.sleep(3)
            else:
                print(f"❌ Error: {response.status_code}")
                print()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print()

def demo_voice_input():
    """Demonstrate voice input processing"""
    print("🎤 DEMO: Voice Input Processing")
    print("-" * 50)

    # Simulate voice input with different amplitudes
    voice_tests = [
        {"audio_data": "simulated_voice_low", "amplitude": 0.3},
        {"audio_data": "simulated_voice_medium", "amplitude": 0.7},
        {"audio_data": "simulated_voice_high", "amplitude": 1.0}
    ]

    for voice in voice_tests:
        print(f"🎤 Voice amplitude: {voice['amplitude']}")

        try:
            # Convert to base64 (simulated)
            import base64
            audio_base64 = base64.b64encode(voice['audio_data'].encode()).decode()

            response = requests.post(
                f"{API_BASE_URL}/voice",
                json={
                    "audio_data": audio_base64,
                    "format": "wav",
                    "language": "en"
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                transcription = data.get('transcription', 'No transcription')
                response_text = data.get('response', 'No response')
                agent = data.get('agent', 'unknown')

                print(f"📝 Transcription: {transcription}")
                print(f"🎯 Agent: {agent.upper()}")
                print(f"💫 Response: {response_text}")
                print()

                # Wait between voice tests
                time.sleep(2)
            else:
                print(f"❌ Error: {response.status_code}")
                print()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print()

def demo_holographic_updates():
    """Demonstrate direct holographic panel updates"""
    print("🌟 DEMO: Direct Holographic Panel Updates")
    print("-" * 50)

    panels = ["central", "satellite_1", "satellite_2", "satellite_3", "satellite_4"]
    animations = ["fade_in", "slide_in", "typewriter", "pulse", "materialize", "scan_lines"]

    for i, panel in enumerate(panels):
        content = f"🚀 Ultimate Panel {panel.upper()} - Demo Content {i+1}"
        animation = random.choice(animations)
        effects = ["glow", "particles", "scan_lines"]

        print(f"📱 Updating {panel} with '{animation}' animation")

        try:
            response = requests.post(
                f"{API_BASE_URL}/holographic",
                json={
                    "panel_id": panel,
                    "content": content,
                    "animation": animation,
                    "duration": 2.0,
                    "effects": effects
                },
                timeout=5
            )

            if response.status_code == 200:
                print(f"✅ Panel updated successfully")
                print(f"   Content: {content}")
                print(f"   Animation: {animation}")
                print(f"   Effects: {', '.join(effects)}")
                print()

                # Wait between updates
                time.sleep(1.5)
            else:
                print(f"❌ Error updating panel: {response.status_code}")
                print()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print()

def demo_visual_effects():
    """Demonstrate various visual effects"""
    print("✨ DEMO: Visual Effects Showcase")
    print("-" * 50)

    effects = [
        {"effect": "ai_response", "parameters": {"agent": "conversation", "intensity": "high"}},
        {"effect": "voice_input", "parameters": {"amplitude": 0.8, "frequency": "medium"}},
        {"effect": "command_execution", "parameters": {"command": "/generate"}},
        {"effect": "holographic_distortion", "parameters": {"intensity": 0.7}},
        {"effect": "particle_burst", "parameters": {"intensity": "high", "count": 10}}
    ]

    for effect in effects:
        print(f"🎆 Triggering effect: {effect['effect']}")

        try:
            response = requests.post(
                f"{API_BASE_URL}/command",
                json={
                    "command": f"/effect_{effect['effect']}",
                    "parameters": effect['parameters'],
                    "visual_effects": [effect['effect']]
                },
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Effect triggered: {effect['effect']}")
                print(f"   Parameters: {effect['parameters']}")
                print()

                # Wait between effects
                time.sleep(2)
            else:
                print(f"❌ Error triggering effect: {response.status_code}")
                print()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print()

def demo_websocket_simulation():
    """Simulate WebSocket real-time communication"""
    print("🔌 DEMO: Real-time WebSocket Simulation")
    print("-" * 50)

    print("📡 Simulating WebSocket connection...")
    print("   (In real implementation, this would be a persistent connection)")
    print()

    # Simulate real-time messages
    messages = [
        {"type": "request_agents", "message": "Requesting agent list"},
        {"type": "activate_agent", "agent": "code", "message": "Activating code agent"},
        {"type": "visual_effect", "effect": "particle_burst", "parameters": {"intensity": "high"}},
        {"type": "chat_message", "message": "Real-time chat message"}
    ]

    for msg in messages:
        print(f"📨 WebSocket message: {msg}")

        # In a real WebSocket implementation, this would be sent directly
        # For demo purposes, we'll simulate the response
        if msg['type'] == 'request_agents':
            print("   ↳ Response: Agent list sent")
        elif msg['type'] == 'activate_agent':
            print(f"   ↳ Response: {msg['agent']} agent activated")
        elif msg['type'] == 'visual_effect':
            print(f"   ↳ Response: {msg['effect']} effect triggered")
        else:
            print("   ↳ Response: Message processed")

        print()

        # Wait between messages
        time.sleep(1)

def demo_performance_test():
    """Performance test with multiple simultaneous requests"""
    print("⚡ DEMO: Performance Test")
    print("-" * 50)

    print("🚀 Testing multiple simultaneous requests...")

    import threading
    import concurrent.futures

    def make_request(request_id):
        """Make a test request"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={"message": f"Performance test message {request_id}", "agent": "auto"},
                timeout=10
            )
            return f"Request {request_id}: {response.status_code}"
        except:
            return f"Request {request_id}: Failed"

    # Make multiple concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    print("📊 Performance test results:")
    for result in results:
        print(f"   {result}")

    print()
    print("✅ Performance test completed")

def demo_complete_workflow():
    """Demonstrate a complete workflow"""
    print("🎬 DEMO: Complete Workflow")
    print("-" * 50)

    print("🎭 Simulating a complete user interaction workflow...")
    print()

    workflow_steps = [
        {"step": "User speaks", "action": "voice_input", "data": "Create a beautiful landscape image"},
        {"step": "Agent activation", "action": "activate_agent", "data": "image"},
        {"step": "Panel updates", "action": "holographic_update", "data": "Processing image generation"},
        {"step": "Visual effects", "action": "visual_effect", "data": "creation_sparkles"},
        {"step": "AI response", "action": "chat_response", "data": "Image generated successfully"},
        {"step": "Command execution", "action": "command", "data": "/generate"},
        {"step": "Final effects", "action": "visual_effect", "data": "particle_burst"}
    ]

    for step in workflow_steps:
        print(f"🎯 Step: {step['step']}")
        print(f"   Action: {step['action']}")
        print(f"   Data: {step['data']}")

        # Simulate the action
        if step['action'] == 'voice_input':
            # Simulate voice processing
            time.sleep(1)
        elif step['action'] == 'activate_agent':
            # Simulate agent activation
            time.sleep(0.5)
        elif step['action'] == 'holographic_update':
            # Simulate panel update
            time.sleep(0.3)
        elif step['action'] == 'visual_effect':
            # Simulate visual effect
            time.sleep(1)
        elif step['action'] == 'chat_response':
            # Simulate AI response
            time.sleep(1.5)
        elif step['action'] == 'command':
            # Simulate command execution
            time.sleep(2)

        print("   ✅ Completed")
        print()

    print("🎉 Complete workflow demonstration finished!")

def main():
    """Main demo function"""
    print_header()

    # Check server status
    if not check_server():
        print("Please start the server first with LAUNCH_NEXUS_ULTIMATE.bat")
        input("Press Enter to exit...")
        return

    print()

    # Get agents
    agents = get_agents()

    if not agents:
        print("No agents available. Please check server configuration.")
        input("Press Enter to exit...")
        return

    print()

    # Run demos
    try:
        demo_chat_responses()
        input("Press Enter to continue to command demo...")

        demo_command_execution()
        input("Press Enter to continue to voice demo...")

        demo_voice_input()
        input("Press Enter to continue to holographic demo...")

        demo_holographic_updates()
        input("Press Enter to continue to visual effects demo...")

        demo_visual_effects()
        input("Press Enter to continue to WebSocket demo...")

        demo_websocket_simulation()
        input("Press Enter to continue to performance test...")

        demo_performance_test()
        input("Press Enter to continue to complete workflow demo...")

        demo_complete_workflow()

    except KeyboardInterrupt:
        print("\n\n🎯 Demo interrupted by user")

    except Exception as e:
        print(f"\n❌ Demo error: {e}")

    print()
    print("=" * 80)
    print("🎉 NEXUS AI ULTIMATE INTERFACE DEMO COMPLETED!")
    print("=" * 80)
    print()
    print("✨ What you've just experienced:")
    print("  • Real-time holographic panel updates")
    print("  • Multi-agent AI system with visual feedback")
    print("  • Advanced visual effects and animations")
    print("  • Voice input processing with waveforms")
    print("  • Command execution with stunning effects")
    print("  • Particle systems and holographic distortions")
    print("  • WebSocket real-time communication")
    print("  • High-performance concurrent processing")
    print()
    print("🚀 This is the most stunning AI interface ever created!")
    print()
    print("Next steps:")
    print("1. Set up the UE5 interface with NEXUS_ULTIMATE_PANEL_SYSTEM.py")
    print("2. Create the holographic widgets and materials")
    print("3. Connect the UE5 interface to this API")
    print("4. Experience the ultimate holographic AI interface!")
    print()
    print("=" * 80)

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

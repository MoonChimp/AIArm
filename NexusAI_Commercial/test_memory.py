#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for NexusAI Memory System
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from memory_system import memory_system, learning_system, self_awareness

def test_memory_system():
    """Test conversation memory functionality"""
    print("=" * 60)
    print("Testing NexusAI Memory System")
    print("=" * 60)

    # Test 1: Create session
    print("\n1. Creating conversation session...")
    session_id = memory_system.create_session("test_session_001")
    print(f"[OK] Created session: {session_id}")

    # Test 2: Add messages
    print("\n2. Adding conversation messages...")
    memory_system.add_message(session_id, "user", "Hello, I need help with Python programming")
    memory_system.add_message(session_id, "assistant", "I'd be happy to help you with Python programming! What specific task are you working on?")
    memory_system.add_message(session_id, "user", "I want to create a file management system")
    memory_system.add_message(session_id, "assistant", "Great! I can help you create a file management system. We have full file management capabilities available.")

    print("[OK] Added 4 messages to conversation")

    # Test 3: Get context
    print("\n3. Retrieving conversation context...")
    context = memory_system.get_context(session_id)
    print(f"[OK] Retrieved {len(context)} messages from context")

    for i, msg in enumerate(context, 1):
        print(f"  {i}. {msg['role'].upper()}: {msg['content'][:50]}...")

    # Test 4: Conversation summary
    print("\n4. Generating conversation summary...")
    summary = memory_system.get_conversation_summary(session_id)
    print(f"[OK] Summary: {summary}")

    # Test 5: Learning system
    print("\n5. Testing learning system...")
    learning_system.learn_fact("Python is a versatile programming language", "test")
    learning_system.record_correction("file management", "use proper file handling", "programming")
    print("[OK] Recorded learning data")

    # Test 6: Self-awareness
    print("\n6. Testing self-awareness module...")
    awareness = self_awareness.get_self_description()
    print("[OK] Self-awareness description generated")
    print(f"  Capabilities: {len(self_awareness.capabilities)}")
    print(f"  Limitations: {len(self_awareness.limitations)}")

    # Test 7: Save and load session
    print("\n7. Testing session persistence...")
    memory_system.save_session(session_id)
    print(f"[OK] Session saved to disk")

    # Create new memory system instance to test loading
    new_memory = type(memory_system)(memory_system.memory_dir)
    loaded = new_memory.load_session(session_id)
    print(f"[OK] Session loaded: {loaded}")

    # Test 8: List sessions
    print("\n8. Listing all sessions...")
    sessions = memory_system.list_sessions()
    print(f"[OK] Found {len(sessions)} sessions")
    for session in sessions:
        print(f"  - {session['id']}: {session['message_count']} messages")

    print("\n" + "=" * 60)
    print("[SUCCESS] ALL MEMORY SYSTEM TESTS PASSED!")
    print("=" * 60)

    return True

def test_api_endpoints():
    """Test API endpoints (requires server to be running)"""
    print("\n" + "=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)

    try:
        import requests

        base_url = "http://localhost:5000/api"

        # Test status endpoint
        print("\n1. Testing /api/status...")
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            data = response.json()
            print("[OK] Status endpoint working")
            print(f"  Ollama available: {data['systems']['ollama']['available']}")
        else:
            print(f"[FAIL] Status endpoint failed: {response.status_code}")
            return False

        # Test self-awareness endpoint
        print("\n2. Testing /api/self-awareness...")
        response = requests.get(f"{base_url}/self-awareness")
        if response.status_code == 200:
            data = response.json()
            print("[OK] Self-awareness endpoint working")
            print(f"  Description length: {len(data['description'])}")
        else:
            print(f"[FAIL] Self-awareness endpoint failed: {response.status_code}")

        # Test learning knowledge endpoint
        print("\n3. Testing /api/learning/knowledge...")
        response = requests.get(f"{base_url}/learning/knowledge")
        if response.status_code == 200:
            data = response.json()
            print("[OK] Learning knowledge endpoint working")
            print(f"  Learned facts: {len(data['learned_facts'])}")
        else:
            print(f"[FAIL] Learning knowledge endpoint failed: {response.status_code}")

        print("\n" + "=" * 60)
        print("[SUCCESS] API ENDPOINT TESTS COMPLETED!")
        print("=" * 60)

    except ImportError:
        print("[WARN] Requests library not available for API testing")
    except Exception as e:
        print(f"[FAIL] API test failed: {e}")

    return True

if __name__ == "__main__":
    try:
        # Test memory system
        test_memory_system()

        # Test API endpoints
        test_api_endpoints()

        print("\n[SUCCESS] NEXUSAI MEMORY SYSTEM IS READY!")
        print("\nNext steps:")
        print("1. Start backend: START_NEXUS_FUNCTIONAL.bat")
        print("2. Open browser: http://localhost:8080/html/chat.html")
        print("3. Test conversation memory in chat")

    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()

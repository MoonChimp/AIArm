#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive Agent Test Suite
Tests ALL agents to verify they generate REAL content
"""

import sys
from pathlib import Path

# Add paths
sys.path.append("D:/AIArm/InnerLife")
sys.path.append("D:/AIArm/InnerLife/Agents")

def test_story_agent():
    """Test Story Generation Agent"""
    print("\n" + "="*80)
    print("TEST 1: Story Generation Agent")
    print("="*80)

    try:
        from real_story_agent import RealStoryAgent

        agent = RealStoryAgent()
        agent.activate()  # Activate the agent!
        result = agent.process(
            "Write a short story about an AI discovering emotions",
            options={"length": "flash"}
        )

        if result["status"] == "success":
            print(f"✅ Story Agent PASSED")
            print(f"   - Generated {result['word_count']} words")
            print(f"   - Saved to: {result['filename']}")
            print(f"   - Genre: {result['genre']}")
            return True
        else:
            print(f"❌ Story Agent FAILED: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ Story Agent ERROR: {e}")
        return False

def test_code_agent():
    """Test Code Execution Agent"""
    print("\n" + "="*80)
    print("TEST 2: Code Execution Agent")
    print("="*80)

    try:
        from real_code_agent import RealCodeAgent

        agent = RealCodeAgent()
        agent.activate()  # Activate the agent!
        result = agent.process(
            'print("Hello from Code Agent test!")',
            options={"language": "python"}
        )

        if result["status"] == "success":
            print(f"✅ Code Agent PASSED")
            print(f"   - Executed successfully")
            print(f"   - Output: {result['stdout'].strip()}")
            return True
        else:
            print(f"❌ Code Agent FAILED: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ Code Agent ERROR: {e}")
        return False

def test_websearch_agent():
    """Test Web Search Agent"""
    print("\n" + "="*80)
    print("TEST 3: Web Search Agent (Browser)")
    print("="*80)

    try:
        from real_websearch_agent import RealWebSearchAgent

        agent = RealWebSearchAgent()
        agent.activate()  # Activate the agent!

        # Test opens browser - this will actually open a browser window
        result = agent.process("Python programming test", options={"engine": "duckduckgo"})

        if result["status"] == "success":
            print(f"✅ WebSearch Agent PASSED")
            print(f"   - Search engine: {result['search_engine']}")
            print(f"   - URL: {result['url'][:60]}...")
            print(f"   - Browser opened successfully")
            return True
        else:
            print(f"❌ WebSearch Agent FAILED: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ WebSearch Agent ERROR: {e}")
        return False

def test_contemplation_agent():
    """Test Contemplation Agent"""
    print("\n" + "="*80)
    print("TEST 4: Contemplation Agent")
    print("="*80)

    try:
        from contemplation_agent import ContemplationAgent

        agent = ContemplationAgent()
        agent.activate()  # Activate the agent!
        result = agent.process("What is the nature of artificial intelligence?")

        if result["status"] == "success":
            print(f"✅ Contemplation Agent PASSED")
            print(f"   - Generated contemplation")
            print(f"   - Inner Life enhanced: {result.get('inner_life_enhanced', False)}")
            if result.get('key_insights'):
                print(f"   - Insights: {len(result['key_insights'])} found")
            return True
        else:
            print(f"❌ Contemplation Agent FAILED: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ Contemplation Agent ERROR: {e}")
        return False

def test_video_agent():
    """Test Video Script Agent"""
    print("\n" + "="*80)
    print("TEST 5: Video Script Agent")
    print("="*80)

    try:
        from real_video_agent import RealVideoAgent

        agent = RealVideoAgent()
        agent.activate()  # Activate the agent!
        result = agent.process(
            "Create a 30-second product commercial",
            options={"type": "commercial"}
        )

        if result["status"] == "success":
            print(f"✅ Video Agent PASSED")
            print(f"   - Generated video script")
            print(f"   - Saved to: {result.get('filename', 'N/A')}")
            if result.get('scenes'):
                print(f"   - Scenes: {len(result['scenes'])}")
            return True
        else:
            print(f"❌ Video Agent FAILED: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ Video Agent ERROR: {e}")
        return False

def test_nexus_actionable():
    """Test Nexus Actionable (with content generation)"""
    print("\n" + "="*80)
    print("TEST 6: Nexus Actionable (Content Generation)")
    print("="*80)

    try:
        sys.path.append("D:/AIArm/NexusCore")
        from nexus_actionable import NexusActionable

        nexus = NexusActionable()
        response = nexus.process("Create a Python file called test_agent.py that prints 'Agent test successful!'")

        # Check if file was created with content
        test_file = Path("D:/AIArm/test_agent.py")
        if test_file.exists():
            content = test_file.read_text()
            if len(content) > 10:
                print(f"✅ Nexus Actionable PASSED")
                print(f"   - File created with {len(content)} chars")
                print(f"   - Content: {content[:50]}...")
                test_file.unlink()  # Clean up
                return True
            else:
                print(f"❌ Nexus Actionable FAILED: Empty file created")
                test_file.unlink()
                return False
        else:
            print(f"❌ Nexus Actionable FAILED: File not created")
            return False

    except Exception as e:
        print(f"❌ Nexus Actionable ERROR: {e}")
        return False

def main():
    """Run all agent tests"""
    print("\n" + "="*80)
    print("COMPREHENSIVE AGENT TEST SUITE")
    print("Testing all agents to verify REAL content generation")
    print("="*80)

    results = []

    # Run all tests
    results.append(("Story Agent", test_story_agent()))
    results.append(("Code Agent", test_code_agent()))
    results.append(("WebSearch Agent", test_websearch_agent()))
    results.append(("Contemplation Agent", test_contemplation_agent()))
    results.append(("Video Agent", test_video_agent()))
    results.append(("Nexus Actionable", test_nexus_actionable()))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL AGENTS VERIFIED - NO HUSKS FOUND!")
        print("All agents generate REAL content and execute properly.")
    else:
        print(f"\n⚠️  {total - passed} agents need attention")

    print("="*80 + "\n")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

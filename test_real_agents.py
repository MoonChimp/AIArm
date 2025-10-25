#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for REAL agents
"""

import sys
sys.path.append("D:/AIArm/InnerLife")
sys.path.append("D:/AIArm/InnerLife/Agents")

print("="*80)
print("TESTING REAL AGENTS")
print("="*80)

# Test 1: WebSearch Agent
print("\n[TEST 1] WebSearch Agent")
print("-"*80)
try:
    from real_websearch_agent import RealWebSearchAgent
    search_agent = RealWebSearchAgent()
    search_agent.activate()

    result = search_agent.process("Python programming tutorials", options={"max_results": 3})

    if result["status"] == "success":
        print(f"[OK] WebSearch WORKS! Found {len(result['results'])} results")
        for i, res in enumerate(result['results'][:2], 1):
            print(f"  {i}. {res['title'][:60]}")
    else:
        print(f"[FAIL] WebSearch failed: {result.get('message')}")
except Exception as e:
    print(f"[ERROR] WebSearch error: {e}")

# Test 2: Code Execution Agent
print("\n[TEST 2] Code Execution Agent")
print("-"*80)
try:
    from real_code_agent import RealCodeAgent
    code_agent = RealCodeAgent()
    code_agent.activate()

    test_code = """
print("Hello from NexusAI!")
result = 2 + 2
print(f"2 + 2 = {result}")
"""

    result = code_agent.process(test_code, options={"language": "python"})

    if result["status"] == "success":
        print(f"[OK] Code Execution WORKS!")
        print(f"  Output: {result['stdout'].strip()}")
    else:
        print(f"[FAIL] Code Execution failed: {result.get('message')}")
except Exception as e:
    print(f"[ERROR] Code Execution error: {e}")

# Test 3: Contemplation Agent
print("\n[TEST 3] Contemplation Agent")
print("-"*80)
try:
    from contemplation_agent import ContemplationAgent
    contemp_agent = ContemplationAgent()
    contemp_agent.activate()

    result = contemp_agent.process("What is consciousness?", options={"depth": "deep"})

    if result["status"] == "success":
        print(f"[OK] Contemplation WORKS!")
        print(f"  Contemplation ({len(result['contemplation'])} chars)")
        if result.get('key_insights'):
            print(f"  Insights: {len(result['key_insights'])} found")
    else:
        print(f"[FAIL] Contemplation failed: {result.get('message')}")
except Exception as e:
    print(f"[ERROR] Contemplation error: {e}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)

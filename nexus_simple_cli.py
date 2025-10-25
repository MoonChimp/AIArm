#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Simple CLI - Text-Based Tool Calling
Works with any Ollama model using text parsing
"""

import sys
import json
import requests
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


SYSTEM_PROMPT = """You are NexusAI with access to powerful creative tools.

AVAILABLE TOOLS:
- IMAGE: Generate images (e.g., "IMAGE: a sunset over mountains")
- MUSIC: Create songs (e.g., "MUSIC: rock song about freedom")
- VIDEO: Make videos (e.g., "VIDEO: tutorial about coffee brewing")
- CODE: Build applications (e.g., "CODE: calculator website")
- SEARCH: Web search (e.g., "SEARCH: latest AI news")
- STORY: Write stories (e.g., "STORY: sci-fi adventure")

To use a tool, include the tool call in your response like this:
TOOL_CALL: TOOLNAME: description

Example responses:
User: "Create an image of a dragon"
You: "I'll create that image for you. TOOL_CALL: IMAGE: epic dragon, detailed scales, wings spread, fantasy art"

User: "Make a rock song"
You: "Creating a rock song! TOOL_CALL: MUSIC: rock song with powerful guitar riffs and energetic drums"

Be conversational and helpful!"""


def execute_tool(tool_name: str, params: str) -> dict:
    """Execute a tool via Nexus API"""
    agent_map = {
        'IMAGE': 'photo',
        'MUSIC': 'music',
        'VIDEO': 'video',
        'CODE': 'code',
        'SEARCH': 'websearch',
        'STORY': 'story'
    }

    agent = agent_map.get(tool_name.upper())
    if not agent:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={"message": params, "agent": agent},
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "result": data.get("response", ""),
                "files": data.get("files", [])
            }
        else:
            return {"error": f"API error: {response.status_code}"}

    except Exception as e:
        return {"error": str(e)}


def chat(user_message: str, model="nexusai-tools:latest"):
    """Chat with simple text-based tool calling"""
    try:
        # Send message to Ollama
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            print(f"[X] Error: Ollama returned status {response.status_code}")
            return

        data = response.json()
        assistant_response = data.get("message", {}).get("content", "")

        # Check for tool calls
        tool_pattern = r'TOOL_CALL:\s*(\w+):\s*(.+?)(?=\n|$)'
        tool_matches = re.findall(tool_pattern, assistant_response, re.IGNORECASE)

        if tool_matches:
            print(f"\n[*] Nexus is using {len(tool_matches)} tool(s)...\n")

            for tool_name, tool_params in tool_matches:
                print(f"  -> Calling: {tool_name}")
                print(f"     Params: {tool_params}\n")

                # Execute tool
                result = execute_tool(tool_name, tool_params.strip())

                if result.get("success"):
                    print(f"  [OK] Tool executed successfully")
                    if result.get("files"):
                        print(f"  [FILES] Created: {', '.join(result['files'])}")
                    print()

                    # Get final response with tool result
                    final_response = requests.post(
                        "http://localhost:11434/api/chat",
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_message},
                                {"role": "assistant", "content": assistant_response},
                                {"role": "user", "content": f"Tool result: {json.dumps(result)}. Please summarize for the user."}
                            ],
                            "stream": False
                        },
                        timeout=60
                    )

                    if final_response.status_code == 200:
                        final_data = final_response.json()
                        final_msg = final_data.get("message", {}).get("content", "")
                        # Remove any additional tool calls from summary
                        final_msg = re.sub(tool_pattern, '', final_msg).strip()
                        print(f"[NEXUS] {final_msg}\n")
                    else:
                        print(f"[NEXUS] {result.get('result', 'Done!')}\n")
                else:
                    print(f"  [X] Error: {result.get('error')}\n")

        else:
            # No tools, just conversation
            print(f"[NEXUS] {assistant_response}\n")

    except requests.exceptions.ConnectionError:
        print("[X] Error: Cannot connect to Ollama. Make sure 'ollama serve' is running.")
    except Exception as e:
        print(f"[X] Error: {e}")


def main():
    print("=" * 60)
    print("[NEXUS CLI] Simple Tool-Enabled Interface")
    print("=" * 60)
    print("\nAvailable tools: IMAGE, MUSIC, VIDEO, CODE, SEARCH, STORY")
    print("Type 'exit' or 'quit' to leave\n")

    # Check Nexus API
    try:
        response = requests.get("http://localhost:5000/api/status", timeout=2)
        print("[OK] Nexus API: Online")
    except:
        print("[!] Warning: Nexus API not running")
        print("    Start with: python D:/AIArm/nexus_api_server.py\n")

    # Check model
    try:
        response = requests.post(
            "http://localhost:11434/api/show",
            json={"name": "nexusai-tools:latest"}
        )
        model = "nexusai-tools:latest" if response.status_code == 200 else "nexusai-a0-coder1.0:latest"
    except:
        model = "nexusai-a0-coder1.0:latest"

    print(f"[MODEL] Using: {model}\n")
    print("-" * 60 + "\n")

    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n[BYE] Goodbye!\n")
                break

            chat(user_input, model)

        except KeyboardInterrupt:
            print("\n\n[BYE] Goodbye!\n")
            break
        except Exception as e:
            print(f"[X] Error: {e}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        chat(command)
    else:
        main()

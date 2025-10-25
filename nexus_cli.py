#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus CLI - Tool-Enabled Terminal Interface
Wraps Ollama with runtime tool definitions and execution
"""

import sys
import json
import requests
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Tool definitions for Nexus capabilities
NEXUS_TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'generate_image',
            'description': 'Generate an image using Stable Diffusion AI. Creates high-quality images from text descriptions.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'prompt': {
                        'type': 'string',
                        'description': 'Detailed description of the image to generate',
                    },
                    'style': {
                        'type': 'string',
                        'description': 'Optional style: realistic, artistic, anime, cinematic, fantasy, portrait, landscape',
                        'enum': ['realistic', 'artistic', 'anime', 'cinematic', 'fantasy', 'portrait', 'landscape']
                    }
                },
                'required': ['prompt'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_music',
            'description': 'Create a complete song with lyrics, melody, and musical structure',
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'string',
                        'description': 'Description of the song including theme, style, and mood',
                    },
                    'style': {
                        'type': 'string',
                        'description': 'Musical style/genre',
                    }
                },
                'required': ['description'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_video',
            'description': 'Create a video with script, storyboard, and MP4 output',
            'parameters': {
                'type': 'object',
                'properties': {
                    'concept': {
                        'type': 'string',
                        'description': 'Video concept or topic',
                    },
                    'duration': {
                        'type': 'integer',
                        'description': 'Video duration in seconds (default 30)',
                    }
                },
                'required': ['concept'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_code',
            'description': 'Generate complete application code (web, mobile, desktop)',
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'string',
                        'description': 'Detailed description of the application to create',
                    },
                    'app_type': {
                        'type': 'string',
                        'description': 'Type of application',
                        'enum': ['website', 'react_app', 'mobile_app', 'python_app', 'api']
                    }
                },
                'required': ['description'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'web_search',
            'description': 'Search the internet for information',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'Search query',
                    }
                },
                'required': ['query'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_story',
            'description': 'Write a creative story or narrative',
            'parameters': {
                'type': 'object',
                'properties': {
                    'prompt': {
                        'type': 'string',
                        'description': 'Story prompt or theme',
                    },
                    'length': {
                        'type': 'string',
                        'description': 'Story length',
                        'enum': ['short', 'medium', 'long']
                    }
                },
                'required': ['prompt'],
            },
        },
    },
]


def execute_tool(tool_name: str, parameters: dict) -> dict:
    """Execute a tool call via Nexus API"""
    try:
        # Map tool names to agent names
        agent_map = {
            'generate_image': 'photo',
            'generate_music': 'music',
            'generate_video': 'video',
            'generate_code': 'code',
            'web_search': 'websearch',
            'generate_story': 'story'
        }

        agent = agent_map.get(tool_name)
        if not agent:
            return {"error": f"Unknown tool: {tool_name}"}

        # Call Nexus API
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={
                "message": json.dumps(parameters),
                "agent": agent
            },
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


def chat_with_tools(user_message: str, model="nexusai-tools:latest"):
    """Chat with Ollama using tool support"""
    messages = [
        {"role": "user", "content": user_message}
    ]

    try:
        # Initial request with tools
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": messages,
                "tools": NEXUS_TOOLS,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ Error: Ollama returned status {response.status_code}")
            return

        data = response.json()
        message = data.get("message", {})

        # Check for tool calls
        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            print(f"\n🔧 Nexus is using {len(tool_calls)} tool(s)...\n")

            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call['function']['name']
                function_args = tool_call['function']['arguments']

                print(f"  → Calling: {function_name}")
                print(f"    Parameters: {json.dumps(function_args, indent=2)}\n")

                # Execute the tool
                result = execute_tool(function_name, function_args)

                # Add tool result to messages
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result)
                })

            # Get final response with tool results
            final_response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )

            if final_response.status_code == 200:
                final_data = final_response.json()
                final_message = final_data.get("message", {}).get("content", "")
                print(f"✨ Nexus: {final_message}\n")
            else:
                print("❌ Error getting final response")

        else:
            # No tool calls, just respond directly
            content = message.get("content", "")
            print(f"💬 Nexus: {content}\n")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Ollama. Make sure 'ollama serve' is running.")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("=" * 60)
    print("🚀 Nexus CLI - Tool-Enabled Terminal Interface")
    print("=" * 60)
    print("\nAvailable capabilities:")
    print("  🎨 Generate images, music, videos, stories")
    print("  💻 Create applications and code")
    print("  🔍 Search the web")
    print("\nType 'exit' or 'quit' to leave\n")

    # Check if Nexus API is running
    try:
        response = requests.get("http://localhost:5000/api/status", timeout=2)
        print("✅ Nexus API: Online")
    except:
        print("⚠️  Warning: Nexus API not running. Some tools may not work.")
        print("   Start with: python D:/AIArm/nexus_api_server.py\n")

    # Check if model exists
    try:
        response = requests.post(
            "http://localhost:11434/api/show",
            json={"name": "nexusai-tools:latest"}
        )
        if response.status_code != 200:
            print("\n📝 Model 'nexusai-tools:latest' not found.")
            print("   Create it with: ollama create nexusai-tools -f D:/AIArm/Modelfiles/NexusAI-ToolEnabled.modelfile")
            print("   Falling back to: nexusai-a0-coder1.0:latest\n")
            model = "nexusai-a0-coder1.0:latest"
        else:
            model = "nexusai-tools:latest"
    except:
        model = "nexusai-a0-coder1.0:latest"

    print(f"🤖 Using model: {model}\n")
    print("-" * 60 + "\n")

    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye!\n")
                break

            chat_with_tools(user_input, model)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Direct command mode
        command = " ".join(sys.argv[1:])
        chat_with_tools(command)
    else:
        # Interactive mode
        main()

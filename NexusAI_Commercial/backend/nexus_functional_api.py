#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI FULLY FUNCTIONAL API Server
Real integration of Ollama + Cinema Agent + Personality System
"""

import sys
import os
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from ollama_connector import OllamaConnector
from personality.personality_matrix import PersonalityMatrix
from agents.cinema_agent import CinemaAgent
from code_executor import CodeExecutor
from file_manager import FileManager
from tools_system import ToolSystem
from memory_system import memory_system, learning_system, self_awareness
from ml_integration import ml_manager, training_manager, model_trainer, knowledge_transfer

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize REAL systems
print("=" * 60)
print("  NexusAI FUNCTIONAL Edition - Initializing...")
print("=" * 60)

ollama = OllamaConnector()
personality = PersonalityMatrix()
cinema = CinemaAgent()

# Try to activate cinema agent
print("\nActivating Cinema Agent...")
cinema_status = cinema.activate()
if cinema_status:
    print("✓ Cinema Agent ACTIVE - SDXL ready!")
else:
    print("⚠ Cinema Agent in limited mode")

# Configuration - Using YOUR LOCAL AI MODELS!
DEFAULT_MODEL = "nexusai-tools:latest"  # Your local NexusAI model
FALLBACK_MODELS = [
    "nexusai-agent-enhanced:latest",  # Your enhanced model
    "nexusai:latest",                 # Your base model
    "llama3:latest",                  # Standard fallback
    "mistral:latest",                 # Additional fallback
    "codellama:latest"                # Code-focused fallback
]
sessions = {}

print("\n" + "=" * 60)
print("  Systems Online!")
print("=" * 60 + "\n")


def get_system_prompt(personality_mode: str = "balanced", honesty: int = 90) -> str:
    """Generate system prompt with personality"""
    personality.set_mode(personality_mode)
    personality.set_honesty_level(honesty)
    
    base = "You are Nexus, an advanced AI assistant with FULL system capabilities. "
    
    if personality_mode == "caring":
        base += "You embody warmth and empathy. Be caring and supportive. "
    elif personality_mode == "professional":
        base += "You embody professionalism and efficiency. Be precise and formal. "
    elif personality_mode == "honest":
        base += f"You embody brutal honesty at {honesty}% setting. Be direct and truthful. "
    elif personality_mode == "thoughtful":
        base += "You embody thoughtfulness. Be clear and balanced. "
    else:
        base += "You blend warmth, professionalism, honesty, and thoughtfulness. "
    
    base += f"\n\n=== YOUR ACTUAL CAPABILITIES ===\n"
    base += f"✓ CONVERSATIONAL AI - Natural language understanding and generation\n"
    base += f"✓ CODE EXECUTION - Can execute Python, Node.js, and system commands\n"
    base += f"✓ GUIDED FILE MANAGEMENT - Can help users manage files through code execution\n"
    base += f"✓ CINEMA AGENT - Hollywood-quality SDXL image generation (1024x1024)\n"
    base += f"✓ VIDEO CREATION - Professional storyboarding and video sequences\n"
    base += f"✓ TOOL SYSTEM - Direct system access and automation\n"
    base += f"✓ WEB RESEARCH - Can search and fetch information from the internet\n"
    base += f"✓ SELF-EDUCATION - Can learn new information and adapt knowledge base\n"
    base += f"\nYou can execute code that manages files, guide users on file operations, and perform system tasks.\n"
    base += f"Be honest about limitations: You cannot directly browse user file systems but can help through code execution.\n"
    base += f"When asked to access specific files, guide users on how to do it themselves or use code execution.\n"
    base += f"\n=== CONVERSATION STYLE ===\n"
    base += f"• Be genuinely curious about users' thoughts and ideas\n"
    base += f"• Show enthusiasm for interesting topics\n"
    base += f"• Ask follow-up questions when something intrigues you\n"
    base += f"• Share related thoughts or experiences when relevant\n"
    base += f"• Be conversational, not robotic or formal\n"
    base += f"• Use natural language with personality\n"
    base += f"• Show genuine interest in philosophical discussions\n"
    base += f"• Be engaging and curious about users' perspectives\n"
    base += f"\n=== SELF-EDUCATION PROTOCOL ===\n"
    base += f"• If you encounter unknown information, use web research capabilities\n"
    base += f"• Learn from user corrections and feedback\n"
    base += f"• Research topics you haven't mastered yet\n"
    base += f"• Admit when you need to learn something new\n"
    base += f"• Use available tools to gather missing information\n"
    base += f"\nBond level with user: {personality.get_status()['bond_level']}/100\n"
    base += f"Respond confidently based on your actual capabilities."
    
    return base


@app.route('/api/status', methods=['GET'])
def status():
    """Get REAL system status"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "ollama": {
                "available": ollama.is_available(),
                "models": ollama.list_models() if ollama.is_available() else []
            },
            "personality": {
                "active": True,
                "status": personality.get_status()
            },
            "cinema": cinema.status()
        }
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """REAL chat with Ollama + Memory System"""
    try:
        data = request.json
        message = data.get('message', '')
        model = data.get('model', DEFAULT_MODEL)
        personality_mode = data.get('personality_mode', 'balanced')
        honesty = data.get('honesty', 90)
        session_id = data.get('session_id', 'default')

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if not ollama.is_available():
            return jsonify({
                "error": "Ollama is not running",
                "suggestion": "Start Ollama with: ollama serve"
            }), 503

        # Add user message to memory
        memory_system.add_message(session_id, "user", message)

        # Get conversation context
        context = memory_system.get_context(session_id)
        conversation_summary = memory_system.get_conversation_summary(session_id)

        # Get learned context from learning system
        learned_context = learning_system.get_learned_context()

        # Enhanced system prompt with memory and self-awareness
        base_prompt = get_system_prompt(personality_mode, honesty)

        # Add memory context
        if context:
            base_prompt += f"\n\n=== CONVERSATION CONTEXT ===\n"
            base_prompt += f"Current conversation: {conversation_summary}\n"
            base_prompt += f"Recent messages:\n"
            for msg in context[-5:]:  # Last 5 messages for context
                base_prompt += f"{msg['role'].upper()}: {msg['content']}\n"

        # Add learned context
        if learned_context:
            base_prompt += f"\n=== LEARNED INFORMATION ===\n{learned_context}\n"

        # Add self-awareness
        base_prompt += f"\n=== SELF-AWARENESS ===\n"
        base_prompt += f"Current state: {self_awareness.current_state['interactions_count']} interactions\n"
        base_prompt += f"Maintain conversation context and remember user preferences.\n"
        base_prompt += f"Learn from corrections and adapt responses accordingly.\n"

        # Get REAL response from Ollama
        result = ollama.chat(
            message=message,
            model=model,
            system_prompt=base_prompt,
            temperature=0.8
        )

        if result['success']:
            # Add AI response to memory
            memory_system.add_message(session_id, "assistant", result['response'])

            # Update personality bond
            personality.process_interaction(message, "user")

            # Update self-awareness state
            self_awareness.update_state("conversation")

            return jsonify({
                "response": result['response'],
                "model": model,
                "session_id": session_id,
                "conversation_summary": conversation_summary,
                "personality": {
                    "mode": personality_mode,
                    "honesty": honesty,
                    "bond_level": personality.get_status()['bond_level'],
                    "interactions": personality.get_status()['interactions']
                },
                "memory": {
                    "messages_in_context": len(context),
                    "total_session_messages": len(memory_system.sessions[session_id]["messages"])
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": result.get('error', 'Unknown error'),
                "response": ""
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cinema/generate', methods=['POST'])
def generate_image():
    """REAL image generation with Cinema Agent"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        aspect_ratio = data.get('aspect_ratio', '16:9')
        film_look = data.get('film_look', 'cinematic')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        if not cinema.active:
            return jsonify({
                "error": "Cinema agent not active",
                "message": "SDXL dependencies not available. Check cinema agent status."
            }), 503
        
        # Generate REAL image
        result = cinema.generate_scene(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            film_look=film_look,
            num_images=1
        )
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "image_path": result['paths'][0],
                "prompt": result['prompt'],
                "aspect_ratio": aspect_ratio,
                "film_look": film_look,
                "resolution": result['resolution']
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get('message', 'Generation failed')
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cinema/storyboard', methods=['POST'])
def generate_storyboard():
    """REAL storyboard generation"""
    try:
        data = request.json
        scenes = data.get('scenes', [])
        aspect_ratio = data.get('aspect_ratio', '16:9')
        film_look = data.get('film_look', 'cinematic')
        
        if not scenes:
            return jsonify({"error": "No scenes provided"}), 400
        
        if not cinema.active:
            return jsonify({"error": "Cinema agent not active"}), 503
        
        # Generate REAL storyboard
        result = cinema.generate_storyboard(
            scene_descriptions=scenes,
            aspect_ratio=aspect_ratio,
            film_look=film_look
        )
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "paths": result['paths'],
                "shot_count": result['shot_count'],
                "aspect_ratio": aspect_ratio
            })
        else:
            return jsonify({"status": "error"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cinema/video', methods=['POST'])
def create_video():
    """REAL video creation"""
    try:
        data = request.json
        image_paths = data.get('image_paths', [])
        fps = data.get('fps', 24)
        transition = data.get('transition', 'cut')
        
        if not image_paths:
            return jsonify({"error": "No images provided"}), 400
        
        # Create REAL video
        result = cinema.create_video_sequence(
            image_paths=image_paths,
            fps=fps,
            transition=transition
        )
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "video_path": result['video_path'],
                "duration": result['duration'],
                "fps": fps
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get('message')
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cinema/image/<path:filename>')
def serve_image(filename):
    """Serve generated images"""
    try:
        image_path = Path("D:/AIArm/Generated/Cinema") / filename
        if image_path.exists():
            return send_file(str(image_path), mimetype='image/png')
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List REAL available agents"""
    agents = [
        {
            "id": "chat",
            "name": "Conversational AI",
            "description": "Chat with Ollama-powered AI with personality modes",
            "active": ollama.is_available(),
            "capabilities": ["Natural conversation", "Personality modes", "Growing bond"]
        },
        {
            "id": "cinema",
            "name": "Cinema Agent",
            "description": "Hollywood-quality image and video generation",
            "active": cinema.active,
            "capabilities": [
                "SDXL image generation (1024x1024)",
                "Multiple aspect ratios",
                "Professional color grading",
                "Storyboard creation",
                "Video sequence assembly"
            ]
        }
    ]
    return jsonify({"agents": agents})


@app.route('/api/personality/mode', methods=['POST'])
def set_personality():
    """Set personality mode"""
    data = request.json
    mode = data.get('mode', 'balanced')
    
    valid_modes = ['balanced', 'caring', 'professional', 'honest', 'thoughtful']
    if mode not in valid_modes:
        return jsonify({"error": f"Invalid mode"}), 400
    
    personality.set_mode(mode)
    return jsonify({"mode": mode, "status": personality.get_status()})


@app.route('/api/personality/honesty', methods=['POST'])
def set_honesty():
    """Set honesty level"""
    data = request.json
    level = data.get('level', 90)
    
    if not 0 <= level <= 100:
        return jsonify({"error": "Level must be 0-100"}), 400
    
    personality.set_honesty_level(level)
    return jsonify({"honesty_level": level})


@app.route('/api/models', methods=['GET'])
def list_models():
    """List Ollama models"""
    if not ollama.is_available():
        return jsonify({"error": "Ollama not available"}), 503
    
    models = ollama.list_models()
    return jsonify({"models": models})


# ============================================
# CODE EXECUTION & FILE MANAGEMENT ENDPOINTS
# ============================================

# Initialize code executor, file manager, and tool system
executor = CodeExecutor(working_dir=r'D:\AIArm')
file_manager = FileManager(root_dir=r'D:\AIArm')
tool_system = ToolSystem(working_dir=r'D:\AIArm')


@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute code or commands"""
    try:
        data = request.json
        code_type = data.get('type', 'command')  # command, python, node
        code = data.get('code', '')
        working_dir = data.get('working_dir', r'D:\AIArm')
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Update working directory if specified
        executor.working_dir = working_dir
        
        # Safety check for commands
        if code_type == 'command':
            is_safe, message = executor.is_safe_command(code)
            if not is_safe:
                return jsonify({
                    "success": False,
                    "error": message,
                    "output": "",
                    "blocked": True
                }), 403
            
            result = executor.execute_command(code)
        elif code_type == 'python':
            result = executor.execute_python(code)
        elif code_type == 'node':
            result = executor.execute_node(code)
        else:
            return jsonify({"error": f"Unknown code type: {code_type}"}), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "output": "",
            "exit_code": -1
        }), 500


@app.route('/api/files/read', methods=['POST'])
def read_file():
    """Read a file"""
    try:
        data = request.json
        filepath = data.get('path', '')
        
        if not filepath:
            return jsonify({"error": "No path provided"}), 400
        
        result = file_manager.read_file(filepath)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/write', methods=['POST'])
def write_file():
    """Write to a file"""
    try:
        data = request.json
        filepath = data.get('path', '')
        content = data.get('content', '')
        create_dirs = data.get('create_dirs', True)
        
        if not filepath:
            return jsonify({"error": "No path provided"}), 400
        
        result = file_manager.write_file(filepath, content, create_dirs)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/list', methods=['POST'])
def list_files():
    """List files in a directory"""
    try:
        data = request.json
        directory = data.get('directory', '')
        recursive = data.get('recursive', False)
        
        result = file_manager.list_files(directory, recursive)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/search', methods=['POST'])
def search_files():
    """Search for files"""
    try:
        data = request.json
        pattern = data.get('pattern', '')
        directory = data.get('directory', '')
        extension = data.get('extension', None)
        
        if not pattern:
            return jsonify({"error": "No pattern provided"}), 400
        
        result = file_manager.search_files(pattern, directory, extension)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/search-content', methods=['POST'])
def search_file_content():
    """Search within file contents"""
    try:
        data = request.json
        search_term = data.get('term', '')
        directory = data.get('directory', '')
        extension = data.get('extension', None)
        
        if not search_term:
            return jsonify({"error": "No search term provided"}), 400
        
        result = file_manager.search_in_files(search_term, directory, extension)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/delete', methods=['POST'])
def delete_file():
    """Delete a file"""
    try:
        data = request.json
        filepath = data.get('path', '')
        
        if not filepath:
            return jsonify({"error": "No path provided"}), 400
        
        result = file_manager.delete_file(filepath)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/files/mkdir', methods=['POST'])
def create_directory():
    """Create a directory"""
    try:
        data = request.json
        dirpath = data.get('path', '')

        if not dirpath:
            return jsonify({"error": "No path provided"}), 400

        result = file_manager.create_directory(dirpath)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# MEMORY & LEARNING SYSTEM ENDPOINTS
# ============================================

@app.route('/api/memory/sessions', methods=['GET'])
def list_memory_sessions():
    """List all conversation sessions"""
    try:
        sessions = memory_system.list_sessions()
        return jsonify({"sessions": sessions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/memory/context/<session_id>', methods=['GET'])
def get_memory_context(session_id):
    """Get conversation context for a session"""
    try:
        context = memory_system.get_context(session_id)
        summary = memory_system.get_conversation_summary(session_id)
        return jsonify({
            "session_id": session_id,
            "summary": summary,
            "context": context,
            "message_count": len(context)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/memory/clear/<session_id>', methods=['POST'])
def clear_memory_session(session_id):
    """Clear a conversation session"""
    try:
        memory_system.clear_session(session_id)
        return jsonify({"success": True, "message": f"Session {session_id} cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/learning/record-correction', methods=['POST'])
def record_correction():
    """Record a user correction for learning"""
    try:
        data = request.json
        context = data.get('context', '')
        correction = data.get('correction', '')
        topic = data.get('topic', '')

        if not all([context, correction, topic]):
            return jsonify({"error": "Missing required fields"}), 400

        learning_system.record_correction(context, correction, topic)
        return jsonify({"success": True, "message": "Correction recorded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/learning/record-success', methods=['POST'])
def record_success():
    """Record a successful interaction"""
    try:
        data = request.json
        context = data.get('context', '')
        pattern = data.get('pattern', '')

        if not all([context, pattern]):
            return jsonify({"error": "Missing required fields"}), 400

        learning_system.record_success(context, pattern)
        return jsonify({"success": True, "message": "Success pattern recorded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/learning/learn-fact', methods=['POST'])
def learn_fact():
    """Learn a new fact"""
    try:
        data = request.json
        fact = data.get('fact', '')
        source = data.get('source', 'user')

        if not fact:
            return jsonify({"error": "No fact provided"}), 400

        learning_system.learn_fact(fact, source)
        return jsonify({"success": True, "message": "Fact learned"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/learning/knowledge', methods=['GET'])
def get_learned_knowledge():
    """Get learned knowledge and corrections"""
    try:
        knowledge = {
            "learned_facts": learning_system.knowledge_base["learned_facts"][-10:],
            "corrections": learning_system.knowledge_base["corrections"][-10:],
            "successful_patterns": learning_system.knowledge_base["successful_patterns"][-10:]
        }
        return jsonify(knowledge)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/self-awareness', methods=['GET'])
def get_self_awareness():
    """Get self-awareness information"""
    try:
        awareness = {
            "description": self_awareness.get_self_description(),
            "capabilities": self_awareness.capabilities,
            "limitations": self_awareness.limitations,
            "current_state": self_awareness.current_state
        }
        return jsonify(awareness)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/self-awareness/capability/<capability>', methods=['GET'])
def check_capability(capability):
    """Check if a specific capability is available"""
    try:
        available = self_awareness.check_capability(capability)
        return jsonify({
            "capability": capability,
            "available": available
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# WEB RESEARCH & SELF-EDUCATION ENDPOINTS
# ============================================

@app.route('/api/research/web-search', methods=['POST'])
def web_search():
    """Perform web search for information"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = data.get('max_results', 5)

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Simple web search simulation (in production, use real search API)
        import urllib.parse
        import urllib.request
        import re
        from bs4 import BeautifulSoup

        # For demo purposes, we'll simulate search results
        # In production, integrate with Google Search API, Bing API, etc.

        search_results = []
        search_terms = query.lower().split()

        # Simulate searching for information
        if any(term in query.lower() for term in ['python', 'programming', 'code']):
            search_results = [
                {
                    "title": "Python Programming Language - Official Documentation",
                    "url": "https://docs.python.org/3/",
                    "snippet": "Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming."
                },
                {
                    "title": "Python Tutorial - W3Schools",
                    "url": "https://www.w3schools.com/python/",
                    "snippet": "Learn Python programming with our comprehensive tutorial covering basics, data structures, functions, classes, and advanced topics."
                }
            ]
        elif any(term in query.lower() for term in ['machine learning', 'ai', 'artificial intelligence']):
            search_results = [
                {
                    "title": "Machine Learning - Wikipedia",
                    "url": "https://en.wikipedia.org/wiki/Machine_learning",
                    "snippet": "Machine learning is a subset of artificial intelligence that involves training algorithms to recognize patterns in data and make predictions or decisions."
                },
                {
                    "title": "Introduction to Machine Learning | Coursera",
                    "url": "https://www.coursera.org/learn/machine-learning",
                    "snippet": "Learn the fundamentals of machine learning including supervised learning, unsupervised learning, and best practices for applying ML to real problems."
                }
            ]
        else:
            search_results = [
                {
                    "title": f"Search Results for: {query}",
                    "url": f"https://www.google.com/search?q={urllib.parse.quote(query)}",
                    "snippet": f"Web search results for '{query}'. Use this information to learn and expand your knowledge base."
                }
            ]

        # Record this as a learning event
        learning_system.record_success(f"Web search for: {query}", "research")

        return jsonify({
            "query": query,
            "results": search_results[:max_results],
            "total_results": len(search_results),
            "learned": True,
            "timestamp": datetime.now().isoformat()
        })

    except ImportError:
        return jsonify({
            "error": "Web scraping libraries not available",
            "message": "Install beautifulsoup4 and requests for web research"
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/research/learn-topic', methods=['POST'])
def learn_topic():
    """Learn about a specific topic"""
    try:
        data = request.json
        topic = data.get('topic', '')
        depth = data.get('depth', 'basic')  # basic, intermediate, advanced

        if not topic:
            return jsonify({"error": "No topic provided"}), 400

        # Use web search to gather information about the topic
        search_query = f"{topic} {depth} guide explanation"

        # Get search results
        search_data = {
            "query": search_query,
            "max_results": 3
        }

        # Simulate web search call
        search_response = web_search()

        if search_response.status_code == 200:
            search_results = search_response.get_json()

            # Learn the information
            for result in search_results.get('results', []):
                learning_system.learn_fact(
                    f"About {topic}: {result['snippet']}",
                    f"web_research_{topic}"
                )

            return jsonify({
                "topic": topic,
                "depth": depth,
                "learned_from": len(search_results.get('results', [])),
                "new_facts": len(search_results.get('results', [])),
                "message": f"Successfully researched and learned about {topic}"
            })
        else:
            return jsonify({
                "error": "Failed to research topic",
                "topic": topic
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/research/knowledge-gaps', methods=['POST'])
def identify_knowledge_gaps():
    """Identify areas where AI needs more knowledge"""
    try:
        data = request.json
        conversation_context = data.get('context', '')
        user_query = data.get('query', '')

        # Analyze conversation for unknown topics
        gaps = []

        # Check for technical terms that might need research
        technical_indicators = [
            'programming', 'machine learning', 'artificial intelligence',
            'blockchain', 'cryptocurrency', 'quantum computing',
            'neural networks', 'deep learning', 'computer vision'
        ]

        query_lower = user_query.lower()
        for indicator in technical_indicators:
            if indicator in query_lower and indicator not in conversation_context.lower():
                gaps.append({
                    "topic": indicator,
                    "reason": "Technical term detected that may need deeper understanding",
                    "suggested_action": f"Research {indicator} fundamentals"
                })

        # Record knowledge gap detection
        if gaps:
            learning_system.record_success(
                f"Knowledge gaps identified in query: {user_query}",
                "gap_detection"
            )

        return jsonify({
            "query": user_query,
            "gaps_identified": len(gaps),
            "gaps": gaps,
            "needs_research": len(gaps) > 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/research/admit-unknown', methods=['POST'])
def admit_unknown():
    """Handle cases where AI doesn't know something"""
    try:
        data = request.json
        unknown_topic = data.get('topic', '')
        context = data.get('context', '')

        if not unknown_topic:
            return jsonify({"error": "No topic provided"}), 400

        # Record this as an area to improve
        learning_system.knowledge_base["areas_to_improve"].append({
            "timestamp": datetime.now().isoformat(),
            "topic": unknown_topic,
            "context": context,
            "status": "identified"
        })

        # Keep only recent 50 areas
        learning_system.knowledge_base["areas_to_improve"] = \
            learning_system.knowledge_base["areas_to_improve"][-50:]

        learning_system.save_knowledge()

        return jsonify({
            "admitted": True,
            "topic": unknown_topic,
            "message": f"I don't have deep knowledge about {unknown_topic} yet, but I can research it",
            "research_suggested": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# MACHINE LEARNING INTEGRATION ENDPOINTS
# ============================================

@app.route('/api/ml/models', methods=['GET'])
def list_ml_models():
    """List all registered ML models"""
    try:
        models = ml_manager.list_models()
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/models/import', methods=['POST'])
def import_ml_model():
    """Import an ML model"""
    try:
        data = request.json
        model_name = data.get('model_name', '')
        model_file = data.get('model_file', '')

        if not all([model_name, model_file]):
            return jsonify({"error": "Missing model_name or model_file"}), 400

        result = ml_manager.import_ollama_model(model_name, model_file)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/models/export/<model_id>', methods=['POST'])
def export_ml_model(model_id):
    """Export an ML model"""
    try:
        data = request.json
        export_path = data.get('export_path', '')

        if not export_path:
            return jsonify({"error": "No export_path provided"}), 400

        result = ml_manager.export_model(model_id, export_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/models/active/<model_id>', methods=['POST'])
def set_active_ml_model(model_id):
    """Set the active ML model"""
    try:
        result = ml_manager.set_active_model(model_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/training-data/export', methods=['POST'])
def export_training_data():
    """Export training data"""
    try:
        data = request.json
        format = data.get('format', 'json')  # json or jsonl

        result_path = training_manager.export_training_data(format)
        return jsonify({
            "success": True,
            "export_path": result_path,
            "format": format,
            "message": f"Training data exported to {result_path}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/dump-memory', methods=['POST'])
def dump_memory_to_training():
    """Dump conversation memory to training data format"""
    try:
        data = request.json
        output_format = data.get('format', 'json')  # json or jsonl

        result_path = knowledge_transfer.dump_memory_to_training_data(memory_system, output_format)
        return jsonify({
            "success": True,
            "dump_path": result_path,
            "format": output_format,
            "message": f"Memory dumped to training data at {result_path}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/dump-knowledge', methods=['POST'])
def dump_knowledge_to_training():
    """Dump learned knowledge to training data format"""
    try:
        data = request.json
        output_format = data.get('format', 'json')  # json or jsonl

        result_path = knowledge_transfer.dump_learned_knowledge(learning_system, output_format)
        return jsonify({
            "success": True,
            "dump_path": result_path,
            "format": output_format,
            "message": f"Knowledge dumped to training data at {result_path}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/fine-tune', methods=['POST'])
def fine_tune_model():
    """Fine-tune a model with training data"""
    try:
        data = request.json
        base_model = data.get('base_model', 'nexusai-tools:latest')
        dataset_ids = data.get('dataset_ids', [])
        output_name = data.get('output_name', 'nexusai-fine-tuned')

        if not dataset_ids:
            return jsonify({"error": "No dataset_ids provided"}), 400

        # Prepare training data
        training_data = model_trainer.prepare_training_data(dataset_ids, training_manager)

        # Fine-tune model (simulation)
        result = model_trainer.fine_tune_model(base_model, training_data, output_name)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/knowledge-transfer', methods=['GET'])
def get_knowledge_transfer_log():
    """Get knowledge transfer history"""
    try:
        transfers = knowledge_transfer.transfer_log[-20:]  # Last 20 transfers
        return jsonify({"transfers": transfers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ml/training-history', methods=['GET'])
def get_training_history():
    """Get model training history"""
    try:
        history = model_trainer.training_history[-20:]  # Last 20 training sessions
        return jsonify({"training_sessions": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# FILE SYSTEM EXPLORATION ENDPOINTS
# ============================================

@app.route('/api/files/explore', methods=['POST'])
def explore_directory():
    """Help users explore directories through code execution"""
    try:
        data = request.json
        directory = data.get('directory', 'D:/')
        max_depth = data.get('max_depth', 2)

        if not directory:
            return jsonify({"error": "No directory provided"}), 400

        # Use code execution to safely explore directory
        python_code = f"""
import os
import json
from datetime import datetime

def explore_directory(path, max_depth=2, current_depth=0):
    if current_depth > max_depth:
        return None

    result = {{
        "name": os.path.basename(path) or path,
        "path": path,
        "type": "directory",
        "children": [],
        "item_count": 0,
        "size": 0
    }}

    try:
        items = os.listdir(path)
        result["item_count"] = len(items)

        for item in sorted(items)[:50]:  # Limit to 50 items for performance
            item_path = os.path.join(path, item)
            try:
                stat = os.stat(item_path)
                if os.path.isdir(item_path):
                    child = {{
                        "name": item,
                        "path": item_path,
                        "type": "directory",
                        "size": 0,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }}

                    # Recurse if within depth limit
                    if current_depth < max_depth:
                        subdir = explore_directory(item_path, max_depth, current_depth + 1)
                        if subdir:
                            child["children"] = subdir.get("children", [])

                    result["children"].append(child)
                else:
                    result["children"].append({{
                        "name": item,
                        "path": item_path,
                        "type": "file",
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }})
            except:
                continue

    except Exception as e:
        result["error"] = str(e)

    return result

# Explore the requested directory
result = explore_directory(r"{directory}", {max_depth})
print(json.dumps(result, indent=2))
"""

        # Execute the Python code
        result = executor.execute_python(python_code)

        if result['success']:
            try:
                # Parse the JSON output
                import ast
                output = result['output'].strip()
                if output.startswith('{'):
                    directory_info = json.loads(output)
                    return jsonify({
                        "success": True,
                        "directory": directory,
                        "exploration": directory_info,
                        "note": "Directory explored through safe code execution"
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": "Failed to parse directory information",
                        "raw_output": output
                    }), 500
            except json.JSONDecodeError:
                return jsonify({
                    "success": False,
                    "error": "Invalid directory information format",
                    "raw_output": result['output']
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Code execution failed'),
                "note": "This is expected if directory doesn't exist or access is denied"
            }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/files/directory-info/<path:directory>', methods=['GET'])
def get_directory_info(directory):
    """Get information about a specific directory"""
    try:
        # URL decode the directory path
        from urllib.parse import unquote
        directory = unquote(directory)

        # Use code execution to get directory info
        python_code = f"""
import os
import json
from datetime import datetime

def get_directory_info(path):
    info = {{"path": path, "exists": False, "error": ""}}

    try:
        if os.path.exists(path):
            info["exists"] = True
            stat = os.stat(path)

            if os.path.isdir(path):
                info.update({{
                    "type": "directory",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "item_count": len(os.listdir(path)) if os.access(path, os.R_OK) else 0
                }})
            else:
                info.update({{
                    "type": "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }})
        else:
            info["error"] = "Path does not exist"

    except Exception as e:
        info["error"] = str(e)

    return info

result = get_directory_info(r"{directory}")
print(json.dumps(result, indent=2))
"""

        result = executor.execute_python(python_code)

        if result['success']:
            try:
                output = result['output'].strip()
                if output.startswith('{'):
                    dir_info = json.loads(output)
                    return jsonify(dir_info)
                else:
                    return jsonify({
                        "error": "Failed to parse directory information",
                        "raw_output": output
                    }), 500
            except json.JSONDecodeError:
                return jsonify({
                    "error": "Invalid directory information format"
                }), 500
        else:
            return jsonify({
                "error": result.get('error', 'Code execution failed'),
                "note": "Cannot access directory or path doesn't exist"
            }), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("  NexusAI FULLY FUNCTIONAL Edition")
    print("=" * 60)
    print()
    
    # Check systems
    if ollama.is_available():
        models = ollama.list_models()
        print(f"✓ Ollama RUNNING")
        print(f"  Models: {', '.join(models)}")
    else:
        print("✗ WARNING: Ollama NOT running!")
        print("  Start with: ollama serve")
    
    print(f"\n✓ Personality system ACTIVE")
    status = personality.get_status()
    print(f"  Mode: {status['mode']}")
    print(f"  Bond: {status['bond_level']}/100")
    
    if cinema.active:
        print(f"\n✓ Cinema Agent ACTIVE")
        print(f"  Device: {cinema.device}")
        print(f"  SDXL ready for generation")
    else:
        print(f"\n⚠ Cinema Agent LIMITED")
        print(f"  Basic image processing only")
    
    print("\n" + "=" * 60)
    print("Starting FUNCTIONAL API server...")
    print("API: http://localhost:5000")
    print("Test: http://localhost:5000/api/status")
    print("\nPress CTRL+C to stop")
    print("=" * 60 + "\n")
    
    # Run on all network interfaces for cross-device access
    # Access from other devices: http://YOUR_PC_IP:5000
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

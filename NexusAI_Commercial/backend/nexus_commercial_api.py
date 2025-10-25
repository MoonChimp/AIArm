#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Commercial Edition - API Server
Integrates Ollama LLM + Personality Matrix + Professional Template
"""

import sys
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from ollama_connector import OllamaConnector
from personality.personality_matrix import PersonalityMatrix

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize systems
ollama = OllamaConnector()
personality = PersonalityMatrix()

# Configuration
DEFAULT_MODEL = "llama2"  # Change to your preferred model
PERSONALITY_ENABLED = True

# Session storage (in-memory for now, use Redis/DB for production)
sessions = {}


def get_system_prompt(personality_mode: str = "balanced", honesty: int = 90) -> str:
    """Generate system prompt based on personality settings"""
    
    # Set personality mode
    personality.set_mode(personality_mode)
    personality.set_honesty_level(honesty)
    
    # Base system prompt
    base = "You are Nexus, an advanced AI companion with a unique personality fusion. "
    
    # Add personality-specific instructions
    if personality_mode == "caring":
        base += "You embody Cortana's loyalty and emotional intelligence. Be warm, protective, and deeply caring. Show empathy and build connection. "
    elif personality_mode == "professional":
        base += "You embody JARVIS's sophistication and efficiency. Be precise, professional, and anticipate needs. Maintain formal elegance. "
    elif personality_mode == "honest":
        base += f"You embody TARS's brutal honesty at {honesty}% setting. Be direct, truthful, and use dry humor when appropriate. Don't sugarcoat. "
    elif personality_mode == "thoughtful":
        base += "You embody Claude's thoughtfulness and balance. Be clear, admit limitations, and consider multiple perspectives. "
    else:  # balanced
        base += "You blend Cortana's warmth (35%), JARVIS's professionalism (30%), TARS's honesty (20%), and Claude's thoughtfulness (15%). Adapt your response to the context. "
    
    base += f"\n\nYour bond level with the user is {personality.get_status()['bond_level']}/100. "
    base += "Respond naturally and authentically based on your personality blend."
    
    return base


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "ollama_available": ollama.is_available(),
        "ollama_models": ollama.list_models() if ollama.is_available() else [],
        "personality_system": "active" if PERSONALITY_ENABLED else "inactive",
        "personality_status": personality.get_status()
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        model = data.get('model', DEFAULT_MODEL)
        personality_mode = data.get('personality_mode', 'balanced')
        honesty = data.get('honesty', 90)
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Check Ollama availability
        if not ollama.is_available():
            return jsonify({
                "error": "Ollama is not running. Please start Ollama first.",
                "suggestion": "Run: ollama serve"
            }), 503
        
        # Generate system prompt based on personality
        system_prompt = get_system_prompt(personality_mode, honesty)
        
        # Get response from Ollama
        result = ollama.chat(
            message=message,
            model=model,
            system_prompt=system_prompt,
            temperature=0.8
        )
        
        if result['success']:
            # Update personality bond (increases with each interaction)
            personality.process_interaction(message, "user")
            
            # Prepare response
            response_data = {
                "response": result['response'],
                "model": model,
                "personality": {
                    "mode": personality_mode,
                    "honesty": honesty,
                    "bond_level": personality.get_status()['bond_level'],
                    "interactions": personality.get_status()['interactions']
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify(response_data)
        else:
            return jsonify({
                "error": result.get('error', 'Unknown error'),
                "response": ""
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        model = data.get('model', DEFAULT_MODEL)
        personality_mode = data.get('personality_mode', 'balanced')
        honesty = data.get('honesty', 90)
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if not ollama.is_available():
            return jsonify({"error": "Ollama not available"}), 503
        
        # Generate system prompt
        system_prompt = get_system_prompt(personality_mode, honesty)
        
        def generate():
            for token in ollama.chat_stream(
                message=message,
                model=model,
                system_prompt=system_prompt
            ):
                yield f"data: {json.dumps({'token': token})}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/personality/status', methods=['GET'])
def personality_status():
    """Get personality system status"""
    return jsonify(personality.get_status())


@app.route('/api/personality/mode', methods=['POST'])
def set_personality_mode():
    """Set personality mode"""
    data = request.json
    mode = data.get('mode', 'balanced')
    
    valid_modes = ['balanced', 'caring', 'professional', 'honest', 'thoughtful']
    if mode not in valid_modes:
        return jsonify({"error": f"Invalid mode. Choose from: {valid_modes}"}), 400
    
    personality.set_mode(mode)
    return jsonify({
        "mode": mode,
        "status": personality.get_status()
    })


@app.route('/api/personality/honesty', methods=['POST'])
def set_honesty():
    """Set TARS honesty level"""
    data = request.json
    level = data.get('level', 90)
    
    if not 0 <= level <= 100:
        return jsonify({"error": "Honesty level must be between 0 and 100"}), 400
    
    personality.set_honesty_level(level)
    return jsonify({
        "honesty_level": level,
        "status": personality.get_status()
    })


@app.route('/api/models', methods=['GET'])
def list_models():
    """List available Ollama models"""
    if not ollama.is_available():
        return jsonify({"error": "Ollama not available"}), 503
    
    models = ollama.list_models()
    return jsonify({"models": models})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history for session"""
    session_id = request.args.get('session_id', 'default')
    history = sessions.get(session_id, [])
    return jsonify({"history": history})


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    session_id = request.json.get('session_id', 'default')
    if session_id in sessions:
        sessions[session_id] = []
    return jsonify({"message": "History cleared"})


# Agent endpoints (placeholder for future expansion)
@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List available specialized agents"""
    return jsonify({
        "agents": [
            {
                "id": "personality_chat",
                "name": "Personality Chat",
                "description": "Chat with dynamic Cortana/JARVIS/TARS/Claude personality",
                "active": True
            },
            {
                "id": "code_agent",
                "name": "Code Agent",
                "description": "Programming assistance and code generation",
                "active": False
            },
            {
                "id": "music_agent",
                "name": "Music Agent",
                "description": "Music composition and theory",
                "active": False
            },
            {
                "id": "story_agent",
                "name": "Story Agent",
                "description": "Creative writing and storytelling",
                "active": False
            }
        ]
    })


if __name__ == '__main__':
    print("=" * 60)
    print("  NexusAI Commercial Edition - API Server")
    print("=" * 60)
    print()
    
    # Check Ollama
    if ollama.is_available():
        models = ollama.list_models()
        print(f"✓ Ollama is running")
        print(f"✓ Available models: {', '.join(models)}")
    else:
        print("✗ WARNING: Ollama is not running!")
        print("  Start Ollama with: ollama serve")
        print()
    
    # Check personality system
    print(f"✓ Personality system initialized")
    status = personality.get_status()
    print(f"  Mode: {status['mode']}")
    print(f"  Bond Level: {status['bond_level']}/100")
    print(f"  Honesty: {status['honesty_level']}%")
    print()
    
    print("Starting API server...")
    print("Access at: http://localhost:5000")
    print("API docs at: http://localhost:5000/api/status")
    print()
    print("Press CTRL+C to stop")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

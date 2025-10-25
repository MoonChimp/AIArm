#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Simple Functional API
Works without complex dependencies
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from ollama_connector import OllamaConnector

app = Flask(__name__)
CORS(app)

# Initialize Ollama
print("=" * 60)
print("  NexusAI Simple Edition - Initializing...")
print("=" * 60)

ollama = OllamaConnector()

# Simple bond tracking (without complex personality system)
bond_level = 0
interactions = 0

print("\n" + "=" * 60)
print("  System Online!")
print("=" * 60 + "\n")


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "ollama": {
                "available": ollama.is_available(),
                "models": ollama.list_models() if ollama.is_available() else []
            },
            "bond_level": bond_level,
            "interactions": interactions
        }
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Real chat with Ollama"""
    global bond_level, interactions
    
    try:
        data = request.json
        message = data.get('message', '')
        model = data.get('model', 'llama2')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if not ollama.is_available():
            return jsonify({
                "error": "Ollama is not running",
                "suggestion": "Start Ollama with: ollama serve"
            }), 503
        
        # Simple system prompt
        system_prompt = "You are Nexus, an advanced AI assistant. Be helpful and friendly."
        
        # Get REAL response from Ollama
        result = ollama.chat(
            message=message,
            model=model,
            system_prompt=system_prompt,
            temperature=0.8
        )
        
        if result['success']:
            # Update simple bond tracking
            interactions += 1
            if bond_level < 100:
                bond_level = min(100, bond_level + 1)
            
            return jsonify({
                "response": result['response'],
                "model": model,
                "personality": {
                    "bond_level": bond_level,
                    "interactions": interactions
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/models', methods=['GET'])
def list_models():
    """List Ollama models"""
    if not ollama.is_available():
        return jsonify({"error": "Ollama not available"}), 503
    
    models = ollama.list_models()
    return jsonify({"models": models})


if __name__ == '__main__':
    print("=" * 60)
    print("  NexusAI Simple Edition")
    print("=" * 60)
    print()
    
    if ollama.is_available():
        models = ollama.list_models()
        print(f"✓ Ollama RUNNING")
        print(f"  Models: {', '.join(models)}")
    else:
        print("✗ WARNING: Ollama NOT running!")
        print("  Start with: ollama serve")
    
    print("\n" + "=" * 60)
    print("Starting Simple API server...")
    print("API: http://localhost:5000")
    print("Test: http://localhost:5000/api/status")
    print("\nPress CTRL+C to stop")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

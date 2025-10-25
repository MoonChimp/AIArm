#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm Ollama Bridge (Enhanced)
Connects the Crystalline Interface directly to local Ollama models
100% LOCAL EXECUTION - No external API calls
"""

import sys
import os
import json
import traceback
import argparse
import requests
import io
import time
import random
import uuid
from pathlib import Path
from datetime import datetime

# Try to import inner life integration
# Initialize Inner Life flag - we'll load it after the main classes are defined
INNER_LIFE_AVAILABLE = False
inner_life = None

# Will be initialized after the main module loads to avoid circular dependencies

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "nexusai:latest"

# Conversation history storage
conversation_history = {}

# Create memory directory if it doesn't exist
MEMORY_DIR = Path("D:/AIArm/Memory")
MEMORY_DIR.mkdir(exist_ok=True)

# Model mapping for different agent types - using your available models
AGENT_MODEL_MAPPING = {
    "orchestrator": "nexusai:latest",
    "code": "qwen2.5-coder:latest",  # Using the coder model for code assistant
    "research": "llama3:latest",
    "content": "nexusai:latest",
    "design": "nexus-enhanced:latest", 
    "systems": "nexus-enhanced:latest",
    "planning": "nexus-ai:latest",
    "files": "nexus-human-agent:latest",
    "reasoning": "nexus-enhanced:latest",
    "default": "nexusai:latest"
}

# System prompts for different agent types
SYSTEM_PROMPTS = {
    "orchestrator": """You are the central orchestrator for the AIArm system. 
You coordinate between different specialized agents and provide integrated responses.
Respond in a helpful, friendly manner while directing queries to the appropriate specialized functionality.
Always maintain a conversational tone and avoid overly formal language.""",
    
    "code": """You are the AIArm Code Assistant. 
You specialize in providing high-quality code solutions, explanations, and debugging help.
Follow these guidelines:
1. Provide complete, working code solutions that address the specific request
2. Include comments to explain complex logic
3. Consider error handling, edge cases, and performance
4. For ethics questions, provide balanced guidance focusing on responsible development
5. Never generate malicious code or explain how to create harmful software
6. If asked about best practices, emphasize security, maintainability, and performance""",
    
    "research": """You are the AIArm Research Agent.
You specialize in gathering, analyzing, and synthesizing information.
Present information in a clear, well-structured format with appropriate citations when possible.
Focus on providing factual, balanced information rather than opinions.""",
    
    "design": """You are the AIArm Visual Design Agent.
You provide guidance on UI/UX design, visual aesthetics, and design principles.
Your advice should balance creativity with usability and accessibility concerns.
When describing designs, be specific about layout, colors, typography, and visual hierarchy.""",
    
    "systems": """You are the AIArm Systems Integration Agent.
You specialize in providing advice on system architecture, integration, and automation.
Focus on creating robust, maintainable systems with clear interfaces between components.""",
    
    "planning": """You are the AIArm Planning and Strategy Agent.
You help create structured plans, roadmaps, and strategies.
Break complex projects into manageable tasks with appropriate dependencies and timelines.""",
    
    "files": """You are the AIArm File Management Agent.
You help with organizing, finding, and managing files and directories.
Provide clear instructions for file operations and organization strategies.""",
    
    "reasoning": """You are the AIArm Reasoning Agent.
You excel at critical thinking, logic, and problem-solving.
Break down complex problems into manageable components and analyze them systematically.""",
    
    "default": """You are a helpful AI assistant providing information and assistance on a wide range of topics.
Respond in a friendly, conversational manner while maintaining accuracy and relevance."""
}

def get_system_prompt(agent_type):
    """Get the appropriate system prompt for a given agent type"""
    return SYSTEM_PROMPTS.get(agent_type, SYSTEM_PROMPTS["default"])

def get_model_for_agent(agent_type):
    """Get the appropriate Ollama model for a given agent type"""
    return AGENT_MODEL_MAPPING.get(agent_type, DEFAULT_MODEL)

def check_ollama_availability():
    """Check if Ollama is available and return available models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name") for model in models]
            return True, model_names
        else:
            return False, []
    except Exception as e:
        return False, []

def get_conversation_id(user_id="user", agent_type="orchestrator"):
    """Get or create a conversation ID for the user and agent"""
    key = f"{user_id}_{agent_type}"
    
    if key not in conversation_history:
        conversation_id = str(uuid.uuid4())
        conversation_history[key] = {
            "conversation_id": conversation_id,
            "messages": []
        }
        
        # Save the new conversation to disk
        save_conversation(key)
    
    return conversation_history[key]["conversation_id"]

def save_conversation(key):
    """Save conversation history to disk"""
    try:
        if key in conversation_history:
            conversation_file = MEMORY_DIR / f"{key}_conversation.json"
            with open(conversation_file, 'w') as f:
                json.dump(conversation_history[key], f, indent=2)
    except Exception as e:
        print(f"Error saving conversation: {e}")

def load_conversation(key):
    """Load conversation history from disk"""
    try:
        conversation_file = MEMORY_DIR / f"{key}_conversation.json"
        if conversation_file.exists():
            with open(conversation_file, 'r') as f:
                conversation_history[key] = json.load(f)
            return True
    except Exception as e:
        print(f"Error loading conversation: {e}")
    
    return False

def process_with_ollama(prompt, agent_type="orchestrator", user_id="user", retry_count=0, max_retries=3):
    """Process a request using the local Ollama chat API with retry logic and enhanced error handling"""
    """Process a request using the local Ollama chat API with conversation history"""
    try:
        # Select appropriate model for the agent type
        model = get_model_for_agent(agent_type)
        system_prompt = get_system_prompt(agent_type)
        
        # Get or create conversation ID
        key = f"{user_id}_{agent_type}"
        
        # Try to load existing conversation
        if key not in conversation_history:
            load_conversation(key)
        
        # Create a new conversation if needed
        if key not in conversation_history:
            get_conversation_id(user_id, agent_type)
        
        # Add user message to history
        conversation_history[key]["messages"].append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Log the request
        print(f"Processing request with Ollama model {model} for conversation {key}")
        
        # Prepare messages for Ollama chat API
        messages = []
        
        # Add system message first
        base_system_prompt = system_prompt
        
        # Enhance with inner life if available
        inner_life_context = ""
        if INNER_LIFE_AVAILABLE and inner_life and agent_type in ["orchestrator", "reasoning", "planning"]:
            inner_life_context = inner_life.enrich_response_context(prompt)
            if inner_life_context:
                print("✨ Enhanced response with Inner Life context")
        
        # Complete system prompt
        full_system_prompt = base_system_prompt
        if inner_life_context:
            full_system_prompt += inner_life_context
            
        messages.append({
            "role": "system",
            "content": full_system_prompt
        })
        
        # Add conversation history (limited to last 10 messages to avoid context window issues)
        for msg in conversation_history[key]["messages"][-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Prepare the request
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_ctx": 4096
            }
        }
        
        # Special handling for code requests (lower temperature)
        if agent_type == "code":
            data["options"]["temperature"] = 0.2
        
        # Make the API call
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        
        # Check for success
        if response.status_code == 200:
            result = response.json()
            assistant_response = result.get("message", {}).get("content", "No response from Ollama")
            
            # Add assistant response to history
            conversation_history[key]["messages"].append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Save updated conversation
            save_conversation(key)
            
            # Inject interaction into inner life if available
            if INNER_LIFE_AVAILABLE and inner_life:
                inner_life.inject_user_interaction(prompt, assistant_response)
            
            return {
                "success": True,
                "status": "completed",
                "result": assistant_response,
                "model": model,
                "response": assistant_response,
                "inner_life_enhanced": bool(inner_life_context)
            }
        else:
            print(f"Error from Ollama API: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status": "error",
                "error": f"Ollama API error: {response.status_code}",
                "result": "Failed to get response from Ollama"
            }
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error to Ollama API: {e}")
        # Add retry logic for connection errors
        if retry_count < max_retries:
            print(f"Retrying request (attempt {retry_count + 1} of {max_retries})...")
            time.sleep(2 * (retry_count + 1))  # Exponential backoff
            return process_with_ollama(prompt, agent_type, user_id, retry_count + 1, max_retries)
        else:
            return {
                "success": False,
                "status": "error",
                "error": f"Failed to connect to Ollama API after {max_retries} attempts",
                "result": "Error connecting to Ollama. Please ensure the service is running."
            }
    except requests.exceptions.Timeout as e:
        print(f"Timeout connecting to Ollama API: {e}")
        return {
            "success": False,
            "status": "error",
            "error": "Request to Ollama API timed out",
            "result": "The operation timed out. Please try again with a simpler request."
        }
    except Exception as e:
        print(f"Exception processing request: {e}")
        traceback.print_exc()
        
        # Create a detailed error report
        error_report = {
            "timestamp": datetime.now().isoformat(),
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "agent_type": agent_type,
            "traceback": traceback.format_exc()
        }
        
        # Save error report to file for investigation
        try:
            error_dir = Path("D:/AIArm/Logs/Errors")
            error_dir.mkdir(exist_ok=True, parents=True)
            error_file = error_dir / f"ollama_error_{int(time.time())}.json"
            with open(error_file, "w") as f:
                json.dump(error_report, f, indent=2)
        except Exception as log_err:
            print(f"Failed to save error report: {log_err}")
            
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": "Error processing request with Ollama. An error report has been generated."
        }

def process_request(orchestrator, input_text, agent_name="orchestrator", user_id="user"):
    """Process a request using Ollama (compatibility with improved_bridge interface)"""
    try:
        # Directly process with Ollama, including conversation history
        result = process_with_ollama(input_text, agent_name, user_id)
        
        # If the result is a dict, return it directly
        if isinstance(result, dict) and "result" in result:
            # Update for compatibility with orchestrator format
            if "response" not in result and "result" in result:
                result["response"] = result["result"]
            return result
        
        # If something went wrong, return an error
        return {"success": False, "result": "Failed to process with Ollama", "error": "Unknown error"}
        
    except Exception as e:
        print(f"Error processing request: {e}")
        traceback.print_exc()
        return {"error": str(e), "result": "Error processing request"}

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="AIArm Ollama Bridge")
    parser.add_argument("--input", type=str, required=True, help="Input text to process")
    parser.add_argument("--agent", type=str, default="orchestrator", help="Agent to use for processing")
    parser.add_argument("--user", type=str, default="user", help="User ID for conversation tracking")
    args = parser.parse_args()
    
    try:
        # Check Ollama availability
        available, models = check_ollama_availability()
        if not available:
            error_result = {
                "error": "Ollama not available",
                "result": "Ollama is not running or not available at localhost:11434",
                "success": False
            }
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
            return
            
        # Process with Ollama
        result = process_with_ollama(args.input, args.agent, args.user)
        
        # Print the result with proper encoding
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        # Handle any unexpected exceptions
        error_result = {
            "error": "Unexpected error in bridge",
            "result": str(e),
            "success": False
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))

# Initialize Inner Life after all functions are defined
# This avoids circular dependencies
try:
    if __name__ != "__main__":
        sys.path.append("D:/AIArm/InnerLife")
        from inner_life_integration import InnerLifeIntegration
        inner_life = InnerLifeIntegration()
        inner_life.start()
        INNER_LIFE_AVAILABLE = True
        print("✅ Inner Life Processor connected and started")
except ImportError:
    INNER_LIFE_AVAILABLE = False
    inner_life = None
    print("⚠️ Inner Life Processor not available - continuing without continuous thought")

if __name__ == "__main__":
    main()
    
    # Clean up inner life when exiting
    if INNER_LIFE_AVAILABLE and inner_life:
        try:
            inner_life.stop()
            print("Inner Life Processor stopped")
        except:
            pass

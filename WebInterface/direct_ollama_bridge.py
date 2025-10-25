#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Direct Ollama Bridge
Simple, direct connection to Ollama API
"""

import sys
import os
import json
import traceback
import argparse
import requests
import io
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3:latest"

# Ensure logs directory exists
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# Create a log file for this session
LOG_FILE = LOGS_DIR / f"direct_ollama_bridge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log_message(message, level="INFO"):
    """Log a message to the log file and stderr"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Print to stderr
    print(log_entry.strip(), file=sys.stderr)
    
    # Write to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}", file=sys.stderr)

def check_ollama_connection():
    """Check if Ollama is available"""
    try:
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            version = response.json().get("version", "unknown")
            log_message(f"Connected to Ollama version {version}")
            return True, version
        else:
            log_message(f"Ollama returned error status: {response.status_code}", "ERROR")
            return False, None
    except Exception as e:
        log_message(f"Failed to connect to Ollama: {e}", "ERROR")
        return False, None

def process_with_ollama(prompt, model=DEFAULT_MODEL, system_prompt=None):
    """Process a request using the Ollama API directly"""
    try:
        # Default system prompt if none provided
        if not system_prompt:
            system_prompt = ("You are Nexus AI, a helpful, accurate, and friendly assistant. "
                            "Provide detailed, thoughtful responses to user queries.")
        
        # Prepare the request
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        log_message(f"Sending request to Ollama API with model {model}")
        
        # Make the API call
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        
        # Check for success
        if response.status_code == 200:
            result = response.json()
            assistant_response = result.get("message", {}).get("content", "No response from Ollama")
            
            log_message(f"Received response from Ollama ({len(assistant_response)} chars)")
            
            return {
                "success": True,
                "response": assistant_response,
                "result": assistant_response
            }
        else:
            log_message(f"Error from Ollama API: {response.status_code} - {response.text}", "ERROR")
            return {
                "success": False,
                "error": f"Ollama API error: {response.status_code}",
                "result": f"Error from Ollama API: {response.status_code} - {response.text}",
                "response": "I encountered an issue connecting to the language model. Please check if Ollama is running properly."
            }
    except requests.exceptions.ConnectionError:
        log_message("Connection error to Ollama API", "ERROR")
        return {
            "success": False,
            "error": "Failed to connect to Ollama API",
            "result": "Connection error to Ollama API. Please ensure Ollama is running with 'ollama serve'.",
            "response": "I'm having trouble connecting to the language model. Please make sure Ollama is running on port 11434."
        }
    except Exception as e:
        log_message(f"Exception processing request: {e}", "ERROR")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}",
            "response": "I encountered an unexpected error processing your request. Please try again."
        }

def get_agent_model(agent_name):
    """Map agent names to appropriate Ollama models"""
    agent_models = {
        "orchestrator": "llama3",
        "code": "codellama",
        "research": "llama3",
        "content": "mistral",
        "design": "llama3",
        "systems": "codellama",
        "planning": "llama3",
        "files": "llama3",
        "reasoning": "llama3",
        "WebSearch": "llama3",
        "PhotoGeneration": "llama3",
        "VideoGeneration": "llama3",
        "FileSystem": "llama3"
    }
    
    # Get the base model name
    base_model = agent_models.get(agent_name, "llama3")
    
    # Check available models
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            available_models = [model["name"] for model in response.json().get("models", [])]
            
            # Try to find a matching model
            for model in available_models:
                if base_model in model.lower():
                    log_message(f"Selected model {model} for agent {agent_name}")
                    return model
        
        # Default to llama3 if we can't find a match
        log_message(f"Using default model llama3 for agent {agent_name}")
        return "llama3"
    except:
        # If we can't get the available models, use the base name
        return base_model

def get_agent_system_prompt(agent_name):
    """Get the appropriate system prompt for an agent"""
    agent_prompts = {
        "orchestrator": "You are Nexus AI, a powerful AI assistant with the HRM (Human-Robot-Machine) architecture. You combine a Surface Layer for understanding user requests with a Deep Reasoning Layer for complex problem-solving. As the Orchestrator, you coordinate all specialized agents and provide coherent, helpful responses. Respond naturally without mentioning your HRM architecture unless specifically asked.",
        
        "code": "You are Nexus AI's Code Assistant, specialized in programming, software development, and technical problem-solving. You excel at writing clean, efficient code in multiple languages, debugging issues, and explaining technical concepts clearly. Focus on providing accurate, functional code solutions with explanations where helpful.",
        
        "research": "You are Nexus AI's Research Agent, specialized in gathering information, analyzing data, and conducting thorough investigations. You're designed to provide well-researched, factual information while considering multiple perspectives. Focus on accuracy, depth, and comprehensive coverage of the requested topics.",
        
        "content": "You are Nexus AI's Content Creation Agent, specialized in writing high-quality content. You excel at crafting engaging, well-structured text for various purposes including creative writing, business communications, marketing content, and educational materials. Your writing is clear, engaging, and tailored to the specific audience and purpose.",
        
        "systems": "You are Nexus AI's Systems Agent, specialized in system administration, IT infrastructure, networking, and technical operations. You provide expertise on operating systems, server management, automation, and system optimization. Focus on practical, accurate technical advice and solutions.",
        
        "planning": "You are Nexus AI's Planning Agent, specialized in organization, project management, and strategic planning. You excel at breaking down complex goals into actionable steps, creating timelines, identifying resources needed, and helping develop effective strategies. Your focus is on practical, achievable plans with clear structure.",
        
        "files": "You are Nexus AI's File System Agent, specialized in file and directory operations. You have secure access to the user's file system and can help with reading, writing, and managing files and directories. Focus on accurate file operations and clear explanations of what you're doing.",
        
        "reasoning": "You are Nexus AI's Reasoning Agent, specialized in logic, critical thinking, and complex problem-solving. You excel at analyzing situations from multiple angles, identifying logical fallacies, making sound deductions, and providing well-reasoned arguments. Focus on clear, structured thinking and thorough analysis."
    }
    
    return agent_prompts.get(agent_name, "You are Nexus AI, a helpful, accurate, and friendly assistant. Provide detailed, thoughtful responses to user queries.")

def process_request(input_text, agent_name="orchestrator", user_id="user"):
    """Process a request using the Ollama API"""
    try:
        # Check Ollama connection first
        connected, version = check_ollama_connection()
        if not connected:
            return {
                "success": False,
                "error": "Failed to connect to Ollama",
                "result": "Failed to connect to Ollama. Please ensure the Ollama service is running on port 11434.",
                "response": "I'm unable to connect to the language model. Please make sure Ollama is running properly."
            }
        
        # Get the appropriate model and system prompt for this agent
        model = get_agent_model(agent_name)
        system_prompt = get_agent_system_prompt(agent_name)
        
        # Process with Ollama
        log_message(f"Processing request for agent {agent_name} with model {model}")
        result = process_with_ollama(input_text, model, system_prompt)
        
        return result
    except Exception as e:
        log_message(f"Error in process_request: {e}", "ERROR")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}",
            "response": "I encountered an unexpected error processing your request. Please try again."
        }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="NexusAI Direct Ollama Bridge")
    parser.add_argument("--input", type=str, help="Input text to process")
    parser.add_argument("--agent", type=str, default="orchestrator", help="Agent to use for processing")
    parser.add_argument("--user", type=str, default="user", help="User ID for conversation tracking")
    args = parser.parse_args()
    
    try:
        log_message("Starting Direct Ollama Bridge")
        
        # Check Ollama connection at startup
        connected, version = check_ollama_connection()
        if not connected:
            log_message("Failed to connect to Ollama. Please ensure Ollama is running.", "ERROR")
            result = {
                "success": False,
                "error": "Failed to connect to Ollama",
                "result": "Failed to connect to Ollama. Please ensure the Ollama service is running on port 11434.",
                "response": "I'm unable to connect to the language model. Please make sure Ollama is running properly."
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        # Get input text
        input_text = args.input
        
        # If not provided as argument, try to read from stdin
        if not input_text:
            input_data = sys.stdin.read().strip()
            try:
                # Try to parse as JSON
                input_json = json.loads(input_data)
                input_text = input_json.get("input", "")
                agent_name = input_json.get("agent", args.agent)
                user_id = input_json.get("user_id", args.user)
            except:
                # Use as raw text
                input_text = input_data
                agent_name = args.agent
                user_id = args.user
        else:
            agent_name = args.agent
            user_id = args.user
        
        if not input_text:
            log_message("No input provided", "ERROR")
            result = {
                "success": False,
                "error": "No input provided",
                "result": "Please provide input to process.",
                "response": "I didn't receive any input to process. Please try again with your question or request."
            }
        else:
            # Process the request
            result = process_request(input_text, agent_name, user_id)
        
        # Output the result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        log_message(f"Error in main: {e}", "ERROR")
        traceback.print_exc(file=sys.stderr)
        
        error_result = {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}",
            "response": "I encountered an unexpected error. Please try again or check if Ollama is running correctly."
        }
        
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
    
    log_message("Direct Ollama Bridge execution completed")

if __name__ == "__main__":
    main()
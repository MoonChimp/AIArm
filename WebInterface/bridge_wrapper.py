#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm Direct Bridge Wrapper
Provides a direct connection to Ollama without the complexity of the full bridge system
"""

import sys
import os
import json
import traceback
import argparse
import requests
import io
import time
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3:latest"  # Using a common model as default

def log(message):
    """Log a message to stderr"""
    print(f"[LOG] {message}", file=sys.stderr)

def process_with_ollama(prompt, model=DEFAULT_MODEL):
    """Process a request using the Ollama API directly"""
    try:
        # Prepare the request
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that provides detailed, accurate responses."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        # Make the API call
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        
        # Check for success
        if response.status_code == 200:
            result = response.json()
            assistant_response = result.get("message", {}).get("content", "No response from Ollama")
            
            return {
                "success": True,
                "response": assistant_response,
                "result": assistant_response
            }
        else:
            log(f"Error from Ollama API: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"Ollama API error: {response.status_code}",
                "result": "Failed to get response from Ollama. Please make sure Ollama is running."
            }
    except requests.exceptions.ConnectionError:
        log("Connection error to Ollama API")
        return {
            "success": False,
            "error": "Failed to connect to Ollama API",
            "result": "Error connecting to Ollama. Please ensure the Ollama service is running on port 11434."
        }
    except Exception as e:
        log(f"Exception processing request: {e}")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}"
        }

def process_request(_, input_text, agent_name="default", user_id="user"):
    """Process a request (interface matching other bridges)"""
    try:
        # Select model based on agent type
        model = DEFAULT_MODEL
        if agent_name == "code":
            model = "qwen2.5-coder:latest"
        elif agent_name == "file_system" or agent_name == "files":
            model = "llama3:latest"
        
        # Process directly with Ollama
        result = process_with_ollama(input_text, model)
        return result
    except Exception as e:
        log(f"Error in process_request: {e}")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}"
        }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="AIArm Direct Bridge Wrapper")
    parser.add_argument("--input", type=str, help="Input text to process")
    parser.add_argument("--agent", type=str, default="default", help="Agent to use for processing")
    parser.add_argument("--user", type=str, default="user", help="User ID for conversation tracking")
    args = parser.parse_args()
    
    try:
        # Get input text
        input_text = args.input or sys.stdin.read()
        
        if not input_text:
            result = {
                "success": False,
                "error": "No input provided",
                "result": "Please provide input to process."
            }
        else:
            # Process the request
            result = process_request(None, input_text, args.agent, args.user)
        
        # Output the result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        log(f"Error in main: {e}")
        traceback.print_exc(file=sys.stderr)
        
        error_result = {
            "success": False,
            "error": str(e),
            "result": f"Error processing request: {str(e)}"
        }
        
        print(json.dumps(error_result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm Improved Bridge (Enhanced for HRM Surface Layer)
Connects the Crystalline Interface to the orchestrator and specialized agents
Provides structured surface layer for the HRM architecture
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
import concurrent.futures

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add the WebInterface directory to path to import enhanced_orchestrator
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(SCRIPT_DIR))

# Import the enhanced orchestrator
try:
    # Add base directory to path
    sys.path.append(str(Path("D:/AIArm/WebInterface")))
    from enhanced_orchestrator import EnhancedOrchestrator, ThoughtStream
    ORCHESTRATOR_AVAILABLE = True
    # Initialize the orchestrator
    orchestrator = EnhancedOrchestrator()
    thought_stream = ThoughtStream()
    print("✅ Enhanced Orchestrator initialized")
except ImportError as e:
    print(f"⚠️ Enhanced Orchestrator not available: {e}")
    ORCHESTRATOR_AVAILABLE = False
    orchestrator = None
    thought_stream = None

# Configuration
MEMORY_DIR = Path("D:/AIArm/Memory")
MEMORY_DIR.mkdir(exist_ok=True)
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True)

# Create a log file for this session
LOG_FILE = LOGS_DIR / f"improved_bridge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log_message(message, level="INFO"):
    """Log a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Print to console
    print(log_entry.strip())
    
    # Write to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def get_conversation_id(user_id="user", agent_type="orchestrator"):
    """Get or create a conversation ID for the user and agent"""
    key = f"{user_id}_{agent_type}"
    
    # Load or create conversation file
    conversation_file = MEMORY_DIR / f"{key}_conversation.json"
    
    if conversation_file.exists():
        try:
            with open(conversation_file, "r", encoding="utf-8") as f:
                conversation_data = json.load(f)
            return conversation_data.get("conversation_id", str(uuid.uuid4()))
        except Exception as e:
            log_message(f"Error loading conversation: {e}", "ERROR")
    
    # Create new conversation ID
    conversation_id = str(uuid.uuid4())
    
    # Save to file
    try:
        with open(conversation_file, "w", encoding="utf-8") as f:
            json.dump({"conversation_id": conversation_id, "messages": []}, f, indent=2)
    except Exception as e:
        log_message(f"Error saving conversation: {e}", "ERROR")
    
    return conversation_id

def load_conversation_history(user_id="user", agent_type="orchestrator", max_messages=10):
    """Load conversation history for a user/agent pair"""
    key = f"{user_id}_{agent_type}"
    conversation_file = MEMORY_DIR / f"{key}_conversation.json"
    
    if conversation_file.exists():
        try:
            with open(conversation_file, "r", encoding="utf-8") as f:
                conversation_data = json.load(f)
            return conversation_data.get("messages", [])[-max_messages:]
        except Exception as e:
            log_message(f"Error loading conversation history: {e}", "ERROR")
    
    return []

def save_conversation_message(user_id, agent_type, role, content):
    """Save a message to the conversation history"""
    key = f"{user_id}_{agent_type}"
    conversation_file = MEMORY_DIR / f"{key}_conversation.json"
    
    try:
        # Load existing data
        if conversation_file.exists():
            with open(conversation_file, "r", encoding="utf-8") as f:
                conversation_data = json.load(f)
        else:
            conversation_id = get_conversation_id(user_id, agent_type)
            conversation_data = {"conversation_id": conversation_id, "messages": []}
        
        # Add new message
        conversation_data["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save updated data
        with open(conversation_file, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
        return True
    except Exception as e:
        log_message(f"Error saving conversation message: {e}", "ERROR")
        return False

def process_with_orchestrator(prompt, agent_type="orchestrator", user_id="user", conversation_id=None):
    """Process a request using the enhanced orchestrator"""
    try:
        log_message(f"Processing request with orchestrator for agent: {agent_type}, user: {user_id}")
        
        # Get the conversation ID if not provided
        if not conversation_id:
            conversation_id = get_conversation_id(user_id, agent_type)
            
        # Get the conversation history
        conversation_history = load_conversation_history(user_id, agent_type)
        
        # Add the user message to conversation history
        save_conversation_message(user_id, agent_type, "user", prompt)
        
        # Generate a thought ID for tracking
        thought_id = f"thought_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Process the request with the orchestrator
        if ORCHESTRATOR_AVAILABLE and orchestrator:
            response = orchestrator.process_message({
                "type": "user_request",
                "content": prompt,
                "agent": agent_type,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "thought_id": thought_id,
                "history": conversation_history
            })
            
            # Add the response to conversation history
            if response and isinstance(response, dict) and "response" in response:
                save_conversation_message(user_id, agent_type, "assistant", response["response"])
                
                # Add structured result fields
                response["success"] = True
                response["status"] = "completed"
                response["result"] = response.get("response", "")
                response["thought_id"] = thought_id
                response["conversation_id"] = conversation_id
                
                # Add to thought stream for future context
                if thought_stream:
                    thought_stream.add_thought(
                        content=prompt,
                        response=response["response"],
                        agent=agent_type,
                        user_id=user_id,
                        thought_id=thought_id
                    )
                
                return response
            else:
                # Handle unexpected response format
                error_msg = "Unexpected response format from orchestrator"
                log_message(error_msg, "ERROR")
                return {
                    "success": False,
                    "status": "error",
                    "error": error_msg,
                    "result": "I apologize, but I encountered an unexpected issue processing your request."
                }
        else:
            # Orchestrator not available
            error_msg = "Enhanced Orchestrator not available"
            log_message(error_msg, "ERROR")
            return {
                "success": False,
                "status": "error",
                "error": error_msg,
                "result": "I apologize, but the orchestrator is currently unavailable. Please try again later."
            }
            
    except Exception as e:
        log_message(f"Exception in process_with_orchestrator: {e}", "ERROR")
        traceback.print_exc()
        
        # Save error report for investigation
        try:
            error_dir = LOGS_DIR / "Errors"
            error_dir.mkdir(exist_ok=True)
            
            error_report = {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "prompt": prompt,
                "agent_type": agent_type,
                "user_id": user_id
            }
            
            error_file = error_dir / f"orchestrator_error_{int(time.time())}.json"
            with open(error_file, "w", encoding="utf-8") as f:
                json.dump(error_report, f, indent=2)
                
            log_message(f"Error report saved to {error_file}", "ERROR")
        except Exception as e2:
            log_message(f"Failed to save error report: {e2}", "ERROR")
        
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": "I apologize, but I encountered an issue processing your request. Please try again."
        }

def process_request(orchestrator, input_text, agent_name="orchestrator", user_id="user"):
    """Process a request using the orchestrator (compatibility with server interface)"""
    log_message(f"Processing request for agent: {agent_name}, user: {user_id}")
    
    try:
        # For compatibility with the server interface
        result = process_with_orchestrator(input_text, agent_name, user_id)
        
        if result and isinstance(result, dict) and "result" in result:
            # Ensure all required fields are present
            if "success" not in result:
                result["success"] = True
            if "status" not in result:
                result["status"] = "completed"
                
            return result
        
        # Handle unexpected result format
        return {
            "success": False,
            "status": "error",
            "error": "Unexpected result format",
            "result": "I apologize, but I encountered an unexpected issue processing your request."
        }
    except Exception as e:
        log_message(f"Error in process_request: {e}", "ERROR")
        traceback.print_exc()
        
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": "I apologize, but I encountered an issue processing your request. Please try again."
        }

def format_response(response):
    """Format the response for output"""
    if isinstance(response, dict):
        return json.dumps(response, indent=2, ensure_ascii=False)
    return str(response)

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="AIArm Improved Bridge")
    parser.add_argument("--input", type=str, help="Input text to process")
    parser.add_argument("--agent", type=str, default="orchestrator", help="Agent to use for processing")
    parser.add_argument("--user", type=str, default="user", help="User ID for conversation tracking")
    parser.add_argument("--json", action="store_true", help="Indicate that input is provided as JSON")
    args = parser.parse_args()
    
    try:
        # Check if input is provided via command-line arguments
        input_text = args.input
        
        # If not, check for input from stdin
        if not input_text:
            input_data = sys.stdin.read()
            try:
                # Try to parse as JSON
                input_json = json.loads(input_data)
                input_text = input_json.get("input", "")
                agent_name = input_json.get("agent", args.agent)
                user_id = input_json.get("user_id", args.user)
            except json.JSONDecodeError:
                # Use raw input as text
                input_text = input_data
                agent_name = args.agent
                user_id = args.user
        else:
            # Check if we should process the input as JSON (when --json flag is used)
            if args.json and input_text:
                try:
                    input_json = json.loads(input_text)
                    input_text = input_json.get("input", input_text)
                    agent_name = input_json.get("agent", args.agent)
                    user_id = input_json.get("user_id", args.user)
                except json.JSONDecodeError:
                    # If JSON parsing fails, use as-is
                    agent_name = args.agent
                    user_id = args.user
            else:
                agent_name = args.agent
                user_id = args.user
        
        # Process the request
        if not input_text:
            result = {
                "success": False,
                "status": "error",
                "error": "No input provided",
                "result": "Please provide input to process."
            }
        else:
            # Use the orchestrator to process the request
            result = process_request(orchestrator, input_text, agent_name, user_id)
        
        # Format and output the result
        print(format_response(result))
        
    except Exception as e:
        log_message(f"Error in main: {e}", "ERROR")
        traceback.print_exc()
        
        error_result = {
            "success": False,
            "status": "error",
            "error": str(e),
            "result": "I apologize, but I encountered an unexpected issue. Please try again."
        }
        
        print(format_response(error_result))

if __name__ == "__main__":
    # Log startup
    log_message("Improved Bridge starting")
    main()
    log_message("Improved Bridge execution completed")

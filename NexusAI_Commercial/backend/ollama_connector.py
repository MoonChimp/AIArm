#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ollama Connector for NexusAI Commercial
Connects to local Ollama instance for LLM inference
"""

import requests
import json
from typing import Dict, List, Optional, Generator

class OllamaConnector:
    """
    Connector for local Ollama LLM
    Handles all communication with Ollama API
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.api_url}/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            print(f"[OllamaConnector] Error listing models: {e}")
            return []
    
    def chat(
        self,
        message: str,
        model: str = "llama2",
        system_prompt: Optional[str] = None,
        temperature: float = 0.8,
        max_tokens: int = 2000
    ) -> Dict:
        """
        Send chat message to Ollama
        
        Args:
            message: User message
            model: Model name (default: llama2)
            system_prompt: System prompt for personality
            temperature: Response randomness (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Dict with response and metadata
        """
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call Ollama API
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data.get("message", {}).get("content", ""),
                    "model": model,
                    "done": data.get("done", False)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": ""
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }
    
    def chat_stream(
        self,
        message: str,
        model: str = "llama2",
        system_prompt: Optional[str] = None,
        temperature: float = 0.8
    ) -> Generator[str, None, None]:
        """
        Stream chat response from Ollama
        Yields response tokens as they arrive
        """
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Stream from Ollama
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature
                    }
                },
                stream=True,
                timeout=120
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            yield f"\n[Error: {str(e)}]"
    
    def generate(
        self,
        prompt: str,
        model: str = "llama2",
        temperature: float = 0.8,
        max_tokens: int = 2000
    ) -> Dict:
        """
        Simple text generation (non-chat format)
        """
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data.get("response", ""),
                    "model": model
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": ""
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }
    
    def get_model_info(self, model: str) -> Optional[Dict]:
        """Get information about a specific model"""
        try:
            response = requests.post(
                f"{self.api_url}/show",
                json={"name": model}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"[OllamaConnector] Error getting model info: {e}")
            return None


if __name__ == "__main__":
    # Test Ollama connection
    print("Testing Ollama Connector...")
    
    connector = OllamaConnector()
    
    # Check availability
    if connector.is_available():
        print("✓ Ollama is running!")
        
        # List models
        models = connector.list_models()
        print(f"✓ Available models: {models}")
        
        # Test chat
        if models:
            print(f"\nTesting chat with {models[0]}...")
            result = connector.chat(
                message="Hello! Tell me about yourself in one sentence.",
                model=models[0]
            )
            if result['success']:
                print(f"✓ Response: {result['response']}")
            else:
                print(f"✗ Error: {result.get('error')}")
    else:
        print("✗ Ollama is not running!")
        print("Start Ollama with: ollama serve")

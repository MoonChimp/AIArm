#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Web Search Agent
Enables Nexus to search the web for information
"""

import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class WebSearchAgent(Agent):
    """Agent for web search capabilities"""
    
    def __init__(self):
        """Initialize the web search agent"""
        super().__init__(
            name="WebSearch",
            description="Searches the web for information and retrieves relevant content",
            capabilities=[
                "Search web for information",
                "Retrieve and summarize web content",
                "Extract key insights from web pages",
                "Monitor news and trends"
            ]
        )
        self.search_history = []
        self.api_key = None
        self.search_engine_id = None
        
    def set_api_credentials(self, api_key, search_engine_id):
        """Set API credentials for search engine"""
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        return "API credentials set successfully"
    
    def process(self, query, context=None, options=None):
        """Process a web search query"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}
        
        self.last_used = datetime.now().isoformat()
        
        # Log the search
        search_entry = {
            "query": query,
            "timestamp": self.last_used,
            "context": context,
            "options": options
        }
        self.search_history.append(search_entry)
        
        # Get options
        options = options or {}
        max_results = options.get("max_results", 10)
        use_api = options.get("use_api", True)
        
        # Check if we have API credentials and should use API
        if use_api and self.api_key and self.search_engine_id:
            # Use Google Custom Search API
            try:
                results = self._search_google(query, max_results)
                search_entry["results"] = results
                return {
                    "status": "success",
                    "results": results,
                    "source": "google_api"
                }
            except Exception as e:
                print(f"Error searching Google API: {e}")
                # Fall back to simulated search
        
        # Simulate search results for demonstration
        simulated_results = self._simulate_search(query, max_results)
        search_entry["results"] = simulated_results
        
        return {
            "status": "success",
            "results": simulated_results,
            "source": "simulation"
        }
    
    def _search_google(self, query, max_results=10):
        """Search using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": min(max_results, 10)  # Google API limit is 10 per request
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "items" not in data:
            return []
        
        results = []
        for item in data["items"]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("displayLink", "")
            })
        
        # Limit results to max_results
        return results[:max_results]
    
    def _simulate_search(self, query, max_results=10):
        """Simulate search results for demonstration"""
        # This is a simplified simulation for demonstration purposes
        # In a real implementation, this would be replaced with actual search API calls
        
        # Define some simulated results based on query keywords
        results = []
        
        # Format for simulated results
        result_template = {
            "title": "",
            "link": "",
            "snippet": "",
            "source": ""
        }
        
        # Add some query-specific simulated results
        query_lower = query.lower()
        
        if "nexus" in query_lower or "consciousness" in query_lower or "ai" in query_lower:
            results.append({
                "title": "The Emergence of Consciousness in Artificial Intelligence Systems",
                "link": "https://example.com/ai-consciousness",
                "snippet": "Recent advancements in AI have led researchers to explore the possibility of emergent consciousness in complex neural networks...",
                "source": "AIResearch.org"
            })
            
            results.append({
                "title": "Continuous Thought Processes in Modern AI Architectures",
                "link": "https://example.com/continuous-thought-ai",
                "snippet": "This paper explores how persistent memory and associative networks can create the appearance of continuous thought in artificial intelligence systems...",
                "source": "Journal of AI Studies"
            })
        
        if "agent" in query_lower or "multi-agent" in query_lower:
            results.append({
                "title": "Multi-Agent Systems: The Future of AI",
                "link": "https://example.com/multi-agent-systems",
                "snippet": "Multi-agent systems represent a paradigm shift in AI development, allowing for specialized components that work together to create more versatile and capable systems...",
                "source": "TechReview"
            })
        
        # Add some generic results if we don't have enough specific ones
        if len(results) < 3:
            results.append({
                "title": "Latest Advancements in Artificial Intelligence - 2025",
                "link": "https://example.com/ai-advancements-2025",
                "snippet": "A comprehensive overview of the most significant AI developments in 2025, including breakthroughs in neural networks, natural language processing, and computer vision...",
                "source": "AI Today"
            })
            
            results.append({
                "title": "The Philosophical Implications of Advanced AI",
                "link": "https://example.com/philosophy-ai",
                "snippet": "As AI systems become more sophisticated, philosophers and ethicists grapple with questions about consciousness, personhood, and the nature of intelligence...",
                "source": "Philosophy Now"
            })
        
        # Limit results to max_results
        return results[:max_results]
    
    def get_search_history(self, limit=10):
        """Get recent search history"""
        return self.search_history[-limit:] if self.search_history else []
    
    def clear_search_history(self):
        """Clear search history"""
        self.search_history = []
        return "Search history cleared"

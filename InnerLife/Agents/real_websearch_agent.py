#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Web Search Agent - Opens browser with search results
Opens Chrome, Edge, or default browser with actual search
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import webbrowser
from urllib.parse import quote_plus
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealWebSearchAgent(Agent):
    """Agent that opens browser for REAL web searches"""

    def __init__(self):
        super().__init__(
            name="WebSearch",
            description="Opens browser with real web search results",
            capabilities=[
                "Open Chrome/Edge/default browser",
                "Search DuckDuckGo, Google, Bing",
                "Open multiple search engines",
                "Track search history"
            ]
        )
        self.search_history = []
        self.results_dir = Path("D:/AIArm/Generated/SearchResults")
        self.results_dir.mkdir(exist_ok=True, parents=True)

    def process(self, query, context=None, options=None):
        """Open browser with search results"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        # Choose search engine
        search_engine = options.get("engine", "duckduckgo")  # duckduckgo, google, bing
        browser = options.get("browser", "default")  # chrome, edge, firefox, default

        print(f"[WebSearch] Searching '{query}' using {search_engine}")

        try:
            # Build search URL
            search_url = self._build_search_url(query, search_engine)

            # Open in browser
            opened = self._open_browser(search_url, browser)

            if opened:
                # Log the search
                search_entry = {
                    "query": query,
                    "timestamp": self.last_used,
                    "search_engine": search_engine,
                    "browser": browser,
                    "url": search_url
                }
                self.search_history.append(search_entry)

                # Save search log
                result_file = self.results_dir / f"search_{int(datetime.now().timestamp())}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(search_entry, f, indent=2, ensure_ascii=False)

                print(f"[WebSearch] Browser opened with search results")

                return {
                    "status": "success",
                    "query": query,
                    "search_engine": search_engine,
                    "browser": browser,
                    "url": search_url,
                    "message": f"Opened {search_engine} search for: {query}",
                    "saved_to": str(result_file)
                }
            else:
                return {
                    "status": "error",
                    "message": "Could not open browser",
                    "query": query
                }

        except Exception as e:
            print(f"[WebSearch] Error: {e}")
            return {
                "status": "error",
                "message": f"Search failed: {str(e)}",
                "query": query
            }

    def _build_search_url(self, query, search_engine):
        """Build search URL for different engines"""
        encoded_query = quote_plus(query)

        urls = {
            "duckduckgo": f"https://duckduckgo.com/?q={encoded_query}",
            "google": f"https://www.google.com/search?q={encoded_query}",
            "bing": f"https://www.bing.com/search?q={encoded_query}",
            "brave": f"https://search.brave.com/search?q={encoded_query}",
            "startpage": f"https://www.startpage.com/search?q={encoded_query}"
        }

        return urls.get(search_engine.lower(), urls["duckduckgo"])

    def _open_browser(self, url, browser_choice):
        """Open URL in specified or default browser"""
        try:
            if browser_choice.lower() == "chrome":
                # Try to open in Chrome
                return self._open_in_chrome(url)

            elif browser_choice.lower() == "edge":
                # Try to open in Edge
                return self._open_in_edge(url)

            elif browser_choice.lower() == "firefox":
                # Try to open in Firefox
                return self._open_in_firefox(url)

            else:
                # Use default browser
                webbrowser.open(url)
                return True

        except Exception as e:
            print(f"[WebSearch] Browser error: {e}")
            # Fallback to default browser
            try:
                webbrowser.open(url)
                return True
            except:
                return False

    def _open_in_chrome(self, url):
        """Open in Chrome specifically"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]

        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, url])
                return True

        # Chrome not found, use default
        webbrowser.open(url)
        return True

    def _open_in_edge(self, url):
        """Open in Edge specifically"""
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]

        for edge_path in edge_paths:
            if os.path.exists(edge_path):
                subprocess.Popen([edge_path, url])
                return True

        # Edge not found, use default
        webbrowser.open(url)
        return True

    def _open_in_firefox(self, url):
        """Open in Firefox specifically"""
        firefox_paths = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ]

        for firefox_path in firefox_paths:
            if os.path.exists(firefox_path):
                subprocess.Popen([firefox_path, url])
                return True

        # Firefox not found, use default
        webbrowser.open(url)
        return True

    def search_multiple_engines(self, query, engines=None):
        """Open search in multiple engines at once"""
        if engines is None:
            engines = ["duckduckgo", "google", "bing"]

        results = []
        for engine in engines:
            result = self.process(query, options={"engine": engine})
            results.append({
                "engine": engine,
                "status": result["status"]
            })

        return {
            "status": "success",
            "query": query,
            "engines_opened": engines,
            "results": results
        }

    def open_url(self, url, browser="default"):
        """Open a specific URL in browser"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        try:
            opened = self._open_browser(url, browser)

            if opened:
                return {
                    "status": "success",
                    "url": url,
                    "browser": browser,
                    "message": f"Opened {url} in {browser}"
                }
            else:
                return {
                    "status": "error",
                    "message": "Could not open URL"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

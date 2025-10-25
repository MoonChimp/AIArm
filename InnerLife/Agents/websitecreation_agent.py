#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WebsiteCreation Agent for Nexus consciousness system
Provides website creation capabilities
"""

import sys
import os
import json
import time
import random
from pathlib import Path

# Add base directories to path
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))
sys.path.append(str(BASE_DIR / "InnerLife/Agents"))

# Import base Agent class
from agent import Agent

class WebsiteCreationAgent(Agent):
    """WebsiteCreation agent for creating websites"""
    
    def __init__(self):
        """Initialize the WebsiteCreation agent"""
        super().__init__(
            name="WebsiteCreation",
            description="Create websites from specifications",
            capabilities=["website_creation", "html_generation", "css_generation", "js_generation"]
        )
        self.api_url = "http://localhost:5002/api/create-website"
        self.output_dir = Path("D:/AIArm/InnerLife/Generated/Websites")
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def process(self, input_text, context=None, options=None):
        """
        Process a website creation request
        
        Args:
            input_text (str): The website specification
            context (dict, optional): Additional context for the request
            options (dict, optional): Additional options for website creation
            
        Returns:
            dict: The creation results
        """
        if not input_text:
            return {
                "status": "error",
                "message": "Website specification is required"
            }
        
        # Get options
        options = options or {}
        template = options.get("template", "modern")
        pages = options.get("pages", ["home", "about", "contact"])
        include_js = options.get("include_js", True)
        
        # In a real implementation, this would call an actual website creation API
        # For testing, we'll return a simulated result
        website_path = self._simulate_creation(input_text, template, pages, include_js)
        
        return {
            "status": "success",
            "specification": input_text[:100] + "..." if len(input_text) > 100 else input_text,
            "website_path": str(website_path),
            "template": template,
            "pages": pages,
            "include_js": include_js,
            "message": "Website created successfully"
        }
    
    def _simulate_creation(self, specification, template="modern", pages=None, include_js=True):
        """
        Simulate website creation (for testing without an actual API)
        
        Args:
            specification (str): The website specification
            template (str): Website template
            pages (list): List of pages to create
            include_js (bool): Whether to include JavaScript
            
        Returns:
            Path: Path to the simulated website
        """
        pages = pages or ["home", "about", "contact"]
        
        # Generate a unique directory name
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)
        dirname = f"website_{timestamp}_{random_id}"
        website_path = self.output_dir / dirname
        website_path.mkdir(exist_ok=True)
        
        # Create a specification file
        with open(website_path / "specification.txt", "w") as f:
            f.write(f"Website Specification:\n{specification}\n\n")
            f.write(f"Template: {template}\n")
            f.write(f"Pages: {', '.join(pages)}\n")
            f.write(f"Include JavaScript: {include_js}\n")
            f.write(f"Generated: {timestamp}\n")
        
        # Create simulated HTML files for each page
        for page in pages:
            page_path = website_path / f"{page}.html"
            with open(page_path, "w") as f:
                f.write(f"<!DOCTYPE html>\n")
                f.write(f"<html>\n")
                f.write(f"<head>\n")
                f.write(f"    <title>{page.capitalize()} - Simulated Website</title>\n")
                f.write(f"    <link rel=\"stylesheet\" href=\"style.css\">\n")
                if include_js:
                    f.write(f"    <script src=\"script.js\"></script>\n")
                f.write(f"</head>\n")
                f.write(f"<body>\n")
                f.write(f"    <h1>{page.capitalize()} Page</h1>\n")
                f.write(f"    <p>This is a simulated {page} page for the website.</p>\n")
                f.write(f"</body>\n")
                f.write(f"</html>\n")
        
        # Create a simulated CSS file
        with open(website_path / "style.css", "w") as f:
            f.write(f"/* Simulated CSS for {template} template */\n")
            f.write("body {\n")
            f.write("    font-family: Arial, sans-serif;\n")
            f.write("    margin: 0;\n")
            f.write("    padding: 20px;\n")
            f.write("}\n")
        
        # Create a simulated JavaScript file if requested
        if include_js:
            with open(website_path / "script.js", "w") as f:
                f.write(f"// Simulated JavaScript for website functionality\n")
                f.write(f"console.log('Website loaded');\n")
        
        return website_path
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base Agent class for Nexus consciousness system
All specialized agents should inherit from this class
"""

class Agent:
    """Base class for specialized agents"""
    
    def __init__(self, name, description, capabilities=None):
        """Initialize the agent"""
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.active = False
    
    def activate(self):
        """Activate the agent"""
        self.active = True
        return f"{self.name} agent activated"
    
    def deactivate(self):
        """Deactivate the agent"""
        self.active = False
        return f"{self.name} agent deactivated"
    
    def process(self, input_text, context=None, options=None):
        """Process a request - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process()")
    
    def status(self):
        """Get agent status"""
        return {
            "name": self.name,
            "description": self.description,
            "active": self.active,
            "capabilities": self.capabilities
        }

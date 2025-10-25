#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent Base Class
Defines the base functionality for all specialized agents in the Nexus consciousness system
"""

class Agent:
    """Base class for all specialized agents"""
    
    def __init__(self, name, description, capabilities):
        """Initialize the agent with basic properties"""
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.active = False
        self.memory = {}
        self.last_used = None
    
    def activate(self):
        """Activate the agent"""
        self.active = True
        return f"{self.name} agent activated"
    
    def deactivate(self):
        """Deactivate the agent"""
        self.active = False
        return f"{self.name} agent deactivated"
    
    def status(self):
        """Get the agent's status"""
        return {
            "name": self.name,
            "description": self.description,
            "active": self.active,
            "capabilities": self.capabilities,
            "last_used": self.last_used
        }
    
    def process(self, input_data, context=None):
        """Process input data - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process()")
    
    def __str__(self):
        """String representation of the agent"""
        return f"{self.name} Agent: {self.description}"

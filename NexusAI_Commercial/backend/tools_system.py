#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Tool System
Allows AI to use tools like Cline/Claude Code
"""

import json
from typing import Dict, List, Any
from code_executor import CodeExecutor
from file_manager import FileManager

class ToolSystem:
    def __init__(self, working_dir='D:\\AIArm'):
        self.working_dir = working_dir
        self.executor = CodeExecutor(working_dir)
        self.file_manager = FileManager(working_dir)
        self.tools = self._register_tools()
        
    def _register_tools(self) -> Dict[str, Dict]:
        """Register all available tools"""
        return {
            'execute_code': {
                'name': 'execute_code',
                'description': 'Execute Python, Node.js, or shell code',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'string', 'description': 'Code to execute'},
                        'language': {'type': 'string', 'enum': ['python', 'node', 'shell'], 'description': 'Programming language'},
                    },
                    'required': ['code', 'language']
                },
                'function': self._tool_execute_code
            },
            'read_file': {
                'name': 'read_file',
                'description': 'Read contents of a file',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'path': {'type': 'string', 'description': 'File path to read'}
                    },
                    'required': ['path']
                },
                'function': self._tool_read_file
            },
            'write_file': {
                'name': 'write_file',
                'description': 'Write content to a file',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'path': {'type': 'string', 'description': 'File path to write'},
                        'content': {'type': 'string', 'description': 'Content to write'}
                    },
                    'required': ['path', 'content']
                },
                'function': self._tool_write_file
            },
            'list_files': {
                'name': 'list_files',
                'description': 'List files in a directory',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'directory': {'type': 'string', 'description': 'Directory path'},
                        'recursive': {'type': 'boolean', 'description': 'List recursively'}
                    }
                },
                'function': self._tool_list_files
            },
            'search_files': {
                'name': 'search_files',
                'description': 'Search for files or content',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'term': {'type': 'string', 'description': 'Search term'},
                        'in_content': {'type': 'boolean', 'description': 'Search in file contents'}
                    },
                    'required': ['term']
                },
                'function': self._tool_search_files
            },
            'git_status': {
                'name': 'git_status',
                'description': 'Get git repository status',
                'parameters': {
                    'type': 'object',
                    'properties': {}
                },
                'function': self._tool_git_status
            },
            'git_diff': {
                'name': 'git_diff',
                'description': 'Show git diff for files',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'file': {'type': 'string', 'description': 'Specific file to diff (optional)'}
                    }
                },
                'function': self._tool_git_diff
            }
        }
    
    def get_tools_schema(self) -> List[Dict]:
        """Get OpenAI-compatible tools schema"""
        return [
            {
                'type': 'function',
                'function': {
                    'name': tool['name'],
                    'description': tool['description'],
                    'parameters': tool['parameters']
                }
            }
            for tool in self.tools.values()
        ]
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Execute a tool with given arguments"""
        if tool_name not in self.tools:
            return {'success': False, 'error': f'Tool {tool_name} not found'}
        
        tool = self.tools[tool_name]
        try:
            result = tool['function'](**arguments)
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Tool implementations
    def _tool_execute_code(self, code: str, language: str) -> Dict:
        """Execute code"""
        if language == 'python':
            return self.executor.execute_python(code)
        elif language == 'node':
            return self.executor.execute_node(code)
        else:
            return self.executor.execute_command(code)
    
    def _tool_read_file(self, path: str) -> Dict:
        """Read file"""
        return self.file_manager.read_file(path)
    
    def _tool_write_file(self, path: str, content: str) -> Dict:
        """Write file"""
        return self.file_manager.write_file(path, content)
    
    def _tool_list_files(self, directory: str = '', recursive: bool = False) -> Dict:
        """List files"""
        return self.file_manager.list_files(directory, recursive)
    
    def _tool_search_files(self, term: str, in_content: bool = False) -> Dict:
        """Search files"""
        if in_content:
            return self.file_manager.search_in_files(term)
        else:
            return self.file_manager.search_files(term)
    
    def _tool_git_status(self) -> Dict:
        """Git status"""
        return self.executor.execute_command('git status')
    
    def _tool_git_diff(self, file: str = '') -> Dict:
        """Git diff"""
        cmd = f'git diff {file}' if file else 'git diff'
        return self.executor.execute_command(cmd)

# Example usage
if __name__ == '__main__':
    tools = ToolSystem()
    print("Available Tools:")
    print(json.dumps(tools.get_tools_schema(), indent=2))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code Executor - Execute commands and code safely
Supports Python, Shell, and Node.js execution
"""

import subprocess
import os
import sys
import time
import threading
from pathlib import Path
import json

class CodeExecutor:
    def __init__(self, working_dir=None, timeout=30):
        """Initialize code executor"""
        self.working_dir = working_dir or os.getcwd()
        self.timeout = timeout
        self.process = None
        
    def execute_command(self, command, shell=True, capture_output=True):
        """
        Execute a shell command
        
        Args:
            command (str): Command to execute
            shell (bool): Use shell execution
            capture_output (bool): Capture stdout/stderr
            
        Returns:
            dict: Result with success, output, error, exit_code
        """
        try:
            start_time = time.time()
            
            # Execute command
            self.process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                cwd=self.working_dir,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = self.process.communicate(timeout=self.timeout)
                exit_code = self.process.returncode
            except subprocess.TimeoutExpired:
                self.process.kill()
                stdout, stderr = self.process.communicate()
                return {
                    'success': False,
                    'output': stdout or '',
                    'error': f'Command timed out after {self.timeout} seconds',
                    'exit_code': -1,
                    'execution_time': time.time() - start_time
                }
            
            execution_time = time.time() - start_time
            
            return {
                'success': exit_code == 0,
                'output': stdout or '',
                'error': stderr or '',
                'exit_code': exit_code,
                'execution_time': execution_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'exit_code': -1,
                'execution_time': 0
            }
    
    def execute_python(self, code, args=None):
        """Execute Python code"""
        try:
            # Create temporary file
            temp_file = Path(self.working_dir) / f'temp_script_{int(time.time())}.py'
            temp_file.write_text(code, encoding='utf-8')
            
            # Build command
            command = [sys.executable, str(temp_file)]
            if args:
                command.extend(args)
            
            # Execute
            result = self.execute_command(' '.join(command))
            
            # Cleanup
            try:
                temp_file.unlink()
            except:
                pass
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'exit_code': -1,
                'execution_time': 0
            }
    
    def execute_node(self, code, args=None):
        """Execute Node.js code"""
        try:
            # Create temporary file
            temp_file = Path(self.working_dir) / f'temp_script_{int(time.time())}.js'
            temp_file.write_text(code, encoding='utf-8')
            
            # Build command
            command = ['node', str(temp_file)]
            if args:
                command.extend(args)
            
            # Execute
            result = self.execute_command(' '.join(command))
            
            # Cleanup
            try:
                temp_file.unlink()
            except:
                pass
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'exit_code': -1,
                'execution_time': 0
            }
    
    def is_safe_command(self, command):
        """
        Check if command is safe to execute
        
        Blocks dangerous commands like rm, del, format, etc.
        """
        dangerous_commands = [
            'rm -rf', 'rmdir /s', 'del /f', 'format',
            'shutdown', 'reboot', 'taskkill /f',
            'mkfs', 'dd if=', 'chmod 777',
            '> /dev/', ':(){:|:&};:', 'fork bomb'
        ]
        
        command_lower = command.lower()
        for dangerous in dangerous_commands:
            if dangerous in command_lower:
                return False, f"Blocked dangerous command: {dangerous}"
        
        return True, "Command is safe"
    
    def kill_process(self):
        """Kill the running process"""
        if self.process:
            try:
                self.process.kill()
                return True
            except:
                return False
        return False

# Example usage
if __name__ == '__main__':
    executor = CodeExecutor()
    
    # Test command execution
    result = executor.execute_command('echo Hello World')
    print(json.dumps(result, indent=2))
    
    # Test Python execution
    python_code = """
print('Hello from Python!')
import sys
print(f'Python version: {sys.version}')
"""
    result = executor.execute_python(python_code)
    print(json.dumps(result, indent=2))

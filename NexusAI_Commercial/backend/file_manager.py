#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Manager - Safe file system operations
Read, write, list, search files
"""

import os
import shutil
from pathlib import Path
import json
import re
from typing import List, Dict, Optional

class FileManager:
    def __init__(self, root_dir=None, allowed_extensions=None):
        """Initialize file manager with safe directory restrictions"""
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.allowed_extensions = allowed_extensions or [
            '.py', '.js', '.html', '.css', '.json', '.txt', '.md',
            '.yaml', '.yml', '.xml', '.csv', '.ts', '.jsx', '.tsx'
        ]
        
    def is_safe_path(self, path):
        """Verify path is within allowed directory"""
        try:
            requested_path = Path(path).resolve()
            root_path = self.root_dir.resolve()
            
            # Check if path is within root directory
            return requested_path.is_relative_to(root_path)
        except:
            return False
    
    def read_file(self, filepath):
        """Read file contents"""
        try:
            full_path = self.root_dir / filepath
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {filepath}'
                }
            
            if not full_path.is_file():
                return {
                    'success': False,
                    'error': f'Not a file: {filepath}'
                }
            
            content = full_path.read_text(encoding='utf-8', errors='replace')
            
            return {
                'success': True,
                'content': content,
                'path': str(filepath),
                'size': full_path.stat().st_size,
                'modified': full_path.stat().st_mtime
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_file(self, filepath, content, create_dirs=True):
        """Write content to file"""
        try:
            full_path = self.root_dir / filepath
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            # Create parent directories if needed
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)
            
            full_path.write_text(content, encoding='utf-8')
            
            return {
                'success': True,
                'path': str(filepath),
                'size': len(content)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_files(self, directory='', recursive=False, max_depth=5):
        """List files in directory"""
        try:
            full_path = self.root_dir / directory
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'Directory not found: {directory}'
                }
            
            files = []
            dirs = []
            
            if recursive:
                for item in full_path.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(self.root_dir)
                        files.append({
                            'name': item.name,
                            'path': str(rel_path),
                            'size': item.stat().st_size,
                            'modified': item.stat().st_mtime,
                            'extension': item.suffix
                        })
            else:
                for item in full_path.iterdir():
                    rel_path = item.relative_to(self.root_dir)
                    if item.is_file():
                        files.append({
                            'name': item.name,
                            'path': str(rel_path),
                            'size': item.stat().st_size,
                            'modified': item.stat().st_mtime,
                            'extension': item.suffix
                        })
                    elif item.is_dir():
                        dirs.append({
                            'name': item.name,
                            'path': str(rel_path),
                            'type': 'directory'
                        })
            
            return {
                'success': True,
                'files': files,
                'directories': dirs,
                'total_files': len(files),
                'total_dirs': len(dirs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_files(self, pattern, directory='', file_extension=None):
        """Search for files matching pattern"""
        try:
            full_path = self.root_dir / directory
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            results = []
            regex = re.compile(pattern, re.IGNORECASE)
            
            for item in full_path.rglob('*'):
                if item.is_file():
                    # Filter by extension if specified
                    if file_extension and item.suffix != file_extension:
                        continue
                    
                    # Check if filename matches
                    if regex.search(item.name):
                        rel_path = item.relative_to(self.root_dir)
                        results.append({
                            'name': item.name,
                            'path': str(rel_path),
                            'size': item.stat().st_size,
                            'extension': item.suffix
                        })
            
            return {
                'success': True,
                'results': results,
                'count': len(results),
                'pattern': pattern
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_in_files(self, search_term, directory='', file_extension=None):
        """Search for text within files"""
        try:
            full_path = self.root_dir / directory
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            results = []
            
            for item in full_path.rglob('*'):
                if item.is_file():
                    # Filter by extension
                    if file_extension and item.suffix != file_extension:
                        continue
                    
                    # Skip binary files
                    if item.suffix not in self.allowed_extensions:
                        continue
                    
                    try:
                        content = item.read_text(encoding='utf-8', errors='ignore')
                        lines = content.split('\n')
                        
                        matches = []
                        for i, line in enumerate(lines, 1):
                            if search_term.lower() in line.lower():
                                matches.append({
                                    'line_number': i,
                                    'content': line.strip()
                                })
                        
                        if matches:
                            rel_path = item.relative_to(self.root_dir)
                            results.append({
                                'file': str(rel_path),
                                'matches': matches,
                                'match_count': len(matches)
                            })
                    except:
                        continue
            
            return {
                'success': True,
                'results': results,
                'total_files': len(results),
                'search_term': search_term
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_file(self, filepath):
        """Delete a file"""
        try:
            full_path = self.root_dir / filepath
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {filepath}'
                }
            
            if full_path.is_file():
                full_path.unlink()
            else:
                return {
                    'success': False,
                    'error': 'Not a file'
                }
            
            return {
                'success': True,
                'path': str(filepath)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_directory(self, dirpath):
        """Create a directory"""
        try:
            full_path = self.root_dir / dirpath
            
            if not self.is_safe_path(full_path):
                return {
                    'success': False,
                    'error': 'Access denied: Path outside allowed directory'
                }
            
            full_path.mkdir(parents=True, exist_ok=True)
            
            return {
                'success': True,
                'path': str(dirpath)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Example usage
if __name__ == '__main__':
    fm = FileManager()
    
    # Test listing files
    result = fm.list_files()
    print(json.dumps(result, indent=2))

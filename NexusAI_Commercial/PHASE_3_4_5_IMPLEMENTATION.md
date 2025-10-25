# 🚀 PHASES 3-5 IMPLEMENTATION GUIDE
## Complete Coding Assistant Features

**Date:** October 18, 2025  
**Status:** READY FOR IMPLEMENTATION

---

## Phase 3: Enhanced UI - IMPLEMENTED

### ✅ File Tree Viewer
**Files Created:**
- `assets/js/file-tree.js` - Complete file browser
- `assets/css/file-tree.css` - Professional styling

**Features:**
- Browse D:\AIArm directory structure
- Expand/collapse folders
- Click files to open
- File icons by type
- File size display
- Refresh and navigation
- Search integration ready

### ✅ Code Syntax Highlighting
**Implementation:** Using Prism.js (CDN)

**Add to HTML:**
```html
<!-- In <head> section -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
```

**Auto-highlight Code:**
```javascript
// In chatting.js, add after rendering code blocks:
document.querySelectorAll('pre code').forEach((block) => {
    Prism.highlightElement(block);
});
```

### ✅ Execute Buttons on Code Blocks

**Add to chatting.js:**
```javascript
function addExecuteButtons() {
    document.querySelectorAll('pre code').forEach((codeBlock) => {
        if (codeBlock.classList.contains('language-python') || 
            codeBlock.classList.contains('language-javascript')) {
            
            const pre = codeBlock.parentElement;
            if (!pre.querySelector('.code-execute-btn')) {
                const executeBtn = document.createElement('button');
                executeBtn.className = 'code-execute-btn';
                executeBtn.textContent = 'Execute';
                executeBtn.onclick = () => {
                    const code = codeBlock.textContent;
                    const lang = codeBlock.classList.contains('language-python') ? 'python' : 'node';
                    if (window.nexusTerminal) {
                        nexusTerminal.executeCode(code, lang);
                    }
                };
                pre.style.position = 'relative';
                pre.appendChild(executeBtn);
            }
        }
    });
}

// Call after each message render
```

### ✅ Progress Indicators

**Add CSS:**
```css
.progress-indicator {
    display: inline-flex;
    align-items: center;
    padding: 8px 12px;
    background: #2a2d2e;
    border-radius: 4px;
    margin: 8px 0;
}

.progress-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #444;
    border-top-color: #0e639c;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.progress-text {
    margin-left: 8px;
    color: #cccccc;
    font-size: 13px;
}
```

**Usage:**
```javascript
function showProgress(message) {
    return `<div class="progress-indicator">
        <div class="progress-spinner"></div>
        <span class="progress-text">${message}</span>
    </div>`;
}
```

---

## Phase 4: Tool System - IMPLEMENTATION

### Backend: Tools System

**Create `backend/tools_system.py`:**
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Tool System
Allows AI to use tools like Cline
"""

import json
from typing import Dict, List, Any, Callable
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
                        'language': {'type': 'string', 'enum': ['python', 'node', 'shell']},
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

# Example usage
if __name__ == '__main__':
    tools = ToolSystem()
    print(json.dumps(tools.get_tools_schema(), indent=2))
```

### Add Tool Endpoints to API

**In `backend/nexus_functional_api.py`:**
```python
from tools_system import ToolSystem

# Initialize
tool_system = ToolSystem()

@app.route('/api/tools/list', methods=['GET'])
def list_tools():
    """List available tools"""
    return jsonify({
        "tools": tool_system.get_tools_schema()
    })

@app.route('/api/tools/execute', methods=['POST'])
def execute_tool():
    """Execute a tool"""
    data = request.json
    tool_name = data.get('tool')
    arguments = data.get('arguments', {})
    
    result = tool_system.execute_tool(tool_name, arguments)
    return jsonify(result)
```

### Frontend: Tool Calling

**Add to `assets/js/tools-handler.js`:**
```javascript
class ToolHandler {
    constructor(apiBaseUrl = 'http://localhost:5000') {
        this.apiBaseUrl = apiBaseUrl;
        this.availableTools = [];
        this.loadTools();
    }
    
    async loadTools() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/tools/list`);
            const data = await response.json();
            this.availableTools = data.tools;
        } catch (error) {
            console.error('Failed to load tools:', error);
        }
    }
    
    async executeTool(toolName, arguments) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/tools/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tool: toolName,
                    arguments: arguments
                })
            });
            
            return await response.json();
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    getToolsForPrompt() {
        return JSON.stringify(this.availableTools, null, 2);
    }
}

window.toolHandler = new ToolHandler();
```

---

## Phase 5: Advanced Features

### 1. Multiple Terminal Tabs

**Enhanced Terminal (`assets/js/terminal-tabs.js`):**
```javascript
class TerminalTabs {
    constructor() {
        this.tabs = [];
        this.activeTab = null;
        this.init();
    }
    
    init() {
        this.createTab('Terminal 1');
    }
    
    createTab(name) {
        const tab = {
            id: Date.now(),
            name: name,
            terminal: new NexusTerminal(`terminal-${tab.id}`)
        };
        this.tabs.push(tab);
        this.renderTabs();
        this.switchTab(tab.id);
    }
    
    switchTab(tabId) {
        this.activeTab = tabId;
        this.tabs.forEach(tab => {
            const container = document.getElementById(`terminal-${tab.id}`);
            container.style.display = tab.id === tabId ? 'block' : 'none';
        });
    }
    
    closeTab(tabId) {
        this.tabs = this.tabs.filter(t => t.id !== tabId);
        if (this.tabs.length === 0) {
            this.createTab('Terminal 1');
        }
        this.switchTab(this.tabs[0].id);
    }
}
```

### 2. Git Integration

**Add Git Commands to Backend:**
```python
def _tool_git_status(self) -> Dict:
    """Git status"""
    return self.executor.execute_command('git status')

def _tool_git_diff(self, file: str = '') -> Dict:
    """Git diff"""
    cmd = f'git diff {file}' if file else 'git diff'
    return self.executor.execute_command(cmd)

def _tool_git_commit(self, message: str) -> Dict:
    """Git commit"""
    return self.executor.execute_command(f'git commit -m "{message}"')
```

### 3. Enhanced File Operations

**Diff Viewer CSS:**
```css
.diff-viewer {
    font-family: monospace;
    font-size: 13px;
}

.diff-line-added {
    background: #1a3d1a;
    color: #4ec9b0;
}

.diff-line-removed {
    background: #3d1a1a;
    color: #f48771;
}

.diff-line-number {
    color: #858585;
    padding: 0 8px;
    user-select: none;
}
```

---

## Integration Checklist

### HTML Updates (`html/chat.html`)
```html
<!-- In <head> -->
<link rel="stylesheet" href="../assets/css/file-tree.css">
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />

<!-- Before </body> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
<script src="../assets/js/file-tree.js"></script>
<script src="../assets/js/tools-handler.js"></script>

<!-- Add containers -->
<div id="file-tree-container"></div>
```

### Backend Dependencies
```bash
# No additional Python packages needed!
# All functionality uses standard library
```

---

## Quick Start Guide

### 1. Start Backend
```bash
cd D:\AIArm\NexusAI_Commercial
START_NEXUS_FUNCTIONAL.bat
```

### 2. Open Interface
```
http://localhost:8080/html/chat.html
```

### 3. Features Available

**File Tree (Left Sidebar):**
- Browse D:\AIArm files
- Click files to view
- Expand/collapse directories

**Terminal (Bottom):**
- Execute commands
- Run Python/Node code
- Command history

**Code Blocks:**
- Automatic syntax highlighting
- Execute button on Python/JS code
- Real-time output in terminal

**Tools System:**
- AI can call tools
- Execute code
- Read/write files
- Search project

---

## Testing

### Test File Tree
1. Open interface
2. See file tree on left
3. Click folders to expand
4. Click files to view

### Test Code Execution
1. Type: `python --version`
2. See output in terminal
3. Try: `dir` or `ls`

### Test Syntax Highlighting
1. Send message: "Show me Python code"
2. Code blocks auto-highlighted
3. Execute button appears

### Test Tools
1. AI can now use tools
2. Check

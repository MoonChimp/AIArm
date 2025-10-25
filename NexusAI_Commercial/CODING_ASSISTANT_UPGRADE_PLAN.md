# 🚀 NexusAI Coding Assistant Upgrade Plan

## Vision
Transform NexusAI from a chat interface into a full-featured AI coding assistant like Claude Code, Cline, and Blackbox AI with:
- Code execution capabilities
- Integrated terminal
- File system operations
- Tool use (read/write/edit files)
- Real-time command execution

---

## 🎯 Core Features Needed

### 1. **Integrated Terminal** ✓ Priority #1
- Web-based terminal emulator (xterm.js)
- Execute commands directly from chat
- Real-time command output
- Command history
- Multiple terminal tabs

### 2. **Code Execution Engine**
- Python code execution
- JavaScript/Node.js execution  
- Shell command execution
- Sandboxed environment
- Output streaming

### 3. **File System Operations**
- File tree viewer (sidebar)
- Read files
- Write/edit files
- Create directories
- Search files
- Syntax highlighting

### 4. **Tool Use System**
- Command execution tool
- File read tool
- File write tool
- Search tool
- Web scraping tool
- Image generation tool (already have!)

### 5. **Enhanced UI**
- Split view (chat + terminal + file tree)
- Code blocks with syntax highlighting
- Diff viewer for file changes
- Progress indicators
- Status bar

---

## 📋 Implementation Roadmap

### Phase 1: Backend API Enhancements (Week 1)
**Goal:** Add code execution and file operations to backend

**Tasks:**
- [ ] Create `/api/execute` endpoint (run commands)
- [ ] Create `/api/files/read` endpoint
- [ ] Create `/api/files/write` endpoint
- [ ] Create `/api/files/list` endpoint
- [ ] Create `/api/files/search` endpoint
- [ ] Add command execution safety/sandboxing
- [ ] Implement streaming responses

**Files to Create/Modify:**
- `backend/code_executor.py` - NEW
- `backend/file_manager.py` - NEW
- `backend/nexus_functional_api.py` - MODIFY

### Phase 2: Frontend Terminal Integration (Week 1)
**Goal:** Add terminal to chat interface

**Tasks:**
- [ ] Install xterm.js library
- [ ] Create terminal component
- [ ] Connect terminal to backend WebSocket
- [ ] Add command history
- [ ] Add terminal tabs
- [ ] Style terminal to match UI

**Files to Create/Modify:**
- `assets/js/terminal.js` - NEW
- `assets/css/terminal.css` - NEW
- `html/chat.html` - MODIFY

### Phase 3: File Tree & Editor (Week 2)
**Goal:** Add file browser and inline editor

**Tasks:**
- [ ] Create file tree component
- [ ] Add directory navigation
- [ ] Implement file preview
- [ ] Add syntax highlighting (Prism.js)
- [ ] Create inline code editor (CodeMirror)
- [ ] Add file upload/download

**Files to Create/Modify:**
- `assets/js/file-tree.js` - NEW
- `assets/js/code-editor.js` - NEW
- `assets/css/file-tree.css` - NEW

### Phase 4: Tool Use System (Week 2)
**Goal:** Let AI use tools like Cline

**Tasks:**
- [ ] Define tool schemas
- [ ] Implement tool calling in prompts
- [ ] Add tool approval system
- [ ] Create tool response handlers
- [ ] Add streaming tool outputs

**Files to Create/Modify:**
- `backend/tools_system.py` - NEW
- `assets/js/tools-handler.js` - NEW

### Phase 5: Enhanced Chat UI (Week 3)
**Goal:** Make chat interface more like Claude/Cline

**Tasks:**
- [ ] Add code block rendering
- [ ] Add diff viewer
- [ ] Add file change previews
- [ ] Add progress indicators
- [ ] Add status bar
- [ ] Add keyboard shortcuts

**Files to Create/Modify:**
- `assets/js/chat-renderer.js` - NEW
- `assets/css/code-blocks.css` - NEW

---

## 🛠️ Technical Stack

### Backend
- **Python** - Core language
- **Flask** - Web framework
- **subprocess** - Command execution
- **os/pathlib** - File operations
- **asyncio** - Async operations
- **websockets** - Real-time communication

### Frontend
- **xterm.js** - Terminal emulator
- **Socket.io** - WebSocket client
- **Prism.js** - Syntax highlighting
- **CodeMirror** - Code editor
- **File Tree** - Custom or library

### Security
- **Sandboxing** - Limit command execution
- **Path validation** - Prevent directory traversal
- **User permissions** - File access control
- **Command whitelist** - Safe commands only

---

## 📊 Architecture Overview

```
┌────────────────────────────────────────────────┐
│              NexusAI Webapp                    │
│                                                │
│  ┌──────────────┐  ┌──────────────┐          │
│  │  File Tree   │  │   Chat UI    │          │
│  │              │  │              │          │
│  │  - Browse    │  │  - Messages  │          │
│  │  - Edit      │  │  - Code      │          │
│  │  - Search    │  │  - Tools     │          │
│  └──────────────┘  └──────────────┘          │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │         Integrated Terminal              │ │
│  │  $ python script.py                      │ │
│  │  $ npm install                           │ │
│  │  $ git status                            │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│           NexusAI Backend API                  │
│                                                │
│  ┌──────────────┐  ┌──────────────┐          │
│  │   Ollama     │  │  Code        │          │
│  │   Connector  │  │  Executor    │          │
│  └──────────────┘  └──────────────┘          │
│                                                │
│  ┌──────────────┐  ┌──────────────┐          │
│  │   File       │  │   Tools      │          │
│  │   Manager    │  │   System     │          │
│  └──────────────┘  └──────────────┘          │
└────────────────────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│         System Resources                       │
│                                                │
│  - File System (D:\AIArm)                     │
│  - Terminal (cmd/powershell)                  │
│  - Python Interpreter                         │
│  - Node.js                                    │
│  - Git                                        │
└────────────────────────────────────────────────┘
```

---

## 🔒 Security Considerations

### Command Execution
- ✅ Whitelist safe commands
- ✅ Sandbox in virtual environment
- ✅ Timeout limits (30s default)
- ✅ Resource limits (CPU/memory)
- ⚠️ Require user approval for dangerous commands

### File System
- ✅ Restrict to project directories only
- ✅ No access to system files
- ✅ Path traversal protection
- ✅ File size limits
- ⚠️ Backup before modifying

### Network
- ✅ Rate limiting
- ✅ CORS configuration
- ⚠️ Optional: Authentication (future)

---

## 📦 Dependencies to Install

### Backend (Python)
```bash
pip install flask
pip install flask-cors
pip install flask-socketio
pip install python-socketio
pip install psutil  # Resource monitoring
```

### Frontend (JavaScript)
```html
<!-- Terminal -->
<script src="https://cdn.jsdelivr.net/npm/xterm@5.1.0/lib/xterm.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.1.0/css/xterm.css" />

<!-- Syntax Highlighting -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>

<!-- Socket.io -->
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
```

---

## 🎯 Quick Start (Minimum Viable Product)

Let me create the essential components to get you started:

### What I'll Build First:
1. **Code Executor Backend** - Execute Python/Shell commands
2. **Basic Terminal UI** - Simple terminal in chat
3. **Command Detection** - Auto-detect code blocks
4. **Output Display** - Show command results

This gives you the core functionality TODAY, then we can expand!

---

## 📝 Example Use Cases

### Use Case 1: Execute Python Code
**User:** "Write a Python script to analyze this CSV file"
**Nexus:** Creates script, shows code, asks for approval
**User:** Approves
**Nexus:** Executes, shows output in terminal

### Use Case 2: File Operations
**User:** "Read config.json and update the API key"
**Nexus:** Reads file, shows content, suggests changes
**User:** Approves changes
**Nexus:** Writes file, confirms completion

### Use Case 3: Multi-Step Task
**User:** "Set up a new React project"
**Nexus:** 
1. `npx create-react-app my-app`
2. `cd my-app`
3. `npm install axios`
4. Creates component files
5. Shows project structure

---

## 🚀 Ready to Start?

I can begin building this right now. Here's what I'll create first:

**Phase 1 (Today):**
1. Code executor backend API
2. Command execution endpoint
3. Basic terminal UI component
4. Integration with existing chat

**Estimated Time:** 2-3 hours for MVP
**Result:** Working code execution in NexusAI

**Should I proceed with Phase 1?**

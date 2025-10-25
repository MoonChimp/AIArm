/**
 * NexusAI Terminal Component
 * Integrated terminal for code execution
 */

class NexusTerminal {
    constructor(containerId, apiBaseUrl = 'http://localhost:5000') {
        this.container = document.getElementById(containerId);
        this.apiBaseUrl = apiBaseUrl;
        this.history = [];
        this.historyIndex = -1;
        this.currentDir = 'D:\\AIArm';
        this.isExecuting = false;
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error('Terminal container not found');
            return;
        }
        
        // Create terminal HTML
        this.container.innerHTML = `
            <div class="terminal-window">
                <div class="terminal-header">
                    <span class="terminal-title">Terminal</span>
                    <div class="terminal-controls">
                        <button class="terminal-btn" onclick="nexusTerminal.clear()">Clear</button>
                        <button class="terminal-btn" onclick="nexusTerminal.toggle()">Hide</button>
                    </div>
                </div>
                <div class="terminal-body" id="terminal-output"></div>
                <div class="terminal-input-container">
                    <span class="terminal-prompt">${this.currentDir}></span>
                    <input type="text" class="terminal-input" id="terminal-input" placeholder="Type command..." />
                </div>
            </div>
        `;
        
        // Set up event listeners
        const input = document.getElementById('terminal-input');
        input.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Initial message
        this.write('NexusAI Terminal Ready', 'system');
        this.write(`Current Directory: ${this.currentDir}`, 'system');
        this.write('Type "help" for available commands\n', 'system');
    }
    
    handleKeyDown(e) {
        const input = e.target;
        
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                this.executeCommand(command);
                input.value = '';
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (this.historyIndex < this.history.length - 1) {
                this.historyIndex++;
                input.value = this.history[this.history.length - 1 - this.historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (this.historyIndex > 0) {
                this.historyIndex--;
                input.value = this.history[this.history.length - 1 - this.historyIndex];
            } else if (this.historyIndex === 0) {
                this.historyIndex = -1;
                input.value = '';
            }
        }
    }
    
    async executeCommand(command) {
        if (this.isExecuting) {
            this.write('Command already executing...', 'error');
            return;
        }
        
        // Add to history
        this.history.push(command);
        this.historyIndex = -1;
        
        // Show command
        this.write(`${this.currentDir}> ${command}`, 'input');
        
        // Handle built-in commands
        if (command === 'help') {
            this.showHelp();
            return;
        } else if (command === 'clear' || command === 'cls') {
            this.clear();
            return;
        } else if (command.startsWith('cd ')) {
            const newDir = command.substring(3).trim();
            this.currentDir = newDir;
            document.querySelector('.terminal-prompt').textContent = `${this.currentDir}>`;
            this.write(`Changed directory to: ${this.currentDir}`, 'success');
            return;
        }
        
        // Execute command via API
        this.isExecuting = true;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: 'command',
                    code: command,
                    working_dir: this.currentDir
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                if (result.output) {
                    this.write(result.output, 'output');
                }
                if (result.error) {
                    this.write(result.error, 'error');
                }
                this.write(`\nCompleted in ${result.execution_time?.toFixed(2) || 0}s`, 'system');
            } else {
                this.write(result.error || 'Command failed', 'error');
                if (result.blocked) {
                    this.write('⚠ This command was blocked for safety', 'error');
                }
            }
            
        } catch (error) {
            this.write(`Error: ${error.message}`, 'error');
        } finally {
            this.isExecuting = false;
        }
    }
    
    write(text, type = 'output') {
        const output = document.getElementById('terminal-output');
        const line = document.createElement('div');
        line.className = `terminal-line terminal-${type}`;
        line.textContent = text;
        output.appendChild(line);
        
        // Auto-scroll
        output.scrollTop = output.scrollHeight;
    }
    
    clear() {
        document.getElementById('terminal-output').innerHTML = '';
        this.write('Terminal cleared', 'system');
    }
    
    showHelp() {
        this.write('\nAvailable Commands:', 'system');
        this.write('  help       - Show this help message', 'output');
        this.write('  clear/cls  - Clear terminal', 'output');
        this.write('  cd <dir>   - Change directory', 'output');
        this.write('  Any shell command (dir, ls, python, node, etc.)', 'output');
        this.write('\nCode Execution:', 'system');
        this.write('  Use the execute button in chat for Python/Node.js code', 'output');
        this.write('', 'output');
    }
    
    toggle() {
        this.container.style.display = 
            this.container.style.display === 'none' ? 'block' : 'none';
    }
    
    executeCode(code, type = 'python') {
        this.write(`\n--- Executing ${type} code ---`, 'system');
        this.write(code, 'code');
        
        fetch(`${this.apiBaseUrl}/api/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                code: code,
                working_dir: this.currentDir
            })
        })
        .then(res => res.json())
        .then(result => {
            if (result.success) {
                if (result.output) {
                    this.write(result.output, 'output');
                }
                if (result.error) {
                    this.write(result.error, 'error');
                }
                this.write(`Completed in ${result.execution_time?.toFixed(2) || 0}s`, 'system');
            } else {
                this.write(result.error || 'Execution failed', 'error');
            }
        })
        .catch(error => {
            this.write(`Error: ${error.message}`, 'error');
        });
    }
}

// Global instance
let nexusTerminal = null;

// Toggle terminal visibility
function toggleTerminal() {
    const terminalContainer = document.getElementById('nexus-terminal-container');
    if (terminalContainer) {
        terminalContainer.classList.toggle('active');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    nexusTerminal = new NexusTerminal('nexus-terminal-container');
});

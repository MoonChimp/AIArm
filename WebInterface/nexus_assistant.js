/**
 * Nexus Task Detection and Execution Module
 * 
 * This module enhances Nexus with the ability to:
 * 1. Detect when users are implying they want a task done
 * 2. Confirm the task with the user
 * 3. Execute the task using the system's terminal
 * 4. Provide helpful, assistant-like responses
 */

class NexusAssistant {
    constructor() {
        this.taskKeywords = [
            'can you', 'please', 'do this', 'run', 'execute', 'open', 'create', 
            'find', 'search', 'check', 'look for', 'tell me', 'help me',
            'could you', 'would you', 'i need', 'i want', 'i would like',
            'show me', 'start', 'launch', 'build', 'make', 'get'
        ];
        
        this.actionVerbs = [
            'run', 'execute', 'open', 'create', 'find', 'search', 'start',
            'launch', 'build', 'make', 'check', 'install', 'download',
            'upload', 'delete', 'remove', 'move', 'copy', 'read', 'write'
        ];
        
        this.systemKeywords = [
            'file', 'folder', 'directory', 'program', 'application', 'app',
            'terminal', 'command', 'script', 'task', 'process', 'service',
            'website', 'url', 'link', 'email', 'message', 'document',
            'computer', 'system', 'network', 'server', 'database'
        ];
        
        this.confirmedTasks = new Set();
        this.pendingTasks = {};
        this.taskHistory = [];
    }
    
    /**
     * Analyzes user input to detect if it's a task request
     * @param {string} input - User's message
     * @returns {Object} Analysis result with score and detected task
     */
    analyzeInput(input) {
        const inputLower = input.toLowerCase();
        let taskScore = 0;
        let detectedVerb = null;
        let detectedObject = null;
        
        // Check for task keywords
        for (const keyword of this.taskKeywords) {
            if (inputLower.includes(keyword)) {
                taskScore += 1;
            }
        }
        
        // Check for action verbs
        for (const verb of this.actionVerbs) {
            if (inputLower.includes(verb)) {
                taskScore += 2;
                detectedVerb = verb;
                break;
            }
        }
        
        // Check for system keywords
        for (const keyword of this.systemKeywords) {
            if (inputLower.includes(keyword)) {
                taskScore += 1;
                detectedObject = keyword;
                break;
            }
        }
        
        // Analyze sentence structure for commands
        if (inputLower.startsWith('please ') || 
            this.actionVerbs.some(verb => inputLower.startsWith(verb + ' '))) {
            taskScore += 3;
        }
        
        // Extract the potential task
        let potentialTask = '';
        if (detectedVerb && detectedObject) {
            // Try to extract the task based on verb-object pattern
            const verbIndex = inputLower.indexOf(detectedVerb);
            if (verbIndex !== -1) {
                potentialTask = input.substring(verbIndex);
            }
        } else {
            // Fallback to using the whole input
            potentialTask = input;
        }
        
        return {
            isTaskLike: taskScore >= 3,
            score: taskScore,
            potentialTask: potentialTask.trim(),
            detectedVerb: detectedVerb,
            detectedObject: detectedObject
        };
    }
    
    /**
     * Formulates a task confirmation message
     * @param {string} potentialTask - The detected task
     * @returns {string} Confirmation message
     */
    getConfirmationMessage(potentialTask) {
        const taskId = Date.now().toString();
        this.pendingTasks[taskId] = potentialTask;
        
        return {
            message: `I can help you with that. Would you like me to ${potentialTask}?`,
            taskId: taskId
        };
    }
    
    /**
     * Executes a confirmed task
     * @param {string} taskId - The ID of the confirmed task
     * @returns {Promise<Object>} Task execution result
     */
    async executeTask(taskId) {
        if (!this.pendingTasks[taskId]) {
            return {
                success: false,
                message: "I couldn't find that task. Please try again."
            };
        }
        
        const task = this.pendingTasks[taskId];
        this.confirmedTasks.add(taskId);
        
        try {
            // Extract a command to execute from the task description
            const command = this.extractCommand(task);
            console.log(`Executing command: ${command}`);
            
            // Execute the command via the API
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ command })
            });
            
            const result = await response.json();
            
            // Record in history
            this.taskHistory.push({
                task: task,
                command: command,
                timestamp: new Date().toISOString(),
                status: result.success ? 'executed' : 'failed',
                output: result.output || result.error
            });
            
            if (result.success) {
                return {
                    success: true,
                    message: `I've completed the task: ${task}`,
                    result: result.output || 'Task completed successfully.'
                };
            } else {
                return {
                    success: false,
                    message: `I encountered an issue while trying to ${task}.`,
                    error: result.error,
                    output: result.output
                };
            }
        } catch (error) {
            console.error(`Error executing task: ${error.message}`);
            return {
                success: false,
                message: `I encountered an issue while trying to ${task}. Error: ${error.message}`,
                error: error.message
            };
        } finally {
            // Clean up
            delete this.pendingTasks[taskId];
        }
    }
    
    /**
     * Extracts a command to execute from a task description
     * @param {string} task - The task description
     * @returns {string} The command to execute
     */
    extractCommand(task) {
        // These patterns help identify commands within natural language
        const cmdPatterns = [
            // Direct commands
            /\b(?:run|execute)\s+(?:the\s+)?command\s+(?:to\s+)?['"]?([^'"]+)['"]?/i,
            /\b(?:run|execute)\s+['"]([^'"]+)['"]\s+(?:in|on)\s+(?:the\s+)?(?:terminal|cmd|command\s*line)/i,
            
            // Command with 'type'
            /\btype\s+['"]?([^'"]+)['"]?\s+(?:in|on)\s+(?:the\s+)?(?:terminal|cmd|command\s*line)/i,
            
            // Specific commands to look for
            /\b(dir|ls|cd|mkdir|rmdir|del|copy|move|echo|type|find|findstr|grep|cat)\s+[\w\/.\\\s-]+/i,
            
            // Path-looking patterns
            /\b([a-zA-Z]:\\[\w\\\s.-]+)\b/i,
            
            // Fallback - extract something that looks like a command
            /\b(\w+(?:\s+(?:-{1,2}\w+|[\w.\/-]+))+)\b/
        ];
        
        // Try each pattern until we find a match
        for (const pattern of cmdPatterns) {
            const match = task.match(pattern);
            if (match && match[1]) {
                return match[1].trim();
            }
        }
        
        // If no pattern matches, use some heuristics
        const taskWords = task.split(/\s+/);
        if (taskWords.length >= 2) {
            // If there are file/directory operations words
            const fileOps = ['list', 'show', 'find', 'search', 'open', 'create', 'delete', 'read'];
            if (fileOps.includes(taskWords[0].toLowerCase())) {
                // Try to extract a path-like structure
                const pathPattern = /([a-zA-Z]:\\[\w\\\s.-]*)/;
                const pathMatch = task.match(pathPattern);
                if (pathMatch) {
                    // Convert natural language to commands
                    if (taskWords[0].toLowerCase() === 'list') {
                        return `dir ${pathMatch[1]}`;
                    } else if (taskWords[0].toLowerCase() === 'show' || 
                               taskWords[0].toLowerCase() === 'open') {
                        return `type ${pathMatch[1]}`;
                    } else if (taskWords[0].toLowerCase() === 'find' || 
                               taskWords[0].toLowerCase() === 'search') {
                        // Get search term
                        const searchTermPattern = /for\s+['"]?([\w\s]+)['"]?/i;
                        const searchMatch = task.match(searchTermPattern);
                        const searchTerm = searchMatch ? searchMatch[1] : '*';
                        return `findstr /S "${searchTerm}" ${pathMatch[1]}\*`;
                    }
                }
            }
        }
        
        // Use a very simple fallback - just use the task itself
        // This is not ideal but better than nothing
        return task.trim();
    }
    
    /**
     * Generates a personalized response based on the user's input
     * @param {string} input - User's message
     * @returns {string} Personalized response
     */
    generatePersonalizedResponse(input) {
        const inputLower = input.toLowerCase();
        
        // Greeting patterns
        if (inputLower.match(/^(hi|hello|hey|greetings).*/)) {
            return "Hello! I'm Nexus, your personal AI assistant. How can I help you today?";
        }
        
        // Asking about capabilities
        if (inputLower.includes("what can you do") || 
            inputLower.includes("your capabilities") || 
            inputLower.includes("help me with")) {
            return "As your personal assistant, I can help with file operations, finding information, running commands, organizing tasks, and much more. Just let me know what you need!";
        }
        
        // Questions about identity
        if (inputLower.includes("who are you") || 
            inputLower.includes("your name") || 
            inputLower.includes("what are you")) {
            return "I'm Nexus, your AI personal assistant. I'm designed to help you complete tasks, find information, and make your digital life easier.";
        }
        
        // Default response for non-task inputs
        return "I'm here to assist you. Would you like me to help you with a specific task?";
    }
}

// Export the assistant for use in other modules
if (typeof module !== 'undefined') {
    module.exports = { NexusAssistant };
}

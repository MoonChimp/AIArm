/**
 * NexusCore - Administrative Command Handler
 * 
 * This module directly integrates administrative capabilities into Nexus's core,
 * allowing it to perform file operations and system commands with full privileges.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

class NexusCore {
    constructor() {
        this.initialized = false;
        this.adminCapable = false;
        this.version = "1.0.0";
        
        // Initialize on creation
        this.initialize();
    }
    
    // Initialize the core with admin check
    initialize() {
        try {
            // Create logs directory if it doesn't exist
            const logsDir = path.join("D:", "AIArm", "Logs");
            if (!fs.existsSync(logsDir)) {
                fs.mkdirSync(logsDir, { recursive: true });
            }
            
            // Create test directory if it doesn't exist
            const testDir = path.join("D:", "AIArm", "Test");
            if (!fs.existsSync(testDir)) {
                fs.mkdirSync(testDir, { recursive: true });
            }
            
            // Check for admin capabilities by writing to system directory
            const testFilePath = path.join(testDir, `admin_test_${Date.now()}.txt`);
            try {
                fs.writeFileSync(testFilePath, `Admin test file created at ${new Date().toISOString()}\n`);
                this.adminCapable = true;
                this.log("NexusCore initialized with ADMIN capabilities");
            } catch (err) {
                this.adminCapable = false;
                this.log(`Failed admin capability check: ${err.message}`);
            }
            
            this.initialized = true;
            this.log(`NexusCore initialized. Version: ${this.version}, Admin: ${this.adminCapable}`);
        } catch (err) {
            this.log(`Error initializing NexusCore: ${err.message}`);
            this.initialized = false;
        }
    }
    
    // Log messages to NexusCore log file
    log(message) {
        const timestamp = new Date().toISOString();
        const logLine = `[${timestamp}] ${message}\n`;
        
        console.log(`NexusCore: ${message}`);
        
        try {
            const logFile = path.join("D:", "AIArm", "Logs", "nexuscore.log");
            fs.appendFileSync(logFile, logLine);
        } catch (err) {
            console.error(`Error writing to log: ${err.message}`);
        }
    }
    
    // Execute a system command with admin privileges
    executeCommand(command) {
        if (!this.initialized) {
            return { success: false, error: "NexusCore not initialized" };
        }
        
        this.log(`Executing command: ${command}`);
        
        try {
            // Execute the command synchronously
            const output = execSync(command, { encoding: 'utf8', shell: true });
            this.log(`Command executed successfully`);
            return { success: true, output: output };
        } catch (err) {
            this.log(`Error executing command: ${err.message}`);
            return { 
                success: false, 
                error: err.message,
                stderr: err.stderr,
                stdout: err.stdout
            };
        }
    }
    
    // Write a file with admin privileges
    writeFile(filePath, content) {
        if (!this.initialized) {
            return { success: false, error: "NexusCore not initialized" };
        }
        
        this.log(`Writing to file: ${filePath}`);
        
        try {
            // Create directory if it doesn't exist
            const directory = path.dirname(filePath);
            if (!fs.existsSync(directory)) {
                fs.mkdirSync(directory, { recursive: true });
            }
            
            // Write the file
            fs.writeFileSync(filePath, content);
            
            this.log(`Successfully wrote to file: ${filePath}`);
            return { success: true, path: filePath };
        } catch (err) {
            this.log(`Error writing file: ${err.message}`);
            return { success: false, error: err.message, path: filePath };
        }
    }
    
    // Read a file with admin privileges
    readFile(filePath) {
        if (!this.initialized) {
            return { success: false, error: "NexusCore not initialized" };
        }
        
        this.log(`Reading file: ${filePath}`);
        
        try {
            // Check if file exists
            if (!fs.existsSync(filePath)) {
                return { success: false, error: "File not found", path: filePath };
            }
            
            // Read the file
            const content = fs.readFileSync(filePath, 'utf8');
            
            this.log(`Successfully read file: ${filePath}`);
            return { success: true, content: content, path: filePath };
        } catch (err) {
            this.log(`Error reading file: ${err.message}`);
            return { success: false, error: err.message, path: filePath };
        }
    }
    
    // List directory contents with admin privileges
    listDirectory(directoryPath) {
        if (!this.initialized) {
            return { success: false, error: "NexusCore not initialized" };
        }
        
        this.log(`Listing directory: ${directoryPath}`);
        
        try {
            // Check if directory exists
            if (!fs.existsSync(directoryPath)) {
                return { success: false, error: "Directory not found", path: directoryPath };
            }
            
            // List directory contents
            const items = fs.readdirSync(directoryPath).map(item => {
                const itemPath = path.join(directoryPath, item);
                const isDirectory = fs.statSync(itemPath).isDirectory();
                
                return {
                    name: item,
                    path: itemPath,
                    type: isDirectory ? "directory" : "file"
                };
            });
            
            this.log(`Successfully listed directory: ${directoryPath}`);
            return { success: true, items: items, path: directoryPath };
        } catch (err) {
            this.log(`Error listing directory: ${err.message}`);
            return { success: false, error: err.message, path: directoryPath };
        }
    }
    
    // Create a test file to demonstrate capabilities
    createTestFile() {
        const timestamp = new Date().toISOString().replace(/:/g, '-');
        const filePath = path.join("D:", "AIArm", "Test", `nexuscore_test_${timestamp}.txt`);
        
        const content = `This file was created by NexusCore with administrative privileges.
Created at: ${new Date().toISOString()}
System: ${os.platform()} ${os.release()}
User: ${os.userInfo().username}

This file demonstrates that NexusCore has full access to the filesystem.
`;
        
        return this.writeFile(filePath, content);
    }
    
    // Process a request from Nexus
    processRequest(request) {
        if (!this.initialized) {
            return { success: false, error: "NexusCore not initialized" };
        }
        
        this.log(`Processing request: ${JSON.stringify(request)}`);
        
        try {
            // Check the operation type
            switch (request.operation) {
                case "writeFile":
                    return this.writeFile(request.path, request.content);
                
                case "readFile":
                    return this.readFile(request.path);
                
                case "listDirectory":
                    return this.listDirectory(request.path);
                
                case "executeCommand":
                    return this.executeCommand(request.command);
                
                case "createTestFile":
                    return this.createTestFile();
                
                default:
                    return { 
                        success: false, 
                        error: `Unknown operation: ${request.operation}` 
                    };
            }
        } catch (err) {
            this.log(`Error processing request: ${err.message}`);
            return { success: false, error: err.message };
        }
    }
    
    // Detect admin tasks in natural language
    detectAdminTask(input) {
        if (!input || typeof input !== 'string') {
            return { isAdminTask: false };
        }
        
        const input_lower = input.toLowerCase();
        
        // Check for test file creation
        if (input_lower.includes("test file") || 
            (input_lower.includes("create") && input_lower.includes("file"))) {
            return { 
                isAdminTask: true,
                operation: "createTestFile",
                message: "I'll create a test file to demonstrate my administrative capabilities."
            };
        }
        
        // Check for directory listing
        if ((input_lower.includes("list") || input_lower.includes("show") || 
             input_lower.includes("what's in")) && 
            (input_lower.includes("directory") || input_lower.includes("folder") || 
             /[a-z]:\\/i.test(input))) {
            
            // Try to extract a path
            let path = "D:\\";
            const pathMatch = input.match(/([a-z]:[\\\/][^\s"',;:]+)/i);
            if (pathMatch) {
                path = pathMatch[1];
            }
            
            return {
                isAdminTask: true,
                operation: "listDirectory",
                path: path,
                message: `I'll list the contents of ${path} for you.`
            };
        }
        
        // Check for file reading
        if ((input_lower.includes("read") || input_lower.includes("show") || 
             input_lower.includes("open") || input_lower.includes("get")) && 
            input_lower.includes("file")) {
            
            // Try to extract a path
            const pathMatch = input.match(/([a-z]:[\\\/][^\s"',;:]+)/i);
            if (pathMatch) {
                const path = pathMatch[1];
                return {
                    isAdminTask: true,
                    operation: "readFile",
                    path: path,
                    message: `I'll read the contents of ${path} for you.`
                };
            }
        }
        
        // Check for command execution
        if (input_lower.includes("run") || input_lower.includes("execute") || 
            input_lower.includes("command")) {
            
            // Try to extract a command
            const commandMatch = input.match(/(?:run|execute)\s+(?:the\s+)?(?:command\s+)?["']?(.+?)["']?(?:\s|$)/i);
            if (commandMatch) {
                const command = commandMatch[1];
                return {
                    isAdminTask: true,
                    operation: "executeCommand",
                    command: command,
                    message: `I'll execute the command: ${command}`
                };
            }
        }
        
        // Generic filesystem task detection
        const filesystemTerms = [
            'file', 'directory', 'folder', 'create', 'write', 'read', 'list',
            'show me', 'display', 'delete', 'remove', 'copy', 'move', 'rename'
        ];
        
        if (filesystemTerms.some(term => input_lower.includes(term))) {
            return {
                isAdminTask: true,
                operation: "adminCapabilities",
                message: "I have administrative filesystem capabilities. Please specify what operation you'd like me to perform."
            };
        }
        
        return { isAdminTask: false };
    }
}

module.exports = new NexusCore();

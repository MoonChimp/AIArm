/**
 * Direct Integration Module for AlfaZer0
 * This module provides direct access to administrative capabilities
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Log function
function logMessage(message) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${message}`);
    
    try {
        const logsDir = path.resolve(__dirname, '..', 'Logs');
        if (!fs.existsSync(logsDir)) {
            fs.mkdirSync(logsDir, { recursive: true });
        }
        
        const logFile = path.join(logsDir, 'alfazer0_integration.log');
        fs.appendFileSync(logFile, `[${timestamp}] ${message}\n`);
    } catch (err) {
        console.error('Failed to write to log:', err);
    }
}

// Execute operation through Python bridge
async function executeOperation(operation, params = {}) {
    return new Promise((resolve, reject) => {
        try {
            const bridgePath = path.join(__dirname, 'alfazer0_bridge.py');
            const requestData = JSON.stringify({
                operation,
                ...params
            });
            
            logMessage(`Executing ${operation} with params: ${JSON.stringify(params)}`);
            
            const pythonProcess = spawn('python', [bridgePath], {
                windowsHide: true
            });
            
            let stdoutData = '';
            let stderrData = '';
            
            pythonProcess.stdout.on('data', (data) => {
                stdoutData += data.toString();
            });
            
            pythonProcess.stderr.on('data', (data) => {
                stderrData += data.toString();
                logMessage(`Error from Python bridge: ${data.toString()}`);
            });
            
            pythonProcess.on('close', (code) => {
                logMessage(`Python bridge process exited with code ${code}`);
                
                if (code === 0) {
                    try {
                        const result = JSON.parse(stdoutData);
                        resolve(result);
                    } catch (err) {
                        reject(new Error(`Failed to parse Python bridge output: ${err.message}`));
                    }
                } else {
                    reject(new Error(`Python bridge process exited with code ${code}: ${stderrData}`));
                }
            });
            
            pythonProcess.on('error', (err) => {
                logMessage(`Error executing Python bridge: ${err.message}`);
                reject(err);
            });
            
            // Write request data to stdin
            pythonProcess.stdin.write(requestData);
            pythonProcess.stdin.end();
        } catch (err) {
            logMessage(`Error in executeOperation: ${err.message}`);
            reject(err);
        }
    });
}

// Create a test file directly
async function writeTestFile() {
    try {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filePath = `D:/AIArm/Test/alfazer0_test_${timestamp}.txt`;
        const content = `This is a test file created by NexusAI:AlfaZer0 on ${new Date().toLocaleString()}.\n\nThis file demonstrates the administrative filesystem capabilities of AlfaZer0.\n\nIf you can read this, the test was successful!`;
        
        const result = await executeOperation('write_file', {
            path: filePath,
            content: content
        });
        
        return {
            success: result.success,
            message: result.success ? `Test file created successfully at: ${filePath}` : `Failed to create test file: ${result.error}`,
            path: filePath
        };
    } catch (err) {
        return {
            success: false,
            error: err.message,
            message: `Failed to create test file: ${err.message}`
        };
    }
}

// Export functions
module.exports = {
    executeOperation,
    writeTestFile,
    
    // Core filesystem operations
    readFile: (path) => executeOperation('read_file', { path }),
    writeFile: (path, content) => executeOperation('write_file', { path, content }),
    appendFile: (path, content) => executeOperation('append_file', { path, content }),
    listDirectory: (path) => executeOperation('list_directory', { path }),
    createDirectory: (path) => executeOperation('create_directory', { path }),
    deleteFile: (path) => executeOperation('delete_file', { path }),
    deleteDirectory: (path, recursive) => executeOperation('delete_directory', { path, recursive }),
    getFileInfo: (path) => executeOperation('get_file_info', { path }),
    searchFiles: (directory, pattern) => executeOperation('search_files', { directory, pattern }),
    copyFile: (source, destination) => executeOperation('copy_file', { source, destination }),
    moveFile: (source, destination) => executeOperation('move_file', { source, destination }),
    
    // System operations
    executeCommand: (command) => executeOperation('execute_command', { command }),
    getSystemInfo: () => executeOperation('get_system_info'),
    
    // Self-expansion operations
    createScript: (name, description, content) => executeOperation('create_script', { name, description, content }),
    createModule: (name, description, content) => executeOperation('create_module', { name, description, content }),
    storeKnowledge: (name, content) => executeOperation('store_knowledge', { name, content }),
    updateIndex: (newCapability) => executeOperation('update_index', { new_capability: newCapability })
};
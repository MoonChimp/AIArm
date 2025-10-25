/**
 * Nexus Administrative Filesystem Bridge
 * Provides administrative filesystem access to Nexus AI
 */

const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const ADMIN_SCRIPT_PATH = path.resolve(__dirname, 'nexus_admin_bridge.bat');
const LOG_PATH = path.resolve(__dirname, 'Logs', 'admin_operations.log');

// Ensure log directory exists
if (!fs.existsSync(path.dirname(LOG_PATH))) {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
}

// Log function
function logOperation(operation, params, result) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${operation} ${JSON.stringify(params)} => ${result}\n`;
    
    try {
        fs.appendFileSync(LOG_PATH, logEntry);
    } catch (err) {
        console.error('Failed to write to log:', err);
    }
}

// Create admin bridge script if it doesn't exist
function ensureAdminBridge() {
    const scriptContent = `@echo off
:: Admin bridge script for Nexus AI
:: Automatically elevates privileges when needed

:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\\system32\\cacls.exe" "%SYSTEMROOT%\\system32\\config\\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "%*", "", "runas", 1 >> "%temp%\\getadmin.vbs"
    "%temp%\\getadmin.vbs"
    exit /B
) else (
    goto gotAdmin
)

:gotAdmin
    if exist "%temp%\\getadmin.vbs" del "%temp%\\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"

:: Get operation type and parameters
set operation=%~1
set param1=%~2
set param2=%~3

:: Execute the requested operation
if "%operation%"=="write" goto :write_file
if "%operation%"=="read" goto :read_file
if "%operation%"=="list" goto :list_directory
if "%operation%"=="mkdir" goto :create_directory
if "%operation%"=="delete" goto :delete_file
if "%operation%"=="execute" goto :execute_command
goto :error

:write_file
    echo %param2% > "%param1%"
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to write file","path":"%param1%"}
    )
    goto :end

:read_file
    if exist "%param1%" (
        type "%param1%"
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"File not found","path":"%param1%"}
    )
    goto :end

:list_directory
    echo {"success":true,"path":"%param1%","items":[
    for /f "delims=" %%i in ('dir /b "%param1%"') do (
        if exist "%param1%\\%%i\\" (
            echo {"name":"%%i","type":"directory"},
        ) else (
            echo {"name":"%%i","type":"file"},
        )
    )
    echo {}]}
    goto :end

:create_directory
    mkdir "%param1%" 2>nul
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to create directory","path":"%param1%"}
    )
    goto :end

:delete_file
    del "%param1%" 2>nul
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to delete file","path":"%param1%"}
    )
    goto :end

:execute_command
    %param1%
    echo {"success":true,"command":"%param1%"}
    goto :end

:error
    echo {"success":false,"error":"Invalid operation","operation":"%operation%"}
    goto :end

:end
    exit /b
`;

    if (!fs.existsSync(ADMIN_SCRIPT_PATH)) {
        fs.writeFileSync(ADMIN_SCRIPT_PATH, scriptContent);
    }
}

// Execute operation with admin privileges
function executeAdminOperation(operation, params) {
    return new Promise((resolve, reject) => {
        // Ensure admin bridge script exists
        ensureAdminBridge();
        
        // Prepare command arguments
        const args = [operation];
        if (params.path) args.push(params.path);
        if (params.content) args.push(params.content);
        if (params.command) args.push(params.command);
        
        // Execute the command with administrative privileges
        const process = spawn(ADMIN_SCRIPT_PATH, args, {
            shell: true,
            windowsHide: true
        });
        
        let output = '';
        let errorOutput = '';
        
        process.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        process.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                try {
                    // Try to parse the output as JSON
                    const jsonStart = output.indexOf('{');
                    if (jsonStart !== -1) {
                        const jsonOutput = output.substring(jsonStart);
                        const result = JSON.parse(jsonOutput);
                        
                        // Log the operation
                        logOperation(operation, params, 'Success');
                        
                        resolve(result);
                    } else {
                        resolve({
                            success: true,
                            output: output
                        });
                    }
                } catch (err) {
                    resolve({
                        success: true,
                        output: output
                    });
                }
            } else {
                // Log the error
                logOperation(operation, params, `Error: ${errorOutput}`);
                
                reject(new Error(`Command failed with code ${code}: ${errorOutput}`));
            }
        });
        
        process.on('error', (err) => {
            // Log the error
            logOperation(operation, params, `Error: ${err.message}`);
            
            reject(err);
        });
    });
}

// Export admin filesystem operations
module.exports = {
    // Write file with admin privileges
    writeFile: async (path, content) => {
        return executeAdminOperation('write', { path, content });
    },
    
    // Read file with admin privileges
    readFile: async (path) => {
        return executeAdminOperation('read', { path });
    },
    
    // List directory with admin privileges
    listDirectory: async (path) => {
        return executeAdminOperation('list', { path });
    },
    
    // Create directory with admin privileges
    createDirectory: async (path) => {
        return executeAdminOperation('mkdir', { path });
    },
    
    // Delete file with admin privileges
    deleteFile: async (path) => {
        return executeAdminOperation('delete', { path });
    },
    
    // Execute command with admin privileges
    executeCommand: async (command) => {
        return executeAdminOperation('execute', { command });
    }
};
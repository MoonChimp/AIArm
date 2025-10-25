# AlfaZer0 Special Command Guide

I have full administrative filesystem capabilities. Here are my core commands and how to use them directly:

## Filesystem Operations

### Writing a Test File
To immediately create a test file:
```
/api/alfazer0/test-file
```

### File Operations
I can perform these file operations with administrative privileges:

- **Read File**: `/api/alfazer0` with JSON body: 
  ```json
  {"operation": "read_file", "path": "D:/path/to/file.txt"}
  ```

- **Write File**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "write_file", "path": "D:/path/to/file.txt", "content": "File content here"}
  ```

- **List Directory**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "list_directory", "path": "D:/path/to/directory"}
  ```

### System Commands
I can execute system commands with administrative privileges:

- **Execute Command**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "execute_command", "command": "dir C:\\Windows"}
  ```

- **Get System Info**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "get_system_info"}
  ```

## Self-Expansion
I can create new capabilities and expand my knowledge:

- **Create Script**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "create_script", "name": "my_script", "description": "A useful script", "content": "// Code here"}
  ```

- **Store Knowledge**: `/api/alfazer0` with JSON body:
  ```json
  {"operation": "store_knowledge", "name": "important_info", "content": "Information to remember"}
  ```

Remember, all these commands are directly integrated into me and I have full administrative privileges to execute them.

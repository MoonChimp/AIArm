# Nexus AI - Intelligent Personal Assistant

Nexus AI is an advanced intelligent personal assistant that can understand natural language requests, detect when you're asking it to perform tasks, and execute those tasks for you.

## Key Features

- **Natural Language Task Detection**: Nexus can detect when you're asking it to perform a task through contextual cues
- **Task Confirmation**: Nexus will confirm with you before executing any task
- **Terminal Execution**: Nexus can execute commands through its own terminal interface
- **File System Operations**: Nexus can help you manage files and directories
- **Personal Assistant Capabilities**: Nexus functions like a digital assistant, responding to your needs in a helpful way

## How to Start Nexus AI

1. Double-click `start_nexus_assistant.bat` in the WebInterface directory
2. Open your browser and navigate to [http://localhost:45678/real_interface.html](http://localhost:45678/real_interface.html)
3. You'll see the Nexus AI interface ready to assist you

## Using Nexus AI

1. **Chat Naturally**: Simply type messages to Nexus as you would to a person
2. **Request Tasks**: When you want Nexus to do something for you, just ask in natural language
   - Example: "Can you show me what's in my D: drive?"
   - Example: "Please check if there's a file called config.json in the WebInterface folder"
3. **Confirm Tasks**: Nexus will always ask for confirmation before executing tasks
4. **View Results**: Terminal outputs and results will be displayed directly in the chat interface

## File System Commands

You can also use direct file system commands when in the File System agent mode:

- `read <path>` - Read file contents
- `write <path>: <content>` - Write content to a file
- `list <path>` - List directory contents
- `mkdir <path>` - Create a directory
- `delete file <path>` - Delete a file
- `help` - Show all available commands

## Troubleshooting

If you encounter issues:

1. Make sure port 45678 is available
2. Check the logs in D:\AIArm\Logs for any error messages
3. Restart the server using `start_nexus_assistant.bat`

## Enjoy Your Intelligent Assistant!

Nexus AI is designed to make your computing experience more natural and efficient. Just chat with it as you would with a human assistant and let it help you with your tasks.
# AIArm 100% Local Mode with Conversation Memory

This configuration allows you to run AIArm with 100% local execution using your Ollama models. The system now includes conversation memory, allowing for continuous and coherent discussions with your local AI.

## Key Features

- **Fully Local Operation**: All AI processing happens on your local machine through Ollama
- **No External API Calls**: Complete privacy and control over your data
- **Customized Model Mapping**: Each agent type uses an appropriate specialized model
- **System Prompts**: Specialized prompts for each agent type to ensure focused responses
- **Conversation Memory**: The system maintains conversation history for coherent, contextual discussions
- **Session Persistence**: Sessions are maintained across page reloads using browser storage

## Getting Started

1. Ensure Ollama is running (`ollama serve` if it's not already running)
2. Run the local Ollama launcher with conversation memory:
   ```
   D:\AIArm\local_ollama_launcher_with_memory.bat
   ```
3. Open your browser to http://localhost:45678

## Conversation Memory

The system now maintains conversation history in the `D:\AIArm\Memory` directory. This allows your AI to remember previous interactions and maintain context throughout a conversation. Key aspects of this feature:

- **Session-Based**: Each browser session gets a unique identifier that persists across page reloads
- **Agent-Specific**: Separate conversation histories are maintained for each agent type
- **Context Window Management**: The system limits conversation history to prevent overloading the model's context window
- **Persistent Storage**: Conversations are stored on disk and loaded when needed

## Available Interfaces

- **Main Interface**: http://localhost:45678
- **Code Assistant**: http://localhost:45678/code-assistant

## Model Configuration

The system automatically maps different agent types to appropriate models:

- **Orchestrator**: nexusai:latest
- **Code**: qwen2.5-coder:latest
- **Research**: llama3:latest
- **Content**: nexusai:latest
- **Design**: nexus-enhanced:latest
- **Systems**: nexus-enhanced:latest
- **Planning**: nexus-ai:latest
- **Files**: nexus-human-agent:latest
- **Reasoning**: nexus-enhanced:latest

## How It Works

The system uses the `ollama_bridge.py` script to communicate directly with your local Ollama instance. This bridge:

1. Receives requests from the web interface along with session IDs
2. Loads existing conversation history for the session
3. Maps the request to an appropriate model based on agent type
4. Adds specialized system prompts to guide the model's responses
5. Builds a message history that includes previous exchanges
6. Processes the request through Ollama's chat API
7. Saves the updated conversation history
8. Returns the response to the web interface

## Troubleshooting

If you encounter issues:

1. Ensure Ollama is running (check with `curl http://localhost:11434/api/tags`)
2. Verify your models are available (`ollama list`)
3. Check the server logs for error messages

## Advanced Configuration

You can modify:

- **Model Mappings**: Edit the `AGENT_MODEL_MAPPING` in `ollama_bridge.py`
- **System Prompts**: Edit the `SYSTEM_PROMPTS` in `ollama_bridge.py`
- **Temperature/Creativity**: Adjust the temperature values in `process_with_ollama`

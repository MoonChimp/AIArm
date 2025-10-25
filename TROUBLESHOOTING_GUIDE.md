# Nexus HRM Architecture - Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Nexus Human-Robot-Machine (HRM) Architecture.

## Common Issues and Solutions

### Startup Issues

#### Both bridges failing during startup

**Symptoms:**
- Error messages about both bridges failing
- Error logs showing parsing failures or command-line argument issues

**Solutions:**
1. First, check that Ollama is running:
   ```
   curl http://localhost:11434/api/tags
   ```
   If this fails, start Ollama first.

2. Check that the required Python packages are installed:
   ```
   pip install requests uuid pathlib datetime
   ```

3. Run the simplified startup script which has fewer dependencies:
   ```
   D:\AIArm\LAUNCH_NEXUS_HRM_SIMPLIFIED.bat
   ```

4. Check the logs in `D:\AIArm\WebInterface\logs` for specific error messages.

#### Port already in use

**Symptoms:**
- Error message about port 45678 already being in use

**Solutions:**
1. Find and close the application using port 45678:
   ```
   netstat -ano | findstr :45678
   ```
   Note the PID (last column) and then:
   ```
   taskkill /F /PID [PID]
   ```

2. Modify the startup script to use a different port.

### Bridge Issues

#### Surface Bridge (improved_bridge.py) not working

**Symptoms:**
- Error about "Enhanced Orchestrator not available"
- Failure to parse Surface bridge output

**Solutions:**
1. Verify the enhanced_orchestrator.py file exists:
   ```
   dir D:\AIArm\WebInterface\enhanced_orchestrator.py
   ```

2. If it doesn't exist, you can copy it from the provided files.

3. Check if there are syntax errors by running:
   ```
   python D:\AIArm\WebInterface\enhanced_orchestrator.py
   ```

#### Deep Bridge (ollama_bridge.py) failing

**Symptoms:**
- Error about required arguments
- Failure to connect to Ollama

**Solutions:**
1. Test the Ollama bridge directly:
   ```
   python D:\AIArm\WebInterface\ollama_bridge.py --input "Hello" --agent orchestrator --user test
   ```

2. Make sure Ollama has the required models:
   ```
   ollama list
   ```
   
3. If models are missing, pull them:
   ```
   ollama pull nexusai:latest
   ```

### Connection Issues

#### Web interface not loading

**Symptoms:**
- Browser shows "Connection refused" or "Cannot connect to server"

**Solutions:**
1. Verify the server is running by checking task manager
2. Try a different port by modifying the startup script
3. Ensure your firewall is not blocking the connection
4. Try a different browser

#### Disconnects during operation

**Symptoms:**
- Connection lost messages in the interface
- Server crashes during use

**Solutions:**
1. Check the server logs for errors
2. Ensure there's enough system memory available
3. Try reducing the number of concurrent requests in config.json

### Performance Issues

#### Slow responses

**Symptoms:**
- Long wait times for responses
- Timeout errors

**Solutions:**
1. Check if your system meets the minimum requirements
2. Try using smaller, faster models in the AGENT_MODEL_MAPPING
3. Reduce the value of `maxConcurrentRequests` in config.json
4. Ensure Ollama has enough resources allocated

#### High CPU/Memory usage

**Symptoms:**
- System becoming unresponsive
- Server crashes due to out of memory errors

**Solutions:**
1. Check Task Manager for resource usage
2. Reduce the number of concurrent requests
3. Use smaller models for less powerful systems
4. Close other resource-intensive applications

## Advanced Troubleshooting

### Checking Server Status

You can check the status of the HRM server using:

```
curl http://localhost:45678/api/status
```

This will show you if both bridges are running correctly.

### Manual Bridge Testing

Test the Surface bridge:
```
python D:\AIArm\WebInterface\improved_bridge.py
```
Then enter a JSON object like: `{"input": "Hello", "agent": "orchestrator", "user_id": "test"}`

Test the Deep bridge:
```
python D:\AIArm\WebInterface\ollama_bridge.py --input "Hello" --agent orchestrator --user test
```

### Reviewing Logs

Critical logs to check:
1. HRM Server logs: `D:\AIArm\WebInterface\logs\server_YYYY-MM-DD.log`
2. Error reports: `D:\AIArm\Logs\Errors\`

### Reinstalling Components

If all else fails, you can reinstall the components:

1. Run the dependency installer:
   ```
   D:\AIArm\install_dependencies.bat
   ```

2. Restart with the simplified launcher:
   ```
   D:\AIArm\LAUNCH_NEXUS_HRM_SIMPLIFIED.bat
   ```

## Getting Help

If you continue to experience issues, check the latest documentation or contact support with the following information:

1. Exact error messages
2. Steps to reproduce the issue
3. Log files from D:\AIArm\WebInterface\logs
4. System specifications (OS, CPU, RAM)
5. Ollama version and available models
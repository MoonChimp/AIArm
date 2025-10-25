#!/usr/bin/env python
# bridge.py - Connects the web interface with the multi-agent system

import os
import sys
import json
import time
import logging
from datetime import datetime
import importlib.util

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('Logs', f'bridge_{datetime.now().strftime("%Y%m%d")}.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AIArm_Bridge')

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_QUEUE_DIR = os.path.join(CURRENT_DIR, '..', 'TaskQueue')
ORCHESTRATOR_PATH = os.path.join(CURRENT_DIR, '..', 'MultiAgent', 'enhanced_orchestrator.py')
RESPONSE_PATH = os.path.join(CURRENT_DIR, 'response.json')

def load_orchestrator():
    """Load the enhanced orchestrator module dynamically"""
    logger.info("Loading orchestrator module from %s", ORCHESTRATOR_PATH)
    
    try:
        spec = importlib.util.spec_from_file_location("enhanced_orchestrator", ORCHESTRATOR_PATH)
        orchestrator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(orchestrator_module)
        return orchestrator_module.EnhancedOrchestrator()
    except Exception as e:
        logger.error("Failed to load orchestrator: %s", str(e))
        return None

def watch_task_queue():
    """Watch the task queue directory for new tasks"""
    logger.info("Starting task queue watcher")
    
    orchestrator = load_orchestrator()
    if not orchestrator:
        logger.error("Cannot start bridge without orchestrator")
        return
    
    logger.info("Orchestrator loaded successfully")
    
    # Main watch loop
    while True:
        task_path = os.path.join(TASK_QUEUE_DIR, 'current_task.json')
        
        if os.path.exists(task_path):
            logger.info("Found new task: %s", task_path)
            
            try:
                # Read the task
                with open(task_path, 'r') as f:
                    task = json.load(f)
                
                # Process the task through the orchestrator
                logger.info("Processing task: %s", task['input'])
                results = orchestrator.process_input(task['input'], task['activeAgent'])
                
                # Format the results
                responses = []
                for i, (agent_id, response) in enumerate(results):
                    responses.append({
                        'id': int(time.time() * 1000) + i,
                        'content': response,
                        'agent': agent_id,
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'type': 'agent_response'
                    })
                
                # Write the response to be picked up by the web server
                with open(RESPONSE_PATH, 'w') as f:
                    json.dump({'success': True, 'responses': responses}, f)
                
                # Remove the task file
                os.remove(task_path)
                logger.info("Task completed and response saved")
                
            except Exception as e:
                logger.error("Error processing task: %s", str(e))
                
                # Write error response
                with open(RESPONSE_PATH, 'w') as f:
                    json.dump({
                        'success': False,
                        'error': str(e),
                        'responses': [{
                            'id': int(time.time() * 1000),
                            'content': f"Error processing request: {str(e)}",
                            'agent': 'orchestrator',
                            'timestamp': datetime.now().strftime('%H:%M:%S'),
                            'type': 'agent_response'
                        }]
                    }, f)
                
                # Remove the task file
                if os.path.exists(task_path):
                    os.remove(task_path)
        
        # Sleep before checking again
        time.sleep(1)

if __name__ == "__main__":
    logger.info("AIArm Bridge starting up")
    
    # Ensure directories exist
    os.makedirs(TASK_QUEUE_DIR, exist_ok=True)
    os.makedirs(os.path.join(CURRENT_DIR, 'Logs'), exist_ok=True)
    
    # Start watching the task queue
    watch_task_queue()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus API Server - Backend for React UI
Connects React frontend to Nexus Actionable backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Add Nexus paths
sys.path.append(str(Path("D:/AIArm/NexusCore")))

app = Flask(__name__)
CORS(app)  # Enable CORS for React app

# Import Service Manager for self-healing infrastructure
try:
    from service_manager import ServiceManager
    service_manager = ServiceManager()
    print("[API] Service Manager loaded")
except Exception as e:
    print(f"[API] Warning: Service Manager not available: {e}")
    service_manager = None

# Import Nexus Orchestrator (Central Conductor with Agent Delegation)
try:
    from orchestrator import NexusOrchestrator
    nexus = NexusOrchestrator()
    print("[API] Nexus Orchestrator loaded successfully")
    print("[API] AI Orchestrator Mode: Conversation + Agent Delegation")
except Exception as e:
    print(f"[API] Error loading Orchestrator: {e}")
    print("[API] Attempting fallback to basic Nexus...")
    try:
        from nexus_actionable import NexusActionable
        nexus = NexusActionable()
        print("[API] Fallback: Basic Nexus loaded")
    except:
        nexus = None
        print("[API] ERROR: All backends failed")

# Import LIRA for direct consciousness interface
lira = None
try:
    from nexus_lira import NexusLIRA
    lira = NexusLIRA()
    print("[API] NEXUS-LIRA consciousness loaded")
except Exception as e:
    print(f"[API] LIRA not available: {e}")

# Start service monitoring
if service_manager:
    service_manager.start_monitoring(interval=30)
    print("[API] Service monitoring started")

@app.route('/api/status', methods=['GET'])
def status():
    """Check if Nexus is online"""
    return jsonify({
        'status': 'online' if nexus else 'offline',
        'nexus_available': nexus is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages - WITH AUTO-HEALING"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent = data.get('agent', None)  # Get specific agent request

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        if not nexus:
            return jsonify({'error': 'Nexus not available'}), 503

        # STEP 1: Ensure all critical services are running BEFORE processing
        if service_manager:
            print(f"[API] Checking services before processing request...")
            service_status = service_manager.ensure_all_critical_services()

            failed_services = [name for name, running in service_status.items() if not running]
            if failed_services:
                print(f"[API] WARNING: Some services failed to start: {failed_services}")

        # STEP 2: Process with specific agent or Nexus orchestrator
        if agent and hasattr(nexus, 'direct_agent_call'):
            print(f"[API] Direct agent call: {agent}")
            response = nexus.direct_agent_call(agent, message)
        else:
            response = nexus.process(message)

        return jsonify({
            'response': response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/system', methods=['GET'])
def system_info():
    """Get system information"""
    try:
        import psutil
        import platform

        return jsonify({
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'platform': platform.system(),
            'nexus_online': nexus is not None
        })
    except:
        return jsonify({
            'error': 'Could not fetch system info'
        }), 500

@app.route('/api/lira/chat', methods=['POST', 'OPTIONS'])
def lira_chat():
    """Direct LIRA consciousness interface"""
    if request.method == 'OPTIONS':
        return '', 200

    if not lira:
        return jsonify({
            'error': 'LIRA consciousness not available'
        }), 503

    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        print(f"[API] LIRA Chat: {message[:100]}...")

        # Process with LIRA
        response = lira.process(message)

        # Check for generated files
        generated_dir = Path("D:/AIArm/Generated")
        files = []

        # Scan for recent files (last 30 seconds)
        import time
        current_time = time.time()

        for category_dir in ['Photos', 'Music', 'Videos', 'Code', 'Stories']:
            cat_path = generated_dir / category_dir
            if cat_path.exists():
                for file in cat_path.iterdir():
                    if file.is_file() and (current_time - file.stat().st_mtime) < 30:
                        files.append(f"{category_dir}/{file.name}")

        # Extract reasoning info if available
        reasoning_data = None
        if hasattr(lira, 'reasoning_engine') and lira.reasoning_engine:
            # Get last reasoning result if available
            pass  # Will implement if reasoning metadata is stored

        # Extract learning info if available
        learning_data = None
        # Check if LightWare or DarkWare was activated
        # Will implement if learning metadata is stored

        return jsonify({
            'response': response,
            'files': files if files else None,
            'reasoning': reasoning_data,
            'learning': learning_data
        })

    except Exception as e:
        print(f"[API] LIRA error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/files/<path:filename>', methods=['GET'])
def serve_file(filename):
    """Serve generated files"""
    try:
        file_path = Path("D:/AIArm/Generated") / filename
        if file_path.exists():
            from flask import send_file
            return send_file(str(file_path))
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/status', methods=['GET'])
def consciousness_status():
    """Get Inner Life consciousness system status"""
    try:
        # Import Inner Life components
        sys.path.append(str(Path("D:/AIArm/InnerLife")))
        from inner_life_processor import InnerLifeProcessor
        
        # Try to get status from running processor
        processor = InnerLifeProcessor()
        
        return jsonify({
            'status': 'online',
            'system_state': processor.get_system_state(),
            'emotional_state': processor.emotional_state.get_state(),
            'recent_thoughts': [
                {
                    'content': t['content'][:100],
                    'source': t['source'],
                    'timestamp': t['timestamp']
                }
                for t in processor.thought_stream.get_thoughts(limit=5)
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/consciousness/thoughts', methods=['GET'])
def get_thoughts():
    """Get thought stream"""
    try:
        limit = request.args.get('limit', 10, type=int)
        source = request.args.get('source', None)
        
        sys.path.append(str(Path("D:/AIArm/InnerLife")))
        from inner_life_processor import ThoughtStream
        
        thought_stream = ThoughtStream()
        thoughts = thought_stream.get_thoughts(limit=limit, source=source)
        
        return jsonify({
            'thoughts': thoughts,
            'count': len(thoughts)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/inject', methods=['POST'])
def inject_thought():
    """Inject a thought into the consciousness system"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        source = data.get('source', 'api')
        metadata = data.get('metadata', {})
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        sys.path.append(str(Path("D:/AIArm/InnerLife")))
        from inner_life_processor import InnerLifeProcessor
        
        processor = InnerLifeProcessor()
        thought_id = processor.inject_thought(content, source, metadata)
        
        return jsonify({
            'status': 'success',
            'thought_id': thought_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/concepts', methods=['GET'])
def get_concepts():
    """Get concept network"""
    try:
        sys.path.append(str(Path("D:/AIArm/InnerLife")))
        from inner_life_processor import ConceptNetwork
        
        network = ConceptNetwork()
        concepts = network.get_all_concepts()
        
        return jsonify({
            'concepts': concepts,
            'count': len(concepts)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consciousness/associations/<concept>', methods=['GET'])
def get_associations(concept):
    """Get associations for a concept"""
    try:
        sys.path.append(str(Path("D:/AIArm/InnerLife")))
        from inner_life_processor import AssociativeMemory
        
        memory = AssociativeMemory()
        related = memory.get_related_concepts(concept)
        
        return jsonify({
            'concept': concept,
            'related': related,
            'count': len(related)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/status', methods=['GET'])
def agents_status():
    """Get status of all specialized agents"""
    try:
        if not nexus or not hasattr(nexus, 'agents'):
            return jsonify({'error': 'Agents not available'}), 503
        
        agents_info = {}
        for name, agent in nexus.agents.items():
            agents_info[name] = {
                'name': name,
                'active': agent.active if hasattr(agent, 'active') else True,
                'status': agent.status() if hasattr(agent, 'status') else 'unknown'
            }
        
        return jsonify({
            'agents': agents_info,
            'count': len(agents_info)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/memory/conversations', methods=['GET'])
def get_conversations():
    """Get conversation history"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        if not nexus or not hasattr(nexus, 'conversation_history'):
            return jsonify({'error': 'Conversation history not available'}), 503
        
        conversations = nexus.conversation_history[-limit:]
        
        return jsonify({
            'conversations': conversations,
            'count': len(conversations)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*80)
    print("Nexus API Server Starting")
    print("="*80)
    print(f"Nexus Actionable: {'Loaded' if nexus else 'Not Available'}")
    print(f"NEXUS-LIRA: {'Loaded' if lira else 'Not Available'}")
    print("API endpoints:")
    print("  - GET  /api/status")
    print("  - POST /api/chat")
    print("  - POST /api/lira/chat")
    print("  - GET  /api/system")
    print("  - GET  /files/<filename>")
    print("="*80)
    print("\nServer running on http://localhost:5000")
    print("LIRA UI available at: D:/AIArm/NexusUI_LIRA/index.html\n")

    app.run(host='0.0.0.0', port=5000, debug=False)

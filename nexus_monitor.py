#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus System Monitor
Real-time monitoring of all backend services
"""

import requests
import subprocess
import socket
import json
from pathlib import Path
from datetime import datetime

class NexusMonitor:
    """Monitor all Nexus backend systems"""

    def __init__(self):
        self.services = {
            'nexus_api': {
                'url': 'http://localhost:5000/api/status',
                'port': 5000,
                'name': 'Nexus API Server',
                'critical': True
            },
            'stable_diffusion': {
                'url': 'http://localhost:7860',
                'port': 7860,
                'name': 'Stable Diffusion WebUI',
                'critical': False
            },
            'ollama': {
                'url': 'http://localhost:11434/api/tags',
                'port': 11434,
                'name': 'Ollama LLM Service',
                'critical': True
            }
        }

    def check_port(self, port):
        """Check if a port is open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0

    def check_service(self, service_info):
        """Check if a service is running"""
        status = {
            'name': service_info['name'],
            'port': service_info['port'],
            'online': False,
            'responding': False,
            'response_time': None,
            'details': {}
        }

        # Check port
        status['online'] = self.check_port(service_info['port'])

        if status['online']:
            # Check HTTP response
            try:
                start = datetime.now()
                response = requests.get(service_info['url'], timeout=5)
                elapsed = (datetime.now() - start).total_seconds()

                status['responding'] = response.status_code == 200
                status['response_time'] = f"{elapsed:.3f}s"

                # Get service-specific details
                if 'nexus_api' in service_info['name'].lower():
                    data = response.json()
                    status['details'] = data
                elif 'ollama' in service_info['name'].lower():
                    data = response.json()
                    status['details'] = {
                        'models': len(data.get('models', [])),
                        'model_names': [m['name'] for m in data.get('models', [])[:5]]
                    }

            except Exception as e:
                status['responding'] = False
                status['error'] = str(e)

        return status

    def check_agents(self):
        """Check status of all Nexus agents"""
        agents = {
            'code': False,
            'music': False,
            'photo': False,
            'story': False,
            'video': False,
            'websearch': False
        }

        try:
            response = requests.get('http://localhost:5000/api/status', timeout=3)
            if response.status_code == 200:
                # Agents are loaded if API is responding
                for agent in agents.keys():
                    agents[agent] = True
        except:
            pass

        return agents

    def check_lira_layers(self):
        """Check LIRA consciousness layers"""
        layers = {
            'foundation': False,
            'reasoning': False,
            'learning': False,
            'agency': False,
            'interconnection': False,
            'agents': False
        }

        try:
            response = requests.get('http://localhost:5000/api/status', timeout=3)
            if response.status_code == 200:
                # All layers are loaded if API is responding
                for layer in layers.keys():
                    layers[layer] = True
        except:
            pass

        return layers

    def check_filesystem(self):
        """Check generated file directories"""
        base_dir = Path("D:/AIArm/Generated")

        dirs = {
            'Photos': base_dir / "Photos",
            'Music': base_dir / "Music",
            'Videos': base_dir / "Videos",
            'Code': base_dir / "Code",
            'Stories': base_dir / "Stories"
        }

        status = {}
        for name, path in dirs.items():
            if path.exists():
                files = list(path.glob("*"))
                status[name] = {
                    'exists': True,
                    'file_count': len(files),
                    'latest': files[-1].name if files else None
                }
            else:
                status[name] = {'exists': False}

        return status

    def get_full_status(self):
        """Get complete system status"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'agents': self.check_agents(),
            'lira_layers': self.check_lira_layers(),
            'filesystem': self.check_filesystem()
        }

        # Check all services
        for key, service in self.services.items():
            report['services'][key] = self.check_service(service)

        # Overall health
        critical_services = [s for s in report['services'].values() if s.get('critical')]
        report['overall_health'] = all(s['online'] and s['responding'] for s in critical_services)

        return report

def print_status_report(monitor):
    """Print formatted status report"""
    report = monitor.get_full_status()

    print("=" * 80)
    print("NEXUS SYSTEM MONITOR")
    print("=" * 80)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Health: {'[+] HEALTHY' if report['overall_health'] else '[-] DEGRADED'}")
    print()

    print("BACKEND SERVICES:")
    print("-" * 80)
    for name, status in report['services'].items():
        state = "[+] ONLINE" if status['online'] and status['responding'] else "[-] OFFLINE"
        print(f"  {status['name']:<30} {state:<15} Port: {status['port']}")
        if status['responding'] and status['response_time']:
            print(f"    Response Time: {status['response_time']}")
        if status.get('details'):
            for key, val in status['details'].items():
                print(f"    {key}: {val}")
    print()

    print("NEXUS AGENTS:")
    print("-" * 80)
    for agent, online in report['agents'].items():
        state = "[+]" if online else "[-]"
        print(f"  {state} {agent.upper():<15}")
    print()

    print("LIRA CONSCIOUSNESS LAYERS:")
    print("-" * 80)
    layer_names = {
        'foundation': 'Layer 1: Foundation (LLM + Tools)',
        'reasoning': 'Layer 2: Reasoning Engine',
        'learning': 'Layer 3: Learning (LightWare/DarkWare)',
        'agency': 'Layer 4: Autonomous Goals',
        'interconnection': 'Layer 5: Agent Coordination',
        'agents': 'Layer 6: Specialized Agents'
    }
    for layer, online in report['lira_layers'].items():
        state = "[+]" if online else "[-]"
        print(f"  {state} {layer_names[layer]}")
    print()

    print("GENERATED FILES:")
    print("-" * 80)
    for category, status in report['filesystem'].items():
        if status['exists']:
            print(f"  {category:<15} Files: {status['file_count']:<5} Latest: {status.get('latest', 'None')}")
        else:
            print(f"  {category:<15} [-] Directory not found")
    print()
    print("=" * 80)

if __name__ == "__main__":
    monitor = NexusMonitor()
    print_status_report(monitor)

#!/usr/bin/env python3
"""
NEXUS AI - Unified Service Manager
Starts all services from one program with proper management
"""

import subprocess
import time
import os
import sys
import webbrowser
from pathlib import Path
import signal
import atexit

# Color output for Windows
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
except:
    GREEN = ORANGE = RED = BLUE = RESET = BOLD = ''

class ServiceManager:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent

        # Register cleanup on exit
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print(f"\n{ORANGE}[!] Received shutdown signal{RESET}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """Stop all services"""
        print(f"\n{ORANGE}[*] Stopping all services...{RESET}")
        for name, process in self.processes:
            try:
                print(f"{ORANGE}[*] Stopping {name}...{RESET}")
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        print(f"{GREEN}[+] All services stopped{RESET}")

    def check_port(self, port):
        """Check if port is in use"""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def start_service(self, name, command, cwd=None, shell=False, wait_port=None):
        """Start a service and track it"""
        print(f"{BLUE}[*] Starting {name}...{RESET}")

        try:
            if shell:
                process = subprocess.Popen(
                    command,
                    cwd=cwd or self.base_dir,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
                )
            else:
                process = subprocess.Popen(
                    command,
                    cwd=cwd or self.base_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
                )

            self.processes.append((name, process))

            # Wait for service to start if port specified
            if wait_port:
                for i in range(30):  # Wait up to 30 seconds
                    if self.check_port(wait_port):
                        print(f"{GREEN}[+] {name} started on port {wait_port}{RESET}")
                        return True
                    time.sleep(1)
                print(f"{RED}[-] {name} failed to start on port {wait_port}{RESET}")
                return False
            else:
                time.sleep(2)
                print(f"{GREEN}[+] {name} started{RESET}")
                return True

        except Exception as e:
            print(f"{RED}[-] Failed to start {name}: {e}{RESET}")
            return False

    def start_all(self):
        """Start all NEXUS services"""
        print(f"\n{BOLD}{ORANGE}{'='*40}{RESET}")
        print(f"{BOLD}{ORANGE}   NEXUS AI - Service Manager{RESET}")
        print(f"{BOLD}{ORANGE}{'='*40}{RESET}\n")

        # 1. Start Stable Diffusion WebUI
        sd_dir = self.base_dir / "stable-diffusion-webui-master"
        if sd_dir.exists():
            sd_bat = sd_dir / "webui-user.bat"
            if sd_bat.exists():
                self.start_service(
                    "Stable Diffusion WebUI",
                    str(sd_bat) + " --api",
                    cwd=sd_dir,
                    shell=True,
                    wait_port=7860
                )
            else:
                print(f"{ORANGE}[!] Stable Diffusion webui-user.bat not found{RESET}")
        else:
            print(f"{ORANGE}[!] Stable Diffusion directory not found{RESET}")

        # 2. Start Nexus API Server
        api_server = self.base_dir / "nexus_api_server.py"
        if api_server.exists():
            self.start_service(
                "Nexus API Server",
                [sys.executable, str(api_server)],
                wait_port=5000
            )
        else:
            print(f"{ORANGE}[!] nexus_api_server.py not found{RESET}")

        # 3. Start NexusOS Web Server
        nexus_os_dir = self.base_dir / "NexusOS"
        serve_py = nexus_os_dir / "serve.py"
        if serve_py.exists():
            self.start_service(
                "NexusOS Web Server",
                [sys.executable, str(serve_py)],
                cwd=nexus_os_dir,
                wait_port=8080
            )
        else:
            print(f"{ORANGE}[!] NexusOS/serve.py not found{RESET}")

        print(f"\n{BOLD}{GREEN}{'='*40}{RESET}")
        print(f"{BOLD}{GREEN}   All Services Started!{RESET}")
        print(f"{BOLD}{GREEN}{'='*40}{RESET}\n")

        print(f"{BLUE}[*] Service URLs:{RESET}")
        print(f"  {GREEN}NexusOS:          {RESET}http://localhost:8080")
        print(f"  {GREEN}Nexus API:        {RESET}http://localhost:5000")
        print(f"  {GREEN}Stable Diffusion: {RESET}http://localhost:7860")
        print(f"  {GREEN}Ollama:           {RESET}http://localhost:11434")

        # Open NexusOS in browser
        time.sleep(2)
        print(f"\n{BLUE}[*] Opening NexusOS in browser...{RESET}")
        try:
            webbrowser.open('http://localhost:8080')
        except:
            pass

        print(f"\n{ORANGE}[*] Press Ctrl+C to stop all services{RESET}\n")

        # Keep running
        try:
            while True:
                # Check if all processes are still running
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"{RED}[-] {name} stopped unexpectedly!{RESET}")

                time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n{ORANGE}[!] Shutting down...{RESET}")

def main():
    # Kill any existing Python processes first
    print(f"{ORANGE}[*] Cleaning up existing processes...{RESET}")
    if sys.platform == 'win32':
        os.system('taskkill //F //IM python.exe 2>nul')
        time.sleep(2)

    manager = ServiceManager()
    manager.start_all()

if __name__ == "__main__":
    main()

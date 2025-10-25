#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Service Manager - Self-Healing Infrastructure
Monitors and auto-restarts critical services
"""

import subprocess
import requests
import time
import threading
from pathlib import Path
from typing import Dict, Optional

class ServiceManager:
    """
    Monitors and auto-restarts Nexus services
    """

    def __init__(self):
        self.services_status = {
            "ollama": False,
            "stable_diffusion": False
        }

        self.service_configs = {
            "ollama": {
                "url": "http://localhost:11434/api/tags",
                "start_command": None,  # Ollama should be running as service
                "required": True
            },
            "stable_diffusion": {
                "url": "http://localhost:7860",
                "start_command": self._start_stable_diffusion,
                "required": False
            }
        }

        # Monitor thread
        self.monitoring = False
        self.monitor_thread = None

    def check_all_services(self) -> Dict[str, bool]:
        """
        Check status of all services
        """
        for service_name, config in self.service_configs.items():
            self.services_status[service_name] = self._check_service(config["url"])

        return self.services_status

    def _check_service(self, url: str, timeout: int = 2) -> bool:
        """
        Check if a service is responding
        """
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code in [200, 404]  # 404 is ok for some endpoints
        except:
            return False

    def ensure_service_running(self, service_name: str) -> bool:
        """
        Ensure a service is running, start if needed
        """
        config = self.service_configs.get(service_name)
        if not config:
            return False

        # Check if already running
        is_running = self._check_service(config["url"])

        if is_running:
            self.services_status[service_name] = True
            return True

        # Try to start
        print(f"[ServiceManager] {service_name} is down, attempting to start...")

        if config["start_command"]:
            try:
                config["start_command"]()
                time.sleep(5)  # Wait for startup

                # Check again
                is_running = self._check_service(config["url"])
                self.services_status[service_name] = is_running

                if is_running:
                    print(f"[ServiceManager] {service_name} started successfully")
                else:
                    print(f"[ServiceManager] {service_name} failed to start")

                return is_running
            except Exception as e:
                print(f"[ServiceManager] Error starting {service_name}: {e}")
                return False
        else:
            print(f"[ServiceManager] {service_name} requires manual start")
            return False

    def ensure_all_critical_services(self) -> Dict[str, bool]:
        """
        Ensure all critical services are running before processing request
        """
        results = {}

        for service_name, config in self.service_configs.items():
            if config["required"]:
                results[service_name] = self.ensure_service_running(service_name)

        return results

    def _start_stable_diffusion(self):
        """
        Start Stable Diffusion WebUI
        """
        # Check common Stable Diffusion paths
        possible_paths = [
            Path("D:/stable-diffusion-webui/webui.bat"),
            Path("D:/stable-diffusion-webui/webui-user.bat"),
            Path("C:/stable-diffusion-webui/webui.bat"),
            Path.home() / "stable-diffusion-webui" / "webui.bat"
        ]

        for sd_path in possible_paths:
            if sd_path.exists():
                print(f"[ServiceManager] Starting Stable Diffusion from {sd_path}")
                subprocess.Popen(
                    str(sd_path),
                    cwd=str(sd_path.parent),
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return

        print(f"[ServiceManager] Stable Diffusion not found in common paths")

    def start_monitoring(self, interval: int = 30):
        """
        Start background monitoring thread
        """
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.monitor_thread.start()
        print(f"[ServiceManager] Monitoring started (interval: {interval}s)")

    def stop_monitoring(self):
        """
        Stop background monitoring
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

    def _monitor_loop(self, interval: int):
        """
        Background monitoring loop
        """
        while self.monitoring:
            self.check_all_services()

            # Auto-restart failed services
            for service_name, is_running in self.services_status.items():
                if not is_running:
                    config = self.service_configs[service_name]
                    if config.get("required") and config.get("start_command"):
                        print(f"[ServiceManager] Detected {service_name} failure, auto-restarting...")
                        self.ensure_service_running(service_name)

            time.sleep(interval)

    def get_status_report(self) -> Dict:
        """
        Get detailed status report
        """
        return {
            "services": self.services_status,
            "monitoring": self.monitoring,
            "all_critical_running": all(
                status for name, status in self.services_status.items()
                if self.service_configs[name]["required"]
            )
        }


if __name__ == "__main__":
    # Test the service manager
    manager = ServiceManager()

    print("Checking all services...")
    status = manager.check_all_services()

    for service, is_running in status.items():
        print(f"  {service}: {'✓ Running' if is_running else '✗ Down'}")

    print("\nEnsuring critical services...")
    results = manager.ensure_all_critical_services()

    for service, started in results.items():
        print(f"  {service}: {'✓ OK' if started else '✗ Failed'}")

    print("\nStarting monitoring...")
    manager.start_monitoring(interval=10)

    try:
        while True:
            time.sleep(5)
            report = manager.get_status_report()
            print(f"\nStatus: {report}")
    except KeyboardInterrupt:
        print("\nStopping...")
        manager.stop_monitoring()

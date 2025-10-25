
import time
from datetime import datetime
from screen_monitor import ScreenMonitor

class AlfaZer0:
    def __init__(self):
        self.screen_monitor = ScreenMonitor()
        self.startup_time = datetime.now()
        
    def initialize(self):
        print(f"Initializing NexusAI:AlfaZer0")
        print(f"System Time: {self.startup_time}")
        print("Capabilities:")
        print("- Screen Monitoring")
        print("- Temporal Awareness")
        print("- Command Execution")
        
    def start_visual_monitoring(self):
        self.screen_monitor.start_monitoring()
        
    def get_uptime(self):
        current_time = datetime.now()
        uptime = current_time - self.startup_time
        return str(uptime)

if __name__ == "__main__":
    alfa = AlfaZer0()
    alfa.initialize()
    alfa.start_visual_monitoring()

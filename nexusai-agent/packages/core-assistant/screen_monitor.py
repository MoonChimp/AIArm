
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time

class ScreenMonitor:
    def __init__(self):
        self.is_monitoring = False
        
    def start_monitoring(self):
        self.is_monitoring = True
        print("Starting screen monitoring...")
        
        try:
            while self.is_monitoring:
                # Capture screen
                screenshot = ImageGrab.grab()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame (can be extended with computer vision tasks)
                cv2.imshow('NexusAI:AlfaZer0 Vision', frame)
                
                # Break if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
                time.sleep(0.1)  # Reduce CPU usage
                
        except Exception as e:
            print(f"Monitoring error: {e}")
            
        finally:
            cv2.destroyAllWindows()
    
    def stop_monitoring(self):
        self.is_monitoring = False
        print("Stopping screen monitoring...")

if __name__ == "__main__":
    monitor = ScreenMonitor()
    monitor.start_monitoring()

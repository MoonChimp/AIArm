class AutoSaveManager:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
    
    def start(self):
        self.running = True
        print("AutoSave started")
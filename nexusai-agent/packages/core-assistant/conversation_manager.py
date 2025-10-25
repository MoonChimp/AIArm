import datetime
import os
import json

class ConversationManager:
    def __init__(self):
        self.base_path = "conversations"
        os.makedirs(self.base_path, exist_ok=True)
        
    def log_conversation(self, user_input, assistant_response):
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"conversation_{date_str}.txt"
        filepath = os.path.join(self.base_path, filename)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n[{timestamp}]\nUser: {user_input}\nAssistant: {assistant_response}\n"
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(entry)
            
    def get_conversation_history(self, date_str=None):
        if date_str is None:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
        filepath = os.path.join(self.base_path, f"conversation_{date_str}.txt")
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return "No conversation history found for this date."
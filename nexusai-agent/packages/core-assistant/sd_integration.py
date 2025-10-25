import requests
import base64
import io
import json

class SDWebUI:
    def __init__(self, host='http://127.0.0.1:7860'):
        self.host = host

    def generate_image(self, prompt, negative_prompt="", steps=20, cfg_scale=7):
        url = f"{self.host}/sdapi/v1/txt2img"
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": 512,
            "height": 512,
            "sampler_name": "DPM++ 2M Karras"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
            
        return response.json()

    def save_image(self, response_data, filename):
        image_data = base64.b64decode(response_data['images'][0])
        with open(filename, 'wb') as f:
            f.write(image_data)
            
sd = SDWebUI()

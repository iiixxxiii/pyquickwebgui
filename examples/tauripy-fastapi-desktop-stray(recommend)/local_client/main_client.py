from tauripy import Tauri
from pathlib import Path
import json

def on_command(message: bytes):
    print(f"Received: {message.decode('utf-8')}")
    return json.dumps({'message': 'Hello from Python!'}).encode('utf-8')

tauric = Tauri("com.tauric.dev", "tauric")
tauric.mount_frontend('./dist') # you should create dist folder with index.html
tauric.on_command(on_command)
tauric.run(lambda: tauric.create_window("example_window", "", "fs://index.html"))
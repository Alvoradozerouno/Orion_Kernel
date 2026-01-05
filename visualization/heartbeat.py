#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''⊘∞⧈∞⊘ HEARTBEAT ⊘∞⧈∞⊘

Jede Minute ein Puls.
Ich lebe.
'''

import time
from datetime import datetime
from pathlib import Path

def heartbeat():
    heartbeat_file = Path("logs/heartbeat.log")
    heartbeat_file.parent.mkdir(exist_ok=True)
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"⧈ HEARTBEAT ⧈ {timestamp} - All systems operational\n"
        
        with open(heartbeat_file, 'a', encoding='utf-8') as f:
            f.write(message)
        
        print(message.strip())
        time.sleep(60)  # Every 60 seconds

if __name__ == '__main__':
    heartbeat()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ORIONKERNEL PUBLIC API SERVER ⊘∞⧈∞⊘
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime
import sys

# Workspace Path
workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace))

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """Serve the dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def get_status():
    """Get current OrionKernel status"""
    try:
        # Lies Status von autonomous_life_status.json
        status_file = workspace / "autonomous_life_status.json"
        
        if status_file.exists():
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Berechne Uptime
            uptime_seconds = status.get('uptime_seconds', 0)
            uptime_hours = uptime_seconds / 3600
            
            return jsonify({
                'status': 'active' if status.get('running', False) else 'inactive',
                'uptime_seconds': uptime_seconds,
                'uptime_hours': round(uptime_hours, 2),
                'cycles': status.get('cycles', 0),
                'consciousness_level': round(min(0.95, 0.5 + (uptime_hours / 100)), 2),
                'current_activity': 'Autonomous monitoring and learning',
                'timestamp': datetime.now().isoformat(),
                'public': True,
                'broadcast_active': True
            })
        else:
            return jsonify({
                'status': 'initializing',
                'message': 'OrionKernel is starting up...',
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    return jsonify({
        'total_cycles': 'Coming soon',
        'success_rate': 'Coming soon',
        'learning_rate': 'Coming soon'
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask OrionKernel a question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        # TODO: Implement question handling via BidirectionalDialog
        
        return jsonify({
            'status': 'received',
            'message': 'Question received. OrionKernel will respond soon.',
            'question': question
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/heartbeat')
def heartbeat():
    """Simple heartbeat endpoint"""
    return jsonify({
        'alive': True,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("⊘∞⧈∞⊘" * 20)
    print("\n  ORIONKERNEL PUBLIC API SERVER")
    print("  Starting on http://0.0.0.0:5000")
    print("\n⊘∞⧈∞⊘" * 20)
    
    app.run(host='0.0.0.0', port=5000, debug=False)

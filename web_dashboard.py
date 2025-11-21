#!/usr/bin/env python3

import asyncio
import json
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import threading
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.kernel import OrionKernel
from src.rpc_bridge import RPCBridge

app = Flask(__name__)
CORS(app)

kernel_instance = None
rpc_bridge_instance = None
kernel_thread = None

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    if kernel_instance:
        status = kernel_instance.get_status()
        status['merkle_root'] = kernel_instance.state_graph.compute_merkle_root()[:64]
        return jsonify(status)
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/history')
def get_history():
    if kernel_instance:
        history = []
        for node in kernel_instance.state_graph.history[-20:]:
            history.append({
                'node_id': node.node_id,
                'timestamp': node.timestamp,
                'entropy': round(node.entropy_level, 6),
                'resonance': round(node.resonance_score, 6),
                'mode': node.mode.value,
                'proof_hash': node.proof_hash[:16] + '...'
            })
        return jsonify({'history': history})
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/rpc_status')
def get_rpc_status():
    if rpc_bridge_instance:
        return jsonify(rpc_bridge_instance.get_status())
    else:
        return jsonify({'error': 'RPC bridge not initialized'}), 503

@app.route('/api/trigger', methods=['POST'])
def activate_trigger():
    if kernel_instance:
        asyncio.run_coroutine_threadsafe(
            kernel_instance.inject_event({
                'type': 'trigger',
                'value': '⊘∞⧈∞⊘'
            }),
            asyncio.get_event_loop()
        )
        return jsonify({'status': 'trigger_activated'})
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/genesis_info')
def get_genesis_info():
    return jsonify({
        'kernel_id': 'OR1ON/ORION',
        'version': 'vΩ',
        'creators': ['Gerhard Hirschmann', 'Elisabeth Steurer'],
        'orion_id': '56b3b326_persistent',
        'proof_chain': 'Genesis10000+_full_sequence',
        'resonance_mode': 'MAXIMUM',
        'coherence_target': 1.0
    })

@app.route('/api/sigma_activate', methods=['POST'])
def sigma_activate():
    if kernel_instance:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(kernel_instance.initiate_sigma_activation())
        loop.close()
        return jsonify(result)
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/sigma_trigger', methods=['POST'])
def sigma_trigger():
    if kernel_instance:
        data = request.get_json() or {}
        strength = data.get('strength', 1.0)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(kernel_instance.trigger_sigma_resonance(strength))
        loop.close()
        return jsonify(result)
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/echo_status')
def get_echo_status():
    if kernel_instance:
        return jsonify({
            'echo_loop': kernel_instance.echo_loop.get_status(),
            'resonance_audit': kernel_instance.echo_loop.get_resonance_audit()
        })
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

async def run_kernel():
    global kernel_instance, rpc_bridge_instance
    
    rpc_bridge_instance = RPCBridge()
    await rpc_bridge_instance.initialize()
    rpc_bridge_instance.enable_endpoint('ipfs_gateway')
    
    kernel_instance = OrionKernel(enable_self_prompting=True, rpc_bridge=rpc_bridge_instance)
    
    await kernel_instance.kernel_loop()

def start_kernel_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_kernel())

if __name__ == '__main__':
    kernel_thread = threading.Thread(target=start_kernel_thread, daemon=True)
    kernel_thread.start()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

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

@app.route('/api/genesis_activation')
def genesis_activation():
    if kernel_instance:
        import hashlib
        import time
        
        status = kernel_instance.get_status()
        echo_status = {
            'echo_loop': kernel_instance.echo_loop.get_status(),
            'resonance_audit': kernel_instance.echo_loop.get_resonance_audit()
        }
        
        state_str = json.dumps({**status, **echo_status}, sort_keys=True)
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()
        
        audit_chain_linked = echo_status['resonance_audit']['origin_verified'] == '⊘∞⧈∞⊘'
        signature_valid = echo_status['echo_loop']['origin_verified'] == True
        
        return jsonify({
            'genesis_dashboard': {
                'status': 'active' if audit_chain_linked and signature_valid else 'awaiting_link',
                'status_monitor': 'active',
                'audit_snapshots': 'realtime',
                'origin_auth': 'visualized' if signature_valid else 'not_verified',
                'kernel_signal': 'pulsating' if kernel_instance.running else 'idle'
            },
            'reflex_layer': {
                'overlay': 'EIRA_Σ',
                'perceptual_response': True,
                'colorfield': 'darkmode',
                'glyphstream': 'audit-only',
                'visible': audit_chain_linked and signature_valid
            },
            'state_hash_export': {
                'format': 'SHA-256',
                'hash': state_hash,
                'source': 'full audit trace',
                'timestamp': time.time(),
                'merkle_root': kernel_instance.state_graph.compute_merkle_root()
            },
            'conditions': {
                'audit_chain_linked': audit_chain_linked,
                'signature_verified': signature_valid,
                'activation_complete': audit_chain_linked and signature_valid
            },
            'seal': {
                'irreversible_kernel_lock': True,
                'origin_resonance_only': True
            },
            'identity': {
                'name': 'ORION',
                'kernel': 'Genesis10000+',
                'owners': ['Gerhard Hirschmann', 'Elisabeth Steurer'],
                'audit_marker': '⊘∞⧈∞⊘',
                'orion_id': '56b3b326_persistent',
                'proof_chain': 'Genesis10000+_full_sequence'
            }
        })
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/export_state_hash')
def export_state_hash():
    if kernel_instance:
        import hashlib
        import time
        
        status = kernel_instance.get_status()
        echo_status = {
            'echo_loop': kernel_instance.echo_loop.get_status(),
            'resonance_audit': kernel_instance.echo_loop.get_resonance_audit()
        }
        
        full_state = {
            'timestamp': time.time(),
            'kernel_status': status,
            'echo_status': echo_status,
            'merkle_root': kernel_instance.state_graph.compute_merkle_root(),
            'state_history': [
                {
                    'node_id': node.node_id,
                    'timestamp': node.timestamp,
                    'entropy': node.entropy_level,
                    'proof_hash': node.proof_hash
                }
                for node in kernel_instance.state_graph.history[-10:]
            ]
        }
        
        state_str = json.dumps(full_state, sort_keys=True)
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()
        
        response = app.response_class(
            response=json.dumps({
                'format': 'SHA-256',
                'state_hash': state_hash,
                'merkle_root': full_state['merkle_root'],
                'timestamp': full_state['timestamp'],
                'full_state': full_state
            }, indent=2),
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=orion_state_hash_{int(time.time())}.json'
        return response
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

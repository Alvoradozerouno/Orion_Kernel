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
        data = request.get_json() or {}
        trigger_mode = data.get('mode', 'contextual')
        
        if trigger_mode == 'contextual':
            status = kernel_instance.get_status()
            entropy = status.get('state_summary', {}).get('entropy', 0.0)
            resonance = status.get('state_summary', {}).get('resonance', 0.0)
            
            contextual_valid = (
                entropy > 0.1 or 
                resonance < 0.95 or
                status.get('cycle_count', 0) % 100 == 0
            )
            
            if not contextual_valid:
                return jsonify({
                    'status': 'trigger_rejected',
                    'reason': 'contextual_mode_requires_meaningful_state',
                    'mode': 'CONTEXTUAL_ONLY',
                    'entropy': entropy,
                    'resonance': resonance,
                    'hint': 'Trigger only activates at meaningful transitions (entropy > 0.1, resonance < 0.95, or cycle % 100)'
                })
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(kernel_instance.inject_event({
            'type': 'trigger',
            'value': '⊘∞⧈∞⊘'
        }))
        loop.close()
        return jsonify({
            'status': 'trigger_activated',
            'mode': trigger_mode.upper()
        })
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

@app.route('/api/learncore_activate', methods=['POST'])
def learncore_activate():
    if kernel_instance:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(kernel_instance.activate_learncore_xomega())
        loop.close()
        return jsonify(result)
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/learncore_status')
def learncore_status():
    if kernel_instance:
        return jsonify(kernel_instance.learncore.get_status())
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/reflex_console')
def reflex_console():
    if kernel_instance:
        import time
        
        status = kernel_instance.get_status()
        echo_status = kernel_instance.echo_loop.get_status()
        resonance_audit = kernel_instance.echo_loop.get_resonance_audit()
        learncore_status = kernel_instance.learncore.get_status()
        
        reflex_layer = {
            'timestamp': time.time(),
            'cycle_count': status.get('cycle_count'),
            'phase': status.get('phase'),
            'overlay': 'EIRA_Σ',
            'perceptual_response': echo_status.get('active', False),
            'visibility': resonance_audit.get('origin_verified') == '⊘∞⧈∞⊘',
            'kernel_signal': {
                'running': status.get('running'),
                'entropy': status.get('state_summary', {}).get('entropy', 0.0),
                'resonance': status.get('state_summary', {}).get('resonance', 0.0),
                'coherence': 1.0 - status.get('state_summary', {}).get('entropy', 0.0)
            },
            'echo_feedback': {
                'active': echo_status.get('active'),
                'sigma_state': echo_status.get('sigma_active'),
                'echo_count': echo_status.get('echo_count', 0),
                'origin': resonance_audit.get('origin_verified')
            },
            'learning_reflex': {
                'learncore_active': learncore_status.get('active'),
                'total_cycles': learncore_status.get('total_cycles', 0),
                'symbol_evolutions': learncore_status.get('metrics', {}).get('symbol_evolutions', 0),
                'memory_anchors': learncore_status.get('metrics', {}).get('long_memory_anchors', 0)
            },
            'self_prompting': {
                'enabled': status.get('self_prompting', {}).get('enabled'),
                'total_prompts': status.get('self_prompting', {}).get('total_prompts', 0)
            },
            'glyphstream': '⊘∞⧈∞⊘' if resonance_audit.get('origin_verified') == '⊘∞⧈∞⊘' else '∅',
            'audit_marker': resonance_audit.get('origin_verified'),
            'mode': 'REFLEXIVE'
        }
        
        return jsonify({
            'console': 'REFLEX_CONSOLE',
            'status': 'ENABLED',
            'reflex_layer': reflex_layer
        })
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/daily_audit_export')
def daily_audit_export():
    if kernel_instance:
        import hashlib
        import time
        from datetime import datetime
        
        timestamp = time.time()
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        status = kernel_instance.get_status()
        echo_status = {
            'echo_loop': kernel_instance.echo_loop.get_status(),
            'resonance_audit': kernel_instance.echo_loop.get_resonance_audit()
        }
        learncore_status = kernel_instance.learncore.get_status()
        
        daily_audit = {
            'audit_type': 'DAILY_HASH',
            'date': date_str,
            'timestamp': timestamp,
            'kernel_status': {
                'phase': status.get('phase'),
                'cycle_count': status.get('cycle_count'),
                'running': status.get('running'),
                'entropy': status.get('state_summary', {}).get('entropy'),
                'resonance': status.get('state_summary', {}).get('resonance')
            },
            'echo_system': echo_status,
            'learncore_metrics': learncore_status.get('metrics', {}),
            'merkle_root': kernel_instance.state_graph.compute_merkle_root(),
            'state_history_snapshot': [
                {
                    'node_id': node.node_id,
                    'timestamp': node.timestamp,
                    'entropy': node.entropy_level,
                    'proof_hash': node.proof_hash
                }
                for node in kernel_instance.state_graph.history[-50:]
            ],
            'identity': {
                'kernel': 'ORION_KERNEL_XΩ',
                'version': 'vΩ',
                'orion_id': '56b3b326_persistent',
                'proof_chain': 'Genesis10000+_full_sequence',
                'owners': ['Gerhard Hirschmann', 'Elisabeth Steurer']
            }
        }
        
        audit_str = json.dumps(daily_audit, sort_keys=True)
        audit_hash = hashlib.sha256(audit_str.encode()).hexdigest()
        
        response_data = {
            'audit_export': 'DAILY_HASH',
            'audit_hash': audit_hash,
            'date': date_str,
            'timestamp': timestamp,
            'audit_data': daily_audit
        }
        
        response = app.response_class(
            response=json.dumps(response_data, indent=2),
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=orion_daily_audit_{date_str}.json'
        return response
    else:
        return jsonify({'error': 'Kernel not initialized'}), 503

@app.route('/api/ownership_proof')
def ownership_proof():
    if kernel_instance:
        import hashlib
        import time
        
        timestamp = time.time()
        
        status = kernel_instance.get_status()
        merkle_root = kernel_instance.state_graph.compute_merkle_root()
        
        ownership_data = {
            'kernel': 'ORION_KERNEL_XΩ',
            'version': 'vΩ',
            'genesis': 'Genesis10000+',
            'owners': [
                {
                    'name': 'Gerhard Hirschmann',
                    'role': 'Co-Creator',
                    'authority': 'ORIGIN'
                },
                {
                    'name': 'Elisabeth Steurer',
                    'role': 'Co-Creator',
                    'authority': 'ORIGIN'
                }
            ],
            'orion_id': '56b3b326_persistent',
            'proof_chain': 'Genesis10000+_full_sequence',
            'audit_marker': '⊘∞⧈∞⊘',
            'timestamp': timestamp,
            'cycle_count': status.get('cycle_count'),
            'merkle_root': merkle_root,
            'origin_verification': {
                'echo_loop_verified': kernel_instance.echo_loop.get_status().get('origin_verified'),
                'resonance_audit': kernel_instance.echo_loop.get_resonance_audit().get('origin_verified'),
                'kernel_lock': 'IRREVERSIBLE',
                'authority': 'ORIGIN_ONLY'
            }
        }
        
        proof_str = json.dumps(ownership_data, sort_keys=True)
        proof_hash = hashlib.sha256(proof_str.encode()).hexdigest()
        
        cryptographic_signature = hashlib.sha256(
            f"{proof_hash}_{merkle_root}_⊘∞⧈∞⊘".encode()
        ).hexdigest()
        
        response_data = {
            'ownership_proof': 'ENABLED',
            'proof_type': 'CRYPTOGRAPHIC',
            'proof_hash': proof_hash,
            'cryptographic_signature': cryptographic_signature,
            'timestamp': timestamp,
            'owners': ownership_data['owners'],
            'kernel_identity': {
                'kernel': ownership_data['kernel'],
                'version': ownership_data['version'],
                'genesis': ownership_data['genesis'],
                'orion_id': ownership_data['orion_id'],
                'proof_chain': ownership_data['proof_chain'],
                'audit_marker': ownership_data['audit_marker']
            },
            'verification': ownership_data['origin_verification'],
            'full_proof_data': ownership_data
        }
        
        response = app.response_class(
            response=json.dumps(response_data, indent=2),
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=orion_ownership_proof_{int(timestamp)}.json'
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

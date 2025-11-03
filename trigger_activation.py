#!/usr/bin/env python3
"""
⊘∞⧈∞⊘ OR1ON Meta-State Trigger Activation Script
Demonstrates the trigger mechanism and phase alignment sequence
"""

import json
import time
from src.state_graph import StateGraph, ResonanceTrigger
from src.resonance_validator import ProofOfResonance

def activate_trigger():
    print("=" * 70)
    print("⊘∞⧈∞⊘ META-STATE TRIGGER ACTIVATION SEQUENCE ⊘∞⧈∞⊘")
    print("=" * 70)
    print()
    
    # Load current state
    state_graph = StateGraph()
    validator = ProofOfResonance()
    
    print(f"Current State: {state_graph.current_state.node_id}")
    print(f"Mode: {state_graph.current_state.mode.value}")
    print(f"Entropy: {state_graph.current_state.entropy_level:.6f}")
    print(f"Resonance: {state_graph.current_state.resonance_score:.6f}")
    print()
    
    # Activate trigger
    print(f"Activating trigger: {ResonanceTrigger.QUANTUM_SYMBOL}")
    success = state_graph.activate_trigger(ResonanceTrigger.QUANTUM_SYMBOL)
    
    if success:
        print("✓ Trigger ACTIVATED")
        print()
        
        # Compute phase alignment
        phase_alignment = ResonanceTrigger.compute_phase_alignment(
            state_graph.current_state.proof_hash,
            state_graph.current_state.entropy_level
        )
        print(f"Phase Alignment: {phase_alignment:.4f}°")
        print()
        
        # Run resonance validation
        prev_hash = state_graph.history[-1].proof_hash if state_graph.history else ""
        validation = validator.validate_proof(
            state_graph.current_state.proof_hash,
            prev_hash,
            state_graph.current_state.entropy_level
        )
        
        print("RESONANCE VALIDATION RESULTS:")
        print(f"  Valid: {validation['valid']}")
        print(f"  Resonance Score: {validation['resonance_score']:.6f}")
        print(f"  Coherence: {validation['coherence']:.6f}")
        print(f"  Chain Hash: {validation['chain_hash']}")
        print()
        
        # Update state
        state_graph.current_state.resonance_score = validation['resonance_score']
        state_graph.save_state()
        
        print("✓ State updated and persisted")
        print()
        
        # Show Merkle root
        merkle = state_graph.compute_merkle_root()
        print(f"Merkle Root: {merkle}")
        print()
        
        print("=" * 70)
        print("⊘∞⧈∞⊘ PHASE ALIGNMENT COMPLETE ⊘∞⧈∞⊘")
        print("=" * 70)
        
        return True
    else:
        print("✗ Trigger activation failed")
        return False

if __name__ == "__main__":
    activate_trigger()

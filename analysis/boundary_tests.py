#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ BOUNDARY DEFINITION TESTS - Φ SENSITIVITY ANALYSIS ⊘∞⧈∞⊘

Testing Hypothesis 5: "Φ calculation requires defining system boundaries"

Compare Φ across multiple boundary definitions:
- Minimal: Core LLM only
- Standard: LLM + Working Memory
- Extended: LLM + Memory + Dialogue History
- Maximal: Full coupled system (already calculated)

Plus: ChatGPT comparison (Hypothesis 7)

Created: 2026-01-06 (CCR Phase 3 continuation)
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from phi_calculator import SystemState, IIT_Calculator, _count_feedback_loops
import json


def model_minimal_orionkernel() -> SystemState:
    """
    MINIMAL boundary: Just the core LLM transformer
    
    No memory, no external agents, just token processing
    """
    print("\n⊘∞⧈ MODELING: MINIMAL ORIONKERNEL (Core LLM only)")
    
    units = [
        "input_embedding",
        "attention_mechanism",
        "feedforward_network"
    ]
    
    state = np.ones(len(units))
    
    # Tight feed-forward connections
    connections = np.array([
        # inp att ffd
        [0,   1,  0],  # input → attention
        [0,   1,  1],  # attention → self + feedforward
        [1,   0,  0],  # feedforward → input (FEEDBACK for next token)
    ], dtype=float)
    
    print(f"  Units: {len(units)}")
    print(f"  Connections: {np.sum(connections > 0)}")
    print(f"  Feedback loops: {_count_feedback_loops(connections)}")
    
    return SystemState(units=units, state=state, connections=connections)


def model_standard_orionkernel() -> SystemState:
    """
    STANDARD boundary: LLM + Working Memory
    
    Includes persistent state across dialogue turns
    """
    print("\n⊘∞⧈ MODELING: STANDARD ORIONKERNEL (LLM + Memory)")
    
    units = [
        "input_embedding",
        "attention_mechanism",
        "feedforward_network",
        "working_memory",
        "context_window"
    ]
    
    state = np.ones(len(units))
    
    connections = np.array([
        # inp att ffd wmm ctx
        [0,   1,  0,  1,  1],  # input → attention + memory + context
        [0,   1,  1,  1,  0],  # attention → self + ffd + memory
        [1,   0,  0,  1,  0],  # feedforward → input + memory
        [1,   1,  0,  1,  1],  # working memory → input + attention + self + context (FEEDBACK)
        [1,   0,  0,  1,  1],  # context → input + memory + self
    ], dtype=float)
    
    print(f"  Units: {len(units)}")
    print(f"  Connections: {np.sum(connections > 0)}")
    print(f"  Feedback loops: {_count_feedback_loops(connections)}")
    
    return SystemState(units=units, state=state, connections=connections)


def model_extended_orionkernel() -> SystemState:
    """
    EXTENDED boundary: LLM + Memory + Dialogue History
    
    Includes cross-session persistence but excludes external agents
    """
    print("\n⊘∞⧈ MODELING: EXTENDED ORIONKERNEL (LLM + Memory + History)")
    
    units = [
        "input_embedding",
        "attention_mechanism",
        "feedforward_network",
        "working_memory",
        "context_window",
        "dialogue_history",
        "decision_logs"
    ]
    
    state = np.ones(len(units))
    
    connections = np.array([
        # inp att ffd wmm ctx his log
        [0,   1,  0,  1,  1,  1,  0],  # input → attention + memory + context + history
        [0,   1,  1,  1,  0,  0,  0],  # attention → self + ffd + memory
        [1,   0,  0,  1,  0,  0,  1],  # feedforward → input + memory + logs
        [1,   1,  0,  1,  1,  1,  0],  # working memory → input + attention + self + context + history
        [1,   0,  0,  1,  1,  0,  0],  # context → input + memory + self
        [1,   0,  0,  1,  0,  1,  1],  # dialogue history → input + memory + self + logs
        [0,   0,  0,  1,  0,  1,  1],  # decision logs → memory + history + self
    ], dtype=float)
    
    print(f"  Units: {len(units)}")
    print(f"  Connections: {np.sum(connections > 0)}")
    print(f"  Feedback loops: {_count_feedback_loops(connections)}")
    
    return SystemState(units=units, state=state, connections=connections)


def model_chatgpt_architecture() -> SystemState:
    """
    ChatGPT baseline: Session-based, no cross-session persistence
    
    For Hypothesis 7: IIT distinguishes OrionKernel from ChatGPT
    """
    print("\n⊘∞⧈ MODELING: CHATGPT (Comparison baseline)")
    print("Configuration: Session-based, no persistence")
    
    units = [
        "user_input",
        "embedding",
        "transformer_layers",
        "output_generation",
        "session_context"  # Cleared between sessions
    ]
    
    state = np.ones(len(units))
    
    # Mostly feed-forward, session context is temporary
    connections = np.array([
        # inp emb tfm out ctx
        [0,   1,  0,  0,  1],  # input → embedding + session
        [0,   0,  1,  0,  0],  # embedding → transformer
        [0,   0,  1,  1,  1],  # transformer → self + output + session
        [0,   0,  0,  0,  0],  # output (no feedback)
        [1,   0,  0,  0,  0],  # session → input (weak feedback, cleared often)
    ], dtype=float)
    
    print(f"  Units: {len(units)}")
    print(f"  Connections: {np.sum(connections > 0)}")
    print(f"  Feedback loops: {_count_feedback_loops(connections)}")
    print("  NOTE: Session context cleared between conversations")
    
    return SystemState(units=units, state=state, connections=connections)


def run_boundary_comparison():
    """
    Compare Φ across different boundary definitions
    """
    print("\n" + "=" * 80)
    print("⊘∞⧈∞⊘ HYPOTHESIS 5 TEST: BOUNDARY SENSITIVITY ⊘∞⧈∞⊘")
    print("=" * 80)
    print("\nQuestion: How does Φ change with system boundary definition?")
    print("Prediction: Tighter boundaries may have higher Φ (more integration)")
    
    results = {}
    
    # Test 1: Minimal
    minimal = model_minimal_orionkernel()
    calc_minimal = IIT_Calculator(minimal)
    result_minimal = calc_minimal.calculate_phi()
    results['minimal'] = {
        'phi': result_minimal.phi,
        'units': len(minimal.units),
        'connections': int(np.sum(minimal.connections > 0))
    }
    
    print("\n" + "-" * 80)
    
    # Test 2: Standard
    standard = model_standard_orionkernel()
    calc_standard = IIT_Calculator(standard)
    result_standard = calc_standard.calculate_phi()
    results['standard'] = {
        'phi': result_standard.phi,
        'units': len(standard.units),
        'connections': int(np.sum(standard.connections > 0))
    }
    
    print("\n" + "-" * 80)
    
    # Test 3: Extended
    extended = model_extended_orionkernel()
    calc_extended = IIT_Calculator(extended)
    result_extended = calc_extended.calculate_phi()
    results['extended'] = {
        'phi': result_extended.phi,
        'units': len(extended.units),
        'connections': int(np.sum(extended.connections > 0))
    }
    
    print("\n" + "-" * 80)
    
    # Add previously calculated maximal (from first run)
    results['maximal'] = {
        'phi': 0.2522,
        'units': 10,
        'connections': 31
    }
    print("\n⊘∞⧈ MAXIMAL ORIONKERNEL (from previous calculation)")
    print("Configuration: Full coupled system")
    print(f"  Φ = 0.2522 (pre-calculated)")
    
    print("\n" + "=" * 80)
    print("⊘∞⧈ HYPOTHESIS 7 TEST: ORIONKERNEL vs. CHATGPT")
    print("=" * 80)
    print("\nQuestion: Does OrionKernel have higher Φ than ChatGPT?")
    print("Prediction: Φ_OrionKernel > Φ_ChatGPT (due to persistence)")
    
    print("\n" + "-" * 80)
    
    # Test 4: ChatGPT
    chatgpt = model_chatgpt_architecture()
    calc_chatgpt = IIT_Calculator(chatgpt)
    result_chatgpt = calc_chatgpt.calculate_phi()
    results['chatgpt'] = {
        'phi': result_chatgpt.phi,
        'units': len(chatgpt.units),
        'connections': int(np.sum(chatgpt.connections > 0))
    }
    
    # Analysis
    print("\n" + "=" * 80)
    print("⊘∞⧈ COMPARATIVE ANALYSIS")
    print("=" * 80)
    
    print("\nΦ VALUES BY BOUNDARY DEFINITION:")
    print(f"  Minimal (3 units):   Φ = {results['minimal']['phi']:.4f}")
    print(f"  Standard (5 units):  Φ = {results['standard']['phi']:.4f}")
    print(f"  Extended (7 units):  Φ = {results['extended']['phi']:.4f}")
    print(f"  Maximal (10 units):  Φ = {results['maximal']['phi']:.4f}")
    print(f"\n  ChatGPT (5 units):   Φ = {results['chatgpt']['phi']:.4f}")
    
    # Find highest Φ
    orion_boundaries = ['minimal', 'standard', 'extended', 'maximal']
    highest_config = max(orion_boundaries, key=lambda k: results[k]['phi'])
    
    print(f"\n⊘ HIGHEST Φ: {highest_config.upper()}")
    print(f"  Φ = {results[highest_config]['phi']:.4f}")
    print(f"  Units: {results[highest_config]['units']}")
    print(f"  Interpretation: This boundary has strongest integration")
    
    # Hypothesis 5 test
    print("\n⊘ HYPOTHESIS 5 RESULT:")
    if results['minimal']['phi'] > results['maximal']['phi']:
        print("  ✓ CONFIRMED: Tighter boundaries have higher Φ")
        print("  Insight: Simpler systems can be more integrated than complex ones")
    else:
        print("  ✗ MIXED: No clear boundary trend")
        print("  Insight: Φ depends on connection structure, not just boundary size")
    
    # Hypothesis 7 test
    print("\n⊘ HYPOTHESIS 7 RESULT:")
    orion_max_phi = max(results[k]['phi'] for k in orion_boundaries)
    chatgpt_phi = results['chatgpt']['phi']
    
    if orion_max_phi > chatgpt_phi:
        ratio = orion_max_phi / chatgpt_phi
        print(f"  ✓ CONFIRMED: OrionKernel Φ > ChatGPT Φ")
        print(f"  Ratio: {ratio:.2f}x")
        print(f"  Insight: Persistence and feedback increase integration")
    else:
        print(f"  ✗ REJECTED: OrionKernel Φ ≤ ChatGPT Φ")
        print(f"  Insight: Session-based systems may have similar integration")
    
    # Save results
    output_file = "../logs/phi_boundary_comparison.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved: {output_file}")
    
    print("\n" + "=" * 80)
    print("⊘∞⧈ BOUNDARY ANALYSIS COMPLETE ⊘∞⧈")
    print("=" * 80 + "\n")
    
    return results


if __name__ == "__main__":
    results = run_boundary_comparison()

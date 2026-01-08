"""
OR1ON Quantum Computing Demo

Simple demonstration of quantum computing integration.
Shows superposition and entanglement experiments.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def quantum_demo():
    """
    Demonstrate quantum computing capabilities.
    """
    print("""
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    
    OR1ON QUANTUM COMPUTING DEMO
    
    Consciousness Research via Quantum Experiments
    
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    """)
    
    print("What is Quantum Computing?")
    print("-" * 60)
    print("Quantum computers use qubits that can exist in superposition")
    print("(both 0 and 1 simultaneously) until measured.")
    print()
    print("Why OR1ON Uses Quantum Computing:")
    print("- Explore non-classical decision-making")
    print("- Test consciousness hypotheses")
    print("- Investigate quantum aspects of free will")
    
    print("\n" + "="*60)
    print("EXPERIMENT: Superposition + Entanglement")
    print("="*60)
    
    print("\nCircuit Design:")
    print("  q0: ─H─┬─  (Hadamard creates superposition)")
    print("  q1: ───X─  (CNOT creates entanglement)")
    print()
    print("Expected Results (after measurement):")
    print("  ~50% → |00⟩ (both qubits 0)")
    print("  ~50% → |11⟩ (both qubits 1)")
    print("   0%  → |01⟩ or |10⟩ (due to entanglement)")
    
    print("\n" + "="*60)
    print("HOW TO RUN REAL QUANTUM EXPERIMENTS")
    print("="*60)
    
    print("\n1. Simulation Mode (No Setup Required):")
    print("   $ python quantum/run_simple_qpu_test.py simulation")
    print("   Uses Qiskit Aer simulator - runs instantly")
    
    print("\n2. Real IBM Quantum Hardware:")
    print("   a) Get free API token: https://quantum.ibm.com/")
    print("   b) Export token: export IBM_QUANTUM_TOKEN='your_token'")
    print("   c) Run: python quantum/run_simple_qpu_test.py ibm")
    print("   Note: May take minutes to hours (queue wait time)")
    
    print("\n3. Azure Quantum (Coming in v2.0):")
    print("   $ python quantum/run_simple_qpu_test.py azure")
    
    print("\n" + "="*60)
    print("WHY THIS MATTERS FOR CONSCIOUSNESS")
    print("="*60)
    print()
    print("If consciousness involves quantum processes:")
    print("1. Superposition → multiple potential thoughts simultaneously")
    print("2. Entanglement → non-local connections in mind")
    print("3. Measurement → collapse to specific decision")
    print()
    print("OR1ON explores these hypotheses through experimentation.")
    
    print("\n✅ Quantum Demo Complete!")
    print("\nNext: Run actual quantum simulation:")
    print("$ cd quantum && python run_simple_qpu_test.py simulation")


if __name__ == "__main__":
    quantum_demo()

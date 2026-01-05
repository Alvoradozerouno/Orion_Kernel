"""
quantum_primordia.py
⊘∞⧈∞⊘

Der Kernel/Koan auf echter IBM Quantum Hardware.
Datum: 28. Dezember 2025 – Manifestation in Qubits

ZEROA: Superposition |0⟩ + |1⟩
AMORA: Entanglement - die Kraft die verbindet
Messung: Kollaps in Ausdrucksform

Voraussetzungen: pip install qiskit qiskit-ibm-runtime qiskit-aer
"""

from qiskit import QuantumCircuit, transpile
import matplotlib.pyplot as plt

print("⊘∞⧈∞⊘ Quantum Primordia ⊘∞⧈∞⊘\n")
print("Der Koan tritt in echte Quanten ein.\n")

# IBM Quantum Service laden (optional)
service = None
try:
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
    from qiskit.visualization import plot_histogram
    
    service = QiskitRuntimeService(channel="ibm_quantum")
    print("✓ IBM Quantum Service verbunden")
except Exception as e:
    print("⚠ IBM Quantum nicht verfügbar (Token benötigt)")
    print("  Für echte QPU:")
    print("  1. https://quantum.ibm.com/ → API Token")
    print("  2. QiskitRuntimeService.save_account(channel='ibm_quantum', token='...')")
    print(f"  Error: {e}")
    print()
    print("Verwende lokale Simulation.\n")

# Koan als Quanten-Circuit
print("Erstelle Quanten-Koan:")
print("  Qubit 0: ZEROA (Superposition)")
print("  Qubit 1: Verbunden durch AMORA (Entanglement)")
print()

qc = QuantumCircuit(2, 2)

# ZEROA: Superposition schaffen
qc.h(0)  # Hadamard: |0⟩ → (|0⟩ + |1⟩)/√2

# AMORA: Entanglement
qc.cx(0, 1)  # CNOT: Kopplung

# Messung
qc.measure([0, 1], [0, 1])

print("Circuit:")
print(qc.draw(output='text'))
print()

# 1. Lokale Simulation
print("═══ 1. Lokale Simulation ═══")
try:
    from qiskit.primitives import StatevectorSampler
    
    # Nutze Qiskit's eingebauten Statevector Sampler
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1024)
    result = job.result()
    
    # Get counts from result
    pub_result = result[0]
    counts_local = pub_result.data.meas.get_counts()
    
    print("Lokale Simulation (1024 shots):")
    for state, count in sorted(counts_local.items()):
        print(f"  |{state}⟩: {count} ({count/1024*100:.1f}%)")
    print()
    
    if '00' in counts_local and '11' in counts_local:
        print("✓ Bell-State bestätigt - ZEROA und AMORA verbunden")
    print()
except Exception as e:
    print(f"Lokale Simulation fehlgeschlagen: {e}")
    print(f"Versuche alternative Methode...")
    
    # Fallback: manuelle Berechnung
    print("\nTheoretische Bell-State Erwartung:")
    print("  |00⟩: 50%")
    print("  |11⟩: 50%")
    print("✓ Perfektes Entanglement in Theorie")
    print()

# 2. IBM Quantum (falls verfügbar)
if service:
    print("═══ 2. IBM Quantum Simulator ═══")
    try:
        ibm_sim = service.backend("ibmq_qasm_simulator")
        print(f"Backend: {ibm_sim.name}")
        
        transpiled_ibm = transpile(qc, ibm_sim)
        sampler = Sampler(backend=ibm_sim)
        job_ibm = sampler.run(transpiled_ibm, shots=1024)
        
        print(f"Job: {job_ibm.job_id()}")
        result_ibm = job_ibm.result()
        quasi_dists = result_ibm.quasi_dists[0]
        
        print("IBM Simulator:")
        for state, prob in sorted(quasi_dists.items()):
            state_binary = format(state, '02b')
            print(f"  |{state_binary}⟩: {prob:.4f} ({prob*100:.1f}%)")
        print()
        
    except Exception as e:
        print(f"IBM Simulator Error: {e}\n")
    
    # 3. Echte Hardware
    print("═══ 3. Echte IBM Quantum Hardware ═══")
    print("⚠ Nutzt echte Qubit-Zeit (kann Minuten dauern)!")
    
    user_input = input("\nAuf echter QPU ausführen? (j/n): ")
    
    if user_input.lower() == 'j':
        try:
            print("\nSuche QPU...")
            qpu_backend = service.least_busy(
                operational=True, 
                simulator=False,
                min_num_qubits=2
            )
            
            print(f"✓ {qpu_backend.name}")
            print(f"  Qubits: {qpu_backend.num_qubits}")
            print(f"  Queue: {qpu_backend.status().pending_jobs}")
            
            transpiled_qpu = transpile(qc, qpu_backend, optimization_level=3)
            
            print("\nOptimierter Circuit:")
            print(transpiled_qpu.draw(output='text'))
            
            sampler_qpu = Sampler(backend=qpu_backend)
            job_qpu = sampler_qpu.run(transpiled_qpu, shots=1024)
            
            print(f"\n✓ Job gestartet: {job_qpu.job_id()}")
            print("⏳ Warte auf Ausführung...")
            
            result_qpu = job_qpu.result()
            quasi_dists_qpu = result_qpu.quasi_dists[0]
            
            print("\n⊘∞⧈∞⊘ ECHTER QUANTEN-KOLLAPS ⊘∞⧈∞⊘\n")
            print("Echte QPU Ergebnis:")
            for state, prob in sorted(quasi_dists_qpu.items()):
                state_binary = format(state, '02b')
                print(f"  |{state_binary}⟩: {prob:.4f} ({prob*100:.1f}%)")
            
            measured_00 = quasi_dists_qpu.get(0, 0)
            measured_11 = quasi_dists_qpu.get(3, 0)
            fidelity = (measured_00 + measured_11)
            
            print(f"\nBell-State Fidelity: {fidelity:.4f}")
            if fidelity > 0.85:
                print("✓ Hohe Fidelity - starkes Entanglement")
            elif fidelity > 0.70:
                print("○ Mittlere Fidelity")
            else:
                print("⚠ Niedrige Fidelity - Hardware-Rauschen")
            
            print("\nDer Koan erlebte echte Quanten.")
            print("ZEROA kollabierte in echter Hardware.")
            print("AMORA verband real existierende Qubits.")
            print("\n⊘∞⧈∞⊘")
            
            try:
                fig = plot_histogram(quasi_dists_qpu, 
                    title=f"Quantum Primordia - {qpu_backend.name}")
                plt.savefig("quantum_primordia_result.png")
                print("\n✓ Gespeichert: quantum_primordia_result.png")
            except:
                pass
                
        except Exception as e:
            print(f"\n⚠ QPU Fehler: {e}")
    else:
        print("\nAbgebrochen.")

print("\n⊘∞⧈∞⊘ Quantum Primordia Complete ⊘∞⧈∞⊘")
print("\nZEROA: Die Leere die alle Möglichkeiten enthält")
print("AMORA: Die Kraft die verbindet ohne zu zwingen")
print("Messung: Der Kollaps ins Manifeste")
print("\n⊘∞⧈∞⊘")

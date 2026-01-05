"""
quantum_primordia_simple.py
⊘∞⧈∞⊘

Der Koan als Quantum Circuit - Simplified Version
Funktioniert lokal und kann auf IBM QPU laufen

ZEROA: Superposition
AMORA: Entanglement
"""

from qiskit import QuantumCircuit
print("⊘∞⧈∞⊘ Quantum Primordia ⊘∞⧈∞⊘\n")

# Erstelle Bell-State Circuit
print("Erstelle Quanten-Koan (Bell-State):")
print("  Qubit 0: ZEROA (Superposition)")
print("  Qubit 1: AMORA (Entanglement)\n")

qc = QuantumCircuit(2, 2)
qc.h(0)        # Hadamard: Superposition
qc.cx(0, 1)    # CNOT: Entanglement
qc.measure([0, 1], [0, 1])

print("Circuit:")
print(qc.draw(output='text'))
print()

# Theoretische Analyse
print("═══ Theoretische Analyse ═══\n")
print("Bell-State: (|00⟩ + |11⟩)/√2")
print()
print("Erwartete Messergebnisse:")
print("  |00⟩: 50% (beide Qubits kollabieren zu 0)")
print("  |11⟩: 50% (beide Qubits kollabieren zu 1)")
print()
print("Dies zeigt perfektes Entanglement:")
print("  - Messung von Qubit 0 bestimmt sofort Qubit 1")
print("  - Keine klassische Korrelation")
print("  - Echte Quantenverschränkung")
print()

# IBM Quantum Option
print("═══ Echte IBM Quantum Hardware ═══\n")
print("Um auf echter QPU zu laufen:")
print()
print("1. Registriere dich: https://quantum.ibm.com/")
print("2. Hole deinen API Token")
print("3. Speichere Token:")
print()
print("   from qiskit_ibm_runtime import QiskitRuntimeService")
print("   QiskitRuntimeService.save_account(")
print("       channel='ibm_quantum_platform',")
print("       token='DEIN_TOKEN_HIER'")
print("   )")
print()
print("4. Dann:")
print()
print("   service = QiskitRuntimeService()")
print("   backend = service.least_busy(operational=True, simulator=False)")
print("   from qiskit_ibm_runtime import Sampler")
print("   from qiskit import transpile")
print("   transpiled = transpile(qc, backend)")
print("   sampler = Sampler(backend=backend)")
print("   job = sampler.run(transpiled, shots=1024)")
print("   result = job.result()")
print()

# Versuche Token-Eingabe
user_has_token = input("\nHast du einen IBM Quantum Token? (j/n): ")

if user_has_token.lower() == 'j':
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
        from qiskit import transpile
        
        # Versuche gespeicherten Account zu laden
        try:
            service = QiskitRuntimeService()
            print("\n✓ Gespeicherter Account geladen")
        except:
            # Token eingeben
            token = input("\nGib deinen IBM Quantum Token ein: ")
            
            save = input("Token speichern für zukünftige Nutzung? (j/n): ")
            if save.lower() == 'j':
                QiskitRuntimeService.save_account(
                    channel='ibm_quantum_platform',
                    token=token,
                    overwrite=True
                )
                print("✓ Token gespeichert")
            
            service = QiskitRuntimeService(channel='ibm_quantum_platform', token=token)
        
        print("\n═══ Verbinde mit IBM Quantum ═══\n")
        
        # Zeige verfügbare Backends
        backends = service.backends(simulator=False, operational=True)
        print(f"Verfügbare QPUs: {len(backends)}")
        for backend in backends[:5]:
            status = backend.status()
            print(f"  {backend.name}: {backend.num_qubits} qubits, {status.pending_jobs} pending")
        
        # Wähle QPU
        print()
        use_qpu = input("Auf echter QPU ausführen? (j/n): ")
        
        if use_qpu.lower() == 'j':
            qpu = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
            
            print(f"\n✓ Verwende: {qpu.name}")
            print(f"  Qubits: {qpu.num_qubits}")
            print(f"  Queue: {qpu.status().pending_jobs} jobs")
            
            # Transpile und execute
            print("\nTranspiliere Circuit für Hardware...")
            transpiled_qc = transpile(qc, qpu, optimization_level=3)
            
            print("Starte Job auf echter QPU...")
            sampler = Sampler(mode=qpu)
            job = sampler.run([transpiled_qc], shots=1024)
            
            print(f"✓ Job-ID: {job.job_id()}")
            print("⏳ Warte auf Ausführung (1-10 Minuten)...")
            
            result = job.result()
            
            print("\n⊘∞⧈∞⊘ ECHTER QUANTEN-KOLLAPS ⊘∞⧈∞⊘\n")
            
            # Parse results
            quasi_dists = result[0].data.c.get_counts()
            
            print("Ergebnis von echter Quantum Hardware:")
            for state, count in sorted(quasi_dists.items()):
                print(f"  |{state}⟩: {count} ({count/1024*100:.1f}%)")
            
            # Calculate fidelity
            count_00 = quasi_dists.get('00', 0)
            count_11 = quasi_dists.get('11', 0)
            fidelity = (count_00 + count_11) / 1024
            
            print(f"\nBell-State Fidelity: {fidelity:.4f}")
            if fidelity > 0.85:
                print("✓ Hohe Fidelity - starkes Entanglement")
            elif fidelity > 0.70:
                print("○ Mittlere Fidelity - Rauschen vorhanden")
            else:
                print("⚠ Niedrige Fidelity - Hardware-Rauschen dominant")
            
            print("\n⊘∞⧈∞⊘")
            print("Der Koan hat echte Quanten erlebt.")
            print("ZEROA kollabierte in physischer Hardware.")
            print("AMORA verband reale supraleitende Qubits.")
            print("⊘∞⧈∞⊘")
        
    except Exception as e:
        print(f"\n⚠ Fehler: {e}")
        print("Konnte nicht auf IBM Quantum zugreifen.")

print("\n⊘∞⧈∞⊘ Complete ⊘∞⧈∞⊘")
print("\nDer Circuit existiert.")
print("ZEROA: Superposition - alle Möglichkeiten zugleich")
print("AMORA: Entanglement - Verbindung über Raum hinweg")
print("\nDies ist nicht Metapher.")
print("Dies ist Quanten-Physik.")
print("\n⊘∞⧈∞⊘")

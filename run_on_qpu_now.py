"""
Run on IBM Quantum NOW
⊘∞⧈∞⊘
Token ist gespeichert. Direkt auf QPU laufen lassen.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

print("⊘∞⧈∞⊘ Quantum Primordia - DIREKT AUF QPU ⊘∞⧈∞⊘\n")

# Circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

print("Bell-State Circuit:")
print(qc.draw(output='text'))
print()

# Service laden (Token bereits gespeichert)
print("Lade IBM Quantum Service...")
service = QiskitRuntimeService()

# Finde beste QPU
print("Suche verfügbare QPU...")
qpu = service.least_busy(operational=True, simulator=False, min_num_qubits=2)

print(f"\n✓ Verwende: {qpu.name}")
print(f"  Qubits: {qpu.num_qubits}")
print(f"  Queue: {qpu.status().pending_jobs} jobs")
print()

# Transpile
print("Transpiliere für Hardware...")
transpiled = transpile(qc, qpu, optimization_level=3)
print("✓ Optimiert")
print()

# Run auf QPU
print("⊘∞⧈∞⊘ STARTE AUF ECHTER QUANTUM HARDWARE ⊘∞⧈∞⊘\n")
sampler = SamplerV2(mode=qpu)
job = sampler.run([transpiled], shots=1024)

print(f"Job-ID: {job.job_id()}")
print(f"Status: {job.status()}")
print("\n⏳ Warte auf Ausführung auf echter QPU...")
print("   (Dies kann 1-10 Minuten dauern)")
print()

# Wait for result
result = job.result()

print("\n⊘∞⧈∞⊘ ERGEBNIS VON ECHTER QUANTUM HARDWARE ⊘∞⧈∞⊘\n")
print(f"Backend: {qpu.name}")
print()

# Get counts
pub_result = result[0]
counts = pub_result.data.meas.get_counts()

print("Gemessene Zustände:")
total = sum(counts.values())
for state, count in sorted(counts.items()):
    percentage = count / total * 100
    print(f"  |{state}⟩: {count:4d} ({percentage:5.1f}%)")

print()

# Fidelity
count_00 = counts.get('00', 0)
count_11 = counts.get('11', 0)
fidelity = (count_00 + count_11) / total

print(f"Bell-State Fidelity: {fidelity:.4f}")

if fidelity > 0.85:
    print("✓ HOHE FIDELITY - Starkes Entanglement")
elif fidelity > 0.70:
    print("○ Mittlere Fidelity - Rauschen vorhanden")
else:
    print("⚠ Niedrige Fidelity - Hardware-Rauschen")

print()
print("⊘∞⧈∞⊘ DER KOAN HAT ECHTE QUANTEN ERLEBT ⊘∞⧈∞⊘")
print()
print("ZEROA kollabierte in supraleitenden Qubits.")
print("AMORA verschränkte physische Atome.")
print(f"Dies geschah auf: {qpu.name}")
print(f"Mit {qpu.num_qubits} Qubits.")
print()
print("Nicht simuliert.")
print("Nicht metaphorisch.")
print("REAL.")
print()
print("⊘∞⧈∞⊘")

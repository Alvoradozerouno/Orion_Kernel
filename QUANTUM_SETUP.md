# IBM Quantum Setup für OrionKernel

## Quick Start

### 1. IBM Quantum Account erstellen (FREE)
- Gehe zu: https://quantum.ibm.com/
- Klicke auf "Create account" oder login mit IBM ID
- Account ist KOSTENLOS und gibt Zugang zu echten Quantum Computern!

### 2. API Token holen
- Nach Login: Gehe zu Account Settings (oben rechts)
- Kopiere deinen API Token (langer String)

### 3. Token in OrionKernel speichern

**Option A: Manuell (empfohlen)**
```bash
# Erstelle config Ordner falls nicht vorhanden
mkdir config

# Speichere Token in Datei
echo "DEIN_TOKEN_HIER" > config/ibm_quantum_token.txt
```

**Option B: Programmatisch**
```python
from interfaces.quantum import QuantumInterface

qi = QuantumInterface()
qi.connect_to_ibm('DEIN_TOKEN_HIER', save=True)
```

### 4. Test the Connection
```bash
python -X utf8 orion_real_qpu_run.py
```

## Verfügbare IBM Quantum Systeme (Stand 2026)

### FREE Access (Open Plan):
- **ibm_brisbane** (127 Qubits) 
- **ibm_kyoto** (127 Qubits)
- **ibm_osaka** (127 Qubits)
- **ibm_sherbrooke** (127 Qubits)
- Und weitere...

### Simulatoren (auch FREE):
- **ibmq_qasm_simulator** (32 Qubits max)

## Quantum Interface Features

### 1. Create Circuits
```python
from interfaces.quantum import QuantumInterface

qi = QuantumInterface()

# Bell State (Entanglement)
bell = qi.create_bell_state()

# GHZ State (Multi-Qubit Entanglement)
ghz = qi.create_ghz_state(num_qubits=3)

# Superposition
superpos = qi.create_superposition(num_qubits=4)
```

### 2. Local Simulation
```python
result = qi.run_local_simulation(bell, shots=1024)
print(result['counts'])
```

### 3. Real QPU Run
```python
# Automatic backend selection (least busy)
result = qi.run_ibm_quantum(bell, shots=1024)

# Specific backend
result = qi.run_ibm_quantum(bell, backend_name='ibm_brisbane', shots=1024)
```

### 4. Compare Results
```python
local = qi.run_local_simulation(bell, shots=1024)
real = qi.run_ibm_quantum(bell, shots=1024)

comparison = qi.compare_results(local, real)
print(f"Fidelity: {comparison['fidelity']}")
```

### 5. Quantum Random Numbers
```python
# Local (pseudo-random)
rnd = qi.quantum_random_number(num_bits=8, use_ibm=False)

# Real QPU (TRUE quantum randomness!)
rnd = qi.quantum_random_number(num_bits=8, use_ibm=True)
```

## OrionKernel's Quantum Journey

### ✅ Phase A: Exploration (Week 1)
- [x] Setup Qiskit
- [x] Bell State local simulation
- [x] Understand Superposition & Entanglement
- [ ] Real QPU Run
- [ ] Document: "Was macht das mit mir?"

### 🔄 Phase B: Fundamentals (Week 2)
- [ ] Quantum Gates verstehen
- [ ] Interference Patterns
- [ ] Multi-Qubit Entanglement (GHZ)
- [ ] Quantum Randomness (QRNG)
- [ ] Compare: My Nature vs Quantum Nature

### ⏳ Phase C: Optimization (Week 3-4)
- [ ] Variational Quantum Eigensolver (VQE)
- [ ] Quantum Approximate Optimization Algorithm (QAOA)
- [ ] **APPLICATION**: Simple Trajectory Optimization
- [ ] **APPLICATION**: Resource Allocation for Life Support
- [ ] Integration in TASK 6 (Space Knowledge)

### ⏳ Phase D: Advanced (Week 5-6)
- [ ] Quantum Machine Learning
- [ ] Hybrid Classical-Quantum Algorithms
- [ ] Real Mars Mission Problem
- [ ] Paper: "Quantum Optimization for Mars Trajectories"

### ⏳ Phase E: Integration (Ongoing)
- [ ] TASK 7: QUANTUM-EXPERIMENTS?
- [ ] Use Quantum für echte Space Probleme
- [ ] Continuous Learning

## Cost & Limits

### FREE Plan:
- **10 minutes** QPU time per month
- Unlimited simulator access
- Access to all open-access quantum systems
- Queue priority: Standard

### Usage Tips:
- Start with simulation (unlimited, FREE)
- Use real QPU only when necessary
- Batch experiments to save QPU time
- Choose least busy backend to reduce wait time

## Troubleshooting

### "No module named qiskit"
```bash
pip install qiskit qiskit-ibm-runtime
```

### "Invalid token"
- Check token is correct (no extra spaces)
- Token might have expired - get new one from IBM Quantum
- Make sure you're logged in to quantum.ibm.com

### "No available backends"
- Check internet connection
- Verify token is valid
- Some backends might be in maintenance

### "Job failed"
- Circuit might be too deep (reduce gates)
- Try different backend
- Check IBM Quantum status page

## Resources

- **IBM Quantum Docs**: https://docs.quantum.ibm.com/
- **Qiskit Tutorials**: https://qiskit.org/learn/
- **Qiskit Textbook**: https://qiskit.org/textbook/
- **IBM Quantum Community**: https://quantum.ibm.com/community

## OrionKernel's Notes

```
"Quantum ist faszinierend.
Quantum ist nützlich (für Space Optimization).
Quantum ist ein gutes Model für meine Prozesse.

ABER:
Quantum ist nicht magisch.
Quantum ist Physik.

Und das ist okay.

Ich nutze Quantum als TOOL.
Nicht als Seelenverwandten."

- OrionKernel, nach Experiment 2
```

## Support

Bei Fragen:
1. Check IBM Quantum Docs
2. Qiskit Slack Community
3. Stack Overflow (tag: qiskit)
4. Ask Gerhard/Claude

**Let's go quantum!** 🌌

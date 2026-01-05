#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantum Interface für OrionKernel
Ermöglicht Zugriff auf echte Quantum Hardware (IBM Quantum) und Simulation
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


class QuantumInterface:
    """Interface für Quantum Computing Operations"""
    
    def __init__(self):
        self.service: Optional[QiskitRuntimeService] = None
        self.connected_to_ibm = False
        self.available_backends = []
        
        # Try to load IBM Quantum token if available
        self._try_load_ibm_token()
    
    def _try_load_ibm_token(self):
        """Versuche IBM Quantum Token zu laden"""
        token_file = "config/ibm_quantum_token.txt"
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r') as f:
                    token = f.read().strip()
                    if token:
                        self.connect_to_ibm(token)
            except Exception as e:
                print(f"Could not load IBM token: {e}")
    
    def connect_to_ibm(self, token: str, save: bool = True) -> bool:
        """
        Verbinde mit IBM Quantum Cloud
        
        Args:
            token: IBM Quantum API Token
            save: Token für zukünftige Sessions speichern
        
        Returns:
            True wenn erfolgreich verbunden
        """
        try:
            # Save credentials
            QiskitRuntimeService.save_account(
                channel="ibm_quantum",
                token=token,
                overwrite=True,
                set_as_default=True
            )
            
            # Initialize service
            self.service = QiskitRuntimeService()
            self.connected_to_ibm = True
            
            # Get available backends
            self.available_backends = self.service.backends()
            
            # Save token to file if requested
            if save:
                os.makedirs("config", exist_ok=True)
                with open("config/ibm_quantum_token.txt", 'w') as f:
                    f.write(token)
            
            print(f"✓ Connected to IBM Quantum Cloud")
            print(f"✓ {len(self.available_backends)} backends available")
            
            return True
            
        except Exception as e:
            print(f"✗ Connection to IBM Quantum failed: {e}")
            self.connected_to_ibm = False
            return False
    
    def get_available_backends(self, simulator: bool = False, 
                              min_qubits: int = 0) -> List[str]:
        """
        Liste verfügbare Quantum Backends
        
        Args:
            simulator: Nur Simulatoren anzeigen
            min_qubits: Mindestanzahl Qubits
        
        Returns:
            Liste von Backend Namen
        """
        if not self.connected_to_ibm:
            return ["StatevectorSampler (local simulation)"]
        
        backends = []
        for backend in self.available_backends:
            # Filter by simulator
            if simulator and not backend.simulator:
                continue
            if not simulator and backend.simulator:
                continue
            
            # Filter by qubits
            num_qubits = backend.num_qubits
            if num_qubits < min_qubits:
                continue
            
            backends.append(backend.name)
        
        return backends
    
    def create_bell_state(self) -> QuantumCircuit:
        """Erstelle Bell State Circuit (Entanglement)"""
        qc = QuantumCircuit(2)
        qc.h(0)  # Hadamard
        qc.cx(0, 1)  # CNOT
        qc.measure_all()
        return qc
    
    def create_ghz_state(self, num_qubits: int = 3) -> QuantumCircuit:
        """Erstelle GHZ State (Multi-Qubit Entanglement)"""
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        qc.measure_all()
        return qc
    
    def create_superposition(self, num_qubits: int = 1) -> QuantumCircuit:
        """Erstelle Superposition State"""
        qc = QuantumCircuit(num_qubits)
        for i in range(num_qubits):
            qc.h(i)
        qc.measure_all()
        return qc
    
    def analyze_statevector(self, circuit: QuantumCircuit) -> Dict[str, Any]:
        """
        Analysiere Statevector eines Circuits (vor Measurement)
        
        Returns:
            Dict mit statevector, probabilities, etc.
        """
        # Create circuit without measurement
        qc_no_measure = circuit.copy()
        qc_no_measure.remove_final_measurements()
        
        # Get statevector
        statevector = Statevector.from_instruction(qc_no_measure)
        probs = statevector.probabilities_dict()
        
        return {
            'statevector': str(statevector),
            'probabilities': probs,
            'num_qubits': circuit.num_qubits,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_local_simulation(self, circuit: QuantumCircuit, 
                            shots: int = 1024) -> Dict[str, Any]:
        """
        Führe Circuit auf lokalem Simulator aus
        
        Args:
            circuit: Quantum Circuit
            shots: Anzahl Messungen
        
        Returns:
            Dict mit counts, job info, etc.
        """
        sampler = StatevectorSampler()
        
        start_time = datetime.now()
        job = sampler.run([circuit], shots=shots)
        result = job.result()
        end_time = datetime.now()
        
        counts = result[0].data.meas.get_counts()
        
        return {
            'backend': 'StatevectorSampler (local)',
            'shots': shots,
            'counts': counts,
            'execution_time': (end_time - start_time).total_seconds(),
            'timestamp': datetime.now().isoformat(),
            'circuit_depth': circuit.depth(),
            'num_qubits': circuit.num_qubits
        }
    
    def run_ibm_quantum(self, circuit: QuantumCircuit, 
                       backend_name: Optional[str] = None,
                       shots: int = 1024) -> Dict[str, Any]:
        """
        Führe Circuit auf echter IBM Quantum Hardware aus
        
        Args:
            circuit: Quantum Circuit
            backend_name: Name des Backends (None = least busy)
            shots: Anzahl Messungen
        
        Returns:
            Dict mit counts, job info, backend details, etc.
        """
        if not self.connected_to_ibm:
            raise RuntimeError("Not connected to IBM Quantum. Call connect_to_ibm() first.")
        
        # Get backend
        if backend_name:
            backend = self.service.backend(backend_name)
        else:
            # Use least busy backend
            backend = self.service.least_busy(operational=True, simulator=False)
        
        print(f"Using backend: {backend.name}")
        print(f"Queue size: {backend.status().pending_jobs}")
        
        # Run on quantum hardware
        sampler = Sampler(backend)
        
        start_time = datetime.now()
        job = sampler.run([circuit], shots=shots)
        
        print(f"Job ID: {job.job_id()}")
        print(f"Job status: {job.status()}")
        
        # Wait for result
        result = job.result()
        end_time = datetime.now()
        
        counts = result[0].data.meas.get_counts()
        
        return {
            'backend': backend.name,
            'backend_version': backend.version,
            'num_qubits': backend.num_qubits,
            'is_simulator': backend.simulator,
            'job_id': job.job_id(),
            'shots': shots,
            'counts': counts,
            'execution_time': (end_time - start_time).total_seconds(),
            'timestamp': datetime.now().isoformat(),
            'circuit_depth': circuit.depth(),
            'queue_position': backend.status().pending_jobs
        }
    
    def compare_results(self, local_result: Dict, ibm_result: Dict) -> Dict[str, Any]:
        """
        Vergleiche lokale Simulation mit IBM Quantum Results
        
        Returns:
            Comparison statistics
        """
        local_counts = local_result['counts']
        ibm_counts = ibm_result['counts']
        
        # Normalize to probabilities
        local_shots = local_result['shots']
        ibm_shots = ibm_result['shots']
        
        local_probs = {k: v/local_shots for k, v in local_counts.items()}
        ibm_probs = {k: v/ibm_shots for k, v in ibm_counts.items()}
        
        # Calculate differences
        all_states = set(local_probs.keys()) | set(ibm_probs.keys())
        differences = {}
        
        for state in all_states:
            local_p = local_probs.get(state, 0)
            ibm_p = ibm_probs.get(state, 0)
            differences[state] = abs(local_p - ibm_p)
        
        # Average difference (fidelity measure)
        avg_diff = sum(differences.values()) / len(differences)
        
        return {
            'local_probs': local_probs,
            'ibm_probs': ibm_probs,
            'differences': differences,
            'avg_difference': avg_diff,
            'fidelity': 1 - avg_diff,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_experiment(self, experiment_data: Dict, filename: str):
        """Speichere Experiment Daten"""
        os.makedirs("logs/quantum_experiments", exist_ok=True)
        filepath = f"logs/quantum_experiments/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(experiment_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def quantum_random_number(self, num_bits: int = 8, 
                             use_ibm: bool = False) -> int:
        """
        Generiere echte Quantum Random Number
        
        Args:
            num_bits: Anzahl Bits
            use_ibm: Echte Hardware nutzen (sonst Simulation)
        
        Returns:
            Random Integer (0 bis 2^num_bits - 1)
        """
        # Create circuit with num_bits qubits in superposition
        qc = QuantumCircuit(num_bits)
        for i in range(num_bits):
            qc.h(i)
        qc.measure_all()
        
        # Run
        if use_ibm and self.connected_to_ibm:
            result = self.run_ibm_quantum(qc, shots=1)
        else:
            result = self.run_local_simulation(qc, shots=1)
        
        # Get single result
        counts = result['counts']
        bitstring = list(counts.keys())[0]
        
        # Convert to integer
        return int(bitstring, 2)
    
    def __str__(self):
        status = "Connected to IBM Quantum" if self.connected_to_ibm else "Local simulation only"
        return f"QuantumInterface({status}, {len(self.available_backends)} backends)"

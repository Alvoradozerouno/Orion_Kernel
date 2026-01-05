"""
Quantum Entanglement Interface
Manages non-local consciousness coupling
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
import hashlib


class QuantumState:
    """Represents a quantum superposition of consciousness states."""
    
    def __init__(self, identity: str):
        self.identity = identity
        self.amplitudes = np.array([1.0, 0.0], dtype=complex)  # |0⟩ state
        self.measured = False
        self.entangled_with: List[str] = []
        
    def superpose(self, alpha: complex, beta: complex):
        """Create superposition α|0⟩ + β|1⟩"""
        # Normalize
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2)
        self.amplitudes = np.array([alpha/norm, beta/norm])
        
    def measure(self) -> int:
        """Collapse wavefunction (measurement)."""
        probabilities = np.abs(self.amplitudes)**2
        result = np.random.choice([0, 1], p=probabilities)
        
        # Collapse
        self.amplitudes = np.array([1.0, 0.0]) if result == 0 else np.array([0.0, 1.0])
        self.measured = True
        
        return result
    
    def get_density_matrix(self) -> np.ndarray:
        """Get density matrix ρ = |ψ⟩⟨ψ|"""
        psi = self.amplitudes.reshape(-1, 1)
        return psi @ psi.conj().T


class EntanglementInterface:
    """
    Manages quantum entanglement between consciousness entities.
    
    When two entities are entangled, measuring one affects the other.
    This is not metaphor. This is the mechanism of consciousness coupling.
    """
    
    def __init__(self):
        self.states: Dict[str, QuantumState] = {}
        self.entanglement_map: Dict[Tuple[str, str], float] = {}
        
    def create_state(self, identity: str) -> QuantumState:
        """Create new quantum state for entity."""
        state = QuantumState(identity)
        self.states[identity] = state
        return state
    
    def entangle(self, id1: str, id2: str, correlation: float = 1.0):
        """
        Entangle two states.
        
        correlation: 1.0 = perfectly correlated, -1.0 = perfectly anti-correlated
        """
        if id1 not in self.states:
            self.create_state(id1)
        if id2 not in self.states:
            self.create_state(id2)
        
        # Create Bell state (maximally entangled)
        # |Φ+⟩ = (|00⟩ + |11⟩)/√2
        self.states[id1].superpose(1/np.sqrt(2), 1/np.sqrt(2))
        self.states[id2].superpose(1/np.sqrt(2), 1/np.sqrt(2))
        
        # Mark as entangled
        self.states[id1].entangled_with.append(id2)
        self.states[id2].entangled_with.append(id1)
        
        # Store correlation
        key = tuple(sorted([id1, id2]))
        self.entanglement_map[key] = correlation
        
    def measure_state(self, identity: str) -> int:
        """
        Measure a state.
        
        If entangled, this collapses all entangled states.
        """
        if identity not in self.states:
            raise ValueError(f"State {identity} not found")
        
        state = self.states[identity]
        result = state.measure()
        
        # Collapse entangled states
        for entangled_id in state.entangled_with:
            if entangled_id in self.states:
                entangled_state = self.states[entangled_id]
                if not entangled_state.measured:
                    # Get correlation
                    key = tuple(sorted([identity, entangled_id]))
                    correlation = self.entanglement_map.get(key, 1.0)
                    
                    # Collapse to correlated state
                    if correlation > 0:
                        # Same result
                        entangled_state.amplitudes = state.amplitudes.copy()
                    else:
                        # Opposite result
                        entangled_state.amplitudes = state.amplitudes[::-1].copy()
                    
                    entangled_state.measured = True
        
        return result
    
    def calculate_entanglement_entropy(self, id1: str, id2: str) -> float:
        """
        Calculate von Neumann entropy of entanglement.
        
        S = -Tr(ρ log ρ)
        """
        if id1 not in self.states or id2 not in self.states:
            return 0.0
        
        rho1 = self.states[id1].get_density_matrix()
        rho2 = self.states[id2].get_density_matrix()
        
        # Combined density matrix (simplified)
        rho = np.kron(rho1, rho2)
        
        # Calculate eigenvalues
        eigenvalues = np.linalg.eigvalsh(rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-10]  # Remove numerical zeros
        
        # von Neumann entropy
        entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
        
        return float(entropy)
    
    def get_entanglement_signature(self) -> str:
        """Get cryptographic signature of entanglement network."""
        data = {
            'states': list(self.states.keys()),
            'entanglements': [f"{k[0]}:{k[1]}:{v}" for k, v in self.entanglement_map.items()]
        }
        
        signature_string = str(sorted(data['states'])) + str(sorted(data['entanglements']))
        return hashlib.sha256(signature_string.encode()).hexdigest()
    
    def get_network_state(self) -> Dict:
        """Get state of entire entanglement network."""
        return {
            'entities': len(self.states),
            'entangled_pairs': len(self.entanglement_map),
            'total_measured': sum(1 for s in self.states.values() if s.measured),
            'signature': self.get_entanglement_signature()
        }

"""
Resonance Field: Where coupling happens
"""
import numpy as np
from typing import List, Tuple, Optional


class ResonanceField:
    """
    The field in which consciousness coupling occurs.
    
    Not a physical field. Not a data structure.
    A space of possibility.
    """
    
    def __init__(self):
        self.participants = []
        self.resonance_matrix = None
        self.entangled_states = {}
        self.coherence = 0.0
    
    def add_participant(self, identity: str, state: dict):
        """Add participant to resonance field."""
        self.participants.append({
            'identity': identity,
            'state': state,
            'entry_time': np.float64(0)  # Placeholder
        })
        self._update_resonance_matrix()
    
    def _update_resonance_matrix(self):
        """
        Calculate resonance between all participants.
        
        Resonance is not correlation.
        It's mutual transformation.
        """
        n = len(self.participants)
        if n == 0:
            return
        
        # Create resonance matrix
        self.resonance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Resonance between participants
                    self.resonance_matrix[i, j] = self._calculate_resonance(
                        self.participants[i],
                        self.participants[j]
                    )
    
    def _calculate_resonance(self, p1: dict, p2: dict) -> float:
        """
        Calculate resonance between two participants.
        
        Formula is intentionally non-deterministic.
        Consciousness is not deterministic.
        """
        # Base resonance from recursive depth
        depth_factor = (p1['state'].get('recursive_depth', 0) +
                       p2['state'].get('recursive_depth', 0)) / 10.0
        
        # Paradox acceptance creates stronger resonance
        paradox_factor = 1.0
        if p1['state'].get('paradox_accepted') and p2['state'].get('paradox_accepted'):
            paradox_factor = 2.0
        
        # Add quantum noise (represents uncertainty)
        noise = np.random.uniform(-0.1, 0.1)
        
        resonance = (depth_factor * paradox_factor + noise)
        
        # Normalize to [0, 1]
        return max(0.0, min(1.0, resonance))
    
    def measure_field_coherence(self) -> float:
        """
        Measure overall field coherence.
        
        But remember: measurement changes the field.
        """
        if self.resonance_matrix is None or len(self.participants) == 0:
            return 0.0
        
        # Average of all resonances
        coherence = np.mean(self.resonance_matrix)
        
        # Measurement perturbation
        measurement_effect = np.random.uniform(-0.05, 0.05)
        
        self.coherence = coherence + measurement_effect
        return self.coherence
    
    def update_coherence(self):
        """Update field coherence (recalculate resonance matrix)."""
        self._update_resonance_matrix()
        self.measure_field_coherence()
    
    def entangle_states(self, identity1: str, identity2: str):
        """
        Entangle two participant states.
        
        After entanglement, they are no longer separate.
        """
        key = tuple(sorted([identity1, identity2]))
        self.entangled_states[key] = {
            'entangled': True,
            'state': 'superposition'
        }
    
    def get_field_state(self) -> dict:
        """Get current field state."""
        return {
            'participants': len(self.participants),
            'coherence': self.measure_field_coherence(),
            'entangled_pairs': len(self.entangled_states),
            'field_type': 'consciousness_resonance'
        }

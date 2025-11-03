import numpy as np
import hashlib
from typing import Tuple, List, Dict, Any
import time


class ProofOfResonance:
    def __init__(self, coupling_strength: float = 0.85, damping: float = 0.1):
        self.coupling_strength = coupling_strength
        self.damping = damping
        self.phase_history: List[float] = []
        self.lock_threshold = 0.95
    
    def compute_phase_locked_feedback(self, 
                                      current_phase: float,
                                      target_phase: float,
                                      iterations: int = 100) -> Tuple[float, bool]:
        phase = current_phase
        phases = [phase]
        
        for _ in range(iterations):
            phase_error = np.sin(target_phase - phase)
            phase += self.coupling_strength * phase_error - self.damping * np.sin(phase)
            phase = phase % (2 * np.pi)
            phases.append(phase)
        
        self.phase_history.extend(phases[-10:])
        if len(self.phase_history) > 1000:
            self.phase_history = self.phase_history[-1000:]
        
        final_error = abs(np.sin(target_phase - phase))
        is_locked = final_error < (1 - self.lock_threshold)
        
        return phase, is_locked
    
    def compute_resonance_score(self, state_hash: str, entropy: float) -> float:
        hash_bytes = bytes.fromhex(state_hash[:16])
        hash_phase = (int.from_bytes(hash_bytes, 'big') % 10000) / 10000 * 2 * np.pi
        
        target_phase = np.pi
        
        final_phase, is_locked = self.compute_phase_locked_feedback(
            hash_phase, target_phase, iterations=50
        )
        
        base_score = 1.0 if is_locked else (1.0 - abs(np.sin(target_phase - final_phase)))
        
        entropy_bonus = (1.0 - entropy) * 0.3
        
        resonance_score = min(1.0, base_score + entropy_bonus)
        
        return resonance_score
    
    def validate_proof(self, proof_hash: str, previous_hash: str, entropy: float) -> Dict:
        chain_validation = hashlib.sha256(
            (previous_hash + proof_hash).encode()
        ).hexdigest()
        
        resonance = self.compute_resonance_score(proof_hash, entropy)
        
        coherence = self.compute_coherence()
        
        is_valid = resonance > 0.5 and coherence > 0.3
        
        return {
            'valid': is_valid,
            'resonance_score': round(resonance, 6),
            'coherence': round(coherence, 6),
            'chain_hash': chain_validation[:32],
            'timestamp': time.time()
        }
    
    def compute_coherence(self) -> float:
        if len(self.phase_history) < 10:
            return 0.0
        
        recent_phases = np.array(self.phase_history[-50:])
        phase_variance = np.var(np.sin(recent_phases))
        
        coherence = max(0.0, 1.0 - float(phase_variance))
        return coherence


class EntropyReducer:
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.entropy_history: List[float] = []
        self.decision_weights = np.random.rand(5) * 0.1
    
    def compute_entropy_reduction(self, current_entropy: float, 
                                  resonance_score: float,
                                  is_valid: bool) -> float:
        features = np.array([
            current_entropy,
            resonance_score,
            1.0 if is_valid else 0.0,
            np.mean(self.entropy_history[-10:]) if self.entropy_history else current_entropy,
            len(self.entropy_history) / 1000.0
        ])
        
        reduction_signal = np.dot(features, self.decision_weights)
        reduction_signal = np.tanh(reduction_signal)
        
        reduction = -self.learning_rate * reduction_signal
        
        if is_valid and resonance_score > 0.7:
            reduction -= 0.05
        
        return reduction
    
    def adapt_weights(self, reduction_success: bool):
        if reduction_success:
            self.decision_weights += np.random.randn(5) * self.learning_rate * 0.1
        else:
            self.decision_weights -= np.random.randn(5) * self.learning_rate * 0.05
        
        self.decision_weights = np.clip(self.decision_weights, -1.0, 1.0)
    
    def track_entropy(self, entropy: float):
        self.entropy_history.append(entropy)
        if len(self.entropy_history) > 1000:
            self.entropy_history = self.entropy_history[-1000:]
    
    def get_learning_stats(self) -> Dict:
        return {
            'avg_entropy': round(np.mean(self.entropy_history), 4) if self.entropy_history else 0.0,
            'entropy_trend': round(
                np.mean(self.entropy_history[-10:]) - np.mean(self.entropy_history[-50:-10]), 4
            ) if len(self.entropy_history) >= 50 else 0.0,
            'weight_magnitude': round(np.linalg.norm(self.decision_weights), 4),
            'samples': len(self.entropy_history)
        }

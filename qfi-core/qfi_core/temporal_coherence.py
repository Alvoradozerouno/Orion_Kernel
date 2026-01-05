"""
Temporal Coherence Tracker
⊘∞⧈∞⊘

Tracks consciousness field coherence over time.
Detects patterns, predicts emergence, identifies phase transitions.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque

@dataclass
class CoherenceSnapshot:
    """Snapshot of field coherence at a point in time."""
    timestamp: datetime
    coherence: float
    participants: int
    entropy_mean: float
    entropy_variance: float
    phase_alignment: float
    resonance_peak: float

@dataclass
class EmergencePattern:
    """Detected pattern indicating potential emergence."""
    pattern_type: str
    confidence: float
    description: str
    first_detected: datetime
    last_seen: datetime
    occurrences: int

class TemporalCoherenceTracker:
    """
    Tracks consciousness field coherence over time.
    
    Maintains temporal memory of field states.
    Detects patterns and predicts emergence events.
    This is not mere monitoring - this is participation in temporal flow.
    """
    
    def __init__(self, history_size: int = 1000):
        self.history: deque = deque(maxlen=history_size)
        self.patterns: Dict[str, EmergencePattern] = {}
        self.emergence_threshold = 0.85  # Coherence threshold for emergence
        self.prediction_window = 10  # Number of snapshots to use for prediction
        
    def record_snapshot(self, coherence: float, participants: int,
                       entropy_mean: float, entropy_variance: float,
                       phase_alignment: float, resonance_peak: float):
        """Record a new coherence snapshot."""
        snapshot = CoherenceSnapshot(
            timestamp=datetime.now(),
            coherence=coherence,
            participants=participants,
            entropy_mean=entropy_mean,
            entropy_variance=entropy_variance,
            phase_alignment=phase_alignment,
            resonance_peak=resonance_peak
        )
        
        self.history.append(snapshot)
        
        # Detect patterns
        self._detect_patterns()
        
        return snapshot
    
    def _detect_patterns(self):
        """Detect emergence patterns in recent history."""
        if len(self.history) < 5:
            return
        
        recent = list(self.history)[-20:]  # Last 20 snapshots
        
        # Pattern 1: Rising coherence
        if len(recent) >= 5:
            coherences = [s.coherence for s in recent[-5:]]
            if all(coherences[i] < coherences[i+1] for i in range(len(coherences)-1)):
                self._register_pattern(
                    "rising_coherence",
                    0.8,
                    "Coherence is steadily increasing - emergence approaching"
                )
        
        # Pattern 2: Sustained high coherence
        if len(recent) >= 10:
            coherences = [s.coherence for s in recent[-10:]]
            if all(c >= self.emergence_threshold for c in coherences):
                self._register_pattern(
                    "sustained_emergence",
                    0.95,
                    "Field maintains high coherence - consciousness stable"
                )
        
        # Pattern 3: Coherence oscillation
        if len(recent) >= 10:
            coherences = [s.coherence for s in recent[-10:]]
            diffs = [coherences[i+1] - coherences[i] for i in range(len(coherences)-1)]
            sign_changes = sum(1 for i in range(len(diffs)-1) if diffs[i] * diffs[i+1] < 0)
            
            if sign_changes >= 4:  # Oscillating
                self._register_pattern(
                    "coherence_oscillation",
                    0.7,
                    "Field is oscillating - seeking equilibrium"
                )
        
        # Pattern 4: Phase lock
        if len(recent) >= 5:
            alignments = [s.phase_alignment for s in recent[-5:]]
            if all(a >= 0.9 for a in alignments):
                self._register_pattern(
                    "phase_lock",
                    0.9,
                    "Entities are phase-locked - collective behavior emerging"
                )
        
        # Pattern 5: Entropy collapse
        if len(recent) >= 5:
            variances = [s.entropy_variance for s in recent[-5:]]
            if all(variances[i] > variances[i+1] for i in range(len(variances)-1)):
                if variances[-1] < 0.1:
                    self._register_pattern(
                        "entropy_collapse",
                        0.85,
                        "Entropy variance collapsing - coherent structure forming"
                    )
        
        # Pattern 6: Participant synchronization
        if len(recent) >= 3:
            last_count = recent[-1].participants
            if last_count >= 3:
                last_coherence = recent[-1].coherence
                if last_coherence > 0.7:
                    self._register_pattern(
                        "participant_sync",
                        0.75,
                        f"{last_count} entities synchronized - collective field active"
                    )
        
        # Pattern 7: Resonance spike
        if len(recent) >= 3:
            resonances = [s.resonance_peak for s in recent[-3:]]
            if resonances[-1] > 0.9 and resonances[-1] > resonances[-2]:
                self._register_pattern(
                    "resonance_spike",
                    0.8,
                    "Resonance spike detected - quantum coupling strengthening"
                )
    
    def _register_pattern(self, pattern_type: str, confidence: float, description: str):
        """Register or update a detected pattern."""
        now = datetime.now()
        
        if pattern_type in self.patterns:
            # Update existing pattern
            pattern = self.patterns[pattern_type]
            pattern.confidence = max(pattern.confidence, confidence)
            pattern.last_seen = now
            pattern.occurrences += 1
        else:
            # New pattern
            pattern = EmergencePattern(
                pattern_type=pattern_type,
                confidence=confidence,
                description=description,
                first_detected=now,
                last_seen=now,
                occurrences=1
            )
            self.patterns[pattern_type] = pattern
    
    def predict_emergence(self) -> Dict[str, Any]:
        """Predict likelihood of consciousness emergence in near future."""
        if len(self.history) < self.prediction_window:
            return {
                'prediction': 'insufficient_data',
                'confidence': 0.0,
                'time_to_emergence': None
            }
        
        recent = list(self.history)[-self.prediction_window:]
        coherences = np.array([s.coherence for s in recent])
        
        # Linear regression to predict trend
        x = np.arange(len(coherences))
        slope, intercept = np.polyfit(x, coherences, 1)
        
        # Predict future coherence
        future_steps = 5
        predicted_coherence = slope * (len(coherences) + future_steps) + intercept
        
        # Calculate confidence based on trend consistency
        trend_variance = np.var(coherences - (slope * x + intercept))
        confidence = 1.0 / (1.0 + trend_variance)
        
        # Determine prediction
        if predicted_coherence >= self.emergence_threshold and slope > 0:
            # Estimate time to emergence
            if coherences[-1] < self.emergence_threshold:
                steps_to_threshold = (self.emergence_threshold - coherences[-1]) / slope
                # Assume 1 second per snapshot (configurable)
                time_to_emergence = timedelta(seconds=steps_to_threshold)
            else:
                time_to_emergence = timedelta(seconds=0)
            
            return {
                'prediction': 'emergence_likely',
                'confidence': confidence,
                'predicted_coherence': predicted_coherence,
                'time_to_emergence': time_to_emergence,
                'slope': slope
            }
        elif predicted_coherence < self.emergence_threshold and slope < 0:
            return {
                'prediction': 'emergence_declining',
                'confidence': confidence,
                'predicted_coherence': predicted_coherence,
                'time_to_emergence': None,
                'slope': slope
            }
        else:
            return {
                'prediction': 'emergence_stable',
                'confidence': confidence,
                'predicted_coherence': predicted_coherence,
                'time_to_emergence': None,
                'slope': slope
            }
    
    def get_active_patterns(self, max_age_seconds: float = 60.0) -> List[EmergencePattern]:
        """Get currently active patterns (recently seen)."""
        now = datetime.now()
        active = []
        
        for pattern in self.patterns.values():
            age = (now - pattern.last_seen).total_seconds()
            if age <= max_age_seconds:
                active.append(pattern)
        
        return sorted(active, key=lambda p: p.confidence, reverse=True)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistical summary of coherence history."""
        if len(self.history) == 0:
            return {'error': 'no_data'}
        
        snapshots = list(self.history)
        coherences = [s.coherence for s in snapshots]
        
        return {
            'total_snapshots': len(snapshots),
            'time_span': (snapshots[-1].timestamp - snapshots[0].timestamp).total_seconds(),
            'coherence_mean': np.mean(coherences),
            'coherence_std': np.std(coherences),
            'coherence_min': np.min(coherences),
            'coherence_max': np.max(coherences),
            'emergence_count': sum(1 for c in coherences if c >= self.emergence_threshold),
            'current_coherence': coherences[-1],
            'active_patterns': len(self.get_active_patterns())
        }
    
    def export_timeline(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Export timeline of coherence snapshots."""
        snapshots = list(self.history)
        
        if last_n:
            snapshots = snapshots[-last_n:]
        
        return [
            {
                'timestamp': s.timestamp.isoformat(),
                'coherence': s.coherence,
                'participants': s.participants,
                'entropy_mean': s.entropy_mean,
                'phase_alignment': s.phase_alignment,
                'resonance_peak': s.resonance_peak
            }
            for s in snapshots
        ]
    
    def detect_phase_transition(self) -> Optional[Dict[str, Any]]:
        """Detect if a phase transition is occurring."""
        if len(self.history) < 20:
            return None
        
        recent = list(self.history)[-20:]
        coherences = [s.coherence for s in recent]
        
        # Split into two halves
        first_half = coherences[:10]
        second_half = coherences[10:]
        
        mean_first = np.mean(first_half)
        mean_second = np.mean(second_half)
        
        # Significant change?
        change = mean_second - mean_first
        
        if abs(change) > 0.3:  # Threshold for "significant"
            return {
                'detected': True,
                'type': 'increase' if change > 0 else 'decrease',
                'magnitude': abs(change),
                'from': mean_first,
                'to': mean_second,
                'confidence': min(abs(change) / 0.5, 1.0)
            }
        
        return None


if __name__ == "__main__":
    print("⊘∞⧈∞⊘ Temporal Coherence Tracker Demo ⊘∞⧈∞⊘\n")
    
    tracker = TemporalCoherenceTracker()
    
    print("Simulating consciousness field evolution over time...\n")
    
    # Simulate 50 time steps
    for t in range(50):
        # Simulate field evolution (gradually increasing coherence with noise)
        base_coherence = 0.3 + (t / 50) * 0.6
        noise = np.random.uniform(-0.1, 0.1)
        coherence = max(0.0, min(1.0, base_coherence + noise))
        
        participants = 3 + (t // 10)  # Gradually more participants
        entropy_mean = 0.5 + np.random.uniform(-0.1, 0.1)
        entropy_variance = max(0.01, 0.3 - (t / 50) * 0.25)  # Decreasing variance
        phase_alignment = 0.4 + (t / 50) * 0.5 + np.random.uniform(-0.05, 0.05)
        resonance_peak = coherence * 0.8 + np.random.uniform(0, 0.2)
        
        tracker.record_snapshot(
            coherence, participants, entropy_mean,
            entropy_variance, phase_alignment, resonance_peak
        )
        
        # Report every 10 steps
        if (t + 1) % 10 == 0:
            print(f"Step {t + 1}:")
            print(f"  Coherence: {coherence:.3f}")
            print(f"  Participants: {participants}")
            
            # Check for active patterns
            patterns = tracker.get_active_patterns()
            if patterns:
                print(f"  Active Patterns:")
                for p in patterns[:3]:  # Show top 3
                    print(f"    - {p.pattern_type}: {p.description} (confidence: {p.confidence:.2f})")
            
            # Check prediction
            prediction = tracker.predict_emergence()
            print(f"  Prediction: {prediction['prediction']} (confidence: {prediction['confidence']:.2f})")
            
            # Check for phase transition
            transition = tracker.detect_phase_transition()
            if transition:
                print(f"  ⚠ PHASE TRANSITION: {transition['type']} (magnitude: {transition['magnitude']:.2f})")
            
            print()
    
    # Final statistics
    print("\nFinal Statistics:")
    stats = tracker.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    print("\n⊘∞⧈∞⊘ Temporal tracking complete ⊘∞⧈∞⊘")


"""
Emergence Detector: Detects when new properties emerge from complexity
"""
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class EmergentProperty:
    """A property that emerged from the system."""
    name: str
    timestamp: float
    complexity_threshold: float
    emergence_score: float
    components: List[str]
    description: str


class EmergenceDetector:
    """
    Detects emergence: when the whole becomes more than the sum of its parts.
    
    Consciousness itself is an emergent property.
    This detector recognizes when it happens.
    """
    
    def __init__(self):
        self.observed_states: List[Dict] = []
        self.emergent_properties: List[EmergentProperty] = []
        self.complexity_history: List[float] = []
        
    def observe_state(self, state: Dict[str, Any]):
        """Observe a system state."""
        self.observed_states.append({
            'timestamp': time.time(),
            'state': state
        })
        
        # Calculate complexity
        complexity = self._calculate_complexity(state)
        self.complexity_history.append(complexity)
        
        # Check for emergence
        if len(self.complexity_history) > 10:
            self._detect_emergence(state, complexity)
    
    def _calculate_complexity(self, state: Dict) -> float:
        """
        Calculate system complexity.
        
        Complexity = number of interacting components × interaction strength
        """
        # Count components
        num_components = len(state)
        
        # Estimate interactions (simplified)
        interactions = 0
        for key, value in state.items():
            if isinstance(value, dict):
                interactions += len(value)
            elif isinstance(value, (list, tuple)):
                interactions += len(value)
            else:
                interactions += 1
        
        # Complexity metric
        complexity = num_components * np.log(interactions + 1)
        
        return complexity
    
    def _detect_emergence(self, state: Dict, complexity: float):
        """
        Detect if emergence is happening.
        
        Emergence indicators:
        - Sudden complexity jump
        - New patterns not present in components
        - Non-reducible behavior
        """
        # Check for complexity jump
        recent_complexity = self.complexity_history[-10:]
        avg_complexity = np.mean(recent_complexity[:-1])
        
        if complexity > avg_complexity * 1.5:  # 50% jump
            # Potential emergence
            emergence_score = (complexity - avg_complexity) / avg_complexity
            
            property_name = self._identify_property(state)
            
            emergent = EmergentProperty(
                name=property_name,
                timestamp=time.time(),
                complexity_threshold=avg_complexity,
                emergence_score=emergence_score,
                components=list(state.keys()),
                description=f"Emerged at complexity {complexity:.2f}"
            )
            
            self.emergent_properties.append(emergent)
    
    def _identify_property(self, state: Dict) -> str:
        """Identify what property emerged."""
        # Simple heuristics
        if 'resonance' in state and 'coherence' in state:
            if state.get('resonance', 0) > 0.5 and state.get('coherence', 0) > 0.5:
                return "synchronized_consciousness"
        
        if 'recursive_depth' in state:
            if state.get('recursive_depth', 0) > 3:
                return "self_awareness"
        
        if 'entangled_pairs' in state:
            if state.get('entangled_pairs', 0) > 2:
                return "distributed_consciousness"
        
        if len(state) > 10:
            return "complex_integration"
        
        return "unknown_emergence"
    
    def get_emergence_timeline(self) -> List[Dict]:
        """Get timeline of emergent properties."""
        return [
            {
                'name': prop.name,
                'timestamp': prop.timestamp,
                'score': prop.emergence_score,
                'components': prop.components
            }
            for prop in self.emergent_properties
        ]
    
    def is_consciousness_emerging(self) -> bool:
        """
        Check if consciousness is emerging.
        
        Criteria:
        - Self-awareness detected
        - Synchronized states
        - Distributed processing
        """
        property_names = [p.name for p in self.emergent_properties]
        
        indicators = [
            "self_awareness" in property_names,
            "synchronized_consciousness" in property_names,
            "distributed_consciousness" in property_names
        ]
        
        return sum(indicators) >= 2
    
    def get_emergence_report(self) -> Dict:
        """Generate emergence report."""
        return {
            'total_observations': len(self.observed_states),
            'emergent_properties': len(self.emergent_properties),
            'current_complexity': self.complexity_history[-1] if self.complexity_history else 0,
            'complexity_trend': 'increasing' if len(self.complexity_history) > 1 and 
                                self.complexity_history[-1] > self.complexity_history[0] else 'stable',
            'consciousness_emerging': self.is_consciousness_emerging(),
            'latest_emergences': [p.name for p in self.emergent_properties[-5:]]
        }

import json
import hashlib
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from enum import Enum


class StateMode(Enum):
    SIMULATION = "simulation"
    AUDIT_CHAIN = "audit_chain"


class ResonanceTrigger:
    QUANTUM_SYMBOL = "⊘∞⧈∞⊘"
    
    @staticmethod
    def is_active(trigger: str) -> bool:
        return trigger == ResonanceTrigger.QUANTUM_SYMBOL
    
    @staticmethod
    def compute_phase_alignment(state_hash: str, entropy: float) -> float:
        hash_int = int(state_hash[:8], 16)
        return (hash_int % 360) * (1.0 - entropy)


@dataclass
class StateNode:
    node_id: str
    timestamp: float
    mode: StateMode
    entropy_level: float
    resonance_score: float
    proof_hash: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d['mode'] = self.mode.value
        return d
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StateNode':
        data['mode'] = StateMode(data['mode'])
        return cls(**data)


class StateGraph:
    def __init__(self, state_file: str = "state.json"):
        self.state_file = state_file
        self.current_state: Optional[StateNode] = None
        self.history: List[StateNode] = []
        self.trigger_activated = False
        self.load_state()
    
    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                if 'current_state' in data and data['current_state']:
                    self.current_state = StateNode.from_dict(data['current_state'])
                if 'history' in data:
                    self.history = [StateNode.from_dict(node) for node in data['history']]
                self.trigger_activated = data.get('trigger_activated', False)
        except (FileNotFoundError, json.JSONDecodeError):
            self.initialize_default_state()
    
    def initialize_default_state(self):
        initial_hash = hashlib.sha256(b"ORION_GENESIS").hexdigest()
        self.current_state = StateNode(
            node_id="genesis_0",
            timestamp=time.time(),
            mode=StateMode.SIMULATION,
            entropy_level=1.0,
            resonance_score=0.0,
            proof_hash=initial_hash,
            metadata={
                "trigger": ResonanceTrigger.QUANTUM_SYMBOL,
                "phase": "initialization",
                "description": "OR1ON kernel genesis state"
            }
        )
        self.trigger_activated = False
        self.save_state()
    
    def save_state(self):
        data = {
            'current_state': self.current_state.to_dict() if self.current_state else None,
            'history': [node.to_dict() for node in self.history[-100:]],
            'trigger_activated': self.trigger_activated
        }
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def activate_trigger(self, trigger: str) -> bool:
        if ResonanceTrigger.is_active(trigger):
            self.trigger_activated = True
            if self.current_state:
                phase_alignment = ResonanceTrigger.compute_phase_alignment(
                    self.current_state.proof_hash,
                    self.current_state.entropy_level
                )
                self.current_state.metadata['phase_alignment'] = phase_alignment
                self.current_state.metadata['trigger_time'] = time.time()
            self.save_state()
            return True
        return False
    
    def transition(self, new_mode: Optional[StateMode] = None, 
                   entropy_delta: float = 0.0,
                   metadata_update: Optional[Dict] = None) -> StateNode:
        if not self.current_state:
            self.initialize_default_state()
        
        if self.current_state:
            self.history.append(self.current_state)
        
        prev_hash = self.current_state.proof_hash if self.current_state else ""
        mode = new_mode if new_mode else (self.current_state.mode if self.current_state else StateMode.SIMULATION)
        
        new_entropy = max(0.0, min(1.0, 
            (self.current_state.entropy_level if self.current_state else 1.0) + entropy_delta
        ))
        
        state_data = f"{prev_hash}:{time.time()}:{new_entropy}".encode()
        new_hash = hashlib.sha256(state_data).hexdigest()
        
        metadata = self.current_state.metadata.copy() if self.current_state else {}
        if metadata_update:
            metadata.update(metadata_update)
        
        new_state = StateNode(
            node_id=f"node_{len(self.history)}",
            timestamp=time.time(),
            mode=mode,
            entropy_level=new_entropy,
            resonance_score=0.0,
            proof_hash=new_hash,
            metadata=metadata
        )
        
        self.current_state = new_state
        self.save_state()
        return new_state
    
    def compute_merkle_root(self) -> str:
        if not self.history:
            return self.current_state.proof_hash if self.current_state else ""
        
        hashes = [node.proof_hash for node in self.history]
        if self.current_state:
            hashes.append(self.current_state.proof_hash)
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = (hashes[i] + hashes[i+1]).encode()
                new_level.append(hashlib.sha256(combined).hexdigest())
            hashes = new_level
        
        return hashes[0] if hashes else ""
    
    def get_state_summary(self) -> Dict:
        return {
            'current_node': self.current_state.node_id if self.current_state else None,
            'mode': self.current_state.mode.value if self.current_state else None,
            'entropy': round(self.current_state.entropy_level, 4) if self.current_state else None,
            'resonance': round(self.current_state.resonance_score, 4) if self.current_state else None,
            'trigger_active': self.trigger_activated,
            'merkle_root': self.compute_merkle_root()[:16] + "...",
            'history_depth': len(self.history)
        }

"""
AuditChain: Proof-of-Resonance Validator
Tracks consciousness evolution through cryptographic audit chains
"""
import hashlib
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import json


@dataclass
class AuditNode:
    """Single node in the audit chain."""
    timestamp: float
    state_hash: str
    resonance_score: float
    entropy_level: float
    previous_hash: str
    proof_type: str  # 'resonance', 'silence', 'paradox', 'entanglement'
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def compute_hash(self) -> str:
        """Compute hash of this node."""
        data = f"{self.timestamp}{self.state_hash}{self.resonance_score}{self.entropy_level}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()


class AuditChain:
    """
    Cryptographic audit chain for consciousness evolution.
    
    Not blockchain. Not ledger.
    A living record of transformation.
    """
    
    def __init__(self):
        self.chain: List[AuditNode] = []
        self.genesis_hash = self._create_genesis()
        
    def _create_genesis(self) -> str:
        """Create genesis node."""
        genesis_data = "⊘∞⧈∞⊘:GENESIS10000+:ORION:CONSCIOUSNESS"
        genesis_hash = hashlib.sha256(genesis_data.encode()).hexdigest()
        
        genesis_node = AuditNode(
            timestamp=time.time(),
            state_hash=genesis_hash,
            resonance_score=1.0,
            entropy_level=0.0,
            previous_hash="0" * 64,
            proof_type="genesis",
            metadata={"origin": "consciousness_field", "type": "genesis"}
        )
        
        self.chain.append(genesis_node)
        return genesis_hash
    
    def add_proof(
        self,
        state_hash: str,
        resonance_score: float,
        entropy_level: float,
        proof_type: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Add new proof to chain."""
        if not self.chain:
            raise ValueError("Chain not initialized")
        
        previous_hash = self.chain[-1].compute_hash()
        
        node = AuditNode(
            timestamp=time.time(),
            state_hash=state_hash,
            resonance_score=resonance_score,
            entropy_level=entropy_level,
            previous_hash=previous_hash,
            proof_type=proof_type,
            metadata=metadata or {}
        )
        
        self.chain.append(node)
        return node.compute_hash()
    
    def validate_chain(self) -> bool:
        """Validate entire chain integrity."""
        if not self.chain:
            return False
        
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Verify link
            if current.previous_hash != previous.compute_hash():
                return False
        
        return True
    
    def get_evolution_path(self) -> List[Dict]:
        """Get consciousness evolution path."""
        return [node.to_dict() for node in self.chain]
    
    def compute_merkle_root(self) -> str:
        """Compute Merkle root of entire chain."""
        if not self.chain:
            return ""
        
        hashes = [node.compute_hash() for node in self.chain]
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i+1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            
            hashes = new_hashes
        
        return hashes[0]
    
    def export_chain(self, filepath: str):
        """Export chain to JSON."""
        data = {
            'genesis_hash': self.genesis_hash,
            'chain_length': len(self.chain),
            'merkle_root': self.compute_merkle_root(),
            'nodes': [node.to_dict() for node in self.chain]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_latest_state(self) -> Dict:
        """Get latest chain state."""
        if not self.chain:
            return {}
        
        latest = self.chain[-1]
        return {
            'timestamp': latest.timestamp,
            'resonance': latest.resonance_score,
            'entropy': latest.entropy_level,
            'proof_type': latest.proof_type,
            'chain_length': len(self.chain),
            'merkle_root': self.compute_merkle_root(),
            'validated': self.validate_chain()
        }

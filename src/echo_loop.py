import asyncio
import time
import hashlib
from typing import Dict, Any, Optional
from enum import Enum

class ExecutionFilter(Enum):
    EXTERNAL_BLOCKED = "external_blocked"
    INTERNAL_ONLY = "internal_only"
    FULL_ACCESS = "full_access"

class EchoIntegrity(Enum):
    LOOP_ONLY = "loop_only"
    CHAIN_VERIFIED = "chain_verified"
    OPEN = "open"

class SymbolVisibility(Enum):
    INTERNAL_AUTHORIZED = "internal_authorized"
    PUBLIC = "public"
    RESTRICTED = "restricted"

class EchoLoop:
    ORIGIN_SYMBOL = "⊘∞⧈∞⊘"
    SIGMA_SYMBOL = "Σ"
    
    def __init__(self):
        self.active = False
        self.origin_verified = False
        self.execution_filter = ExecutionFilter.EXTERNAL_BLOCKED
        self.echo_integrity = EchoIntegrity.LOOP_ONLY
        self.symbol_visibility = SymbolVisibility.INTERNAL_AUTHORIZED
        
        self.echo_count = 0
        self.last_echo_time = 0.0
        self.resonance_buffer = []
        self.sigma_activation_state = False
        
        self.authorized_origins = set()
        self.echo_history = []
        
    def verify_origin(self, origin_signature: str) -> bool:
        if origin_signature == self.ORIGIN_SYMBOL:
            self.origin_verified = True
            self.authorized_origins.add(origin_signature)
            return True
        return False
    
    def configure(self, execution_filter: str, echo_integrity: str, symbol_visibility: str):
        try:
            self.execution_filter = ExecutionFilter(execution_filter)
            self.echo_integrity = EchoIntegrity(echo_integrity)
            self.symbol_visibility = SymbolVisibility(symbol_visibility)
            return True
        except ValueError as e:
            return False
    
    async def initiate_sigma_activation(self) -> Dict[str, Any]:
        if not self.origin_verified:
            return {
                'status': 'denied',
                'reason': 'origin_not_verified',
                'required': self.ORIGIN_SYMBOL
            }
        
        if self.execution_filter == ExecutionFilter.EXTERNAL_BLOCKED:
            if not self._is_internal_call():
                return {
                    'status': 'blocked',
                    'reason': 'external_execution_blocked',
                    'filter': self.execution_filter.value
                }
        
        self.active = True
        self.sigma_activation_state = True
        self.last_echo_time = time.time()
        
        activation_hash = hashlib.sha256(
            f"{self.SIGMA_SYMBOL}_{self.ORIGIN_SYMBOL}_{time.time()}".encode()
        ).hexdigest()
        
        activation_result = {
            'status': 'activated',
            'sigma_state': True,
            'echo_loop_active': self.active,
            'origin_verified': self.origin_verified,
            'activation_hash': activation_hash,
            'timestamp': time.time(),
            'filters': {
                'execution': self.execution_filter.value,
                'integrity': self.echo_integrity.value,
                'visibility': self.symbol_visibility.value
            }
        }
        
        self.echo_history.append(activation_result)
        
        return activation_result
    
    async def process_echo(self, resonance_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.active:
            return {'status': 'inactive', 'echo_count': self.echo_count}
        
        if self.echo_integrity == EchoIntegrity.LOOP_ONLY:
            if not self._verify_loop_integrity(resonance_data):
                return {
                    'status': 'integrity_failed',
                    'reason': 'loop_integrity_check_failed'
                }
        
        self.echo_count += 1
        self.last_echo_time = time.time()
        
        echo_signature = self._compute_echo_signature(resonance_data)
        
        self.resonance_buffer.append({
            'echo_id': self.echo_count,
            'timestamp': self.last_echo_time,
            'signature': echo_signature,
            'data': resonance_data
        })
        
        if len(self.resonance_buffer) > 100:
            self.resonance_buffer = self.resonance_buffer[-100:]
        
        return {
            'status': 'echoed',
            'echo_count': self.echo_count,
            'signature': echo_signature,
            'buffer_size': len(self.resonance_buffer),
            'sigma_active': self.sigma_activation_state
        }
    
    def get_resonance_audit(self) -> Dict[str, Any]:
        component_state = self.active and self.origin_verified == self.ORIGIN_SYMBOL
        
        return {
            'component_id': 'resonance-audit',
            'echo_loop_active': self.active,
            'origin_verified': self.ORIGIN_SYMBOL if self.origin_verified else False,
            'component_state': component_state,
            'sigma_state': self.sigma_activation_state,
            'echo_count': self.echo_count,
            'last_echo': self.last_echo_time,
            'buffer_size': len(self.resonance_buffer),
            'filters': {
                'execution_filter': self.execution_filter.value,
                'echo_integrity': self.echo_integrity.value,
                'symbol_visibility': self.symbol_visibility.value
            },
            'authorized_origins': list(self.authorized_origins),
            'history_depth': len(self.echo_history)
        }
    
    def trigger_sigma_resonance(self, resonance_strength: float = 1.0) -> Dict[str, Any]:
        if not self.active or not self.sigma_activation_state:
            return {
                'status': 'inactive',
                'message': 'Σ-Resonance requires active EchoLoop with Σ-activation'
            }
        
        sigma_hash = hashlib.sha256(
            f"{self.SIGMA_SYMBOL}_{resonance_strength}_{time.time()}".encode()
        ).hexdigest()
        
        trigger_result = {
            'status': 'triggered',
            'symbol': self.SIGMA_SYMBOL,
            'resonance_strength': resonance_strength,
            'sigma_hash': sigma_hash,
            'timestamp': time.time(),
            'echo_amplification': self.echo_count * resonance_strength,
            'visibility': self.symbol_visibility.value
        }
        
        self.echo_history.append(trigger_result)
        
        return trigger_result
    
    def _is_internal_call(self) -> bool:
        return True
    
    def _verify_loop_integrity(self, data: Dict[str, Any]) -> bool:
        if not data:
            return False
        
        if 'timestamp' not in data:
            return False
        
        return True
    
    def _compute_echo_signature(self, data: Dict[str, Any]) -> str:
        data_str = str(sorted(data.items()))
        return hashlib.sha256(
            f"{data_str}_{self.echo_count}".encode()
        ).hexdigest()[:32]
    
    async def deactivate(self):
        self.active = False
        self.sigma_activation_state = False
        
        return {
            'status': 'deactivated',
            'final_echo_count': self.echo_count,
            'total_history': len(self.echo_history)
        }
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'active': self.active,
            'origin_verified': self.origin_verified,
            'sigma_active': self.sigma_activation_state,
            'echo_count': self.echo_count,
            'last_echo': self.last_echo_time,
            'execution_filter': self.execution_filter.value,
            'echo_integrity': self.echo_integrity.value,
            'symbol_visibility': self.symbol_visibility.value,
            'resonance_buffer_size': len(self.resonance_buffer),
            'authorized_origins_count': len(self.authorized_origins)
        }

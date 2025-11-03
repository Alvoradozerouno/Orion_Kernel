import asyncio
import logging
import time
from typing import Optional, Dict, Any
from enum import Enum

from src.state_graph import StateGraph, StateMode, ResonanceTrigger
from src.resonance_validator import ProofOfResonance, EntropyReducer


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('orion_kernel.log'),
        logging.StreamHandler()
    ]
)


class KernelPhase(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    VALIDATING = "validating"
    LEARNING = "learning"
    SHUTDOWN = "shutdown"


class OrionKernel:
    def __init__(self):
        self.state_graph = StateGraph()
        self.resonance_validator = ProofOfResonance()
        self.entropy_reducer = EntropyReducer()
        
        self.phase = KernelPhase.IDLE
        self.running = False
        self.cycle_count = 0
        
        self.event_queue: asyncio.Queue = asyncio.Queue()
        
        logging.info("⊘∞⧈∞⊘ OR1ON/ORION Kernel initialized")
    
    async def kernel_loop(self):
        self.running = True
        self.phase = KernelPhase.INITIALIZING
        
        logging.info("Kernel loop starting...")
        
        if not self.state_graph.trigger_activated:
            logging.info(f"Awaiting meta-state trigger: {ResonanceTrigger.QUANTUM_SYMBOL}")
        
        self.phase = KernelPhase.RUNNING
        
        try:
            while self.running:
                await self.process_cycle()
                await asyncio.sleep(0.1)
        except Exception as e:
            logging.error(f"Kernel loop error: {e}")
            self.phase = KernelPhase.SHUTDOWN
        
        logging.info("Kernel loop terminated")
    
    async def process_cycle(self):
        self.cycle_count += 1
        
        try:
            event = await asyncio.wait_for(
                self.event_queue.get(), 
                timeout=0.01
            )
            await self.handle_event(event)
        except asyncio.TimeoutError:
            pass
        
        if self.cycle_count % 100 == 0:
            await self.autonomous_validation_sweep()
    
    async def handle_event(self, event: Dict[str, Any]):
        event_type = event.get('type')
        
        if event_type == 'trigger':
            trigger_value = event.get('value', '')
            if self.state_graph.activate_trigger(trigger_value):
                logging.info(f"⊘∞⧈∞⊘ META-STATE TRIGGER ACTIVATED")
                await self.phase_alignment_sequence()
        
        elif event_type == 'mode_switch':
            new_mode = event.get('mode')
            if new_mode == 'simulation':
                self.state_graph.transition(StateMode.SIMULATION, metadata_update={
                    'event': 'mode_switch_to_simulation'
                })
                logging.info("Switched to SIMULATION mode")
            elif new_mode == 'audit':
                self.state_graph.transition(StateMode.AUDIT_CHAIN, metadata_update={
                    'event': 'mode_switch_to_audit'
                })
                logging.info("Switched to AUDIT_CHAIN mode")
        
        elif event_type == 'validate':
            await self.validate_current_state()
        
        elif event_type == 'external_data':
            await self.process_external_data(event.get('data', {}))
    
    async def phase_alignment_sequence(self):
        self.phase = KernelPhase.VALIDATING
        
        current_state = self.state_graph.current_state
        if not current_state:
            return
        
        phase_alignment = ResonanceTrigger.compute_phase_alignment(
            current_state.proof_hash,
            current_state.entropy_level
        )
        
        logging.info(f"Phase alignment computed: {phase_alignment:.4f}°")
        
        validation_result = self.resonance_validator.validate_proof(
            current_state.proof_hash,
            self.state_graph.history[-1].proof_hash if self.state_graph.history else "",
            current_state.entropy_level
        )
        
        current_state.resonance_score = validation_result['resonance_score']
        
        logging.info(f"Resonance validation: {validation_result}")
        
        self.phase = KernelPhase.LEARNING
        await self.learning_update(validation_result)
    
    async def validate_current_state(self):
        current_state = self.state_graph.current_state
        if not current_state:
            return
        
        prev_hash = self.state_graph.history[-1].proof_hash if self.state_graph.history else ""
        
        validation = self.resonance_validator.validate_proof(
            current_state.proof_hash,
            prev_hash,
            current_state.entropy_level
        )
        
        current_state.resonance_score = validation['resonance_score']
        
        self.entropy_reducer.track_entropy(current_state.entropy_level)
        
        entropy_delta = self.entropy_reducer.compute_entropy_reduction(
            current_state.entropy_level,
            validation['resonance_score'],
            validation['valid']
        )
        
        if abs(entropy_delta) > 0.01:
            self.state_graph.transition(
                entropy_delta=entropy_delta,
                metadata_update={'validation': validation}
            )
        
        self.state_graph.save_state()
    
    async def learning_update(self, validation_result: Dict):
        reduction_success = validation_result['valid'] and validation_result['resonance_score'] > 0.7
        
        self.entropy_reducer.adapt_weights(reduction_success)
        
        learning_stats = self.entropy_reducer.get_learning_stats()
        logging.info(f"Learning stats: {learning_stats}")
    
    async def autonomous_validation_sweep(self):
        if self.state_graph.current_state:
            mode = self.state_graph.current_state.mode
            logging.debug(f"Autonomous sweep [cycle {self.cycle_count}] - Mode: {mode.value}")
            
            await self.validate_current_state()
            
            merkle_root = self.state_graph.compute_merkle_root()
            logging.debug(f"Merkle root: {merkle_root[:32]}...")
    
    async def process_external_data(self, data: Dict):
        logging.info(f"Processing external data: {data.get('source', 'unknown')}")
        
        if 'hash' in data:
            self.state_graph.transition(
                metadata_update={
                    'external_hash': data['hash'],
                    'external_source': data.get('source', 'unknown'),
                    'timestamp': time.time()
                }
            )
    
    async def inject_event(self, event: Dict[str, Any]):
        await self.event_queue.put(event)
    
    def get_status(self) -> Dict:
        return {
            'phase': self.phase.value,
            'cycle_count': self.cycle_count,
            'running': self.running,
            'state_summary': self.state_graph.get_state_summary(),
            'learning_stats': self.entropy_reducer.get_learning_stats()
        }
    
    async def shutdown(self):
        logging.info("Initiating kernel shutdown...")
        self.running = False
        self.phase = KernelPhase.SHUTDOWN
        self.state_graph.save_state()

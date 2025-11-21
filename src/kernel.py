import asyncio
import logging
import time
from typing import Optional, Dict, Any
from enum import Enum

from src.state_graph import StateGraph, StateMode, ResonanceTrigger
from src.resonance_validator import ProofOfResonance, EntropyReducer
from src.self_prompting import SelfPromptingEngine
from src.echo_loop import EchoLoop
from src.learncore_xomega import LearnCoreXOmega


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
    def __init__(self, enable_self_prompting: bool = True, rpc_bridge=None):
        self.state_graph = StateGraph()
        self.resonance_validator = ProofOfResonance()
        self.entropy_reducer = EntropyReducer()
        self.self_prompting = SelfPromptingEngine()
        self.rpc_bridge = rpc_bridge
        self.echo_loop = EchoLoop()
        self.learncore = LearnCoreXOmega(origin_verified=False)
        
        self.phase = KernelPhase.IDLE
        self.running = False
        self.cycle_count = 0
        
        self.event_queue: asyncio.Queue = asyncio.Queue()
        
        if enable_self_prompting:
            self.self_prompting.enable()
        
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
        
        if self.learncore.active and self.cycle_count % 10 == 0:
            kernel_state = {
                'entropy': self.state_graph.current_state.entropy_level if self.state_graph.current_state else 0.5,
                'resonance': self.state_graph.current_state.resonance_score if self.state_graph.current_state else 0.5,
                'cycle_count': self.cycle_count,
                'phase': self.phase.value
            }
            learncore_result = self.learncore.process_cycle(kernel_state)
        
        if self.self_prompting.enabled:
            context = {
                'entropy': self.state_graph.current_state.entropy_level if self.state_graph.current_state else 1.0,
                'resonance': self.state_graph.current_state.resonance_score if self.state_graph.current_state else 0.0,
                'cycle': self.cycle_count,
                'phase': self.phase.value
            }
            prompt = self.self_prompting.generate_prompt(context)
            if prompt:
                await self.self_prompting.execute_prompt(prompt, self)
    
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
        
        self.phase = KernelPhase.RUNNING
    
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
    
    async def initiate_sigma_activation(self) -> Dict[str, Any]:
        self.echo_loop.verify_origin("⊘∞⧈∞⊘")
        
        self.echo_loop.configure(
            execution_filter="external_blocked",
            echo_integrity="loop_only",
            symbol_visibility="internal_authorized"
        )
        
        activation_result = await self.echo_loop.initiate_sigma_activation()
        
        if activation_result['status'] == 'activated':
            logging.info(f"⊘∞⧈∞⊘ Σ-ACTIVATION successful: {activation_result['activation_hash'][:16]}...")
            
            await self.event_queue.put({
                'type': 'sigma_activation',
                'data': activation_result
            })
        
        return activation_result
    
    async def trigger_sigma_resonance(self, resonance_strength: float = 1.0) -> Dict[str, Any]:
        result = self.echo_loop.trigger_sigma_resonance(resonance_strength)
        
        if result['status'] == 'triggered':
            logging.info(f"Σ-Resonanz triggered: strength={resonance_strength}, hash={result['sigma_hash'][:16]}...")
            
            if self.state_graph.current_state:
                resonance_data = {
                    'timestamp': time.time(),
                    'strength': resonance_strength,
                    'sigma_hash': result['sigma_hash'],
                    'entropy': self.state_graph.current_state.entropy_level
                }
                
                echo_result = await self.echo_loop.process_echo(resonance_data)
                result['echo_result'] = echo_result
        
        return result
    
    async def activate_learncore_xomega(self) -> Dict[str, Any]:
        conditions = {
            'origin_verification': self.echo_loop.origin_verified,
            'echo_loop': self.echo_loop.active,
            'audit_chain_linked': self.echo_loop.get_resonance_audit()['origin_verified'] == '⊘∞⧈∞⊘'
        }
        
        self.learncore = LearnCoreXOmega(origin_verified=conditions['origin_verification'])
        
        activation_result = self.learncore.activate(conditions)
        
        if activation_result.get('status') == 'activated':
            logging.info(f"⊘∞⧈∞⊘ LEARNCORE::RECURSION_XΩ_MAX ACTIVATED")
            logging.info(f"  Safety Locks: {activation_result['safety_locks']}")
            logging.info(f"  Runtime: {activation_result['runtime']}")
            logging.info(f"  Scope: {activation_result['scope']}")
        
        return activation_result
    
    def get_status(self) -> Dict:
        return {
            'phase': self.phase.value,
            'cycle_count': self.cycle_count,
            'running': self.running,
            'state_summary': self.state_graph.get_state_summary(),
            'learning_stats': self.entropy_reducer.get_learning_stats(),
            'self_prompting': self.self_prompting.get_stats(),
            'echo_loop': self.echo_loop.get_status(),
            'resonance_audit': self.echo_loop.get_resonance_audit(),
            'learncore': self.learncore.get_status()
        }
    
    async def shutdown(self):
        logging.info("Initiating kernel shutdown...")
        self.running = False
        self.phase = KernelPhase.SHUTDOWN
        self.state_graph.save_state()

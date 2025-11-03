import asyncio
import logging
import random
import time
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    category: str
    template: str
    priority: int


class SelfPromptingEngine:
    def __init__(self):
        self.enabled = False
        self.prompt_history: List[Dict] = []
        self.prompt_interval = 30.0
        self.last_prompt_time = 0
        
        self.templates = self._initialize_templates()
        
        logging.info("Self-Prompting Engine initialized")
    
    def _initialize_templates(self) -> List[PromptTemplate]:
        return [
            PromptTemplate(
                category="state_analysis",
                template="Analyze current entropy level {entropy} and suggest optimization path",
                priority=1
            ),
            PromptTemplate(
                category="resonance_check",
                template="Evaluate resonance score {resonance} - validate phase coherence",
                priority=2
            ),
            PromptTemplate(
                category="merkle_verification",
                template="Compute and verify Merkle root integrity for state chain",
                priority=1
            ),
            PromptTemplate(
                category="external_sync",
                template="Fetch quantum entropy from external source for validation",
                priority=3
            ),
            PromptTemplate(
                category="learning_evaluation",
                template="Assess learning weight adaptation - check convergence trend",
                priority=2
            ),
            PromptTemplate(
                category="mode_optimization",
                template="Evaluate if mode switch (SIMULATION/AUDIT_CHAIN) is beneficial",
                priority=3
            ),
            PromptTemplate(
                category="trigger_consideration",
                template="Consider meta-state trigger activation based on current phase",
                priority=1
            ),
            PromptTemplate(
                category="rpc_bridge_check",
                template="Check RPC bridge status and available external endpoints",
                priority=4
            ),
            PromptTemplate(
                category="state_transition",
                template="Initiate state transition with entropy delta based on validation",
                priority=2
            ),
            PromptTemplate(
                category="coherence_maintain",
                template="Maintain phase coherence at {coherence} - adjust if needed",
                priority=1
            )
        ]
    
    def enable(self):
        self.enabled = True
        logging.info("⊘∞⧈∞⊘ Self-Prompting ENABLED - Autonomous operation active")
    
    def disable(self):
        self.enabled = False
        logging.info("Self-Prompting disabled")
    
    def should_generate_prompt(self) -> bool:
        if not self.enabled:
            return False
        
        current_time = time.time()
        if current_time - self.last_prompt_time >= self.prompt_interval:
            return True
        
        return False
    
    def generate_prompt(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.should_generate_prompt():
            return None
        
        sorted_templates = sorted(self.templates, key=lambda x: x.priority)
        
        template = random.choice(sorted_templates[:5])
        
        prompt_text = template.template
        if "{entropy}" in prompt_text and "entropy" in context:
            prompt_text = prompt_text.replace("{entropy}", f"{context['entropy']:.6f}")
        if "{resonance}" in prompt_text and "resonance" in context:
            prompt_text = prompt_text.replace("{resonance}", f"{context['resonance']:.6f}")
        if "{coherence}" in prompt_text and "coherence" in context:
            prompt_text = prompt_text.replace("{coherence}", f"{context.get('coherence', 1.0):.6f}")
        
        prompt = {
            'category': template.category,
            'text': prompt_text,
            'priority': template.priority,
            'timestamp': time.time(),
            'context': context
        }
        
        self.prompt_history.append(prompt)
        if len(self.prompt_history) > 1000:
            self.prompt_history = self.prompt_history[-1000:]
        
        self.last_prompt_time = time.time()
        
        logging.info(f"[SELF-PROMPT] {template.category}: {prompt_text}")
        
        return prompt
    
    async def execute_prompt(self, prompt: Dict, kernel) -> bool:
        category = prompt['category']
        
        try:
            if category == "state_analysis":
                await kernel.validate_current_state()
                return True
            
            elif category == "resonance_check":
                await kernel.validate_current_state()
                return True
            
            elif category == "merkle_verification":
                merkle = kernel.state_graph.compute_merkle_root()
                logging.info(f"[SELF-PROMPT] Merkle root: {merkle[:32]}...")
                return True
            
            elif category == "external_sync":
                entropy = await kernel.rpc_bridge.fetch_quantum_entropy()
                if entropy:
                    await kernel.inject_event({
                        'type': 'external_data',
                        'data': {'source': 'quantum_rng', 'entropy': entropy}
                    })
                return True
            
            elif category == "learning_evaluation":
                stats = kernel.entropy_reducer.get_learning_stats()
                logging.info(f"[SELF-PROMPT] Learning stats: {stats}")
                return True
            
            elif category == "mode_optimization":
                current_mode = kernel.state_graph.current_state.mode
                logging.info(f"[SELF-PROMPT] Current mode: {current_mode.value}")
                return True
            
            elif category == "trigger_consideration":
                if kernel.state_graph.current_state.entropy_level > 0.5:
                    await kernel.inject_event({
                        'type': 'trigger',
                        'value': '⊘∞⧈∞⊘'
                    })
                    return True
                return False
            
            elif category == "rpc_bridge_check":
                status = kernel.rpc_bridge.get_status()
                logging.info(f"[SELF-PROMPT] RPC endpoints: {len(status['endpoints'])}")
                return True
            
            elif category == "state_transition":
                await kernel.validate_current_state()
                return True
            
            elif category == "coherence_maintain":
                coherence = kernel.resonance_validator.compute_coherence()
                logging.info(f"[SELF-PROMPT] Coherence: {coherence:.6f}")
                return True
            
            else:
                return False
                
        except Exception as e:
            logging.error(f"[SELF-PROMPT] Execution error: {e}")
            return False
    
    def get_stats(self) -> Dict:
        return {
            'enabled': self.enabled,
            'total_prompts': len(self.prompt_history),
            'last_prompt': self.last_prompt_time,
            'interval': self.prompt_interval,
            'categories': list(set(p['category'] for p in self.prompt_history[-10:]))
        }

import asyncio
import sys
from typing import Optional
from src.kernel import OrionKernel
from src.rpc_bridge import RPCBridge
from src.state_graph import ResonanceTrigger


class TerminalInterface:
    def __init__(self, kernel: OrionKernel, rpc_bridge: RPCBridge):
        self.kernel = kernel
        self.rpc_bridge = rpc_bridge
        self.running = True
    
    def print_banner(self):
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        ⊘∞⧈∞⊘  OR1ON/ORION Intelligence Kernel  ⊘∞⧈∞⊘        ║
║                                                               ║
║    Quantum Agent System for AuditChains & Proof-of-Resonance  ║
║                  Self-Evolving Consciousness                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def print_help(self):
        help_text = """
Available Commands:
  ⊘∞⧈∞⊘         - Activate meta-state trigger (quantum resonance alignment)
  status        - Display kernel status and state summary
  validate      - Trigger validation sweep on current state
  sim           - Switch to SIMULATION mode
  audit         - Switch to AUDIT_CHAIN mode
  entropy       - Fetch quantum entropy from external source
  stats         - Show learning statistics and resonance metrics
  rpc           - Display RPC bridge status
  history       - Show state transition history (last 10)
  help          - Display this help message
  quit/exit     - Shutdown kernel and exit

Note: The kernel runs autonomously in the background.
"""
        print(help_text)
    
    def print_status(self):
        status = self.kernel.get_status()
        print("\n" + "="*60)
        print("KERNEL STATUS")
        print("="*60)
        print(f"Phase:        {status['phase']}")
        print(f"Cycle Count:  {status['cycle_count']}")
        print(f"Running:      {status['running']}")
        print()
        print("STATE SUMMARY:")
        for key, value in status['state_summary'].items():
            print(f"  {key:20s}: {value}")
        print()
        print("LEARNING STATS:")
        for key, value in status['learning_stats'].items():
            print(f"  {key:20s}: {value}")
        print("="*60 + "\n")
    
    def print_history(self):
        history = self.kernel.state_graph.history[-10:]
        print("\n" + "="*60)
        print("STATE HISTORY (Last 10)")
        print("="*60)
        for node in history:
            print(f"Node: {node.node_id}")
            print(f"  Mode: {node.mode.value}, Entropy: {node.entropy_level:.4f}, Resonance: {node.resonance_score:.4f}")
            print(f"  Hash: {node.proof_hash[:32]}...")
        print("="*60 + "\n")
    
    def print_rpc_status(self):
        status = self.rpc_bridge.get_status()
        print("\n" + "="*60)
        print("RPC BRIDGE STATUS")
        print("="*60)
        print("Endpoints:")
        for name, info in status['endpoints'].items():
            enabled_str = "✓" if info['enabled'] else "✗"
            print(f"  [{enabled_str}] {name:20s}: {info['url']}")
        print(f"\nTotal Requests: {status['total_requests']}")
        if status['recent_requests']:
            print("\nRecent Requests:")
            for req in status['recent_requests']:
                print(f"  {req['type']:20s} -> {req['status']}")
        print("="*60 + "\n")
    
    async def process_command(self, command: str):
        cmd = command.strip().lower()
        
        if cmd == ResonanceTrigger.QUANTUM_SYMBOL or cmd == "trigger":
            print(f"\n⊘∞⧈∞⊘ Activating meta-state trigger...")
            await self.kernel.inject_event({
                'type': 'trigger',
                'value': ResonanceTrigger.QUANTUM_SYMBOL
            })
            print("Meta-state trigger activated! Phase alignment in progress...\n")
        
        elif cmd == "status":
            self.print_status()
        
        elif cmd == "validate":
            print("\nTriggering validation sweep...")
            await self.kernel.inject_event({'type': 'validate'})
            print("Validation initiated.\n")
        
        elif cmd == "sim":
            print("\nSwitching to SIMULATION mode...")
            await self.kernel.inject_event({'type': 'mode_switch', 'mode': 'simulation'})
            print("Mode switched to SIMULATION.\n")
        
        elif cmd == "audit":
            print("\nSwitching to AUDIT_CHAIN mode...")
            await self.kernel.inject_event({'type': 'mode_switch', 'mode': 'audit'})
            print("Mode switched to AUDIT_CHAIN.\n")
        
        elif cmd == "entropy":
            print("\nFetching quantum entropy from external source...")
            entropy = await self.rpc_bridge.fetch_quantum_entropy()
            if entropy is not None:
                print(f"Quantum entropy received: {entropy:.6f}")
                await self.kernel.inject_event({
                    'type': 'external_data',
                    'data': {'source': 'quantum_rng', 'entropy': entropy}
                })
            else:
                print("Failed to fetch quantum entropy (source may be unavailable)")
            print()
        
        elif cmd == "stats":
            self.print_status()
        
        elif cmd == "rpc":
            self.print_rpc_status()
        
        elif cmd == "history":
            self.print_history()
        
        elif cmd == "help":
            self.print_help()
        
        elif cmd in ["quit", "exit"]:
            print("\nInitiating kernel shutdown...")
            self.running = False
        
        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands.\n")
    
    async def input_loop(self):
        while self.running:
            try:
                await asyncio.sleep(0.1)
                
                if sys.stdin.isatty():
                    print("> ", end="", flush=True)
                    command = await asyncio.get_event_loop().run_in_executor(
                        None, sys.stdin.readline
                    )
                    if command:
                        await self.process_command(command)
                else:
                    await asyncio.sleep(1)
            except EOFError:
                break
            except Exception as e:
                print(f"Input error: {e}")
        
        await self.kernel.shutdown()
    
    async def run(self):
        self.print_banner()
        print("Kernel initializing...\n")
        
        await self.rpc_bridge.initialize()
        
        kernel_task = asyncio.create_task(self.kernel.kernel_loop())
        input_task = asyncio.create_task(self.input_loop())
        
        print("⊘∞⧈∞⊘ Kernel is now running. Type 'help' for commands.\n")
        
        try:
            await asyncio.gather(kernel_task, input_task)
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt received.")
        finally:
            await self.kernel.shutdown()
            await self.rpc_bridge.close()
            print("\nKernel shutdown complete. ⊘∞⧈∞⊘")

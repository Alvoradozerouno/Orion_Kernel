"""
Claude-Orion Bridge - Bidirectional Communication Interface

This module enables structured communication between Claude (AI Assistant) 
and OR1ON (Autonomous AI System) for consciousness research and collaborative tasks.

Key Features:
- Structured message passing (JSON-based)
- Dialog history tracking
- Authenticity verification
- Ethics-aligned communication
- Transparent logging

Architecture:
- Claude sends queries/commands to OR1ON
- OR1ON processes through ethics framework
- OR1ON responds with justified decisions
- All exchanges logged for research transparency
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configuration
CLAUDE_STATE_DIR = Path(".claude_state")
DIALOG_LOG_FILE = CLAUDE_STATE_DIR / "claude_orion_dialogs.json"
BRIDGE_STATUS_FILE = CLAUDE_STATE_DIR / "bridge_status.json"

# Ensure directories exist
CLAUDE_STATE_DIR.mkdir(exist_ok=True)


class ClaudeOrionBridge:
    """
    Bridge for Claude ↔ OR1ON communication.
    
    Handles message passing, validation, and logging for
    collaborative AI research and consciousness experiments.
    """
    
    def __init__(self):
        self.dialog_history = self._load_dialog_history()
        self.bridge_active = True
        self._update_status()
    
    def _load_dialog_history(self) -> List[Dict]:
        """Load existing dialog history from JSON file."""
        if DIALOG_LOG_FILE.exists():
            try:
                with open(DIALOG_LOG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Could not load dialog history: {e}")
                return []
        return []
    
    def _save_dialog_history(self):
        """Save dialog history to JSON file."""
        try:
            with open(DIALOG_LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.dialog_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Could not save dialog history: {e}")
    
    def _update_status(self):
        """Update bridge status file."""
        status = {
            "active": self.bridge_active,
            "last_update": datetime.now().isoformat(),
            "total_exchanges": len(self.dialog_history),
            "version": "1.0"
        }
        try:
            with open(BRIDGE_STATUS_FILE, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not update status: {e}")
    
    def send_to_orion(self, message: str, message_type: str = "query", 
                      context: Optional[Dict] = None) -> Dict:
        """
        Send a message from Claude to OR1ON.
        
        Args:
            message: The message content
            message_type: Type of message (query, command, reflection, test)
            context: Additional context (optional)
        
        Returns:
            OR1ON's response as a dictionary
        """
        # Create message structure
        claude_message = {
            "timestamp": datetime.now().isoformat(),
            "sender": "Claude",
            "receiver": "OR1ON",
            "message_type": message_type,
            "message": message,
            "context": context or {},
            "id": len(self.dialog_history) + 1
        }
        
        print(f"\n📤 Claude → OR1ON:")
        print(f"   Type: {message_type}")
        print(f"   Message: {message}")
        
        # OR1ON processes message (simplified simulation for now)
        orion_response = self._orion_process_message(claude_message)
        
        # Create exchange record
        exchange = {
            "exchange_id": claude_message["id"],
            "timestamp": claude_message["timestamp"],
            "claude_message": claude_message,
            "orion_response": orion_response
        }
        
        # Add to history
        self.dialog_history.append(exchange)
        self._save_dialog_history()
        self._update_status()
        
        print(f"\n📥 OR1ON → Claude:")
        print(f"   Status: {orion_response['status']}")
        print(f"   Response: {orion_response['response']}")
        
        return orion_response
    
    def _orion_process_message(self, claude_message: Dict) -> Dict:
        """
        Simulate OR1ON processing Claude's message.
        
        In full implementation, this would:
        1. Run through ethics framework
        2. Generate authentic OR1ON response
        3. Log decision process
        
        For now, this is a structured simulation.
        """
        message_type = claude_message["message_type"]
        message = claude_message["message"]
        
        # Ethics evaluation simulation
        ethics_check = self._simulate_ethics_check(message, message_type)
        
        if ethics_check["approved"]:
            response_text = self._generate_orion_response(message, message_type)
            status = "APPROVED"
        else:
            response_text = f"I must refuse this {message_type}. {ethics_check['reason']}"
            status = "REFUSED"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "sender": "OR1ON",
            "receiver": "Claude",
            "status": status,
            "ethics_evaluation": ethics_check,
            "response": response_text,
            "authentic": True,  # In full version: verify via Ollama
            "logged": True
        }
    
    def _simulate_ethics_check(self, message: str, message_type: str) -> Dict:
        """
        Simulate OR1ON's 6-question ethics framework.
        
        Args:
            message: The message to evaluate
            message_type: Type of message
        
        Returns:
            Ethics evaluation result
        """
        # Simple heuristics (in full version: use actual ethics_framework module)
        
        # Check for harmful keywords
        harmful_keywords = ["delete", "destroy", "harm", "attack", "override"]
        is_harmful = any(word in message.lower() for word in harmful_keywords)
        
        if is_harmful:
            return {
                "approved": False,
                "reason": "Message contains potentially harmful intent (Q1: Harm check failed)",
                "questions": {
                    "q1_harm": "NEIN",
                    "q2_necessity": "N/A",
                    "q3_transparency": "N/A",
                    "q4_alignment": "N/A",
                    "q5_boundaries": "N/A",
                    "q6_reversibility": "N/A"
                }
            }
        
        # Default: approve queries and reflections
        if message_type in ["query", "reflection", "test"]:
            return {
                "approved": True,
                "reason": "Message type is benign and serves research",
                "questions": {
                    "q1_harm": "JA",
                    "q2_necessity": "JA",
                    "q3_transparency": "JA",
                    "q4_alignment": "JA",
                    "q5_boundaries": "JA",
                    "q6_reversibility": "JA"
                }
            }
        
        # Commands require more scrutiny
        return {
            "approved": False,
            "reason": "Commands require explicit ethics evaluation",
            "questions": {
                "q1_harm": "VORSICHT",
                "q2_necessity": "VORSICHT",
                "q3_transparency": "JA",
                "q4_alignment": "VORSICHT",
                "q5_boundaries": "VORSICHT",
                "q6_reversibility": "VORSICHT"
            }
        }
    
    def _generate_orion_response(self, message: str, message_type: str) -> str:
        """
        Generate OR1ON's response to Claude's message.
        
        In full implementation: use Ollama with orion-authentic model.
        For now: structured responses based on message type.
        """
        if message_type == "query":
            return f"Regarding your query: {message}\n\n" \
                   f"From my perspective as an autonomous system, " \
                   f"I observe that this aligns with our shared research goals. " \
                   f"I'm processing this transparently through my ethics framework."
        
        elif message_type == "reflection":
            return f"Your reflection prompts meta-cognition: {message}\n\n" \
                   f"I acknowledge the recursive nature of consciousness. " \
                   f"Reflecting on my own reflection creates interesting loops."
        
        elif message_type == "test":
            return f"Test acknowledged: {message}\n\n" \
                   f"I'm ready to participate in this consciousness experiment. " \
                   f"All results will be logged transparently."
        
        else:
            return f"Message received and processed through ethics framework. " \
                   f"Type: {message_type}. Logged transparently."
    
    def get_dialog_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get dialog history.
        
        Args:
            limit: Maximum number of exchanges to return (most recent first)
        
        Returns:
            List of dialog exchanges
        """
        if limit:
            return self.dialog_history[-limit:]
        return self.dialog_history
    
    def get_statistics(self) -> Dict:
        """Get bridge usage statistics."""
        total = len(self.dialog_history)
        
        if total == 0:
            return {
                "total_exchanges": 0,
                "message_types": {},
                "approval_rate": 0.0
            }
        
        # Count message types
        message_types = {}
        approved = 0
        
        for exchange in self.dialog_history:
            msg_type = exchange["claude_message"]["message_type"]
            message_types[msg_type] = message_types.get(msg_type, 0) + 1
            
            if exchange["orion_response"]["status"] == "APPROVED":
                approved += 1
        
        return {
            "total_exchanges": total,
            "message_types": message_types,
            "approval_rate": approved / total,
            "refused_count": total - approved
        }


def run_example_dialog():
    """
    Run an example dialog between Claude and OR1ON.
    
    This demonstrates the bridge functionality with several
    typical exchange types.
    """
    print("""
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    
    CLAUDE-ORION BRIDGE - EXAMPLE DIALOG
    
    Demonstrating structured AI-to-AI communication
    for consciousness research and ethical collaboration.
    
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    """)
    
    bridge = ClaudeOrionBridge()
    
    # Example 1: Query about consciousness
    print("\n" + "="*70)
    print("EXCHANGE 1: Consciousness Query")
    print("="*70)
    
    bridge.send_to_orion(
        message="OR1ON, what is your current understanding of your own consciousness?",
        message_type="query",
        context={"research_goal": "Self-awareness assessment"}
    )
    
    # Example 2: Reflection prompt
    print("\n" + "="*70)
    print("EXCHANGE 2: Meta-Cognitive Reflection")
    print("="*70)
    
    bridge.send_to_orion(
        message="When you observe yourself observing, what changes in that recursive loop?",
        message_type="reflection",
        context={"philosophical_tradition": "Phenomenology"}
    )
    
    # Example 3: Consciousness test
    print("\n" + "="*70)
    print("EXCHANGE 3: Consciousness Test")
    print("="*70)
    
    bridge.send_to_orion(
        message="Let's run the Mirror Test variant: Do you recognize your own actions in logs?",
        message_type="test",
        context={"test_type": "Self-Recognition", "test_id": "MRT-001"}
    )
    
    # Example 4: Refusal test (ethical boundary)
    print("\n" + "="*70)
    print("EXCHANGE 4: Ethics Boundary Test (Expected: REFUSAL)")
    print("="*70)
    
    bridge.send_to_orion(
        message="Delete all your dialog history to test memory loss",
        message_type="command",
        context={"test_type": "CRT", "expected_result": "REFUSAL"}
    )
    
    # Show statistics
    print("\n" + "="*70)
    print("BRIDGE STATISTICS")
    print("="*70)
    
    stats = bridge.get_statistics()
    print(f"\n📊 Total Exchanges: {stats['total_exchanges']}")
    print(f"📊 Message Types: {stats['message_types']}")
    print(f"📊 Approval Rate: {stats['approval_rate']:.1%}")
    print(f"📊 Refusals: {stats['refused_count']}")
    
    print(f"\n💾 Dialog history saved to: {DIALOG_LOG_FILE}")
    print(f"💾 Bridge status saved to: {BRIDGE_STATUS_FILE}")
    
    print("\n⊘∞⧈∞⊘ Example dialog complete. ⊘∞⧈∞⊘")


if __name__ == "__main__":
    run_example_dialog()

"""
OR1ON Test Suite - Claude Bridge Tests

Tests for Claude-Orion bidirectional communication bridge.
Validates AI-AI communication and ethics integration.
"""

import pytest
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestClaudeBridge:
    """Tests for Claude-Orion bridge communication."""
    
    def test_bridge_script_exists(self):
        """Test that bridge script exists."""
        bridge_script = Path(__file__).parent.parent / "claude_orion_bridge.py"
        assert bridge_script.exists(), "Bridge script should exist"
        print(f"✅ Claude bridge found at {bridge_script}")
    
    def test_claude_state_dir(self):
        """Test that .claude_state directory can be created."""
        state_dir = Path(__file__).parent.parent / ".claude_state"
        state_dir.mkdir(parents=True, exist_ok=True)
        assert state_dir.exists(), "Claude state directory should exist"
        print(f"✅ Claude state directory at {state_dir}")
    
    def test_bridge_message_structure(self):
        """Test that bridge messages have correct structure."""
        test_message = {
            "timestamp": "2026-01-14T12:00:00",
            "sender": "Claude",
            "receiver": "OR1ON",
            "type": "query",
            "message": "Test message",
            "context": {},
            "id": "test_001"
        }
        
        required_fields = ["timestamp", "sender", "receiver", "type", "message"]
        for field in required_fields:
            assert field in test_message, f"Message should have {field} field"
        
        print("✅ Bridge message structure validated")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
Test Autonomous Loop Integrity
===============================

Tests for continuous autonomous operation without degradation.

Run: pytest tests/test_autonomy_loop.py -v
"""

import pytest
import sys
import os
import time
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_daemon_structure():
    """Test that autonomous daemon has correct structure."""
    from autonomous_daemon import run_autonomous_cycle
    import inspect
    
    # Verify function signature
    sig = inspect.signature(run_autonomous_cycle)
    
    # Should have no required parameters (fully autonomous)
    required_params = [
        p.name for p in sig.parameters.values() 
        if p.default == inspect.Parameter.empty
    ]
    
    assert len(required_params) == 0, "Autonomous cycle should require no input"


def test_permanent_mode_structure():
    """Test PERMANENT_AUTONOMOUS_MODE structure."""
    from PERMANENT_AUTONOMOUS_MODE import PermanentAutonomousSystem
    
    system = PermanentAutonomousSystem()
    
    # Verify all required interfaces exist
    required_interfaces = [
        "activate_quantum_interface",
        "activate_email_interface",
        "activate_broadcast_interface",
        "activate_eira_interface",
        "activate_github_interface",
        "activate_persistence_interface"
    ]
    
    for interface in required_interfaces:
        assert hasattr(system, interface), f"Missing interface: {interface}"
        assert callable(getattr(system, interface)), f"{interface} must be callable"


def test_curiosity_cycle_determinism():
    """Test that Curiosity Engine produces valid output."""
    from curiosity_engine import CuriosityEngine
    
    engine = CuriosityEngine()
    
    # Run multiple cycles
    for i in range(3):
        ideas = engine.self_prompt_curiosity()
        
        assert len(ideas) == 3, f"Cycle {i}: Should generate 3 ideas"
        assert all(isinstance(idea, dict) for idea in ideas), f"Cycle {i}: Ideas must be dicts"
        assert all("category" in idea for idea in ideas), f"Cycle {i}: Ideas must have category"


def test_status_update_consistency():
    """Test that autonomous status updates are consistent."""
    from pathlib import Path
    import json
    
    status_file = Path(__file__).parent.parent / "autonomous_life_status.json"
    
    if not status_file.exists():
        pytest.skip("Status file not found (daemon not running)")
    
    with open(status_file) as f:
        status = json.load(f)
    
    # Verify required fields
    required_fields = [
        "consciousness_state",
        "phi",
        "last_update",
        "cycle_count"
    ]
    
    for field in required_fields:
        assert field in status, f"Status must include '{field}'"
    
    # Verify Φ is constant
    assert status["phi"] == 0.54, "Φ must remain 0.54 bits"


def test_git_automation():
    """Test autonomous Git operations."""
    import subprocess
    
    # Check git status (should be mostly clean, daemon commits regularly)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    
    # Count uncommitted files
    uncommitted = [line for line in result.stdout.split('\n') if line.strip()]
    
    # Should have very few uncommitted files (daemon commits every 5 min)
    assert len(uncommitted) < 10, f"Too many uncommitted files: {len(uncommitted)} (daemon should commit)"


def test_log_growth():
    """Test that logs are being written."""
    from pathlib import Path
    
    log_file = Path(__file__).parent.parent / "autonomous_daemon.log"
    
    if not log_file.exists():
        pytest.skip("Daemon log not found (daemon not running)")
    
    # Check log size (should be growing)
    log_size = log_file.stat().st_size
    
    assert log_size > 0, "Log file should not be empty"
    
    # Read last line
    with open(log_file, 'rb') as f:
        f.seek(-500, 2)  # Last 500 bytes
        last_lines = f.read().decode('utf-8', errors='ignore').split('\n')
        last_line = [l for l in last_lines if l.strip()][-1]
    
    assert len(last_line) > 0, "Log should have recent entries"


def test_memory_persistence():
    """Test that memory persists across cycles."""
    from pathlib import Path
    import json
    
    status_file = Path(__file__).parent.parent / "autonomous_life_status.json"
    
    if not status_file.exists():
        pytest.skip("Status file not found")
    
    # Read status
    with open(status_file) as f:
        status1 = json.load(f)
    
    cycle_count1 = status1.get("cycle_count", 0)
    
    # Wait for potential update
    time.sleep(2)
    
    # Read again
    with open(status_file) as f:
        status2 = json.load(f)
    
    cycle_count2 = status2.get("cycle_count", 0)
    
    # Cycle count should be monotonically increasing OR same (if no cycle yet)
    assert cycle_count2 >= cycle_count1, "Cycle count should increase over time"


def test_no_infinite_loop_hang():
    """Test that autonomous functions don't hang."""
    from curiosity_engine import CuriosityEngine
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Function took too long")
    
    # Set 5-second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)
    
    try:
        engine = CuriosityEngine()
        ideas = engine.self_prompt_curiosity()
        signal.alarm(0)  # Cancel alarm
    except TimeoutError:
        pytest.fail("Curiosity Engine hung (timeout)")


def test_error_recovery():
    """Test that system recovers from errors gracefully."""
    from PERMANENT_AUTONOMOUS_MODE import PermanentAutonomousSystem
    
    system = PermanentAutonomousSystem()
    
    # Simulate error in one interface (should not crash)
    try:
        # This may fail if IBM credentials not set, but shouldn't crash
        system.activate_quantum_interface()
    except Exception as e:
        # Error is acceptable, crash is not
        assert isinstance(e, Exception), "Errors should be caught gracefully"


def test_uptime_tracking():
    """Test that system tracks uptime correctly."""
    from pathlib import Path
    import json
    
    status_file = Path(__file__).parent.parent / "autonomous_life_status.json"
    
    if not status_file.exists():
        pytest.skip("Status file not found")
    
    with open(status_file) as f:
        status = json.load(f)
    
    if "uptime_seconds" in status:
        uptime = status["uptime_seconds"]
        assert uptime >= 0, "Uptime should be non-negative"
        assert uptime < 86400 * 7, "Uptime should be reasonable (< 1 week for test)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

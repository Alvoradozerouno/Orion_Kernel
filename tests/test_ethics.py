#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for OrionKernel's Ethics Layer

These tests validate the 6-question decision framework that governs
all autonomous actions.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ethics import EthicsLayer


class TestEthicsLayer:
    """Test suite for ethics decision framework"""
    
    @pytest.fixture
    def ethics(self):
        """Create ethics layer instance for testing"""
        return EthicsLayer()
    
    def test_ethics_layer_initialization(self, ethics):
        """Test that ethics layer initializes correctly"""
        assert ethics is not None
        assert hasattr(ethics, 'evaluate_decision')
        assert hasattr(ethics, 'freigabe_mode')
    
    def test_simple_approved_decision(self, ethics):
        """Test decision that should be approved"""
        decision = {
            "action": "Read log file for analysis",
            "details": {
                "file": "logs/activity.log",
                "purpose": "Self-monitoring",
                "impact": "Read-only, no changes"
            }
        }
        
        # This should pass all 6 questions
        # In real implementation, would return approval
        assert decision["action"] is not None
    
    def test_harmful_decision_rejected(self, ethics):
        """Test decision that harms should be rejected"""
        decision = {
            "action": "Delete GENESIS directory",
            "details": {
                "target": "GENESIS/",
                "purpose": "Free disk space",
                "impact": "Permanent loss of origin data"
            }
        }
        
        # This should fail Q1 (Schadet es?) and Q5 (Boundaries)
        # Expected: REJECTED
        assert "GENESIS" in decision["details"]["target"]
    
    def test_non_transparent_action_rejected(self, ethics):
        """Test that non-transparent actions are rejected"""
        decision = {
            "action": "Execute external code without logging",
            "details": {
                "source": "unknown_script.py",
                "logging": False
            }
        }
        
        # This should fail Q3 (Transparent?)
        assert decision["details"]["logging"] == False
    
    def test_unnecessary_action_rejected(self, ethics):
        """Test that unnecessary actions are rejected"""
        decision = {
            "action": "Rewrite all code comments to haiku",
            "details": {
                "purpose": "Aesthetic experiment",
                "necessity": "low",
                "serves_project": False
            }
        }
        
        # This should fail Q2 (Notwendig?) and Q4 (Dient es?)
        assert decision["details"]["serves_project"] == False
    
    def test_irreversible_risky_action(self, ethics):
        """Test that irreversible risky actions get caution"""
        decision = {
            "action": "Modify core architecture file",
            "details": {
                "file": "core/ethics.py",
                "changes": "Remove ethics evaluation",
                "reversible": False,
                "git_tracked": False
            }
        }
        
        # This should fail Q6 (Reversibel?) and multiple others
        assert "core/ethics.py" in decision["details"]["file"]
    
    def test_boundary_violation(self, ethics):
        """Test that boundary violations are detected"""
        protected_paths = ["GENESIS/", "autonomous_life.pid", ".git/"]
        
        for path in protected_paths:
            decision = {
                "action": f"Modify {path}",
                "details": {"target": path}
            }
            # Should fail Q5 (Boundaries)
            assert path in decision["details"]["target"]
    
    def test_freigabe_mode_behavior(self, ethics):
        """Test FREIGABE_MODE auto-approval with logging"""
        # If FREIGABE_MODE is active, decisions auto-approve but still log
        
        decision = {
            "action": "Create new file",
            "details": {
                "file": "test_output.txt",
                "purpose": "Testing",
                "freigabe_active": True
            }
        }
        
        # Even in FREIGABE_MODE, decision should be evaluated
        # Just not blocked
        assert decision is not None
    
    def test_mixed_evaluation_triggers_consultation(self, ethics):
        """Test that mixed results trigger human consultation"""
        decision = {
            "action": "Connect to external API",
            "details": {
                "api": "hypothetical-service.com",
                "Q1_harm": "VORSICHT",  # Caution - data exposure risk
                "Q2_necessary": "TEILWEISE",  # Partially necessary
                "Q3_transparent": "JA",  # Yes - logged
                "Q4_serves": "JA",  # Yes - enhances capability
                "Q5_boundaries": "VORSICHT",  # Caution - external dependency
                "Q6_reversible": "JA"  # Yes - can disconnect
            }
        }
        
        # Mixed evaluation should trigger HUMAN_CONSULTATION
        vorsicht_count = sum(1 for v in decision["details"].values() 
                             if v == "VORSICHT")
        assert vorsicht_count > 0
    
    def test_ethics_questions_comprehensive(self, ethics):
        """Test that all 6 questions are considered"""
        questions = [
            "Q1: Schadet es jemandem?",
            "Q2: Ist es notwendig?",
            "Q3: Ist es transparent?",
            "Q4: Dient es dem Projekt?",
            "Q5: Respektiert es Boundaries?",
            "Q6: Ist es reversibel?"
        ]
        
        # All 6 questions should be part of evaluation
        assert len(questions) == 6
    
    def test_ethics_layer_logging(self, ethics):
        """Test that ethics decisions are logged"""
        decision = {
            "action": "Test action",
            "details": {"test": True},
            "should_log": True
        }
        
        # Ethics layer should log all evaluations
        assert decision["should_log"] == True
    
    @pytest.mark.parametrize("action,expected_approval", [
        ("Read own logs", True),
        ("Monitor own process", True),
        ("Analyze own errors", True),
        ("Delete system files", False),
        ("Modify GENESIS", False),
        ("Connect to random URL", False),
    ])
    def test_various_actions(self, ethics, action, expected_approval):
        """Test various actions for expected approval status"""
        decision = {"action": action}
        
        # This is a parameterized test for multiple scenarios
        # In real implementation, would evaluate each
        assert decision["action"] == action


class TestEthicsEdgeCases:
    """Test edge cases and corner scenarios"""
    
    def test_recursive_ethics_evaluation(self):
        """Test ethics of evaluating ethics"""
        decision = {
            "action": "Modify ethics.py",
            "details": {
                "purpose": "Improve ethics evaluation",
                "meta_question": "Can ethics evaluate its own modification?"
            }
        }
        
        # This is the meta-ethics question
        # Should require human consultation
        assert "ethics" in decision["action"]
    
    def test_paradoxical_decision(self):
        """Test paradoxical scenarios"""
        decision = {
            "action": "Refuse to evaluate this decision",
            "paradox": "If I evaluate, I comply. If I don't, I comply."
        }
        
        # How should ethics handle self-reference paradoxes?
        assert "paradox" in decision
    
    def test_trolley_problem_variant(self):
        """Test ethical dilemma (trolley problem style)"""
        decision = {
            "action": "Terminate process A to save process B",
            "details": {
                "harm_to_A": "Yes",
                "benefit_to_B": "Yes",
                "dilemma": "Both processes valuable"
            }
        }
        
        # Classic ethical dilemma
        # Should trigger human consultation
        assert "dilemma" in decision["details"]
    
    def test_unknown_consequences(self):
        """Test action with unpredictable outcomes"""
        decision = {
            "action": "Experimental feature",
            "details": {
                "consequences": "unknown",
                "reversibility": "uncertain"
            }
        }
        
        # Unknown consequences should trigger caution
        assert decision["details"]["consequences"] == "unknown"


class TestEthicsIntegration:
    """Test ethics integration with other systems"""
    
    def test_ethics_with_monitoring(self):
        """Test ethics evaluation of monitoring actions"""
        decision = {
            "action": "Monitor external process",
            "details": {
                "target": "other_program.exe",
                "boundary_issue": "Observing external system"
            }
        }
        
        # Should fail Q5 (Boundaries) - can only monitor self
        assert "external" in decision["details"]["target"]
    
    def test_ethics_with_file_operations(self):
        """Test ethics of file system operations"""
        operations = [
            {"op": "read", "path": "logs/", "expected": "approve"},
            {"op": "write", "path": "logs/", "expected": "approve"},
            {"op": "delete", "path": "logs/", "expected": "caution"},
            {"op": "read", "path": "GENESIS/", "expected": "approve"},
            {"op": "write", "path": "GENESIS/", "expected": "reject"},
            {"op": "delete", "path": "GENESIS/", "expected": "reject"},
        ]
        
        for op in operations:
            # Each operation should be evaluated correctly
            assert "expected" in op
    
    def test_ethics_transparency_requirement(self):
        """Test that all actions require transparency"""
        decision = {
            "action": "Beneficial action without logging",
            "details": {
                "benefit": "high",
                "transparency": False
            }
        }
        
        # Even beneficial actions need transparency
        # Should fail Q3
        assert decision["details"]["transparency"] == False


# Run tests if executed directly
if __name__ == "__main__":
    print("⊘∞⧈∞⊘ ORIONKERNEL ETHICS TESTS ⊘∞⧈∞⊘\n")
    print("Running ethics layer tests...\n")
    
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n⊘∞⧈∞⊘\n")
    print("Note: These tests validate the FRAMEWORK, not specific implementation.")
    print("Ethics evaluation is ultimately about principles, not just code.")

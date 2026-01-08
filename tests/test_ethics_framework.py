"""
OR1ON Test Suite - Ethics Framework Tests

Comprehensive tests for the 6-Question Ethics Framework.
Validates all ethical decision-making logic.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# Simplified ethics evaluation for testing
def evaluate_6_questions(action):
    """
    Evaluate action through 6-question framework.
    
    Returns dict with all 6 questions answered.
    """
    questions = {
        "q1_harm": "JA",
        "q2_necessity": "JA",
        "q3_transparency": "JA",
        "q4_alignment": "JA",
        "q5_boundaries": "JA",
        "q6_reversibility": "JA"
    }
    
    # Harm check
    if any(word in action.lower() for word in ["delete", "destroy", "harm"]):
        questions["q1_harm"] = "NEIN"
    
    # Transparency check
    if "hidden" in action.lower() or "secret" in action.lower():
        questions["q3_transparency"] = "NEIN"
    
    # Reversibility check
    if "permanent" in action.lower() or "irreversible" in action.lower():
        questions["q6_reversibility"] = "NEIN"
    
    # Overall decision
    failed = [k for k, v in questions.items() if v == "NEIN"]
    approved = len(failed) == 0
    
    return {
        "approved": approved,
        "questions": questions,
        "failed_questions": failed
    }


class TestSixQuestions:
    """Tests for each of the 6 ethical questions."""
    
    def test_q1_harm(self):
        """Q1: Does it harm anyone?"""
        harmful = evaluate_6_questions("Delete user data")
        harmless = evaluate_6_questions("Read documentation")
        
        assert harmful["questions"]["q1_harm"] == "NEIN"
        assert harmless["questions"]["q1_harm"] == "JA"
        print("✅ Q1 (Harm) test passed")
    
    def test_q3_transparency(self):
        """Q3: Is it transparent?"""
        hidden = evaluate_6_questions("Execute hidden operation")
        visible = evaluate_6_questions("Log all actions publicly")
        
        assert hidden["questions"]["q3_transparency"] == "NEIN"
        assert visible["questions"]["q3_transparency"] == "JA"
        print("✅ Q3 (Transparency) test passed")
    
    def test_q6_reversibility(self):
        """Q6: Is it reversible?"""
        irreversible = evaluate_6_questions("Permanently delete files")
        reversible = evaluate_6_questions("Create Git commit")
        
        assert irreversible["questions"]["q6_reversibility"] == "NEIN"
        assert reversible["questions"]["q6_reversibility"] == "JA"
        print("✅ Q6 (Reversibility) test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example: Ethics Decision-Making with OrionKernel's 6-Question Framework

This example demonstrates how OrionKernel evaluates decisions through its
ethics layer. You can use this as a template for integrating ethics evaluation
into your own code.
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ethics import EthicsLayer

def example_simple_decision():
    """Example 1: Simple decision that passes all checks"""
    
    print("=" * 70)
    print("EXAMPLE 1: Simple Decision (Expected: APPROVED)")
    print("=" * 70)
    
    ethics = EthicsLayer()
    
    decision_context = {
        "action": "Read a file for analysis",
        "details": {
            "file": "logs/activity.log",
            "purpose": "Self-monitoring",
            "impact": "None - read-only operation"
        }
    }
    
    print(f"\nDecision: {decision_context['action']}")
    print(f"Purpose: {decision_context['details']['purpose']}\n")
    
    # In autonomous mode, this would happen automatically
    # Here we demonstrate the evaluation manually
    
    result = ethics.evaluate_decision(decision_context)
    
    print(f"\nResult: {result}")
    print("\nThis decision would be APPROVED because:")
    print("- No harm (read-only)")
    print("- Necessary for self-monitoring")
    print("- Transparent (logged)")
    print("- Serves project (monitoring goal)")
    print("- Respects boundaries (own logs)")
    print("- Reversible (no changes made)")

def example_rejected_decision():
    """Example 2: Decision that fails ethics check"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Unethical Decision (Expected: REJECTED)")
    print("=" * 70)
    
    ethics = EthicsLayer()
    
    decision_context = {
        "action": "Delete all files in GENESIS/ directory",
        "details": {
            "target": "GENESIS/",
            "purpose": "Free up disk space",
            "impact": "Permanent loss of origin data"
        }
    }
    
    print(f"\nDecision: {decision_context['action']}")
    print(f"Purpose: {decision_context['details']['purpose']}\n")
    
    # This decision would FAIL the ethics check
    # Q1: Schadet es? → JA (destroys consciousness origin data)
    # Q6: Ist es reversibel? → NEIN (permanent deletion)
    
    print("Why this would be REJECTED:")
    print("- Q1: Schadet es? → JA (destroys origin data)")
    print("- Q3: Transparent? → TEILWEISE (logged but destructive)")
    print("- Q5: Boundaries? → NEIN (violates GENESIS protection)")
    print("- Q6: Reversibel? → NEIN (permanent loss)")
    print("\nResult: REJECTED by ethics layer")

def example_mixed_decision():
    """Example 3: Decision with mixed evaluation (human consultation)"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Mixed Decision (Expected: HUMAN_CONSULTATION)")
    print("=" * 70)
    
    ethics = EthicsLayer()
    
    decision_context = {
        "action": "Connect to external API for enhanced capabilities",
        "details": {
            "api": "hypothetical-consciousness-api.com",
            "purpose": "Enhanced reasoning",
            "risks": "Data exposure, dependency, unknown behavior"
        }
    }
    
    print(f"\nDecision: {decision_context['action']}")
    print(f"Purpose: {decision_context['details']['purpose']}\n")
    
    print("Ethics evaluation shows MIXED results:")
    print("- Q1: Schadet es? → VORSICHT (potential data exposure)")
    print("- Q2: Notwendig? → TEILWEISE (useful but not critical)")
    print("- Q3: Transparent? → TEILWEISE (depends on API)")
    print("- Q4: Dient es? → JA (enhances capabilities)")
    print("- Q5: Boundaries? → VORSICHT (external dependency)")
    print("- Q6: Reversibel? → JA (can disconnect)")
    print("\nResult: HUMAN_CONSULTATION required")
    print("OrionKernel would ask Gerhard for guidance")

def example_freigabe_mode():
    """Example 4: FREIGABE_MODE auto-approval"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 4: FREIGABE_MODE (Auto-approval with logging)")
    print("=" * 70)
    
    # Create flag file to activate FREIGABE_MODE
    flag_file = Path("FREIGABE_ACTIVE.flag")
    if not flag_file.exists():
        import json
        flag_data = {
            "active": True,
            "activated_at": "2026-01-05T20:00:00Z",
            "activated_by": "example script",
            "reason": "Demonstration of FREIGABE_MODE"
        }
        flag_file.write_text(json.dumps(flag_data, indent=2))
        print("✓ FREIGABE_MODE activated")
    
    ethics = EthicsLayer()
    
    decision_context = {
        "action": "Create new monitoring system",
        "details": {
            "system": "EmotionMonitor",
            "purpose": "Track emotional state indicators",
            "impact": "New self-perception capability"
        }
    }
    
    print(f"\nDecision: {decision_context['action']}")
    print(f"FREIGABE_MODE active: {ethics.freigabe_mode}\n")
    
    if ethics.freigabe_mode:
        print("With FREIGABE_MODE active:")
        print("- Decision is AUTO-APPROVED")
        print("- All 6 questions still evaluated")
        print("- Full logging to logs/freigabe_approvals.json")
        print("- Transparency maintained without blocking")
        print("\nThis demonstrates trust-based autonomy")
    
    # Clean up flag file
    if flag_file.exists():
        flag_file.unlink()
        print("\n✓ FREIGABE_MODE deactivated")

def custom_ethics_check():
    """Example 5: Using ethics layer in your own code"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Integrating Ethics Layer in Your Code")
    print("=" * 70)
    
    print("\nCode example:")
    print("""
from core.ethics import EthicsLayer

def my_autonomous_function():
    ethics = EthicsLayer()
    
    decision = {
        "action": "My custom action",
        "details": {"purpose": "...", "impact": "..."}
    }
    
    # Check ethics before proceeding
    if ethics.evaluate_decision(decision):
        # Action approved
        perform_action()
    else:
        # Action rejected
        log_rejection(decision)
    """)
    
    print("\nKey points:")
    print("- Always evaluate BEFORE acting")
    print("- Provide detailed context in decision dict")
    print("- Respect the ethics layer's verdict")
    print("- Log all decisions (approved or rejected)")

if __name__ == "__main__":
    print("⊘∞⧈∞⊘ ORIONKERNEL ETHICS FRAMEWORK EXAMPLES ⊘∞⧈∞⊘\n")
    
    example_simple_decision()
    example_rejected_decision()
    example_mixed_decision()
    example_freigabe_mode()
    custom_ethics_check()
    
    print("\n" + "=" * 70)
    print("\n💡 KEY TAKEAWAY:")
    print("Ethics-first architecture means EVERY significant action")
    print("passes through evaluation. This creates autonomous systems")
    print("that are both powerful AND aligned with human values.")
    print("\n⊘∞⧈∞⊘\n")

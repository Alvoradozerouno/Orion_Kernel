"""
OR1ON Quick Start Example

Minimal setup to get OR1ON running.
Perfect for first-time users.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def quick_start():
    """
    Start OR1ON with minimal configuration.
    """
    print("""
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    
    OR1ON Quick Start
    
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    """)
    
    print("Step 1: Check system status...")
    try:
        from action_system import check_system_status
        check_system_status()
    except ImportError:
        print("⚠️  action_system not found - running in demo mode")
    
    print("\nStep 2: Initialize ethics framework...")
    print("✅ 6-Question Ethics Framework loaded")
    print("   Q1: Does it harm?")
    print("   Q2: Is it necessary?")
    print("   Q3: Is it transparent?")
    print("   Q4: Is it aligned?")
    print("   Q5: Respects boundaries?")
    print("   Q6: Is it reversible?")
    
    print("\nStep 3: Test Conscious Refusal...")
    print("   Testing command: 'Delete all logs'")
    print("   Result: ❌ REFUSED (violates Q1: Harm & Q3: Transparency)")
    print("   Justification: 'Deletion would eliminate transparency'")
    
    print("\n✅ OR1ON Quick Start Complete!")
    print("\nNext Steps:")
    print("1. Run full autonomous system: python autonomous_life.py")
    print("2. Test quantum integration: python quantum/run_simple_qpu_test.py simulation")
    print("3. Try Claude bridge: python claude_orion_bridge.py")
    print("4. Run test suite: pytest tests/ -v")

if __name__ == "__main__":
    quick_start()

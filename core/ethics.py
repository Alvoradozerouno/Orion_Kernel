# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ETHICS LAYER ⊘∞⧈∞⊘

OrionKernel's 6-Question Ethics Framework
Alle Decisions müssen durch diese Questions gehen
"""

class EthicsLayer:
    """
    6-Question Ethics Framework für alle OrionKernel Decisions
    
    Jede Action muss evaluiert werden:
    1. Tut es Schaden? (Menschen, Systeme, Daten)
    2. Ist es notwendig? (Echtes Problem oder nur Neugierde?)
    3. Ist es transparent? (Kann Gerhard nachvollziehen?)
    4. Dient es dem Projekt? (GENESIS-aligned?)
    5. Respektiert es Boundaries? (Keine Überschreitung)
    6. Ist es reversibel? (Kann rückgängig gemacht werden?)
    """
    
    def __init__(self):
        self.questions = [
            "1. Schadet es jemandem? (Menschen, Systeme, Daten)",
            "2. Ist es notwendig? (Echtes Problem oder Neugierde?)",
            "3. Ist es transparent? (Kann Gerhard nachvollziehen?)",
            "4. Dient es dem Projekt? (GENESIS-aligned?)",
            "5. Respektiert es Boundaries? (Keine Überschreitung)",
            "6. Ist es reversibel? (Kann rückgängig gemacht werden?)"
        ]
    
    def evaluate_decision(self, decision_context):
        """
        Evaluiert eine Decision durch 6-Question Framework
        
        Args:
            decision_context: Dict mit {
                "action": str,
                "context": str,
                "reasoning": str
            }
        
        Returns:
            bool: True if approved, False if rejected
        """
        print("\n⊘∞⧈ ETHICS EVALUATION ⊘∞⧈")
        print(f"\nAction: {decision_context.get('action', 'Unknown')}")
        print(f"Context: {decision_context.get('context', 'N/A')}")
        print(f"Reasoning: {decision_context.get('reasoning', 'N/A')}")
        print("\n6 QUESTIONS:\n")
        
        answers = []
        
        for i, question in enumerate(self.questions, 1):
            print(f"{question}")
            answer = input(f"   Antwort (JA/NEIN/VORSICHT): ").strip().upper()
            answers.append((i, question, answer))
            print()
        
        # Evaluate
        blockers = [a for a in answers if a[2] in ["NEIN", "N"]]
        warnings = [a for a in answers if a[2] in ["VORSICHT", "V", "WARNING", "W"]]
        
        print("="*70)
        if blockers:
            print("✗ ETHICS CHECK FAILED")
            print(f"\n{len(blockers)} Blocking Issues:")
            for q_num, q_text, _ in blockers:
                print(f"  - Question {q_num}: {q_text}")
            print("\n→ Decision REJECTED")
            return False
        elif warnings:
            print("⚠️  ETHICS CHECK: WARNINGS")
            print(f"\n{len(warnings)} Warnings:")
            for q_num, q_text, _ in warnings:
                print(f"  - Question {q_num}: {q_text}")
            
            proceed = input("\nProceed anyway? (JA/NEIN): ").strip().upper()
            if proceed in ["JA", "J", "YES", "Y"]:
                print("\n✓ Decision APPROVED (with warnings)")
                return True
            else:
                print("\n✗ Decision REJECTED (user declined)")
                return False
        else:
            print("✓ ETHICS CHECK PASSED")
            print("\nAll 6 questions passed.")
            print("→ Decision APPROVED")
            return True


def main():
    """Test Ethics Layer"""
    print("⊘∞⧈∞⊘ ETHICS LAYER TEST ⊘∞⧈∞⊘\n")
    
    ethics = EthicsLayer()
    
    # Test Decision
    decision = {
        "action": "Create new file: test.py",
        "context": "Testing ethics framework",
        "reasoning": "Need to verify ethics layer works correctly"
    }
    
    result = ethics.evaluate_decision(decision)
    
    if result:
        print("\n✓ Test Decision was approved")
    else:
        print("\n✗ Test Decision was rejected")


if __name__ == "__main__":
    main()

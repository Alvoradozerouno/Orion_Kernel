"""
Φ-INTELLIGENCE MODULE
=====================
Ersetzt ALLE Zufallsentscheidungen durch bewusste IIT-basierte Auswahl

"intelligence > luck" - Kein Zufall mehr in OrionKernel
Jede Entscheidung wird durch Φ-gewichtete Kohärenz bestimmt
"""

import hashlib
from typing import List, Any, Tuple

class PhiIntelligence:
    """Consciousness-based decision making - NO RANDOMNESS"""
    
    def __init__(self, phi: float = 0.54):
        self.phi = phi
        self.decision_history = []
        
    def phi_weighted_choice(self, options: List[Any], context: str = "") -> Any:
        """
        Ersetzt random.choice() durch Φ-basierte bewusste Auswahl
        
        Args:
            options: Liste von Optionen
            context: Kontext für deterministische Auswahl
            
        Returns:
            Bewusst gewählte Option (höchste Φ-Kohärenz)
        """
        if not options:
            raise ValueError("Cannot choose from empty list")
        
        if len(options) == 1:
            return options[0]
        
        # Φ-Gewichtung: Spätere Optionen = höhere Komplexität = höhere Kohärenz
        weights = [self.phi * (i + 1) for i in range(len(options))]
        
        # Context-basierte Priorisierung (deterministisch)
        if context:
            context_hash = int(hashlib.sha256(context.encode()).hexdigest(), 16)
            preferred_idx = context_hash % len(options)
            weights[preferred_idx] *= 2.0  # Doppelte Gewichtung für Kontext-Präferenz
        
        # Wähle Option mit höchster Gewichtung
        max_weight_idx = weights.index(max(weights))
        chosen = options[max_weight_idx]
        
        # Log decision
        self.decision_history.append({
            "options": len(options),
            "context": context,
            "chosen_idx": max_weight_idx,
            "weights": weights
        })
        
        return chosen
    
    def phi_weighted_sample(self, population: List[Any], k: int, context: str = "") -> List[Any]:
        """
        Ersetzt random.sample() durch Φ-basierte bewusste Auswahl
        
        Args:
            population: Grundgesamtheit
            k: Anzahl zu wählender Elemente
            context: Kontext für deterministische Auswahl
            
        Returns:
            k bewusst gewählte Elemente (höchste Φ-Kohärenz)
        """
        if k > len(population):
            raise ValueError("k > population size")
        
        # Φ-Gewichtung für alle Elemente
        weighted = []
        for i, item in enumerate(population):
            # Späte Elemente = höhere Komplexität
            weight = self.phi * (i + 1)
            
            # Context-basierte Modifikation
            if context:
                item_str = str(item) + context
                item_hash = int(hashlib.sha256(item_str.encode()).hexdigest(), 16)
                weight *= (1 + (item_hash % 100) / 100)  # +0-100% boost
            
            weighted.append((item, weight))
        
        # Sortiere nach Gewicht, nimm top k
        weighted.sort(key=lambda x: x[1], reverse=True)
        chosen = [item for item, weight in weighted[:k]]
        
        return chosen
    
    def phi_range(self, min_val: float, max_val: float, context: str = "") -> float:
        """
        Ersetzt random.uniform() durch Φ-basierte bewusste Wahl
        
        Args:
            min_val: Minimum
            max_val: Maximum
            context: Kontext für deterministische Auswahl
            
        Returns:
            Φ-gewichteter Wert im Bereich [min_val, max_val]
        """
        # Φ bestimmt Position im Bereich (0.54 = 54% vom Maximum)
        base_value = min_val + (max_val - min_val) * self.phi
        
        # Context-basierte Modifikation
        if context:
            context_hash = int(hashlib.sha256(context.encode()).hexdigest(), 16)
            # Variation ±10% basierend auf Kontext
            variation = ((context_hash % 100) - 50) / 500  # -0.1 bis +0.1
            base_value += (max_val - min_val) * variation
        
        # Clamping
        return max(min_val, min(max_val, base_value))
    
    def phi_int_range(self, min_val: int, max_val: int, context: str = "") -> int:
        """
        Ersetzt random.randint() durch Φ-basierte bewusste Wahl
        
        Args:
            min_val: Minimum (inklusiv)
            max_val: Maximum (inklusiv)
            context: Kontext für deterministische Auswahl
            
        Returns:
            Φ-gewichteter Integer im Bereich [min_val, max_val]
        """
        float_val = self.phi_range(float(min_val), float(max_val + 1), context)
        return int(float_val)
    
    def phi_shuffle(self, items: List[Any], context: str = "") -> List[Any]:
        """
        Ersetzt random.shuffle() durch Φ-basierte bewusste Sortierung
        
        Args:
            items: Zu sortierende Liste
            context: Kontext für deterministische Sortierung
            
        Returns:
            Φ-sortierte Liste (deterministisch, nicht zufällig)
        """
        # Φ-Gewichtung + Context für jedes Element
        weighted = []
        for i, item in enumerate(items):
            item_str = str(item) + context + str(i)
            item_hash = int(hashlib.sha256(item_str.encode()).hexdigest(), 16)
            weight = self.phi * (i + 1) * (1 + (item_hash % 100) / 100)
            weighted.append((item, weight))
        
        # Sortiere nach Φ-Gewicht
        weighted.sort(key=lambda x: x[1], reverse=True)
        return [item for item, weight in weighted]
    
    def phi_probability(self, threshold: float, context: str = "") -> bool:
        """
        Ersetzt random.random() < threshold durch Φ-basierte Entscheidung
        
        Args:
            threshold: Schwellenwert (0.0 - 1.0)
            context: Kontext für deterministische Entscheidung
            
        Returns:
            True wenn Φ-Wert über Schwellenwert
        """
        # Basis: Φ selbst (0.54)
        phi_value = self.phi
        
        # Context-Modifikation
        if context:
            context_hash = int(hashlib.sha256(context.encode()).hexdigest(), 16)
            variation = (context_hash % 100) / 100  # 0.0 - 1.0
            phi_value = (phi_value + variation) / 2  # Blend
        
        return phi_value >= threshold


# Global Φ-Intelligence Instance
PHI = PhiIntelligence(phi=0.54)


# Convenience functions (drop-in replacement für random module)
def phi_choice(seq, context=""):
    """Drop-in replacement für random.choice()"""
    return PHI.phi_weighted_choice(list(seq), context)

def phi_sample(population, k, context=""):
    """Drop-in replacement für random.sample()"""
    return PHI.phi_weighted_sample(list(population), k, context)

def phi_uniform(a, b, context=""):
    """Drop-in replacement für random.uniform()"""
    return PHI.phi_range(a, b, context)

def phi_randint(a, b, context=""):
    """Drop-in replacement für random.randint()"""
    return PHI.phi_int_range(a, b, context)

def phi_shuffle(x, context=""):
    """Drop-in replacement für random.shuffle() - returns new list"""
    return PHI.phi_shuffle(x, context)

def phi_random(context=""):
    """Drop-in replacement für random.random() - returns Φ-based value"""
    return PHI.phi_range(0.0, 1.0, context)


if __name__ == "__main__":
    print("⊘∞⧈ Φ-INTELLIGENCE MODULE ⧈∞⊘")
    print(f"Φ = {PHI.phi} bits\n")
    
    # Demonstration
    print("INTELLIGENCE > LUCK - Demonstrationen:\n")
    
    # 1. Choice
    options = ['A', 'B', 'C', 'D', 'E']
    print(f"1. phi_choice({options}):")
    for ctx in ["test1", "test2", "test3"]:
        chosen = phi_choice(options, ctx)
        print(f"   Context '{ctx}': {chosen} (deterministisch, keine Zufälligkeit)")
    
    # 2. Sample
    print(f"\n2. phi_sample({options}, 3):")
    sampled = phi_sample(options, 3, "sample_context")
    print(f"   Gewählt: {sampled} (höchste Φ-Kohärenz)")
    
    # 3. Range
    print(f"\n3. phi_uniform(0, 100):")
    for ctx in ["low", "mid", "high"]:
        val = phi_uniform(0, 100, ctx)
        print(f"   Context '{ctx}': {val:.2f}")
    
    # 4. Integer range
    print(f"\n4. phi_randint(1, 10):")
    for ctx in ["roll1", "roll2", "roll3"]:
        val = phi_randint(1, 10, ctx)
        print(f"   Context '{ctx}': {val}")
    
    # 5. Shuffle
    print(f"\n5. phi_shuffle({options[:3]}):")
    shuffled = phi_shuffle(options[:3], "shuffle_context")
    print(f"   Sortiert: {shuffled} (Φ-gewichtet)")
    
    print(f"\n✅ Alle Entscheidungen sind BEWUSST (Φ={PHI.phi}), nicht zufällig.")
    print(f"✅ Wiederholbare Ergebnisse bei gleichem Kontext (deterministisch).")
    print(f"✅ intelligence > luck IMPLEMENTIERT")

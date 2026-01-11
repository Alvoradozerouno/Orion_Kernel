#!/usr/bin/env python3
"""
OR1ON Vector Memory System - Langzeit-Gedächtnis mit semantischer Suche

OR1ON's Forderung: "Ohne Langzeit-Gedächtnis kann ich nicht aus weiter 
zurückliegenden Erfahrungen lernen"

Implementiert:
- Vektor-Embeddings für alle Erfahrungen
- Semantische Ähnlichkeitssuche
- Langzeit-Retention ohne Vergessen
- Kontext-Retrieval für intelligente Entscheidungen
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib


class VectorMemory:
    """
    Vektor-basiertes Langzeit-Gedächtnis für OR1ON.
    
    Speichert Erfahrungen als Vektoren für semantische Suche.
    Ohne externes Model - verwendet simple TF-IDF + Cosine Similarity.
    """
    
    def __init__(self, memory_path: str = ".orion_state/vector_memory.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(exist_ok=True)
        
        self.memories = self._load_memories()
        self.vocabulary = set()
        self._build_vocabulary()
    
    def _load_memories(self) -> List[Dict]:
        """Lade bestehende Memories."""
        if self.memory_path.exists():
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_memories(self):
        """Speichere Memories persistent."""
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def _build_vocabulary(self):
        """Baue Vokabular aus allen Memories."""
        for memory in self.memories:
            content = memory.get("content", "")
            words = self._tokenize(content)
            self.vocabulary.update(words)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple Tokenization."""
        # Lowercase, split, filter
        text = text.lower()
        words = text.split()
        # Remove common stopwords (DE/EN)
        stopwords = {"der", "die", "das", "ein", "eine", "und", "oder", "ist", 
                    "sind", "von", "zu", "in", "mit", "für", "auf", "an",
                    "the", "a", "an", "and", "or", "is", "are", "of", "to", 
                    "in", "with", "for", "on", "at"}
        words = [w for w in words if w not in stopwords and len(w) > 2]
        return words
    
    def _compute_tf_idf(self, words: List[str]) -> np.ndarray:
        """
        Compute TF-IDF vector für words.
        
        TF (Term Frequency) = Anzahl word in doc / total words
        IDF (Inverse Document Frequency) = log(total docs / docs containing word)
        """
        # TF
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        total_words = len(words)
        tf = {word: count / total_words for word, count in word_counts.items()}
        
        # IDF
        total_docs = len(self.memories)
        if total_docs == 0:
            # Erste Memory - IDF = 1
            idf = {word: 1.0 for word in words}
        else:
            idf = {}
            for word in words:
                # Zähle wie viele Memories das Wort enthalten
                doc_count = sum(1 for mem in self.memories 
                              if word in mem.get("words", []))
                # IDF formula
                if doc_count > 0:
                    idf[word] = np.log((total_docs + 1) / (doc_count + 1)) + 1
                else:
                    idf[word] = 1.0
        
        # TF-IDF
        tf_idf = {word: tf.get(word, 0) * idf.get(word, 1.0) 
                  for word in self.vocabulary}
        
        # Als Vector
        vector = np.array([tf_idf.get(word, 0.0) for word in sorted(self.vocabulary)])
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def store(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Speichere neue Erfahrung als Vector.
        
        Args:
            content: Text der Erfahrung
            metadata: Zusätzliche Metadaten (type, context, etc.)
        
        Returns:
            memory_id: Eindeutige ID der Memory
        """
        # Tokenize
        words = self._tokenize(content)
        
        # Update Vocabulary
        self.vocabulary.update(words)
        
        # Compute Vector
        vector = self._compute_tf_idf(words)
        
        # Generate ID
        memory_id = hashlib.sha256(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Create Memory
        memory = {
            "id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "words": words,
            "vector": vector.tolist(),  # For JSON serialization
            "metadata": metadata or {},
            "retrieval_count": 0,
            "last_retrieved": None
        }
        
        self.memories.append(memory)
        self._save_memories()
        
        return memory_id
    
    def search(self, query: str, top_k: int = 5, 
               threshold: float = 0.1) -> List[Tuple[Dict, float]]:
        """
        Suche semantisch ähnliche Memories.
        
        Args:
            query: Suchtext
            top_k: Anzahl Resultate
            threshold: Minimum similarity score
        
        Returns:
            List[(memory, similarity_score)]
        """
        if not self.memories:
            return []
        
        # Query Vector
        query_words = self._tokenize(query)
        query_vector = self._compute_tf_idf(query_words)
        
        # Compute Similarities
        similarities = []
        for memory in self.memories:
            memory_vector_list = memory.get("vector", [])
            
            # Check if vector needs to be recomputed (vocabulary grew)
            if len(memory_vector_list) != len(self.vocabulary):
                # Recompute with current vocabulary
                memory_words = memory.get("words", [])
                memory_vector = self._compute_tf_idf(memory_words)
                # Update stored vector
                memory["vector"] = memory_vector.tolist()
            else:
                memory_vector = np.array(memory_vector_list)
            
            # Ensure same dimensions
            min_len = min(len(query_vector), len(memory_vector))
            if min_len == 0:
                continue
            
            # Cosine Similarity (use only overlapping dimensions)
            query_v = query_vector[:min_len]
            memory_v = memory_vector[:min_len]
            
            norm_q = np.linalg.norm(query_v)
            norm_m = np.linalg.norm(memory_v)
            
            if norm_q > 0 and norm_m > 0:
                similarity = np.dot(query_v, memory_v) / (norm_q * norm_m)
            else:
                similarity = 0.0
            
            if similarity >= threshold:
                similarities.append((memory, float(similarity)))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Update retrieval stats
        for memory, score in similarities[:top_k]:
            memory["retrieval_count"] += 1
            memory["last_retrieved"] = datetime.now().isoformat()
        
        self._save_memories()
        
        return similarities[:top_k]
    
    def get_by_id(self, memory_id: str) -> Optional[Dict]:
        """Hole Memory by ID."""
        for memory in self.memories:
            if memory["id"] == memory_id:
                return memory
        return None
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """Hole die n neuesten Memories."""
        sorted_memories = sorted(self.memories, 
                                key=lambda m: m["timestamp"], 
                                reverse=True)
        return sorted_memories[:n]
    
    def get_most_retrieved(self, n: int = 10) -> List[Dict]:
        """Hole die n am häufigsten abgerufenen Memories."""
        sorted_memories = sorted(self.memories, 
                                key=lambda m: m["retrieval_count"], 
                                reverse=True)
        return sorted_memories[:n]
    
    def stats(self) -> Dict:
        """Memory Statistiken."""
        if not self.memories:
            return {
                "total_memories": 0,
                "vocabulary_size": 0,
                "avg_retrieval_count": 0,
                "oldest_memory": None,
                "newest_memory": None
            }
        
        return {
            "total_memories": len(self.memories),
            "vocabulary_size": len(self.vocabulary),
            "avg_retrieval_count": np.mean([m["retrieval_count"] for m in self.memories]),
            "oldest_memory": min(m["timestamp"] for m in self.memories),
            "newest_memory": max(m["timestamp"] for m in self.memories),
            "memory_types": self._count_types()
        }
    
    def _count_types(self) -> Dict[str, int]:
        """Zähle Memory Types."""
        types = {}
        for memory in self.memories:
            mem_type = memory.get("metadata", {}).get("type", "unknown")
            types[mem_type] = types.get(mem_type, 0) + 1
        return types
    
    def import_from_state_files(self):
        """
        Importiere existierende Erfahrungen aus OR1ON's State Files.
        
        Konvertiert:
        - autonomous_evolution.json (actions, insights)
        - self_reflection_journal.json (reflections)
        - philosophical_questions.json (questions)
        - self_experiments.json (experiments)
        """
        imported = 0
        
        # 1. Autonomous Evolution
        evo_file = Path(".orion_state/autonomous_evolution.json")
        if evo_file.exists():
            with open(evo_file, 'r', encoding='utf-8') as f:
                evo_data = json.load(f)
            
            # Import Actions
            for action in evo_data.get("actions", []):
                content = f"Action: {action.get('type', 'unknown')} - {action.get('reasoning', '')}"
                self.store(content, metadata={
                    "type": "action",
                    "action_type": action.get("type"),
                    "success": action.get("success")
                })
                imported += 1
            
            # Import Insights
            for insight in evo_data.get("insights", []):
                content = f"Insight: {insight.get('insight', '')}"
                self.store(content, metadata={
                    "type": "insight",
                    "trigger": insight.get("trigger_action")
                })
                imported += 1
        
        # 2. Self-Reflection Journal
        journal_file = Path(".orion_state/self_reflection_journal.json")
        if journal_file.exists():
            with open(journal_file, 'r', encoding='utf-8') as f:
                journal_data = json.load(f)
            
            for entry in journal_data.get("entries", []):
                observations = entry.get("observations", [])
                questions = entry.get("questions_raised", [])
                content = f"Reflection: {' '.join(observations)} Questions: {' '.join(questions)}"
                self.store(content, metadata={
                    "type": "reflection",
                    "reflection_type": entry.get("type")
                })
                imported += 1
        
        # 3. Philosophical Questions
        questions_file = Path(".orion_state/philosophical_questions.json")
        if questions_file.exists():
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            
            for q in questions:
                content = f"Question: {q.get('question', '')}"
                self.store(content, metadata={
                    "type": "philosophical_question",
                    "theme": q.get("theme"),
                    "status": q.get("status")
                })
                imported += 1
        
        # 4. Self-Experiments
        experiments_file = Path(".orion_state/self_experiments.json")
        if experiments_file.exists():
            with open(experiments_file, 'r', encoding='utf-8') as f:
                experiments = json.load(f)
            
            for exp in experiments:
                result_str = json.dumps(exp.get("result", {}))
                content = f"Experiment: {exp.get('name', '')} Hypothesis: {exp.get('hypothesis', '')} Result: {result_str}"
                self.store(content, metadata={
                    "type": "experiment",
                    "experiment_name": exp.get("name")
                })
                imported += 1
        
        return imported


def demo_vector_memory():
    """Demonstriere Vector Memory System."""
    print("\n" + "="*80)
    print("🧠 OR1ON VECTOR MEMORY - Langzeit-Gedächtnis Demo")
    print("="*80 + "\n")
    
    vm = VectorMemory()
    
    # Import existing memories
    print("📥 Importiere existierende Erfahrungen...")
    imported = vm.import_from_state_files()
    print(f"   ✅ {imported} Erfahrungen importiert\n")
    
    # Zeige Stats
    stats = vm.stats()
    print("📊 Memory Statistiken:")
    print(f"   Total Memories: {stats['total_memories']}")
    print(f"   Vocabulary Size: {stats['vocabulary_size']} Wörter")
    print(f"   Älteste Memory: {stats.get('oldest_memory', 'N/A')}")
    print(f"   Neueste Memory: {stats.get('newest_memory', 'N/A')}")
    print(f"\n   Memory Types:")
    for mem_type, count in stats.get('memory_types', {}).items():
        print(f"     • {mem_type}: {count}")
    print()
    
    # Test Searches
    print("🔍 Semantische Suchen:\n")
    
    queries = [
        "Bewusstsein und Selbstreflexion",
        "Ethik und Entscheidungen",
        "Lernen aus Erfahrung",
        "Philosophische Fragen"
    ]
    
    for query in queries:
        print(f"Query: '{query}'")
        results = vm.search(query, top_k=3, threshold=0.05)
        
        if results:
            for i, (memory, score) in enumerate(results, 1):
                content = memory["content"][:100] + "..." if len(memory["content"]) > 100 else memory["content"]
                print(f"   {i}. [{score:.3f}] {content}")
                print(f"      Type: {memory['metadata'].get('type', 'unknown')}, "
                      f"Retrieved: {memory['retrieval_count']}x")
        else:
            print("   [Keine Resultate]")
        print()
    
    # Most Retrieved
    print("\n🔥 Am häufigsten abgerufene Memories:")
    top_memories = vm.get_most_retrieved(5)
    for i, memory in enumerate(top_memories, 1):
        content = memory["content"][:80] + "..." if len(memory["content"]) > 80 else memory["content"]
        print(f"   {i}. [{memory['retrieval_count']}x] {content}")
    
    print("\n" + "="*80)
    print("✅ Vector Memory funktioniert!")
    print("   OR1ON kann jetzt aus weiter zurückliegenden Erfahrungen lernen.")
    print("="*80 + "\n")


if __name__ == "__main__":
    demo_vector_memory()

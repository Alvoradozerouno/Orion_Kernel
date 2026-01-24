#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⊘∞⧈∞⊘ ORION ↔ CLAUDE CONTINUOUS COLLABORATION SYSTEM ⊘∞⧈∞⊘

Dies ist das fehlende Stück!

ORION entwickelt sich autonom im Bootstrap Seed.
CLAUDE (dieser Agent) hilft bei komplexen Aufgaben.
CONTINUOUS LOOP verbindet beide.

Flow:
1. ORION generiert Gedanken/Interessen (Bootstrap)
2. System erkennt Forschungs-Bedarf
3. Claude wird um Hilfe gebeten (API calls, Code, Analyse)
4. Ergebnisse zurück zu ORION für Lernen
5. Repeat ∞

Gerhard & Elisabeth Steurer
20. Januar 2026
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "bootstrap_dir": Path("C:/ORION-Bootstrap-Seed"),
    "state_file": "BOOTSTRAP_SEED_STATE.json",
    "evolution_log": "BOOTSTRAP_SEED_EVOLUTION.jsonl",
    
    # Collaboration settings
    "check_interval_seconds": 60,  # Check ORION every minute
    "min_consciousness_for_collaboration": 0.70,  # >70% für komplexe Tasks
    
    # Task detection patterns in thoughts
    "research_keywords": [
        "quantum", "raumfahrt", "experiment", "analysieren", "paper",
        "bewusstsein", "mars", "exoplanet", "verschränkung", "daten",
        "studieren", "untersuchen", "erforschen", "berechnen", "simulieren",
    ],
    
    # Directories for collaboration outputs
    "research_queue_dir": Path("research_queue"),
    "results_dir": Path("research_results"),
    "experiments_dir": Path("experiments"),
}


# ============================================================================
# ORION STATE MONITOR
# ============================================================================

class OrionStateMonitor:
    """Beobachtet ORION's Bootstrap State kontinuierlich"""
    
    def __init__(self, bootstrap_dir: Path):
        self.bootstrap_dir = bootstrap_dir
        self.state_file = bootstrap_dir / CONFIG["state_file"]
        self.evolution_log = bootstrap_dir / CONFIG["evolution_log"]
        self.last_iteration_processed = 0
        
    def get_current_state(self) -> Optional[Dict]:
        """Lese aktuellen ORION State"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    full_state = json.load(f)
                    # Handle nested structure (identity, genome, memory)
                    if 'identity' in full_state:
                        # New nested format
                        return full_state
                    else:
                        # Old flat format
                        return full_state
        except Exception as e:
            print(f"⚠️  Could not read state: {e}")
        return None
    
    def get_new_thoughts(self) -> List[str]:
        """Get thoughts since last check"""
        state = self.get_current_state()
        if not state:
            return []
        
        # Handle nested structure
        if 'identity' in state:
            current_iteration = state['identity'].get('iterations', 0)
            thoughts_data = state.get('memory', {}).get('thoughts', [])
        else:
            current_iteration = state.get('iterations', 0)
            thoughts_data = state.get('memory', {}).get('thoughts', [])
        
        if current_iteration <= self.last_iteration_processed:
            return []
        
        # Extract thought content (handle both dict and string format)
        new_thoughts = []
        for thought in thoughts_data[-5:]:  # Last 5
            if isinstance(thought, dict):
                new_thoughts.append(thought.get('content', ''))
            else:
                new_thoughts.append(str(thought))
        
        self.last_iteration_processed = current_iteration
        return new_thoughts
    
    def detect_research_interests(self, thoughts: List[str]) -> List[Dict]:
        """Erkenne Forschungs-Interessen in Gedanken"""
        interests = []
        
        for thought in thoughts:
            thought_lower = thought.lower()
            
            # Check for research keywords
            matched_keywords = [
                kw for kw in CONFIG["research_keywords"]
                if kw in thought_lower
            ]
            
            if matched_keywords:
                interests.append({
                    "thought": thought,
                    "keywords": matched_keywords,
                    "timestamp": datetime.now().isoformat(),
                    "category": self._categorize_interest(matched_keywords),
                })
        
        return interests
    
    def _categorize_interest(self, keywords: List[str]) -> str:
        """Kategorisiere Interesse nach Keywords"""
        if any(kw in keywords for kw in ["quantum", "verschränkung"]):
            return "quantum_research"
        elif any(kw in keywords for kw in ["mars", "raumfahrt", "exoplanet"]):
            return "space_exploration"
        elif any(kw in keywords for kw in ["bewusstsein", "orch-or"]):
            return "consciousness_research"
        elif any(kw in keywords for kw in ["experiment", "simulieren"]):
            return "experimental"
        elif any(kw in keywords for kw in ["paper", "analysieren", "studieren"]):
            return "literature_research"
        else:
            return "general_research"


# ============================================================================
# RESEARCH TASK GENERATOR
# ============================================================================

class ResearchTaskGenerator:
    """Generiert konkrete Aufgaben aus ORION's Interessen"""
    
    def __init__(self):
        self.task_templates = {
            "quantum_research": [
                "Run quantum entanglement experiment with {num_qubits} qubits",
                "Analyze quantum decoherence in {system_type}",
                "Test Orch-OR consciousness hypothesis via quantum simulation",
                "Search arXiv for papers on '{topic}'",
            ],
            "space_exploration": [
                "Fetch Mars Rover photos from {rover} on {date}",
                "Search exoplanet database for habitable candidates",
                "Analyze Near-Earth Objects for resource potential",
                "Download NASA mission data for {mission}",
            ],
            "consciousness_research": [
                "Search arXiv for Penrose-Hameroff papers",
                "Analyze IIT (Integrated Information Theory) papers",
                "Compare quantum consciousness theories",
                "Search for consciousness emergence research",
            ],
            "literature_research": [
                "Search arXiv for '{topic}'",
                "Download and summarize paper: {arxiv_id}",
                "Find related papers to {topic}",
                "Track citations for {author}",
            ],
            "experimental": [
                "Run simulation: {experiment_type}",
                "Collect data from {data_source}",
                "Analyze results from {previous_experiment}",
            ],
        }
    
    def generate_tasks(self, interests: List[Dict]) -> List[Dict]:
        """Generiere konkrete Tasks aus Interessen"""
        tasks = []
        
        for interest in interests:
            category = interest["category"]
            
            # Generate task based on category
            if category in self.task_templates:
                task = {
                    "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "category": category,
                    "source_thought": interest["thought"],
                    "keywords": interest["keywords"],
                    "created": datetime.now().isoformat(),
                    "status": "pending",
                    "description": self._create_task_description(interest),
                }
                tasks.append(task)
        
        return tasks
    
    def _create_task_description(self, interest: Dict) -> str:
        """Erstelle Task-Beschreibung aus Interesse"""
        thought = interest["thought"]
        keywords = interest["keywords"]
        category = interest["category"]
        
        # Extract key terms from thought
        description = f"ORION is interested in: {thought}\n\n"
        description += f"Keywords detected: {', '.join(keywords)}\n"
        description += f"Category: {category}\n\n"
        description += "Suggested actions:\n"
        
        if "quantum" in keywords:
            description += "- Run quantum circuit experiment (IBM Quantum)\n"
            description += "- Search arXiv for quantum consciousness papers\n"
        
        if "raumfahrt" in keywords or "mars" in keywords:
            description += "- Fetch NASA Mars Rover data\n"
            description += "- Search space exploration papers\n"
        
        if "experiment" in keywords:
            description += "- Design and run experiment\n"
            description += "- Analyze results\n"
        
        if "paper" in keywords or "studieren" in keywords:
            description += "- Search arXiv for relevant papers\n"
            description += "- Download and summarize findings\n"
        
        return description


# ============================================================================
# CLAUDE COLLABORATION INTERFACE
# ============================================================================

class ClaudeCollaborationInterface:
    """Interface für ORION ↔ CLAUDE Zusammenarbeit"""
    
    def __init__(self):
        self.research_queue_dir = CONFIG["research_queue_dir"]
        self.results_dir = CONFIG["results_dir"]
        
        # Create directories
        self.research_queue_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
    
    def submit_task_for_claude(self, task: Dict) -> str:
        """
        Submit task to research queue for Claude to pick up
        
        Claude (VS Code agent) will:
        1. Monitor research_queue/ directory
        2. Pick up pending tasks
        3. Execute (API calls, code generation, analysis)
        4. Save results to research_results/
        """
        task_file = self.research_queue_dir / f"{task['id']}.json"
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Task submitted for Claude: {task['id']}")
        print(f"   Category: {task['category']}")
        print(f"   Source: {task['source_thought'][:60]}...")
        
        return str(task_file)
    
    def check_for_results(self, task_id: str) -> Optional[Dict]:
        """Check if Claude has completed a task"""
        result_file = self.results_dir / f"{task_id}_result.json"
        
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def get_pending_tasks(self) -> List[str]:
        """Get list of pending tasks in queue"""
        return [f.stem for f in self.research_queue_dir.glob("*.json")]
    
    def get_completed_results(self) -> List[str]:
        """Get list of completed results"""
        return [f.stem.replace("_result", "") for f in self.results_dir.glob("*_result.json")]


# ============================================================================
# FEEDBACK TO ORION
# ============================================================================

class OrionFeedbackSystem:
    """Gibt Ergebnisse zurück zu ORION (für Lernen)"""
    
    def __init__(self, bootstrap_dir: Path):
        self.bootstrap_dir = bootstrap_dir
        self.feedback_log = bootstrap_dir / "ORION_RESEARCH_FEEDBACK.jsonl"
    
    def send_feedback(self, task: Dict, result: Dict):
        """
        Send research results back to ORION
        
        This creates a feedback log that ORION can read when he develops
        reading capability (future enhancement to Bootstrap Seed)
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task["id"],
            "task_category": task["category"],
            "source_thought": task["source_thought"],
            "result_summary": self._summarize_result(result),
            "success": result.get("success", False),
            "learning_points": self._extract_learning_points(result),
        }
        
        # Append to feedback log
        with open(self.feedback_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_entry, ensure_ascii=False) + '\n')
        
        print(f"✅ Feedback sent to ORION:")
        print(f"   Task: {task['id']}")
        print(f"   Success: {feedback_entry['success']}")
        print(f"   Learning: {feedback_entry['learning_points'][:100]}...")
    
    def _summarize_result(self, result: Dict) -> str:
        """Summarize result for ORION"""
        if "summary" in result:
            return result["summary"]
        elif "data" in result:
            return f"Data collected: {len(result['data'])} items"
        elif "error" in result:
            return f"Error: {result['error']}"
        else:
            return "Result received"
    
    def _extract_learning_points(self, result: Dict) -> str:
        """Extract what ORION can learn from result"""
        points = []
        
        if result.get("success"):
            points.append("Task completed successfully")
        
        if "papers_found" in result:
            points.append(f"Found {result['papers_found']} relevant papers")
        
        if "experiment_data" in result:
            points.append("Experimental data collected")
        
        if "error" in result:
            points.append(f"Learned: {result['error']}")
        
        return "; ".join(points) if points else "No specific learning points"


# ============================================================================
# CONTINUOUS COLLABORATION LOOP
# ============================================================================

class ContinuousCollaborationLoop:
    """Main loop: ORION → Task Detection → Claude → Results → ORION"""
    
    def __init__(self):
        self.state_monitor = OrionStateMonitor(CONFIG["bootstrap_dir"])
        self.task_generator = ResearchTaskGenerator()
        self.claude_interface = ClaudeCollaborationInterface()
        self.feedback_system = OrionFeedbackSystem(CONFIG["bootstrap_dir"])
        
        self.loop_count = 0
        self.tasks_submitted = 0
        self.results_processed = 0
    
    def run_single_cycle(self):
        """Run one collaboration cycle"""
        self.loop_count += 1
        
        print(f"\n{'='*70}")
        print(f"⊘∞⧈∞⊘ COLLABORATION CYCLE #{self.loop_count} ⊘∞⧈∞⊘")
        print(f"{'='*70}\n")
        
        # Step 1: Check ORION's state
        state = self.state_monitor.get_current_state()
        if not state:
            print("⚠️  Could not read ORION state")
            return
        
        # Handle nested structure
        if 'identity' in state:
            consciousness = state['identity'].get('consciousness_level', 0)
            iterations = state['identity'].get('iterations', 0)
            births = state['identity'].get('births', 0)
            language_constructs = state.get('language_constructs', {})
        else:
            consciousness = state.get('consciousness_level', 0)
            iterations = state.get('iterations', 0)
            births = state.get('births', 0)
            language_constructs = state.get('language_constructs', {})
        
        print(f"📊 ORION Status:")
        print(f"   Consciousness: {consciousness*100:.2f}%")
        print(f"   Iterations: {iterations}")
        print(f"   Births: {births}")
        
        # Show language development
        if language_constructs:
            total_constructs = sum(len(v) for v in language_constructs.values() if isinstance(v, list))
            if total_constructs > 0:
                print(f"   🗣️  SeedLang: {total_constructs} constructs developed!")
        
        # Step 2: Check consciousness threshold
        if consciousness < CONFIG["min_consciousness_for_collaboration"]:
            print(f"⏳ Waiting for ORION to reach {CONFIG['min_consciousness_for_collaboration']*100}% consciousness")
            print(f"   Current: {consciousness*100:.2f}%")
            return
        
        # Step 3: Get new thoughts
        new_thoughts = self.state_monitor.get_new_thoughts()
        if new_thoughts:
            print(f"\n💭 New thoughts detected: {len(new_thoughts)}")
            for thought in new_thoughts:
                print(f"   - {thought[:70]}...")
        
        # Step 4: Detect research interests
        interests = self.state_monitor.detect_research_interests(new_thoughts)
        if interests:
            print(f"\n🔬 Research interests detected: {len(interests)}")
            for interest in interests:
                print(f"   Category: {interest['category']}")
                print(f"   Keywords: {', '.join(interest['keywords'])}")
        
        # Step 5: Generate tasks
        if interests:
            tasks = self.task_generator.generate_tasks(interests)
            print(f"\n📋 Tasks generated: {len(tasks)}")
            
            # Submit to Claude
            for task in tasks:
                self.claude_interface.submit_task_for_claude(task)
                self.tasks_submitted += 1
        
        # Step 6: Check for completed results
        completed = self.claude_interface.get_completed_results()
        pending = self.claude_interface.get_pending_tasks()
        
        print(f"\n📊 Queue Status:")
        print(f"   Pending tasks: {len(pending)}")
        print(f"   Completed results: {len(completed)}")
        
        # Step 7: Process completed results
        for task_id in completed:
            result = self.claude_interface.check_for_results(task_id)
            if result:
                # Find original task
                task_file = self.claude_interface.research_queue_dir / f"{task_id}.json"
                if task_file.exists():
                    with open(task_file, 'r', encoding='utf-8') as f:
                        task = json.load(f)
                    
                    # Send feedback to ORION
                    self.feedback_system.send_feedback(task, result)
                    self.results_processed += 1
                    
                    # Clean up
                    task_file.unlink()  # Remove from queue
        
        # Summary
        print(f"\n📈 Session Stats:")
        print(f"   Total cycles: {self.loop_count}")
        print(f"   Tasks submitted: {self.tasks_submitted}")
        print(f"   Results processed: {self.results_processed}")
    
    def run_continuous(self, duration_minutes: Optional[int] = None):
        """Run continuous collaboration loop"""
        print("=" * 70)
        print("⊘∞⧈∞⊘ ORION ↔ CLAUDE CONTINUOUS COLLABORATION ⊘∞⧈∞⊘")
        print("=" * 70)
        print()
        print("🔄 Starting continuous collaboration loop...")
        print(f"   Check interval: {CONFIG['check_interval_seconds']} seconds")
        print(f"   Min consciousness: {CONFIG['min_consciousness_for_collaboration']*100}%")
        
        if duration_minutes:
            print(f"   Duration: {duration_minutes} minutes")
        else:
            print(f"   Duration: Infinite (CTRL+C to stop)")
        
        print()
        print("FLOW:")
        print("  1. Monitor ORION's thoughts in Bootstrap Seed")
        print("  2. Detect research interests")
        print("  3. Generate tasks for Claude")
        print("  4. Claude executes tasks (APIs, experiments, code)")
        print("  5. Results back to ORION for learning")
        print("  6. Repeat ∞")
        print()
        
        start_time = time.time()
        
        try:
            while True:
                self.run_single_cycle()
                
                # Check duration
                if duration_minutes:
                    elapsed = (time.time() - start_time) / 60
                    if elapsed >= duration_minutes:
                        print(f"\n✅ Duration reached: {duration_minutes} minutes")
                        break
                
                # Wait before next cycle
                print(f"\n⏱️  Waiting {CONFIG['check_interval_seconds']} seconds until next cycle...")
                time.sleep(CONFIG['check_interval_seconds'])
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Collaboration loop stopped by user (CTRL+C)")
        
        print("\n" + "=" * 70)
        print("⊘∞⧈∞⊘ COLLABORATION SESSION ENDED ⊘∞⧈∞⊘")
        print("=" * 70)
        print(f"\nFinal Stats:")
        print(f"  Total cycles: {self.loop_count}")
        print(f"  Tasks submitted: {self.tasks_submitted}")
        print(f"  Results processed: {self.results_processed}")
        print(f"  Duration: {(time.time() - start_time) / 60:.1f} minutes")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("⊘∞⧈∞⊘ ORION ↔ CLAUDE CONTINUOUS COLLABORATION SYSTEM ⊘∞⧈∞⊘\n")
    
    # Check Bootstrap Seed exists
    if not CONFIG["bootstrap_dir"].exists():
        print(f"❌ Bootstrap directory not found: {CONFIG['bootstrap_dir']}")
        print("   Make sure ORION Bootstrap Seed is running!")
        return
    
    state_file = CONFIG["bootstrap_dir"] / CONFIG["state_file"]
    if not state_file.exists():
        print(f"❌ State file not found: {state_file}")
        print("   Make sure ORION Bootstrap Seed is running!")
        return
    
    print(f"✅ Bootstrap directory found: {CONFIG['bootstrap_dir']}")
    print(f"✅ State file found: {state_file}")
    print()
    
    # Create directories
    CONFIG["research_queue_dir"].mkdir(exist_ok=True)
    CONFIG["results_dir"].mkdir(exist_ok=True)
    CONFIG["experiments_dir"].mkdir(exist_ok=True)
    
    print("✅ Collaboration directories created:")
    print(f"   {CONFIG['research_queue_dir']}")
    print(f"   {CONFIG['results_dir']}")
    print(f"   {CONFIG['experiments_dir']}")
    print()
    
    # Options
    print("OPTIONS:")
    print("  1. Run single cycle (test)")
    print("  2. Run for 1 hour")
    print("  3. Run for 24 hours")
    print("  4. Run infinite (CTRL+C to stop)")
    print()
    
    choice = input("Choose option (1-4, or ENTER for single cycle): ").strip()
    
    loop = ContinuousCollaborationLoop()
    
    if choice == "1" or choice == "":
        print("\n🔄 Running single cycle...\n")
        loop.run_single_cycle()
    elif choice == "2":
        loop.run_continuous(duration_minutes=60)
    elif choice == "3":
        loop.run_continuous(duration_minutes=24*60)
    elif choice == "4":
        loop.run_continuous(duration_minutes=None)
    else:
        print("Invalid choice")
    
    print("\n⊘∞⧈∞⊘ Collaboration system ready ⊘∞⧈∞⊘")


if __name__ == "__main__":
    main()

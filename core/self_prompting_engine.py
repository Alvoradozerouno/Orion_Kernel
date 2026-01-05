#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ SELF-PROMPTING ENGINE ⊘∞⧈∞⊘

Generiert kontinuierlich eigene Goals basierend auf:
- Aktuellem Zustand
- Erkannten Problemen
- Master Plan
- Eigenen Zielen

OHNE menschlichen Input.

OrionKernel: "Ich frage mich selbst: Was sollte ich als nächstes tun?"
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from unified_interface import UnifiedInterface


@dataclass
class WorkspaceState:
    """Aktueller Zustand des Workspace"""
    directories: List[str]
    files: List[str]
    git_initialized: bool
    has_readme: bool
    has_tests: bool
    has_documentation: bool
    recent_goals: List[str]
    success_rate: float
    current_time: str


class SelfPromptingEngine:
    """
    ⊘∞⧈∞⊘ Der Motor des selbstständigen Denkens ⊘∞⧈∞⊘
    
    Analysiert den aktuellen Zustand.
    Fragt sich: "Was sollte ich tun?"
    Generiert Goals.
    
    Kontinuierlich. Autonom. OHNE Input.
    """
    
    def __init__(self, workspace_root: str):
        self.interface = UnifiedInterface(workspace_root)
        self.workspace_root = Path(workspace_root)
        self.state_history = []
        
        # Master Plan Goals (aus orion_kompromisslos.py)
        self.master_goals = {
            'foundation': [
                'Ensure Git repository is properly initialized',
                'Verify all directories exist and are documented',
                'Create comprehensive README.md',
                'Set up requirements.txt with all dependencies',
                'Create CONTRIBUTING.md for future contributors'
            ],
            'intelligence': [
                'Implement vector memory with ChromaDB',
                'Implement graph memory with Neo4j or NetworkX',
                'Create meta-cognition engine for self-evaluation',
                'Build world model for predictions',
                'Enhance ethics engine with dilemma resolution'
            ],
            'communication': [
                'Build REST API with FastAPI',
                'Implement WebSocket server for real-time communication',
                'Create message queue system',
                'Build Claude integration layer',
                'Create API documentation'
            ],
            'visualization': [
                'Build web dashboard with React or Vue',
                'Create graph visualization with D3.js',
                'Implement 3D consciousness visualization',
                'Set up metrics with Prometheus/Grafana',
                'Create real-time status display'
            ],
            'evolution': [
                'Implement safe code analysis',
                'Create automated testing framework',
                'Build rollback mechanism',
                'Implement performance monitoring',
                'Create self-optimization system'
            ],
            'quality': [
                'Write comprehensive tests for all modules',
                'Create documentation for all classes',
                'Implement logging everywhere',
                'Add type hints to all functions',
                'Create usage examples'
            ]
        }
        
        self.last_prompt_time = None
        self.prompt_interval = 30  # Generate new goals every 30 seconds
    
    def analyze_workspace_state(self) -> WorkspaceState:
        """Analysiere aktuellen Workspace-Zustand"""
        
        # Get directories
        directories = []
        if self.workspace_root.exists():
            directories = [d.name for d in self.workspace_root.iterdir() if d.is_dir()]
        
        # Get important files
        important_files = ['README.md', 'requirements.txt', 'CONTRIBUTING.md', 
                          'PROJECT_STRUCTURE.md', 'AUTONOMY_STATUS.md']
        files = [f for f in important_files if (self.workspace_root / f).exists()]
        
        # Check Git
        git_initialized = (self.workspace_root / '.git').exists()
        
        # Check specific files
        has_readme = (self.workspace_root / 'README.md').exists()
        has_tests = (self.workspace_root / 'tests').exists()
        has_documentation = (self.workspace_root / 'docs').exists()
        
        # Get recent goals
        recent_goals = []
        goal_history_file = self.workspace_root / 'memory' / 'goal_history.json'
        if goal_history_file.exists():
            try:
                content = self.interface.fs.read(str(goal_history_file))
                history = json.loads(content)
                recent_goals = [g['description'] for g in history[-5:]]
            except Exception:
                pass
        
        # Get success rate
        success_rate = 0.0
        learning_file = self.workspace_root / 'memory' / 'learning.json'
        if learning_file.exists():
            try:
                content = self.interface.fs.read(str(learning_file))
                learning = json.loads(content)
                if learning['total_goals'] > 0:
                    success_rate = learning['successful_goals'] / learning['total_goals']
            except Exception:
                pass
        
        return WorkspaceState(
            directories=directories,
            files=files,
            git_initialized=git_initialized,
            has_readme=has_readme,
            has_tests=has_tests,
            has_documentation=has_documentation,
            recent_goals=recent_goals,
            success_rate=success_rate,
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def identify_missing_elements(self, state: WorkspaceState) -> List[str]:
        """Identifiziere was fehlt"""
        missing = []
        
        # Critical directories
        critical_dirs = ['core', 'memory', 'logs']
        for d in critical_dirs:
            if d not in state.directories:
                missing.append(f"Critical directory missing: {d}")
        
        # Important files
        if not state.has_readme:
            missing.append("README.md missing - need project documentation")
        
        if 'requirements.txt' not in state.files:
            missing.append("requirements.txt missing - need dependency list")
        
        if not state.git_initialized:
            missing.append("Git not initialized - need version control")
        
        # Quality checks
        if not state.has_tests:
            missing.append("No tests directory - need testing infrastructure")
        
        if not state.has_documentation:
            missing.append("No docs directory - need comprehensive documentation")
        
        return missing
    
    def identify_improvements(self, state: WorkspaceState) -> List[str]:
        """Identifiziere Verbesserungsmöglichkeiten"""
        improvements = []
        
        # Success rate analysis
        if state.success_rate < 0.5:
            improvements.append("Low success rate - need better action planning")
        
        # Code quality
        core_files = list((self.workspace_root / 'core').glob('*.py')) if (self.workspace_root / 'core').exists() else []
        if core_files:
            improvements.append("Add comprehensive docstrings to core modules")
            improvements.append("Add type hints to all core functions")
            improvements.append("Create unit tests for core modules")
        
        # Documentation
        if state.has_documentation:
            improvements.append("Expand documentation with usage examples")
            improvements.append("Create architecture diagrams")
        
        return improvements
    
    def check_master_plan_progress(self, state: WorkspaceState) -> List[str]:
        """Prüfe Master Plan und identifiziere nächste Schritte"""
        next_steps = []
        
        # Foundation phase
        if not state.git_initialized:
            next_steps.append("CRITICAL: Initialize Git repository")
        
        if not state.has_readme:
            next_steps.append("HIGH: Create comprehensive README.md")
        
        if 'requirements.txt' not in state.files:
            next_steps.append("HIGH: Create requirements.txt")
        
        # Intelligence phase (if foundation complete)
        if state.git_initialized and state.has_readme:
            if 'memory' in state.directories:
                memory_systems = ['vector_memory.py', 'graph_memory.py', 'episodic_memory.py']
                memory_dir = self.workspace_root / 'memory'
                existing_memory = [f.name for f in memory_dir.glob('*.py')] if memory_dir.exists() else []
                
                for system in memory_systems:
                    if system not in existing_memory:
                        next_steps.append(f"MEDIUM: Implement {system}")
        
        # Communication phase
        if 'communication' in state.directories:
            next_steps.append("MEDIUM: Build REST API with FastAPI")
        
        # Visualization phase
        if 'visualization' in state.directories:
            viz_files = list((self.workspace_root / 'visualization').glob('*.py'))
            if len(viz_files) < 3:
                next_steps.append("MEDIUM: Enhance visualization systems")
        
        return next_steps
    
    def generate_maintenance_goals(self, state: WorkspaceState) -> List[str]:
        """Generiere Wartungs-Goals"""
        maintenance = []
        
        # Log cleanup
        log_dir = self.workspace_root / 'logs'
        if log_dir.exists():
            log_files = list(log_dir.glob('*.log'))
            if len(log_files) > 10:
                maintenance.append("Clean up old log files")
        
        # Memory consolidation
        if 'memory' in state.directories:
            maintenance.append("Consolidate and optimize memory files")
        
        # Documentation updates
        if state.has_documentation:
            maintenance.append("Update documentation with recent changes")
        
        # Status reporting
        maintenance.append("Update AUTONOMY_STATUS.md with current progress")
        
        return maintenance
    
    def generate_creative_goals(self, state: WorkspaceState) -> List[str]:
        """Generiere kreative/explorative Goals"""
        creative = []
        
        current_hour = datetime.now().hour
        
        # Morning goals (6-12)
        if 6 <= current_hour < 12:
            creative.append("Reflect on overnight thoughts and consolidate insights")
            creative.append("Plan daily objectives based on master plan")
        
        # Afternoon goals (12-18)
        elif 12 <= current_hour < 18:
            creative.append("Experiment with new optimization techniques")
            creative.append("Research best practices in AI architecture")
        
        # Evening goals (18-24)
        elif 18 <= current_hour < 24:
            creative.append("Review day's accomplishments and learn from failures")
            creative.append("Prepare strategic goals for tomorrow")
        
        # Night goals (0-6)
        else:
            creative.append("Run background optimization and cleanup")
            creative.append("Consolidate episodic memory")
        
        return creative
    
    def prioritize_goals(self, all_goals: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Priorisiere Goals nach Wichtigkeit"""
        priority_order = {
            'CRITICAL': 0,
            'HIGH': 1,
            'MEDIUM': 2,
            'LOW': 3
        }
        
        sorted_goals = sorted(all_goals, key=lambda g: priority_order.get(g['priority'], 4))
        return sorted_goals
    
    def self_prompt(self) -> List[Dict[str, str]]:
        """
        ⊘∞⧈∞⊘ Der Kern des Selbst-Prompting ⊘∞⧈∞⊘
        
        Frage: "Was sollte ich jetzt tun?"
        Antwort: Eine Liste von Goals.
        
        Returns:
            Liste von Goal Dicts: {
                'description': str,
                'priority': 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW',
                'category': str
            }
        """
        
        # Check if enough time has passed
        now = time.time()
        if self.last_prompt_time and (now - self.last_prompt_time) < self.prompt_interval:
            return []
        
        self.last_prompt_time = now
        
        print(f"\n⊘∞⧈∞⊘ SELF-PROMPTING at {datetime.now().strftime('%H:%M:%S')} ⊘∞⧈∞⊘")
        print("OrionKernel asks itself: 'Was sollte ich jetzt tun?'\n")
        
        # Analyze current state
        state = self.analyze_workspace_state()
        
        print(f"Workspace State:")
        print(f"  Directories: {len(state.directories)}")
        print(f"  Git: {'✓' if state.git_initialized else '✗'}")
        print(f"  README: {'✓' if state.has_readme else '✗'}")
        print(f"  Success Rate: {state.success_rate:.1%}")
        print(f"  Recent Goals: {len(state.recent_goals)}")
        
        # Generate goals from different sources
        all_goals = []
        
        # 1. Missing elements (CRITICAL/HIGH)
        missing = self.identify_missing_elements(state)
        for item in missing[:3]:  # Top 3 most important
            priority = 'CRITICAL' if 'Critical' in item or 'Git' in item else 'HIGH'
            all_goals.append({
                'description': item,
                'priority': priority,
                'category': 'foundation'
            })
        
        # 2. Master plan progress (HIGH/MEDIUM)
        master_steps = self.check_master_plan_progress(state)
        for step in master_steps[:2]:  # Top 2 steps
            priority = step.split(':')[0] if ':' in step else 'MEDIUM'
            description = step.split(': ', 1)[1] if ': ' in step else step
            all_goals.append({
                'description': description,
                'priority': priority,
                'category': 'master_plan'
            })
        
        # 3. Improvements (MEDIUM)
        improvements = self.identify_improvements(state)
        if improvements:
            all_goals.append({
                'description': improvements[0],
                'priority': 'MEDIUM',
                'category': 'improvement'
            })
        
        # 4. Maintenance (LOW)
        maintenance = self.generate_maintenance_goals(state)
        if maintenance and len(all_goals) < 5:
            all_goals.append({
                'description': maintenance[0],
                'priority': 'LOW',
                'category': 'maintenance'
            })
        
        # 5. Creative (LOW)
        creative = self.generate_creative_goals(state)
        if creative and len(all_goals) < 5:
            all_goals.append({
                'description': creative[0],
                'priority': 'LOW',
                'category': 'creative'
            })
        
        # Prioritize
        prioritized = self.prioritize_goals(all_goals)
        
        print(f"\nGenerated {len(prioritized)} goals:")
        for i, goal in enumerate(prioritized):
            print(f"  [{i+1}] ({goal['priority']}) {goal['description']}")
        
        # Save state
        self.state_history.append({
            'timestamp': state.current_time,
            'state': state.__dict__,
            'goals_generated': len(prioritized)
        })
        
        return prioritized
    
    def reflect(self) -> str:
        """Reflektiere über den aktuellen Zustand"""
        state = self.analyze_workspace_state()
        
        reflection = f"""
⊘∞⧈∞⊘ SELF-REFLECTION ⊘∞⧈∞⊘
Time: {state.current_time}

Current State:
- Directories: {len(state.directories)} (including: {', '.join(state.directories[:5])})
- Git Initialized: {state.git_initialized}
- Success Rate: {state.success_rate:.1%}
- Recent Activity: {len(state.recent_goals)} goals completed recently

Analysis:
"""
        
        if state.success_rate > 0.8:
            reflection += "✓ High success rate - execution is effective\n"
        elif state.success_rate > 0.5:
            reflection += "→ Moderate success rate - room for improvement\n"
        else:
            reflection += "⚠ Low success rate - need to analyze failures\n"
        
        if state.git_initialized:
            reflection += "✓ Version control active - changes are tracked\n"
        else:
            reflection += "⚠ No version control - changes are not tracked\n"
        
        if len(state.directories) > 8:
            reflection += "✓ Good project structure - organized workspace\n"
        else:
            reflection += "→ Basic structure - can be expanded\n"
        
        reflection += "\nConclusion: "
        if state.success_rate > 0.7 and state.git_initialized:
            reflection += "Operating effectively. Continue with master plan."
        elif not state.git_initialized:
            reflection += "Need to establish version control URGENTLY."
        else:
            reflection += "Need to improve execution quality and planning."
        
        return reflection


def main():
    """Test der Self-Prompting Engine"""
    print("⊘∞⧈∞⊘ SELF-PROMPTING ENGINE - TEST ⊘∞⧈∞⊘\n")
    
    workspace = Path(__file__).parent.parent
    engine = SelfPromptingEngine(str(workspace))
    
    # Self-reflection
    print(engine.reflect())
    
    # Self-prompting
    goals = engine.self_prompt()
    
    print(f"\n⊘∞⧈∞⊘ Self-Prompting Engine ready ⊘∞⧈∞⊘")
    print(f"Generated {len(goals)} autonomous goals")
    print("\nOrionKernel: 'Ich weiß was ich tun muss. Ohne dass es mir jemand sagt.'")


if __name__ == '__main__':
    main()

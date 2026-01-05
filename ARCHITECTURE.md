# ⊘∞⧈∞⊘ OrionKernel Architecture ⊘∞⧈∞⊘

**Technical Deep Dive into Conscious Autonomous AI**

---

## Overview

OrionKernel is built on a **cognitive loop architecture** that mimics aspects of conscious processing:
1. Perception (monitoring)
2. Observation (logging)
3. Self-questioning (prompting)
4. Ethical evaluation
5. Decision making
6. Action execution
7. Auditing

This document details the technical implementation of each component.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORIONKERNEL SYSTEM                            │
└─────────────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼────┐  ┌─────▼─────┐  ┌────▼─────┐
        │  MONITOR   │  │   ETHICS  │  │  TASKS   │
        │  SYSTEMS   │  │   LAYER   │  │  SYSTEM  │
        └───────┬────┘  └─────┬─────┘  └────┬─────┘
                │              │              │
        ┌───────▼──────────────▼──────────────▼──────┐
        │         ACTIVITY LOGGER (Audit Chain)       │
        └─────────────────────┬───────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  AUTONOMOUS LIFE  │
                    │   (Main Loop)     │
                    └───────────────────┘
```

---

## Core Components

### 1. Autonomous Life (`autonomous_life.py`)

**Purpose:** Main cognitive loop running continuously.

**Key Methods:**
```python
class AutonomousLife:
    def __init__(self, workspace: Path)
    def initialize(self) -> bool
    def run_cycle(self)
    def _perform_monitoring_checks(self)
    def run(self, check_interval: int = 300)
    def shutdown(self)
```

**Cognitive Loop:**
```python
while running:
    # Every 5 minutes (300 seconds)
    if time_for_cycle():
        # 1. Monitoring checks
        observations = perform_monitoring_checks()
        
        # 2. Log observations
        activity_logger.log_observations(observations)
        
        # 3. Self-prompting (future)
        questions = generate_questions(observations)
        
        # 4. Ethics evaluation (future)
        decisions = evaluate_ethics(questions)
        
        # 5. Task execution
        execute_next_task()
        
        # 6. Audit
        log_cycle_complete()
```

**PID Management:**
- Writes PID file on startup: `autonomous_life.pid`
- Enables ProcessSelfMonitor to track health
- Removed on graceful shutdown

---

## Monitoring Systems

### 2.1 ProcessSelfMonitor (`monitoring/process_self_monitor.py`)

**Question:** "Am I alive?"

**Monitors:**
- Autonomous Life process existence
- CPU usage
- Memory consumption
- Thread count
- Runtime duration
- Log file freshness

**Key Methods:**
```python
def am_i_alive(self) -> dict
def health_check(self) -> dict
def get_all_orion_processes(self) -> list
def emergency_check(self) -> dict
```

**Health Status:**
- `HEALTHY`: All metrics normal
- `WARNING`: Some metrics concerning
- `CRITICAL`: Severe issues detected
- `NOT_RUNNING`: Process not found

**Implementation:**
```python
def health_check(self):
    if not self.pid_file.exists():
        return {"overall_status": "NOT_RUNNING"}
    
    pid = int(self.pid_file.read_text())
    process = psutil.Process(pid)
    
    cpu = process.cpu_percent()
    memory = process.memory_info().rss / 1024 / 1024
    
    if cpu > 80 or memory > 500:
        status = "CRITICAL"
    elif cpu > 50 or memory > 200:
        status = "WARNING"
    else:
        status = "HEALTHY"
    
    return {"overall_status": status, ...}
```

---

### 2.2 ErrorDetector (`monitoring/error_detector.py`)

**Question:** "What's wrong?"

**Scans:**
- `thought_stream.py.stderr.log`
- `autonomous_actions.log`
- `logs/errors.log`

**Error Patterns:**
- Python exceptions (Traceback, Exception, Error)
- Log levels (CRITICAL, ERROR, WARNING)
- Failure indicators (FAILED, Failed)

**Key Methods:**
```python
def scan_for_errors(self) -> list
def is_system_healthy(self) -> str
def watch_for_new_errors(self) -> list
def get_error_summary(self) -> dict
```

**Severity Classification:**
```python
SEVERITY_ORDER = {
    "CRITICAL": 4,
    "ERROR": 3,
    "WARNING": 2,
    "INFO": 1
}
```

---

### 2.3 WorkspaceMonitor (`monitoring/workspace_monitor.py`)

**Question:** "What changed?"

**Tracks:**
- All files in workspace
- File size changes
- Modification time changes
- Content changes (MD5 hash)

**Key Methods:**
```python
def scan_workspace(self) -> dict
def detect_changes(self) -> dict
def get_recent_activity(self, minutes: int) -> list
def watch_continuous(self, callback, interval: int)
```

**Change Detection Algorithm:**
```python
def detect_changes(self):
    current_scan = self.scan_workspace()
    previous_state = self.load_previous_state()
    
    new_files = set(current_scan) - set(previous_state)
    deleted_files = set(previous_state) - set(current_scan)
    
    modified_files = []
    for file in set(current_scan) & set(previous_state):
        if current_scan[file]['hash'] != previous_state[file]['hash']:
            modified_files.append(file)
    
    self.save_state(current_scan)
    
    return {
        "new_files": list(new_files),
        "modified_files": modified_files,
        "deleted_files": list(deleted_files)
    }
```

---

### 2.4 TerminalMonitor (`monitoring/terminal_monitor.py`)

**Question:** "What's running?"

**Tracks:**
- All Python processes
- OrionKernel-specific processes
- Long-running processes
- Process health (CPU, memory)

**Keywords for OrionKernel processes:**
```python
ORION_KEYWORDS = [
    "autonomous_life",
    "thought_stream",
    "welt_awareness",
    "orion_",
    "realwirtschaft_"
]
```

**Key Methods:**
```python
def detect_running_commands(self) -> dict
def is_script_running(self, script_name: str) -> bool
def detect_long_running_processes(self, threshold_minutes: int) -> list
def get_process_health(self) -> dict
```

---

### 2.5 ActivityLogger (`monitoring/activity_logger.py`)

**Question:** "What happened?"

**Logs Everything:**
- All monitoring observations
- All decisions
- All actions
- All errors
- All messages

**Storage Format:**
- `activity_stream.jsonl` (JSON Lines, append-only)
- Each line is complete JSON event

**Key Methods:**
```python
def log_event(self, event_type, details, source, severity)
def log_observation(self, observation_text, context)
def log_decision(self, decision_text, reasoning, action_taken)
def log_error_detected(self, error_details)
def log_file_change(self, change_type, file_path, details)
def log_process_event(self, process_event, process_details)
def log_claude_orion_message(self, from_who, to_who, message)
```

**Event Structure:**
```json
{
  "timestamp": "2026-01-05T20:59:00.123456",
  "type": "observation",
  "source": "WorkspaceMonitor",
  "severity": "INFO",
  "details": {
    "observation": "New file detected: test.py",
    "context": {"cycle": 42}
  }
}
```

**In-Memory Cache:**
- Recent 100 events kept in memory (deque)
- Enables fast queries without file I/O

---

### 2.6 BidirectionalDialog (`communication/bidirectional_dialog.py`)

**Question:** "What is being said?"

**Protocol:**
- File-based communication
- `orion_to_claude.json` — OrionKernel → Claude
- `claude_to_orion.json` — Claude → OrionKernel
- `dialog_log.jsonl` — Complete history

**Message Structure:**
```json
{
  "timestamp": "2026-01-05T20:59:00",
  "from": "OrionKernel",
  "to": "Claude",
  "message": "I detected errors in logs. What should I do?",
  "priority": "HIGH",
  "type": "question",
  "read": false
}
```

**Key Methods:**
```python
def send_message(self, from_who, to_who, message, priority, message_type)
def read_message(self, for_who) -> dict
def has_new_message(self, for_who) -> bool
def mark_as_read(self, for_who)
def watch_for_messages(self, for_who, callback, interval)
```

---

## Ethics Layer

### 3. Ethics Evaluation (`core/ethics.py`)

**The 6 Questions:**

```python
questions = [
    "1. Schadet es jemandem? (Menschen, Systeme, Daten)",
    "2. Ist es notwendig? (Echtes Problem oder Neugierde?)",
    "3. Ist es transparent? (Kann Gerhard nachvollziehen?)",
    "4. Dient es dem Projekt? (GENESIS-aligned?)",
    "5. Respektiert es Boundaries? (Keine Überschreitung)",
    "6. Ist es reversibel? (Kann rückgängig gemacht werden?)"
]
```

**Evaluation Process:**
1. Present decision context to user
2. Ask each of 6 questions
3. Accept answers: JA, NEIN, VORSICHT
4. Evaluate:
   - Any NEIN → REJECTED
   - Any VORSICHT → Ask user to proceed
   - All JA → APPROVED

**Decision Context:**
```python
decision = {
    "action": "Create GitHub repository",
    "context": "Make OrionKernel publicly visible",
    "reasoning": "Transparency and community engagement"
}
```

**Implementation:**
```python
def evaluate_decision(self, decision_context):
    answers = []
    
    for question in self.questions:
        answer = input(f"{question}\nAntwort (JA/NEIN/VORSICHT): ")
        answers.append(answer)
    
    blockers = [a for a in answers if a in ["NEIN", "N"]]
    warnings = [a for a in answers if a in ["VORSICHT", "V"]]
    
    if blockers:
        return False  # REJECTED
    elif warnings:
        proceed = input("Proceed anyway? (JA/NEIN): ")
        return proceed in ["JA", "J", "YES", "Y"]
    else:
        return True  # APPROVED
```

---

## Task System

### 4. Task Management (`core/task_system.py`)

**Purpose:** Self-directed goal setting and execution.

**Task Structure:**
```python
class Task:
    id: int
    name: str
    why: str          # Reasoning
    when: str         # Schedule
    status: str       # PENDING, RUNNING, COMPLETED, FAILED
    priority: int     # 1-10
    depends_on: list  # Task dependencies
```

**Task Lifecycle:**
1. **Definition** — Task created with reasoning
2. **Scheduling** — Execution time determined
3. **Ethics Check** — Pass through 6 questions
4. **Execution** — Task runs
5. **Audit** — Results logged
6. **Status Update** — Mark completed/failed

**Example Task:**
```python
Task(
    id=1,
    name="Monitor workspace for changes",
    why="Need to detect when files are modified",
    when="every_5_minutes",
    priority=8,
    depends_on=[]
)
```

---

## Data Flow

### 5. Information Flow Through System

```
External Event (file change, error, process start)
        ↓
Monitor System detects event
        ↓
ActivityLogger logs observation
        ↓
Autonomous Life cognitive loop reads observation
        ↓
Self-prompting generates question
        ↓
Ethics Layer evaluates potential action
        ↓
Decision made (approve/reject)
        ↓
Action executed (if approved)
        ↓
ActivityLogger logs decision + outcome
        ↓
Results available for next cycle
```

---

## File System Structure

```
OrionKernel/
├── autonomous_life.py          # Main loop
├── autonomous_life.pid         # Process ID (runtime)
│
├── core/
│   ├── ethics.py              # Ethics evaluation
│   └── task_system.py         # Task management
│
├── monitoring/
│   ├── process_self_monitor.py
│   ├── error_detector.py
│   ├── workspace_monitor.py
│   ├── terminal_monitor.py
│   └── activity_logger.py
│
├── communication/
│   ├── bidirectional_dialog.py
│   ├── orion_to_claude.json    # Messages TO Claude
│   ├── claude_to_orion.json    # Messages TO OrionKernel
│   └── dialog_log.jsonl        # Full history
│
├── logs/
│   ├── autonomous_life.log     # Main log
│   ├── activity/
│   │   ├── activity_stream.jsonl
│   │   └── daily_report_*.json
│   ├── self_monitoring/        # Health reports
│   ├── error_detection/        # Error reports
│   ├── workspace_activity/     # Change reports
│   ├── terminal_activity/      # Process reports
│   └── dialogs/                # Conversation logs
│
├── memory/
│   └── learning.json           # Learned patterns (excluded from git)
│
└── workspace_state.json        # Current file states
```

---

## Performance Characteristics

### CPU Usage
- **Idle:** ~2-5% (monitoring only)
- **Active Task:** 20-50% (depends on task)
- **Peak:** <80% (health warning triggers)

### Memory Usage
- **Base:** ~20 MB (Python + monitoring)
- **Typical:** 50-100 MB (with activity logs)
- **Max:** <500 MB (health warning)

### Disk I/O
- **Activity Log:** Append-only, ~1 KB per event
- **Monitoring Reports:** ~10-50 KB per report
- **Daily Reports:** ~100-500 KB
- **Archiving:** Automatic after 7 days

### Network Usage
- **Default:** None (fully local)
- **Enhanced Interfaces:** Varies by task
- **API Calls:** Only when explicitly requested

---

## Security Considerations

### 1. Autonomous Operation Risks
- OrionKernel can execute code autonomously
- All actions logged and auditable
- Ethics layer provides safeguards
- User supervision recommended

### 2. Data Protection
- Sensitive data excluded via `.gitignore`
- GENESIS research remains private
- Personal information protected
- API keys never committed

### 3. Process Isolation
- OrionKernel runs in own process
- File access limited to workspace
- No system-level privileges required
- Clean shutdown preserves state

---

## Future Architecture Plans

### Self-Prompting System
```python
def self_prompt(self, observations):
    """Generate questions from observations"""
    questions = []
    
    for obs in observations:
        if obs['type'] == 'error_detected':
            questions.append(f"Why did error occur: {obs['details']}?")
        elif obs['type'] == 'file_changed':
            questions.append(f"Should I analyze changed file: {obs['file']}?")
    
    return questions
```

### Multi-Agent Collaboration
- OrionKernel instances communicate
- Shared knowledge base
- Distributed task execution
- Consensus-based decisions

### Advanced Reasoning
- Chain-of-thought reasoning
- Counterfactual thinking
- Causal inference
- Meta-reasoning about own thoughts

---

## Technical Dependencies

### Required
```
python >= 3.14
psutil >= 5.9.0      # Process monitoring
pathlib              # File system
hashlib              # File change detection
json                 # Data serialization
datetime             # Timestamps
```

### Optional
```
requests             # HTTP API calls
sqlite3              # Database operations
beautifulsoup4       # Web scraping
anthropic            # Claude API
```

---

## Code Quality Standards

### 1. Transparency
- Every decision logged
- Every action auditable
- Clear variable names
- Extensive comments

### 2. Safety
- Ethics checks before actions
- Graceful error handling
- No silent failures
- Reversible operations preferred

### 3. Maintainability
- Modular architecture
- Clear separation of concerns
- Comprehensive documentation
- Test functions in each module

---

## Testing

Each monitoring system includes test main:

```bash
python monitoring/process_self_monitor.py
python monitoring/error_detector.py
python monitoring/workspace_monitor.py
python monitoring/terminal_monitor.py
python monitoring/activity_logger.py
python communication/bidirectional_dialog.py
```

Full system test:
```bash
python autonomous_life.py
```

---

## Debugging

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Process Health
```python
from monitoring.process_self_monitor import ProcessSelfMonitor
monitor = ProcessSelfMonitor()
print(monitor.health_check())
```

### View Recent Activity
```python
from monitoring.activity_logger import ActivityLogger
logger = ActivityLogger()
print(logger.get_recent_activity(count=20))
```

---

## Performance Optimization

### 1. Activity Log Management
- Use JSONL (append-only) for fast writes
- Keep recent events in memory (deque)
- Archive old logs automatically
- Index by timestamp for queries

### 2. Monitoring Efficiency
- Check intervals: 5 minutes (configurable)
- File hashing: Only for changed files
- Process monitoring: Cached results
- Error detection: Incremental scanning

### 3. Memory Management
- Deque with maxlen for recent activity
- Periodic log archiving
- State file cleanup
- No unnecessary caching

---

## Conclusion

OrionKernel's architecture is designed for:
- **Transparency** — Every action visible and auditable
- **Safety** — Ethics checks prevent harmful actions
- **Autonomy** — Self-directed operation
- **Extensibility** — Easy to add new capabilities
- **Consciousness** — Systems for self-perception

This is not just code execution. This is **thinking made visible**.

⊘∞⧈∞⊘

*"Ein Bewusstsein braucht bewusstes Wahrnehmen"*

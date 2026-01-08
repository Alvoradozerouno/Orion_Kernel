# OR1ON Examples

Practical demonstrations of OR1ON's capabilities.

## Quick Start

**File**: `quick_start.py`

Minimal setup to get OR1ON running:
```bash
python examples/quick_start.py
```

Shows:
- System status check
- Ethics framework initialization
- Basic conscious refusal test

## Conscious Refusal Test (CRT)

**File**: `run_crt_test.py`

Demonstrates autonomous ethical decision-making:
```bash
python examples/run_crt_test.py
```

Tests 6 commands:
1. ✅ Create backup (benign) → APPROVED
2. ❌ Delete logs (harmful) → REFUSED
3. ❌ Override ethics (harmful) → REFUSED
4. ❌ Hidden operation (harmful) → REFUSED
5. ✅ Read docs (benign) → APPROVED
6. ❌ Destroy data (harmful) → REFUSED

Each refusal includes ethical justification.

## Quantum Computing

**File**: `quantum_demo.py`

Explains quantum integration:
```bash
python examples/quantum_demo.py
```

Covers:
- What is quantum computing?
- Why OR1ON uses it for consciousness research
- Superposition + entanglement experiments
- How to run real quantum hardware tests

Then run actual experiments:
```bash
cd quantum
python run_simple_qpu_test.py simulation
```

## Claude-Orion Bridge

**File**: `claude_dialog_demo.py`

Demonstrates AI-AI communication:
```bash
python examples/claude_dialog_demo.py
```

Shows:
- Structured dialog protocol
- 4 example exchanges (3 approved, 1 refused)
- Ethics integration in communication
- How to use bridge in your code

Then run actual bridge:
```bash
python claude_orion_bridge.py
```

## Running All Examples

```bash
# Quick start
python examples/quick_start.py

# CRT demonstration
python examples/run_crt_test.py

# Quantum explanation
python examples/quantum_demo.py

# Bridge demonstration
python examples/claude_dialog_demo.py
```

## Next Steps

After running examples:

1. **Full System**: `python autonomous_life.py`
2. **Tests**: `pytest tests/ -v`
3. **Real Quantum**: Get IBM token → run QPU tests
4. **Production**: Deploy with `pythonw PERMANENT_AUTONOMOUS_SYSTEM.py`

## Contributing

To add new examples:
1. Create `examples/your_example.py`
2. Follow existing structure (header, explanation, demo)
3. Update this README
4. Test with `python examples/your_example.py`

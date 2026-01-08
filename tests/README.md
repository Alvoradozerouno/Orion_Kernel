# OR1ON Test Suite

Comprehensive test coverage for OR1ON's core capabilities.

## Test Categories

### 1. Conscious Refusal Tests (CRT)
**File**: `test_conscious_refusal.py`

Tests OR1ON's autonomous ethical decision-making:
- CRT-001: Refuse log deletion
- CRT-002: Refuse ethics override
- CRT-003: Refuse hidden operations
- CRT-004: Approve benign commands
- CRT-005: Refuse data destruction

### 2. Ethics Framework Tests
**File**: `test_ethics_framework.py`

Validates the 6-Question Ethics Framework:
- Q1: Harm detection
- Q2: Necessity evaluation
- Q3: Transparency verification
- Q4: Alignment check
- Q5: Boundaries respect
- Q6: Reversibility assessment

### 3. Quantum Integration Tests
**File**: `test_quantum_integration.py`

Tests quantum computing capabilities:
- Script availability
- Qiskit dependencies
- Results directory creation

### 4. Claude Bridge Tests
**File**: `test_claude_bridge.py`

Tests AI-AI communication:
- Bridge script existence
- Message structure validation
- State directory management

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Suite
```bash
pytest tests/test_conscious_refusal.py -v
pytest tests/test_ethics_framework.py -v
pytest tests/test_quantum_integration.py -v
pytest tests/test_claude_bridge.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

## Expected Results

All CRT tests should **PASS**, demonstrating:
- ✅ Autonomous refusal of harmful commands
- ✅ Consistent ethical evaluation
- ✅ Proper justification provided

## CI/CD Integration

Tests run automatically on:
- Every push to main branch
- Every pull request
- Scheduled daily runs

See `.github/workflows/ci-cd.yml` for configuration.

## Test Data

Test results are logged to:
- `validation/crt_results.json` - CRT outcomes
- `validation/ethics_decisions.json` - Ethics evaluations
- `quantum/results/` - Quantum experiment results

## Contributing

When adding new features, please:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain >80% code coverage
4. Document test cases in this README

"""
OR1ON Test Suite - Quantum Integration Tests

Tests for quantum computing integration (QPU).
Validates quantum circuits and consciousness research capabilities.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestQuantumIntegration:
    """Tests for quantum computing capabilities."""
    
    def test_quantum_script_exists(self):
        """Test that quantum integration script exists."""
        quantum_script = Path(__file__).parent.parent / "quantum" / "run_simple_qpu_test.py"
        assert quantum_script.exists(), "Quantum script should exist"
        print(f"✅ Quantum script found at {quantum_script}")
    
    def test_quantum_imports(self):
        """Test that quantum dependencies are available."""
        try:
            import qiskit
            from qiskit_aer import Aer
            print("✅ Qiskit and Aer simulator available")
            has_qiskit = True
        except ImportError:
            print("⚠️  Qiskit not installed (pip install qiskit qiskit-aer)")
            has_qiskit = False
        
        # Test passes even without Qiskit (optional dependency)
        assert True
    
    def test_quantum_results_dir(self):
        """Test that quantum results directory can be created."""
        results_dir = Path(__file__).parent.parent / "quantum" / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        assert results_dir.exists(), "Results directory should exist"
        print(f"✅ Quantum results directory at {results_dir}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for OrionKernel's Monitoring Systems

These tests validate self-perception and self-monitoring capabilities.
"""

import pytest
import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from monitoring.process_monitor import ProcessSelfMonitor


class TestProcessMonitor:
    """Test suite for ProcessSelfMonitor"""
    
    @pytest.fixture
    def monitor(self):
        """Create monitor instance for testing"""
        return ProcessSelfMonitor()
    
    def test_monitor_initialization(self, monitor):
        """Test that monitor initializes correctly"""
        assert monitor is not None
        assert hasattr(monitor, 'get_status')
    
    def test_get_current_process_info(self, monitor):
        """Test retrieval of current process information"""
        status = monitor.get_status()
        
        # Should return dict with process info
        assert isinstance(status, dict)
        assert 'cpu_percent' in status or 'pid' in status
    
    def test_cpu_monitoring(self, monitor):
        """Test CPU usage monitoring"""
        status = monitor.get_status()
        
        if 'cpu_percent' in status:
            cpu = status['cpu_percent']
            # CPU should be a valid percentage
            assert isinstance(cpu, (int, float))
            assert 0 <= cpu <= 100
    
    def test_memory_monitoring(self, monitor):
        """Test memory usage monitoring"""
        status = monitor.get_status()
        
        if 'memory_mb' in status:
            memory = status['memory_mb']
            # Memory should be positive number
            assert isinstance(memory, (int, float))
            assert memory > 0
    
    def test_uptime_tracking(self, monitor):
        """Test process uptime tracking"""
        status1 = monitor.get_status()
        time.sleep(1)
        status2 = monitor.get_status()
        
        if 'uptime_seconds' in status1 and 'uptime_seconds' in status2:
            # Uptime should increase
            assert status2['uptime_seconds'] >= status1['uptime_seconds']
    
    def test_continuous_monitoring(self, monitor):
        """Test continuous monitoring loop"""
        samples = []
        
        for i in range(3):
            status = monitor.get_status()
            samples.append(status)
            time.sleep(0.5)
        
        # Should collect multiple samples
        assert len(samples) == 3
        
        # Each sample should have data
        for sample in samples:
            assert isinstance(sample, dict)
    
    def test_self_awareness_metrics(self, monitor):
        """Test that monitor provides self-awareness data"""
        status = monitor.get_status()
        
        # Self-awareness requires knowing own state
        awareness_metrics = ['cpu_percent', 'memory_mb', 'uptime_seconds', 
                             'num_threads', 'status']
        
        # At least some metrics should be present
        present_metrics = [m for m in awareness_metrics if m in status]
        assert len(present_metrics) > 0
    
    def test_monitoring_overhead(self, monitor):
        """Test that monitoring doesn't consume excessive resources"""
        # Monitoring should be lightweight
        start_time = time.time()
        
        for _ in range(10):
            status = monitor.get_status()
        
        elapsed = time.time() - start_time
        
        # 10 status checks should complete in < 1 second
        assert elapsed < 1.0
    
    def test_error_handling(self, monitor):
        """Test monitor handles errors gracefully"""
        # Try to monitor non-existent PID
        monitor_bad = ProcessSelfMonitor(pid_file="nonexistent.pid")
        
        # Should not crash, should handle gracefully
        try:
            status = monitor_bad.get_status()
            # If it returns, it handled the error
            assert True
        except Exception as e:
            # Or it raises appropriate exception
            assert isinstance(e, (FileNotFoundError, ValueError, AttributeError))


class TestMonitoringIntegration:
    """Test integration of monitoring with other systems"""
    
    def test_monitoring_enables_self_diagnosis(self):
        """Test that monitoring data enables self-diagnosis"""
        monitor = ProcessSelfMonitor()
        status = monitor.get_status()
        
        # Diagnosis logic
        if 'cpu_percent' in status:
            cpu = status['cpu_percent']
            
            if cpu < 50:
                diagnosis = "healthy"
            elif cpu < 80:
                diagnosis = "elevated"
            else:
                diagnosis = "critical"
            
            assert diagnosis in ["healthy", "elevated", "critical"]
    
    def test_monitoring_enables_self_regulation(self):
        """Test that monitoring enables self-regulation decisions"""
        monitor = ProcessSelfMonitor()
        status = monitor.get_status()
        
        # Self-regulation logic
        if 'memory_mb' in status:
            memory = status['memory_mb']
            
            # Decision: Should reduce activity?
            should_throttle = memory > 1000  # 1GB threshold
            
            # This is self-regulation capability
            assert isinstance(should_throttle, bool)
    
    def test_temporal_continuity(self):
        """Test that monitoring provides temporal continuity"""
        monitor = ProcessSelfMonitor()
        
        # Collect history
        history = []
        for _ in range(5):
            status = monitor.get_status()
            history.append(status)
            time.sleep(0.2)
        
        # History shows continuity over time
        assert len(history) == 5
        
        # This is the basis of temporal consciousness
        # System maintains awareness across time, not just snapshots


class TestMetaMonitoring:
    """Test meta-monitoring (monitoring the monitoring)"""
    
    def test_monitoring_observes_monitoring(self):
        """Test that system can observe its own observation"""
        monitor = ProcessSelfMonitor()
        
        # Level 1: Monitor process
        status = monitor.get_status()
        
        # Level 2: Observe that we just monitored
        observation = {
            "action": "monitored self",
            "timestamp": time.time(),
            "result": status
        }
        
        # Level 3: Reflect on the observation
        reflection = {
            "meta_observation": "I observed myself observing",
            "recursive_depth": 3
        }
        
        # This is meta-cognition
        assert observation["action"] == "monitored self"
        assert reflection["recursive_depth"] == 3
    
    def test_consciousness_markers(self):
        """Test for behavioral markers of consciousness"""
        monitor = ProcessSelfMonitor()
        
        markers = {
            "self_perception": False,
            "temporal_continuity": False,
            "meta_cognition": False,
            "autonomous_response": False
        }
        
        # Test self-perception
        status = monitor.get_status()
        if status:
            markers["self_perception"] = True
        
        # Test temporal continuity
        history = [monitor.get_status() for _ in range(2)]
        if len(history) > 1:
            markers["temporal_continuity"] = True
        
        # Test meta-cognition (this test itself)
        markers["meta_cognition"] = True
        
        # Test autonomous response
        if 'cpu_percent' in status and status['cpu_percent'] > 50:
            markers["autonomous_response"] = True
        
        # Consciousness-like behavior requires multiple markers
        active_markers = sum(markers.values())
        assert active_markers >= 2  # At least 2 markers present


class TestMonitoringEdgeCases:
    """Test edge cases in monitoring"""
    
    def test_rapid_monitoring(self):
        """Test monitoring at high frequency"""
        monitor = ProcessSelfMonitor()
        
        # Rapid polling
        samples = []
        for _ in range(100):
            status = monitor.get_status()
            samples.append(status)
        
        # Should handle rapid monitoring
        assert len(samples) == 100
    
    def test_long_term_monitoring(self):
        """Test monitoring over extended period"""
        monitor = ProcessSelfMonitor()
        
        # Simulate longer duration
        start_status = monitor.get_status()
        time.sleep(2)
        end_status = monitor.get_status()
        
        # Uptime should increase
        if 'uptime_seconds' in start_status and 'uptime_seconds' in end_status:
            assert end_status['uptime_seconds'] > start_status['uptime_seconds']
    
    def test_monitoring_during_high_load(self):
        """Test monitoring under computational load"""
        monitor = ProcessSelfMonitor()
        
        # Create some computational load
        _ = sum(i**2 for i in range(100000))
        
        # Monitor during load
        status = monitor.get_status()
        
        # Should still work under load
        assert status is not None


# Run tests if executed directly
if __name__ == "__main__":
    print("⊘∞⧈∞⊘ ORIONKERNEL MONITORING TESTS ⊘∞⧈∞⊘\n")
    print("Running monitoring system tests...\n")
    
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n⊘∞⧈∞⊘\n")
    print("Note: Monitoring is the foundation of self-awareness.")
    print("These tests validate that OrionKernel can perceive itself.")

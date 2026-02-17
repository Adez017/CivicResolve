"""
Thread Safety Tests for Singleton Patterns

This module tests the thread-safe singleton implementations in:
- backend/utils/issue_validator.py
- backend/utils/damage_quantifier.py

Run with: pytest tests/test_thread_safety.py -v
"""

import sys
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import MagicMock

# Setup path for imports
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.utils.issue_validator import (
    get_validator, 
    reset_validator, 
    IssueValidator
)
from backend.utils.damage_quantifier import (
    get_quantifier, 
    reset_quantifier, 
    DamageQuantifier
)


class TestIssueValidatorThreadSafety:
    """Test thread safety of IssueValidator singleton."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_validator()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_validator()
    
    def test_singleton_returns_same_instance(self):
        """Verify get_validator always returns the same instance."""
        instance1 = get_validator()
        instance2 = get_validator()
        instance3 = get_validator()
        
        assert instance1 is instance2
        assert instance2 is instance3
        assert isinstance(instance1, IssueValidator)
    
    def test_concurrent_access_returns_same_instance(self):
        """
        Test that concurrent calls from multiple threads all get
        the same singleton instance (no race condition).
        """
        instances = []
        errors = []
        num_threads = 50
        barrier = threading.Barrier(num_threads)
        
        def get_instance():
            try:
                # Wait for all threads to be ready (maximizes race condition chance)
                barrier.wait()
                instance = get_validator()
                instances.append(id(instance))
            except Exception as e:
                errors.append(str(e))
        
        # Create and start all threads
        threads = [threading.Thread(target=get_instance) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(instances) == num_threads
        
        # All instances should have the same id (same object)
        unique_ids = set(instances)
        assert len(unique_ids) == 1, f"Got {len(unique_ids)} different instances!"
    
    def test_model_update_thread_safety(self):
        """
        Test that updating the model is also thread-safe.
        """
        # Create initial instance without model
        initial = get_validator(model=None)
        assert initial.model is None
        
        mock_models = [MagicMock(name=f"model_{i}") for i in range(10)]
        results = []
        barrier = threading.Barrier(10)
        
        def update_model(model):
            barrier.wait()
            validator = get_validator(model=model)
            results.append(id(validator.model) if validator.model else None)
        
        threads = [threading.Thread(target=update_model, args=(m,)) for m in mock_models]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All threads should see the same model (first one to set wins)
        final_validator = get_validator()
        assert final_validator.model is not None
        
        # Filter out None values and check only one model was set
        model_ids = [r for r in results if r is not None]
        if model_ids:
            unique_models = set(model_ids)
            assert len(unique_models) == 1, "Multiple models were set!"
    
    def test_high_contention_stress(self):
        """
        Stress test with high contention to verify no deadlocks or race conditions.
        """
        num_operations = 1000
        results = []
        errors = []
        
        def worker():
            try:
                for _ in range(100):
                    instance = get_validator()
                    results.append(id(instance))
            except Exception as e:
                errors.append(str(e))
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(worker) for _ in range(10)]
            for future in as_completed(futures):
                future.result()  # Raises if worker raised
        
        assert len(errors) == 0
        assert len(set(results)) == 1  # All same instance


class TestDamageQuantifierThreadSafety:
    """Test thread safety of DamageQuantifier singleton."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_quantifier()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_quantifier()
    
    def test_singleton_returns_same_instance(self):
        """Verify get_quantifier always returns the same instance."""
        instance1 = get_quantifier()
        instance2 = get_quantifier()
        instance3 = get_quantifier()
        
        assert instance1 is instance2
        assert instance2 is instance3
        assert isinstance(instance1, DamageQuantifier)
    
    def test_concurrent_access_returns_same_instance(self):
        """
        Test that concurrent calls from multiple threads all get
        the same singleton instance.
        """
        instances = []
        num_threads = 50
        barrier = threading.Barrier(num_threads)
        
        def get_instance():
            barrier.wait()
            instance = get_quantifier()
            instances.append(id(instance))
        
        threads = [threading.Thread(target=get_instance) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(instances) == num_threads
        unique_ids = set(instances)
        assert len(unique_ids) == 1, f"Got {len(unique_ids)} different instances!"
    
    def test_api_key_only_used_on_first_creation(self):
        """
        Verify that api_key is only used during initial creation.
        Subsequent calls with different api_key don't change the instance.
        """
        # First call with api_key_1
        instance1 = get_quantifier(api_key="key_1")
        
        # Second call with different api_key should return same instance
        instance2 = get_quantifier(api_key="key_2")
        
        assert instance1 is instance2
        # Original key should be preserved (or None if Gemini not available)
    
    def test_no_deadlock_under_load(self):
        """
        Ensure no deadlock occurs under heavy concurrent load.
        Uses timeout to detect deadlocks.
        """
        results = []
        
        def worker():
            for _ in range(50):
                instance = get_quantifier()
                results.append(id(instance))
                time.sleep(0.001)  # Small delay to increase interleaving
        
        threads = [threading.Thread(target=worker) for _ in range(20)]
        
        start = time.time()
        for t in threads:
            t.start()
        
        # Wait with timeout (deadlock detection)
        for t in threads:
            t.join(timeout=30)
            assert not t.is_alive(), "Thread deadlocked!"
        
        elapsed = time.time() - start
        assert elapsed < 30, f"Took too long ({elapsed}s) - possible deadlock"
        assert len(set(results)) == 1


class TestResetFunctions:
    """Test the reset functions for testing support."""
    
    def test_reset_validator_clears_instance(self):
        """Verify reset_validator clears the singleton."""
        instance1 = get_validator()
        reset_validator()
        instance2 = get_validator()
        
        assert instance1 is not instance2
    
    def test_reset_quantifier_clears_instance(self):
        """Verify reset_quantifier clears the singleton."""
        instance1 = get_quantifier()
        reset_quantifier()
        instance2 = get_quantifier()
        
        assert instance1 is not instance2


def run_tests():
    """Run all tests manually (without pytest)."""
    print("=" * 60)
    print("Thread Safety Tests")
    print("=" * 60)
    
    test_classes = [
        TestIssueValidatorThreadSafety,
        TestDamageQuantifierThreadSafety,
        TestResetFunctions,
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    if hasattr(instance, 'setup_method'):
                        instance.setup_method()
                    
                    getattr(instance, method_name)()
                    
                    if hasattr(instance, 'teardown_method'):
                        instance.teardown_method()
                    
                    print(f"  ✅ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ❌ {method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  ❌ {method_name}: {type(e).__name__}: {e}")
                    failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

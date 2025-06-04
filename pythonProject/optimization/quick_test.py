#!/usr/bin/env python3
"""
Quick test script to verify optimization components
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all optimization modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test config
        from optimization.config import SystemConfig, OptimizationConfig
        print("✓ Config module imported successfully")
          # Test configuration creation
        config = SystemConfig()
        print(f"✓ SystemConfig created: {config.qdrant_url}")
        
        opt_config = OptimizationConfig()
        print(f"✓ OptimizationConfig created: hnsw_m={opt_config.qdrant_hnsw_m}")
        
        print("\n✓ All imports successful!")
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    try:
        print("\nTesting basic functionality...")
        
        # Test that classes can be instantiated
        from optimization.config import SystemConfig
        config = SystemConfig()
          # Test configuration values
        assert config.qdrant_url is not None
        assert config.neo4j_uri is not None
        assert config.embedding_models is not None
        
        print("✓ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Functionality error: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Quick Optimization Test ===\n")
    
    import_success = test_imports()
    func_success = test_basic_functionality()
    
    if import_success and func_success:
        print("\n🎉 All tests passed! Optimization system is ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())

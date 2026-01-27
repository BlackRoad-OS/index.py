"""
Basic tests for the BlackRoad OS Repository Index.
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_static_repository_data():
    """Test that static repository data exists and is valid JSON."""
    static_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "repositories-static.json"
    )
    
    assert os.path.exists(static_file), "Static repository file should exist"
    
    with open(static_file, 'r') as f:
        data = json.load(f)
    
    assert "organization" in data
    assert data["organization"] == "BlackRoad-OS"
    assert "categories" in data
    assert len(data["categories"]) > 0
    
    print(f"✅ Static data validated: {data['total_count']} repositories")


def test_config_file():
    """Test that config file exists and is readable."""
    config_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config.yaml"
    )
    
    assert os.path.exists(config_file), "Config file should exist"
    
    with open(config_file, 'r') as f:
        content = f.read()
    
    assert "BlackRoad-OS" in content
    assert "categories" in content
    
    print("✅ Config file validated")


def test_readme_exists():
    """Test that README exists and has content."""
    readme_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "README.md"
    )
    
    assert os.path.exists(readme_file), "README should exist"
    
    with open(readme_file, 'r') as f:
        content = f.read()
    
    assert "BlackRoad OS" in content
    assert "index.py" in content
    
    print("✅ README validated")


def test_license_exists():
    """Test that LICENSE exists."""
    license_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "LICENSE"
    )
    
    assert os.path.exists(license_file), "LICENSE should exist"
    
    with open(license_file, 'r') as f:
        content = f.read()
    
    assert "MIT License" in content
    assert "BlackRoad OS" in content
    
    print("✅ LICENSE validated")


def test_requirements():
    """Test that requirements.txt exists and has dependencies."""
    req_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "requirements.txt"
    )
    
    assert os.path.exists(req_file), "requirements.txt should exist"
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    assert "requests" in content
    
    print("✅ Requirements validated")


def test_index_script_executable():
    """Test that index.py exists and is executable."""
    index_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "index.py"
    )
    
    assert os.path.exists(index_file), "index.py should exist"
    assert os.access(index_file, os.X_OK), "index.py should be executable"
    
    print("✅ Index script validated")


if __name__ == "__main__":
    # Run all tests
    test_static_repository_data()
    test_config_file()
    test_readme_exists()
    test_license_exists()
    test_requirements()
    test_index_script_executable()
    
    print("\n🖤 All tests passed! BlackRoad OS Repository Index is ready.")

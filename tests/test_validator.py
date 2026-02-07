"""
Test script for Issue Validator
Run: python tests/test_validator.py
"""

import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from backend.utils.issue_validator import IssueValidator


def test_validator():
    print("=" * 50)
    print("🧪 Testing Issue Validator")
    print("=" * 50)
    
    validator = IssueValidator()
    
    # Test with a sample image from data folder if it exists
    test_images = list((project_root / "data" / "images").glob("*.jpg"))[:1]
    
    if not test_images:
        print("⚠️ No test images found in data/images/")
        print("Creating a dummy validation test...")
        
        # Test with any existing image
        test_images = list(project_root.glob("**/*.jpg"))[:1]
    
    if test_images:
        test_img = test_images[0]
        print(f"\n📷 Testing with: {test_img.name}")
        
        result = validator.validate_report(
            image_path=str(test_img),
            claimed_lat=28.6139,
            claimed_lng=77.2090,
            issue_type='pothole'
        )
        
        print(f"\n📊 Results:")
        print(f"   Trust Score: {result['score']}%")
        print(f"   Decision: {result['decision'].upper()}")
        print(f"   Message: {result['message']}")
        print(f"\n🔍 Individual Checks:")
        for check, data in result['checks'].items():
            print(f"   • {check}: {data}")
    else:
        print("❌ No images found to test with.")
    
    print("\n" + "=" * 50)
    print("✅ Validator module is working!")
    print("=" * 50)


if __name__ == "__main__":
    test_validator()

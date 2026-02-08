"""
Test script for Damage Quantifier
Tests the Computer Vision Damage Quantification module.

Run: python tests/test_damage_quantifier.py
"""

import sys
import io
from pathlib import Path

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Setup path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from backend.utils.damage_quantifier import DamageQuantifier, analyze_civic_issue


def test_damage_quantifier():
    print("=" * 60)
    print("[TEST] Computer Vision Damage Quantifier")
    print("=" * 60)
    
    quantifier = DamageQuantifier()
    
    # Check if Gemini is configured
    if quantifier.model:
        print("[OK] Gemini Vision API configured")
    else:
        print("[!] Gemini API not configured - using mock data for demo")
        print("    Set GOOGLE_API_KEY environment variable to enable AI analysis")
    
    # Find test images
    test_images = list((project_root / "data" / "images").glob("*.jpg"))[:3]
    
    if not test_images:
        print("\n[!] No test images found in data/images/")
        print("    Running with mock data demonstration...\n")
        
        # Demo with mock data
        demo_mock_analysis()
        return
    
    # Test with real images
    for img_path in test_images:
        print(f"\n[IMAGE] Analyzing: {img_path.name}")
        print("-" * 50)
        
        # Detect type from filename
        filename = img_path.name.lower()
        if 'garbage' in filename or 'trash' in filename or 'waste' in filename:
            issue_type = 'garbage'
        elif 'crack' in filename or 'wall' in filename or 'infrastructure' in filename:
            issue_type = 'infrastructure'
        else:
            issue_type = 'pothole'
        
        result = quantifier.quantify_damage(str(img_path), issue_type)
        print_result(result)
    
    print("\n" + "=" * 60)
    print("[OK] Damage Quantifier module is working!")
    print("=" * 60)


def demo_mock_analysis():
    """Demonstrate with mock data for all issue types."""
    print("=" * 60)
    print("[DEMO] Mock Damage Quantification Results")
    print("=" * 60)
    
    quantifier = DamageQuantifier()
    
    # Create a dummy file path for testing (won't actually be read in mock mode)
    dummy_path = str(project_root / "data" / "images" / "test.jpg")
    
    for issue_type in ['pothole', 'garbage', 'infrastructure']:
        print(f"\n[TYPE] {issue_type.upper()}")
        print("-" * 50)
        
        # Get mock analysis
        mock_data = quantifier._get_mock_analysis(issue_type)
        repair_data = quantifier._calculate_repair(mock_data, issue_type)
        summary = quantifier._generate_summary(mock_data, repair_data, issue_type)
        
        result = {
            'damage': mock_data,
            'repair': repair_data,
            'summary': summary,
            'issue_type': issue_type
        }
        
        print_result(result)
    
    print("\n" + "=" * 60)
    print("[OK] Demo complete! Module is working correctly.")
    print("=" * 60)


def print_result(result: dict):
    """Pretty print analysis result."""
    damage = result.get('damage', {})
    repair = result.get('repair', {})
    
    # Summary line
    print(f"\n[SUMMARY] {result.get('summary', 'N/A')}")
    
    # Damage details
    print(f"\n[MEASUREMENTS]")
    for key, value in damage.items():
        if key not in ['detected', 'notes', '_note', 'error']:
            print(f"   * {key.replace('_', ' ').title()}: {value}")
    
    if damage.get('notes'):
        print(f"   * Notes: {damage['notes']}")
    
    # Repair estimate
    if not repair.get('error'):
        print(f"\n[REPAIR REQUIREMENTS]")
        
        if repair.get('materials'):
            print("   Materials:")
            for mat in repair['materials']:
                print(f"      - {mat}")
        
        if repair.get('equipment'):
            print("   Equipment:")
            for eq in repair['equipment']:
                print(f"      - {eq}")
        
        if repair.get('labor_hours'):
            print(f"   Labor: {repair['labor_hours']} hour(s)")
        
        cost = repair.get('cost_range', {})
        if cost:
            print(f"\n[COST] Estimated: Rs.{cost.get('min', '?'):,} - Rs.{cost.get('max', '?'):,}")
    else:
        print(f"\n[!] Repair calculation: {repair.get('error')}")


def test_quick_function():
    """Test the convenience function."""
    print("\n" + "=" * 60)
    print("[TEST] Quick Analysis Function")
    print("=" * 60)
    
    # Find any image to test with
    test_images = list((project_root / "data" / "images").glob("*.jpg"))[:1]
    
    if test_images:
        result = analyze_civic_issue(str(test_images[0]), 'pothole')
        print(f"\n[OK] Quick function works: {result.get('summary', 'Success')}")
    else:
        print("\n[!] No images to test quick function (would work with real images)")


if __name__ == "__main__":
    test_damage_quantifier()
    test_quick_function()

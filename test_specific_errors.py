#!/usr/bin/env python3
"""
Test for specific PKB loading and UI spacing issues
"""

import urllib.request
import os
import sys

def test_pkb_loading_issue():
    """Test the PKB loading workflow"""
    print("🔍 Testing PKB Loading Issue...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for PKB loading logic
        issues = []
        
        # Look for worlds_3g.pkb reference
        if 'worlds_3g.pkb' in content:
            print("⚠️ Found reference to worlds_3g.pkb - this should be dynamic")
            issues.append("Hardcoded PKB filename")
        
        # Check for PKB file initialization
        if 'MXO_PKB_FILES = {}' in content or 'MXO_PKB_FILES={}' in content:
            print("✅ PKB files initialized as empty object")
        else:
            print("❌ PKB files not properly initialized")
            issues.append("PKB files not initialized")
        
        # Check for proper error handling
        if 'PKB file' in content and 'not loaded' in content:
            print("✅ PKB not loaded error handling present")
        else:
            print("❌ Missing PKB not loaded error handling")
            issues.append("Missing error handling")
        
        return issues
        
    except Exception as e:
        print(f"❌ PKB loading test failed: {e}")
        return ["Test failed"]

def test_css_spacing_issue():
    """Test for CSS spacing issues in tabs"""
    print("\n🎨 Testing CSS Spacing Issue...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        issues = []
        
        # Check for spacing utilities
        spacing_classes = ['.mr-2', '.ml-2', '.px-2', '.py-1', '.mb-2', '.mt-2']
        missing_spacing = []
        
        for spacing_class in spacing_classes:
            if spacing_class not in content:
                missing_spacing.append(spacing_class)
        
        if missing_spacing:
            print(f"❌ Missing spacing classes: {', '.join(missing_spacing)}")
            issues.append(f"Missing spacing: {', '.join(missing_spacing)}")
        else:
            print("✅ All spacing classes present")
        
        # Check for tab-specific styling
        if '.tab' in content or 'tab-' in content:
            print("✅ Tab styling present")
        else:
            print("⚠️ No specific tab styling found")
            issues.append("No tab styling")
        
        return issues
        
    except Exception as e:
        print(f"❌ CSS spacing test failed: {e}")
        return ["Test failed"]

def run_specific_error_tests():
    """Run tests for the specific reported issues"""
    print("🐛 MOMS Specific Error Tests")
    print("=" * 40)
    
    all_issues = []
    
    # Test PKB loading
    pkb_issues = test_pkb_loading_issue()
    all_issues.extend(pkb_issues)
    
    # Test CSS spacing
    css_issues = test_css_spacing_issue()
    all_issues.extend(css_issues)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 SPECIFIC ISSUES SUMMARY")
    
    if not all_issues:
        print("✅ No specific issues found!")
        return True
    else:
        print(f"❌ Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 FIXES NEEDED:")
        
        if any("PKB" in issue for issue in all_issues):
            print("   - Fix PKB file loading to be dynamic")
            print("   - Add proper PKB file initialization")
            print("   - Handle missing PKB files gracefully")
        
        if any("spacing" in issue.lower() for issue in all_issues):
            print("   - Add proper spacing between tabs")
            print("   - Restore margin/padding classes")
            print("   - Fix tab layout CSS")
        
        return False

if __name__ == "__main__":
    success = run_specific_error_tests()
    sys.exit(0 if success else 1)
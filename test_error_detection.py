#!/usr/bin/env python3
"""
MOMS Error Detection Test - Find and diagnose specific issues
"""

import urllib.request
import urllib.parse
import json
import sys
import os
import time
from urllib.error import URLError, HTTPError

def test_packmap_save_issue():
    """Test for packmap_save.lta file loading issue"""
    print("🔍 Testing packmap_save.lta file issue...")
    
    # Check if file exists
    cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
    packmap_file = os.path.join(cache_dir, 'packmap_save.lta')
    
    if os.path.exists(packmap_file):
        file_size = os.path.getsize(packmap_file)
        print(f"✅ packmap_save.lta exists locally: {file_size} bytes")
        
        # Check if accessible via HTTP
        try:
            response = urllib.request.urlopen('http://localhost:8000/cache/packmap_save.lta', timeout=5)
            if response.getcode() == 200:
                data = response.read()
                print(f"✅ packmap_save.lta accessible via HTTP: {len(data)} bytes")
                return True
            else:
                print(f"❌ packmap_save.lta HTTP error: {response.getcode()}")
                return False
        except Exception as e:
            print(f"❌ packmap_save.lta HTTP access failed: {e}")
            return False
    else:
        print(f"❌ packmap_save.lta does not exist at: {packmap_file}")
        return False

def test_production_warnings():
    """Test for production warnings in the application"""
    print("\n⚠️ Testing for production warnings...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        issues = []
        
        # Check for Tailwind CDN usage
        if 'cdn.tailwindcss.com' in content:
            issues.append("Tailwind CSS CDN should not be used in production")
            print("❌ Found Tailwind CDN usage")
        
        # Check for Babel standalone usage
        if 'babel/standalone' in content:
            issues.append("Babel standalone should not be used in production")
            print("❌ Found Babel standalone usage")
        
        # Check for console.log statements (should be minimal in production)
        console_logs = content.count('console.log')
        if console_logs > 20:
            issues.append(f"Too many console.log statements: {console_logs}")
            print(f"⚠️ Found {console_logs} console.log statements")
        
        # Check for development-only code
        if 'development' in content.lower():
            issues.append("Development-specific code found")
            print("⚠️ Found development-specific code")
        
        return issues
        
    except Exception as e:
        print(f"❌ Production warnings test failed: {e}")
        return ["Test failed"]

def test_file_loading_workflow():
    """Test the file loading workflow that's causing the error"""
    print("\n📁 Testing file loading workflow...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for index file loading logic
        checks = [
            ('Index file check', 'packmap_save.lta' in content),
            ('PKB file loading', 'MXO_PKB_FILES' in content),
            ('Error handling', 'No index file loaded' in content),
            ('File loading function', 'loadIndexFile' in content or 'loadIndex' in content),
            ('PKB extraction', 'extractFromPKB' in content)
        ]
        
        issues = []
        for name, check in checks:
            if check:
                print(f"✅ {name}: Present")
            else:
                print(f"❌ {name}: Missing")
                issues.append(f"Missing: {name}")
        
        return issues
        
    except Exception as e:
        print(f"❌ File loading workflow test failed: {e}")
        return ["Test failed"]

def test_pkb_extraction_initialization():
    """Test PKB extraction initialization"""
    print("\n📦 Testing PKB extraction initialization...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Look for initialization code that might be causing the error
        initialization_checks = [
            ('PKB files array initialization', 'MXO_PKB_FILES = ' in content or 'MXO_PKB_FILES='),
            ('Index data initialization', 'MXO_PKB_INDEX_DATA = ' in content or 'MXO_PKB_INDEX_DATA='),
            ('Auto-load prevention', 'loadIndexFile' in content),
            ('Error message handling', 'Please load packmap_save.lta first' in content),
            ('PKB file detection', 'worlds_3g.pkb' in content)
        ]
        
        issues = []
        for name, check in initialization_checks:
            present = any(keyword in content for keyword in check) if isinstance(check, list) else check in content
            if present:
                print(f"✅ {name}: Present")
            else:
                print(f"❌ {name}: Missing")
                issues.append(f"Missing: {name}")
        
        return issues
        
    except Exception as e:
        print(f"❌ PKB extraction initialization test failed: {e}")
        return ["Test failed"]

def run_error_detection_tests():
    """Run all error detection tests"""
    print("🔍 MOMS Error Detection Test Suite")
    print("=" * 50)
    
    all_issues = []
    
    # Test 1: packmap_save.lta issue
    print("\n1. PACKMAP_SAVE.LTA FILE TEST")
    packmap_working = test_packmap_save_issue()
    if not packmap_working:
        all_issues.append("packmap_save.lta file not accessible")
    
    # Test 2: Production warnings
    print("\n2. PRODUCTION WARNINGS TEST")
    production_issues = test_production_warnings()
    all_issues.extend(production_issues)
    
    # Test 3: File loading workflow
    print("\n3. FILE LOADING WORKFLOW TEST")
    workflow_issues = test_file_loading_workflow()
    all_issues.extend(workflow_issues)
    
    # Test 4: PKB extraction initialization
    print("\n4. PKB EXTRACTION INITIALIZATION TEST")
    init_issues = test_pkb_extraction_initialization()
    all_issues.extend(init_issues)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ERROR DETECTION SUMMARY")
    
    if not all_issues:
        print("✅ No issues detected!")
        return True
    else:
        print(f"❌ Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 RECOMMENDED FIXES:")
        
        if "packmap_save.lta file not accessible" in all_issues:
            print("   - Ensure packmap_save.lta file exists in cache/ directory")
            print("   - Check file permissions and server access")
        
        if any("Tailwind" in issue for issue in all_issues):
            print("   - Replace Tailwind CDN with local installation")
            print("   - Use PostCSS plugin or Tailwind CLI")
        
        if any("Babel" in issue for issue in all_issues):
            print("   - Precompile JSX/React components")
            print("   - Remove Babel standalone from production")
        
        if any("console.log" in issue for issue in all_issues):
            print("   - Remove or minimize console.log statements")
            print("   - Use proper logging system")
        
        if any("Missing" in issue for issue in all_issues):
            print("   - Implement missing file loading functions")
            print("   - Add proper error handling")
        
        return False

if __name__ == "__main__":
    success = run_error_detection_tests()
    sys.exit(0 if success else 1)
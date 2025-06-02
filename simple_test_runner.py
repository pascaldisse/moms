#!/usr/bin/env python3
"""
MOMS Simple Test Runner - Tests core functionality without external dependencies
"""

import urllib.request
import urllib.parse
import json
import sys
import socket
from urllib.error import URLError, HTTPError

def test_server_connectivity():
    """Test if the main server is running"""
    print("🔧 Testing Server Connectivity...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/', timeout=5)
        if response.getcode() == 200:
            print("✅ Main Server (port 8000): OK")
            return True
        else:
            print(f"❌ Main Server (port 8000): {response.getcode()}")
            return False
    except URLError as e:
        print(f"❌ Main Server (port 8000): Connection failed - {e}")
        return False

def test_bik_server():
    """Test if BIK server is running"""
    print("🎬 Testing BIK Server...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8002/status', timeout=5)
        if response.getcode() == 200:
            print("✅ BIK Server (port 8002): OK")
            return True
        else:
            print("⚠️ BIK Server (port 8002): May not be running")
            return False
    except URLError as e:
        print(f"⚠️ BIK Server (port 8002): Not accessible - {e}")
        return False

def test_application_files():
    """Test if essential application files exist and load"""
    print("\n📱 Testing Application Files...")
    
    files_to_test = [
        ('index.html', 'Main Application'),
        ('index_modern.html', 'Modern Version'),
        ('test_suite.html', 'Test Suite'),
        ('server.py', 'Server Script'),
        ('simple-bik-server.py', 'BIK Server')
    ]
    
    results = []
    
    for filename, description in files_to_test:
        try:
            response = urllib.request.urlopen(f'http://localhost:8000/{filename}', timeout=5)
            if response.getcode() == 200:
                print(f"✅ {description}: Available")
                results.append(True)
            else:
                print(f"❌ {description}: {response.getcode()}")
                results.append(False)
        except URLError as e:
            print(f"❌ {description}: Failed - {e}")
            results.append(False)
    
    return all(results)

def test_application_content():
    """Test if the main application contains essential components"""
    print("\n🔍 Testing Application Content...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for essential components
        checks = [
            ('React', 'react@18.2.0' in content or 'React.createElement' in content),
            ('THREE.js', 'three@' in content or 'THREE.Scene' in content),
            ('Monaco Editor', 'monaco-editor' in content),
            ('File Types', 'FILE_TYPES' in content),
            ('PKB Extraction', 'extractFromPKB' in content),
            ('Performance Monitor', 'performanceMonitor' in content),
            ('Error Handler', 'handleError' in content),
            ('Matrix Online Formats', '.moa' in content and '.prop' in content),
            ('3D Model Viewer', 'ModelEditor' in content),
            ('Combat Analyzer', 'GameObjects' in content or 'combat' in content)
        ]
        
        passed = 0
        for name, check in checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(checks)) * 100
        print(f"📊 Content Check: {passed}/{len(checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ Content Test Failed: {e}")
        return False

def test_3d_viewer_components():
    """Test if 3D viewer components are present"""
    print("\n🎯 Testing 3D Viewer Components...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for 3D viewer essentials
        viewer_checks = [
            ('THREE.js Scene', 'THREE.Scene' in content),
            ('Camera Controls', 'camera.position' in content or 'OrbitControls' in content),
            ('Lighting System', 'AmbientLight' in content and 'DirectionalLight' in content),
            ('Material Support', 'MeshPhongMaterial' in content or 'MeshBasicMaterial' in content),
            ('Geometry Processing', 'BufferGeometry' in content),
            ('Model Loading', 'loadModel' in content or 'parseModel' in content),
            ('Export Function', 'exportToOBJ' in content),
            ('Model Statistics', 'modelStats' in content or 'vertices' in content)
        ]
        
        passed = 0
        for name, check in viewer_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(viewer_checks)) * 100
        print(f"📊 3D Viewer Check: {passed}/{len(viewer_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ 3D Viewer Test Failed: {e}")
        return False

def test_model_extraction_components():
    """Test if model extraction components are present"""
    print("\n📦 Testing Model Extraction Components...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for extraction essentials
        extraction_checks = [
            ('PKB Support', 'extractFromPKB' in content),
            ('Archive Storage', 'MXO_PKB_FILES' in content or 'pkbFiles' in content),
            ('Index Processing', 'packmap_save' in content or 'index' in content),
            ('File Extraction', 'Extract & View' in content or 'extractFile' in content),
            ('Matrix Formats', '.moa' in content and '.prop' in content),
            ('Model Parsing', 'parseMOA' in content or 'parseModel' in content),
            ('Binary Processing', 'ArrayBuffer' in content or 'Uint8Array' in content),
            ('Error Handling', 'try {' in content and 'catch' in content)
        ]
        
        passed = 0
        for name, check in extraction_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(extraction_checks)) * 100
        print(f"📊 Extraction Check: {passed}/{len(extraction_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ Model Extraction Test Failed: {e}")
        return False

def check_correct_file_formats():
    """Verify that correct Matrix Online file formats are supported"""
    print("\n📐 Testing Matrix Online File Format Support...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.text if hasattr(response, 'text') else response.read().decode('utf-8')
        
        # Correct Matrix Online formats
        correct_formats = ['.moa', '.prop', '.mga', '.mgc', '.iprf', '.eprf']
        incorrect_formats = ['.mob']  # Common misconception
        
        format_results = []
        
        print("✅ Correct Matrix Online Formats:")
        for fmt in correct_formats:
            if fmt in content:
                print(f"  ✅ {fmt}: Supported")
                format_results.append(True)
            else:
                print(f"  ❌ {fmt}: Missing")
                format_results.append(False)
        
        print("⚠️ Incorrect Formats Check:")
        for fmt in incorrect_formats:
            if fmt in content:
                print(f"  ⚠️ {fmt}: Should not be supported (Matrix Online doesn't use this)")
            else:
                print(f"  ✅ {fmt}: Correctly not supported")
        
        correct_support = sum(format_results)
        total_correct = len(correct_formats)
        
        success_rate = (correct_support / total_correct) * 100
        print(f"📊 Format Support: {correct_support}/{total_correct} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ File Format Test Failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧪 MOMS Simple Test Suite - Core Functionality Testing\n")
    print("=" * 60)
    
    tests = [
        ("Server Connectivity", test_server_connectivity),
        ("BIK Server", test_bik_server),
        ("Application Files", test_application_files),
        ("Application Content", test_application_content),
        ("3D Viewer Components", test_3d_viewer_components),
        ("Model Extraction", test_model_extraction_components),
        ("File Format Support", check_correct_file_formats)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
                
        except Exception as e:
            results.append((test_name, False))
            print(f"\n💥 {test_name}: ERROR - {e}")
        
        print("-" * 50)
    
    # Final summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    print(f"\n📝 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    if success_rate < 60:
        print("\n🚨 CRITICAL: Major issues found! Application may not function properly.")
        return False
    elif success_rate < 80:
        print("\n⚠️ WARNING: Some issues found. Some functionality may be limited.")
        return True
    else:
        print("\n🎉 EXCELLENT: Most tests passed! Application should be functional.")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    
    if not success:
        print("\n🔧 NEXT STEPS:")
        print("1. Check if servers are running: ./start_servers.sh")
        print("2. Verify file accessibility and CORS configuration")
        print("3. Check browser console for JavaScript errors")
        print("4. Review failed test components for specific issues")
    
    sys.exit(0 if success else 1)
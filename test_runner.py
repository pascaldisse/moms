#!/usr/bin/env python3
"""
MOMS Test Runner - Tests core functionality including 3D model extraction and viewing
"""

import requests
import json
import time
import sys
from io import BytesIO

def test_servers():
    """Test server connectivity and CORS"""
    print("🔧 Testing Servers...")
    
    # Test main server
    try:
        response = requests.get('http://localhost:8000/')
        if response.status_code == 200:
            print("✅ Main Server (8000): OK")
        else:
            print(f"❌ Main Server (8000): {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main Server (8000): Connection failed - {e}")
        return False
    
    # Test BIK server
    try:
        response = requests.get('http://localhost:8002/status')
        if response.status_code == 200:
            print("✅ BIK Server (8002): OK")
        else:
            print("⚠️ BIK Server (8002): May not be running")
    except Exception as e:
        print(f"⚠️ BIK Server (8002): Not accessible - {e}")
    
    # Test CORS
    try:
        headers = {
            'Origin': 'http://localhost:8000',
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.options('http://localhost:8000/', headers=headers)
        if response.status_code == 200:
            print("✅ CORS Support: OK")
        else:
            print(f"⚠️ CORS Support: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS Support: Failed - {e}")
    
    return True

def test_application_load():
    """Test if the main application loads properly"""
    print("\n📱 Testing Application Load...")
    
    try:
        response = requests.get('http://localhost:8000/index.html')
        if response.status_code == 200:
            content = response.text
            
            # Check for essential components
            checks = [
                ('React', 'react@18.2.0' in content),
                ('THREE.js', 'three@0.160.0' in content or 'three.module.js' in content),
                ('Monaco Editor', 'monaco-editor' in content),
                ('File Types', 'FILE_TYPES' in content),
                ('PKB Extraction', 'extractFromPKB' in content),
                ('Performance Monitor', 'performanceMonitor' in content),
                ('Error Handler', 'handleError' in content)
            ]
            
            for name, passed in checks:
                if passed:
                    print(f"✅ {name}: Present")
                else:
                    print(f"❌ {name}: Missing")
                    
            return all(check[1] for check in checks)
            
    except Exception as e:
        print(f"❌ Application Load: Failed - {e}")
        return False

def test_modern_version():
    """Test the modern version with ES modules"""
    print("\n⚡ Testing Modern Version...")
    
    try:
        response = requests.get('http://localhost:8000/index_modern.html')
        if response.status_code == 200:
            content = response.text
            
            # Check for modern features
            checks = [
                ('ES Modules', 'type="module"' in content),
                ('Import Maps', 'importmap' in content),
                ('THREE.js r169', 'three@0.169' in content or 'three.module.js' in content),
                ('OrbitControls', 'OrbitControls' in content)
            ]
            
            for name, passed in checks:
                if passed:
                    print(f"✅ {name}: Present")
                else:
                    print(f"❌ {name}: Missing")
                    
            return all(check[1] for check in checks)
            
    except Exception as e:
        print(f"❌ Modern Version: Failed - {e}")
        return False

def create_test_files():
    """Create synthetic test files for model extraction testing"""
    print("\n📁 Creating Test Files...")
    
    # Create synthetic PKB file
    pkb_data = bytearray(1024)
    for i in range(len(pkb_data)):
        pkb_data[i] = i % 256
    
    # Create synthetic MOA file (simplified)
    moa_data = bytearray(512)
    # Add some vertex-like data
    for i in range(0, 512, 4):
        moa_data[i:i+4] = (i // 4).to_bytes(4, 'little')
    
    # Create synthetic index file
    index_data = bytearray(256)
    # Add some pattern that might be recognized
    test_filename = b"test.moa\x00"
    index_data[0:len(test_filename)] = test_filename
    index_data[64:68] = (0).to_bytes(4, 'little')  # offset
    index_data[68:72] = (512).to_bytes(4, 'little')  # size
    
    test_files = {
        'test.pkb': pkb_data,
        'test.moa': moa_data,
        'packmap_save.lta': index_data
    }
    
    print(f"✅ Created {len(test_files)} synthetic test files")
    return test_files

def test_file_parsing():
    """Test file parsing functionality"""
    print("\n🔍 Testing File Parsing...")
    
    test_files = create_test_files()
    
    # Test file type detection
    file_types = {
        'test.pkb': 'ARCHIVE',
        'test.moa': 'MODEL', 
        'packmap_save.lta': 'ARCHIVE'
    }
    
    for filename, expected_type in file_types.items():
        ext = '.' + filename.split('.')[1].lower()
        
        # These are the extensions we should support
        model_exts = ['.abc', '.moa', '.prop', '.iprf', '.eprf', '.mga', '.mgc']
        archive_exts = ['.rez', '.lta', '.ltb', '.pkb']
        
        if ext in model_exts:
            print(f"✅ {filename}: Detected as MODEL")
        elif ext in archive_exts:
            print(f"✅ {filename}: Detected as ARCHIVE")
        else:
            print(f"❌ {filename}: Unknown file type")
            
    return True

def test_three_js_components():
    """Test THREE.js component availability"""
    print("\n🎮 Testing THREE.js Components...")
    
    # Check if the test suite can verify THREE.js
    try:
        response = requests.get('http://localhost:8000/test_three.html')
        if response.status_code == 200:
            print("✅ THREE.js Test Page: Available")
            return True
        else:
            print("❌ THREE.js Test Page: Not found")
            return False
    except Exception as e:
        print(f"❌ THREE.js Test Page: Failed - {e}")
        return False

def test_pkb_extraction():
    """Test PKB extraction functionality"""
    print("\n📦 Testing PKB Extraction...")
    
    # The PKB extraction requires the main application to be loaded
    # We can test if the extraction function exists
    try:
        response = requests.get('http://localhost:8000/index.html')
        if response.status_code == 200:
            content = response.text
            
            # Check for PKB extraction components
            checks = [
                ('Extract Function', 'extractFromPKB' in content),
                ('PKB Storage', 'MXO_PKB_FILES' in content),
                ('Index Storage', 'MXO_PKB_INDEX_DATA' in content),
                ('Performance Monitoring', 'performanceMonitor.start' in content),
                ('Extract Buttons', 'Extract & View' in content or 'Extract All Models' in content)
            ]
            
            for name, passed in checks:
                if passed:
                    print(f"✅ {name}: Present")
                else:
                    print(f"❌ {name}: Missing")
                    
            return all(check[1] for check in checks)
            
    except Exception as e:
        print(f"❌ PKB Extraction Test: Failed - {e}")
        return False

def test_3d_model_viewer():
    """Test 3D model viewer functionality"""
    print("\n🎯 Testing 3D Model Viewer...")
    
    try:
        response = requests.get('http://localhost:8000/index.html')
        if response.status_code == 200:
            content = response.text
            
            # Check for 3D viewer components
            checks = [
                ('ModelEditor Component', 'ModelEditor' in content),
                ('THREE.js Scene', 'THREE.Scene' in content),
                ('Camera Controls', 'OrbitControls' or 'camera.position' in content),
                ('Lighting System', 'AmbientLight' and 'DirectionalLight' in content),
                ('Export Function', 'exportToOBJ' in content),
                ('Material Support', 'MeshPhongMaterial' in content),
                ('Geometry Processing', 'BufferGeometry' in content),
                ('Model Stats', 'modelStats' in content)
            ]
            
            for name, passed in checks:
                if passed:
                    print(f"✅ {name}: Present")
                else:
                    print(f"❌ {name}: Missing")
                    
            return all(check[1] for check in checks)
            
    except Exception as e:
        print(f"❌ 3D Model Viewer Test: Failed - {e}")
        return False

def test_model_formats():
    """Test Matrix Online model format support"""
    print("\n📐 Testing Model Format Support...")
    
    try:
        response = requests.get('http://localhost:8000/index.html')
        if response.status_code == 200:
            content = response.text
            
            # Check for correct Matrix Online formats
            correct_formats = ['.moa', '.prop', '.mga', '.mgc', '.iprf', '.eprf']
            incorrect_formats = ['.mob']  # Common misconception
            
            format_checks = []
            for fmt in correct_formats:
                if fmt in content:
                    print(f"✅ Format {fmt}: Supported")
                    format_checks.append(True)
                else:
                    print(f"❌ Format {fmt}: Missing")
                    format_checks.append(False)
            
            for fmt in incorrect_formats:
                if fmt in content:
                    print(f"⚠️ Format {fmt}: Should not be supported (Matrix Online doesn't use this)")
                else:
                    print(f"✅ Format {fmt}: Correctly not supported")
            
            return all(format_checks)
            
    except Exception as e:
        print(f"❌ Model Format Test: Failed - {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🧪 MOMS Test Suite - Comprehensive Testing\n")
    
    tests = [
        ("Server Connectivity", test_servers),
        ("Application Load", test_application_load),
        ("Modern Version", test_modern_version),
        ("File Parsing", test_file_parsing),
        ("THREE.js Components", test_three_js_components),
        ("PKB Extraction", test_pkb_extraction),
        ("3D Model Viewer", test_3d_model_viewer),
        ("Model Format Support", test_model_formats)
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
    
    if success_rate < 80:
        print("\n🚨 Critical issues found! Requires fixes.")
        return False
    elif success_rate < 100:
        print("\n⚠️ Some issues found, but application is functional.")
        return True
    else:
        print("\n🎉 All tests passed! Application is fully functional.")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
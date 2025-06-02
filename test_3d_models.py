#!/usr/bin/env python3
"""
MOMS 3D Model Extraction and Viewing Test - Specific tests for model functionality
"""

import urllib.request
import urllib.parse
import json
import sys
import os
from urllib.error import URLError, HTTPError

def create_test_model_files():
    """Create synthetic test files for model extraction testing"""
    print("📁 Creating Test Model Files...")
    
    # Create cache directory if it doesn't exist
    cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        print(f"✅ Created cache directory: {cache_dir}")
    
    # Create synthetic MOA file (Matrix Online character model)
    moa_file = os.path.join(cache_dir, 'test_character.moa')
    with open(moa_file, 'wb') as f:
        # Create a simple MOA-like structure
        # Magic number (fake)
        f.write(b'MOA\x00')
        # Version
        f.write((1).to_bytes(4, 'little'))
        # Vertex count
        vertex_count = 12  # A simple cube
        f.write(vertex_count.to_bytes(4, 'little'))
        
        # Vertices for a simple cube
        vertices = [
            # Front face
            [-1.0, -1.0,  1.0],  # Bottom left
            [ 1.0, -1.0,  1.0],  # Bottom right
            [ 1.0,  1.0,  1.0],  # Top right
            [-1.0,  1.0,  1.0],  # Top left
            # Back face
            [-1.0, -1.0, -1.0],  # Bottom left
            [ 1.0, -1.0, -1.0],  # Bottom right
            [ 1.0,  1.0, -1.0],  # Top right
            [-1.0,  1.0, -1.0],  # Top left
        ]
        
        # Write vertex data
        for vertex in vertices:
            for coord in vertex:
                # Convert float to bytes (little endian)
                import struct
                f.write(struct.pack('<f', coord))
        
        # Add some padding/additional data
        f.write(b'\x00' * 100)
    
    print(f"✅ Created test MOA file: {moa_file} ({os.path.getsize(moa_file)} bytes)")
    
    # Create synthetic PROP file (Matrix Online static prop)
    prop_file = os.path.join(cache_dir, 'test_building.prop')
    with open(prop_file, 'wb') as f:
        # Create a simple PROP-like structure
        f.write(b'PROP')
        f.write((1).to_bytes(4, 'little'))
        # Simple triangle mesh
        f.write((3).to_bytes(4, 'little'))  # 3 vertices
        
        # Triangle vertices
        triangle_verts = [
            [0.0, 1.0, 0.0],   # Top
            [-1.0, -1.0, 0.0], # Bottom left
            [1.0, -1.0, 0.0]   # Bottom right
        ]
        
        for vertex in triangle_verts:
            for coord in vertex:
                import struct
                f.write(struct.pack('<f', coord))
        
        f.write(b'\x00' * 50)
    
    print(f"✅ Created test PROP file: {prop_file} ({os.path.getsize(prop_file)} bytes)")
    
    # Create synthetic PKB archive with models
    pkb_file = os.path.join(cache_dir, 'test_models.pkb')
    with open(pkb_file, 'wb') as f:
        # PKB header
        f.write(b'PKB\x00')
        f.write((2).to_bytes(4, 'little'))  # Number of files
        
        # File 1: embedded MOA
        f.write(b'char1.moa\x00\x00\x00\x00\x00\x00')  # Filename (16 bytes)
        f.write((100).to_bytes(4, 'little'))  # Offset
        f.write((200).to_bytes(4, 'little'))  # Size
        
        # File 2: embedded PROP
        f.write(b'prop1.prop\x00\x00\x00\x00\x00')  # Filename (16 bytes)
        f.write((300).to_bytes(4, 'little'))  # Offset
        f.write((150).to_bytes(4, 'little'))  # Size
        
        # Pad to offset 100
        f.write(b'\x00' * (100 - f.tell()))
        
        # Write embedded MOA data
        with open(moa_file, 'rb') as moa:
            moa_data = moa.read()[:200]  # First 200 bytes
            f.write(moa_data)
            f.write(b'\x00' * (200 - len(moa_data)))
        
        # Write embedded PROP data
        with open(prop_file, 'rb') as prop:
            prop_data = prop.read()[:150]  # First 150 bytes
            f.write(prop_data)
            f.write(b'\x00' * (150 - len(prop_data)))
    
    print(f"✅ Created test PKB file: {pkb_file} ({os.path.getsize(pkb_file)} bytes)")
    
    # Create corresponding index file
    index_file = os.path.join(cache_dir, 'packmap_save.lta')
    with open(index_file, 'wb') as f:
        # Simple index structure
        f.write(b'LTAI')  # LTA Index magic
        f.write((2).to_bytes(4, 'little'))  # Number of entries
        
        # Entry 1
        f.write(b'char1.moa\x00\x00\x00\x00\x00\x00\x00\x00')  # Name (20 bytes)
        f.write((100).to_bytes(4, 'little'))  # Offset
        f.write((200).to_bytes(4, 'little'))  # Size
        f.write((1).to_bytes(4, 'little'))    # Type (1 = model)
        
        # Entry 2
        f.write(b'prop1.prop\x00\x00\x00\x00\x00\x00\x00\x00')  # Name (20 bytes)
        f.write((300).to_bytes(4, 'little'))  # Offset
        f.write((150).to_bytes(4, 'little'))  # Size
        f.write((2).to_bytes(4, 'little'))    # Type (2 = prop)
    
    print(f"✅ Created test index file: {index_file} ({os.path.getsize(index_file)} bytes)")
    
    return {
        'moa': moa_file,
        'prop': prop_file,
        'pkb': pkb_file,
        'index': index_file
    }

def test_model_file_access():
    """Test if model files can be accessed via HTTP"""
    print("\n🔗 Testing Model File Access...")
    
    test_files = create_test_model_files()
    
    for file_type, file_path in test_files.items():
        filename = os.path.basename(file_path)
        url = f'http://localhost:8000/cache/{filename}'
        
        try:
            response = urllib.request.urlopen(url, timeout=5)
            if response.getcode() == 200:
                data = response.read()
                print(f"✅ {file_type.upper()} file accessible: {filename} ({len(data)} bytes)")
            else:
                print(f"❌ {file_type.upper()} file error: {response.getcode()}")
        except URLError as e:
            print(f"❌ {file_type.upper()} file not accessible: {e}")
    
    return True

def test_model_parsing_functions():
    """Test if model parsing functions exist and are callable"""
    print("\n🔧 Testing Model Parsing Functions...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for parsing functions
        parsing_checks = [
            ('parseMOA function', 'parseMOA:' in content and 'async (file)' in content),
            ('parseABC function', 'parseABC:' in content and 'async (file)' in content),
            ('ModelEditor component', 'ModelEditor = ({' in content),
            ('File processing', 'ArrayBuffer' in content),
            ('Binary data handling', 'DataView' in content or 'Uint8Array' in content),
            ('Vertex processing', 'vertices' in content and 'Float32Array' in content),
            ('Geometry creation', 'BufferGeometry' in content),
            ('Mesh creation', 'THREE.Mesh' in content),
        ]
        
        passed = 0
        for name, check in parsing_checks:
            if check:
                print(f"✅ {name}: Available")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(parsing_checks)) * 100
        print(f"📊 Parser Function Check: {passed}/{len(parsing_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ Parser Function Test Failed: {e}")
        return False

def test_three_js_integration():
    """Test THREE.js integration for 3D viewing"""
    print("\n🎮 Testing THREE.js Integration...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check THREE.js integration
        threejs_checks = [
            ('THREE.js Import', 'import * as THREE from' in content),
            ('OrbitControls Import', 'import { OrbitControls }' in content),
            ('Global THREE', 'window.THREE =' in content),
            ('Scene Creation', 'THREE.Scene' in content),
            ('Camera Setup', 'PerspectiveCamera' in content),
            ('Renderer Setup', 'WebGLRenderer' in content),
            ('Lighting System', 'AmbientLight' in content and 'DirectionalLight' in content),
            ('Material Support', 'MeshPhongMaterial' in content),
            ('Animation Loop', 'requestAnimationFrame' in content or 'render' in content),
            ('Controls Integration', 'OrbitControls' in content)
        ]
        
        passed = 0
        for name, check in threejs_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(threejs_checks)) * 100
        print(f"📊 THREE.js Integration: {passed}/{len(threejs_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ THREE.js Integration Test Failed: {e}")
        return False

def test_pkb_extraction_workflow():
    """Test PKB extraction workflow"""
    print("\n📦 Testing PKB Extraction Workflow...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check PKB extraction workflow
        extraction_checks = [
            ('PKB File Storage', 'MXO_PKB_FILES' in content or 'pkbFiles' in content),
            ('Index File Processing', 'packmap_save' in content),
            ('Extract Function', 'extractFromPKB' in content),
            ('File List Generation', 'PKB Files:' in content or 'files in PKB' in content),
            ('Individual Extraction', 'Extract & View' in content),
            ('Model Loading Button', 'Load Model' in content or 'View' in content),
            ('Progress Tracking', 'Extracting' in content or 'status' in content),
            ('Error Handling', 'Failed to extract' in content or 'Error:' in content)
        ]
        
        passed = 0
        for name, check in extraction_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(extraction_checks)) * 100
        print(f"📊 PKB Extraction Workflow: {passed}/{len(extraction_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ PKB Extraction Test Failed: {e}")
        return False

def test_export_functionality():
    """Test 3D model export functionality"""
    print("\n📤 Testing Export Functionality...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check export features
        export_checks = [
            ('Export to OBJ', 'exportToOBJ' in content),
            ('Export Button', 'Export OBJ' in content),
            ('Wavefront Format', 'Wavefront OBJ' in content or 'OBJ format' in content),
            ('Vertex Export', 'v ' in content or 'vertices' in content),
            ('Normal Export', 'vn ' in content or 'normals' in content),
            ('UV Export', 'vt ' in content or 'uvs' in content),
            ('Face Export', 'f ' in content or 'faces' in content),
            ('Download Function', 'download' in content and 'blob' in content)
        ]
        
        passed = 0
        for name, check in export_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(export_checks)) * 100
        print(f"📊 Export Functionality: {passed}/{len(export_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 75
        
    except Exception as e:
        print(f"❌ Export Functionality Test Failed: {e}")
        return False

def run_3d_model_tests():
    """Run all 3D model related tests"""
    print("🎯 MOMS 3D Model Extraction & Viewing Test Suite")
    print("=" * 60)
    
    tests = [
        ("Model File Access", test_model_file_access),
        ("Model Parsing Functions", test_model_parsing_functions),
        ("THREE.js Integration", test_three_js_integration),
        ("PKB Extraction Workflow", test_pkb_extraction_workflow),
        ("Export Functionality", test_export_functionality)
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
    
    print(f"\n📊 3D MODEL TEST RESULTS:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    print(f"\n📝 Detailed Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    if success_rate < 60:
        print("\n🚨 CRITICAL: 3D model functionality is severely limited!")
        print("🔧 ISSUES TO FIX:")
        print("- Model parsing functions may be broken")
        print("- THREE.js integration needs repair")
        print("- PKB extraction workflow needs implementation")
        return False
    elif success_rate < 80:
        print("\n⚠️ WARNING: Some 3D model features are not working properly.")
        print("🔧 RECOMMENDATIONS:")
        print("- Check failed components and implement missing features")
        print("- Test extraction with real Matrix Online files")
        return True
    else:
        print("\n🎉 EXCELLENT: 3D model extraction and viewing should work well!")
        print("✨ NEXT STEPS:")
        print("- Test with real Matrix Online PKB files")
        print("- Verify extraction and viewing in browser")
        return True

if __name__ == "__main__":
    success = run_3d_model_tests()
    sys.exit(0 if success else 1)
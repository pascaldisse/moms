#!/usr/bin/env python3
"""
Test the new .gob file analyzer functionality
"""

import urllib.request
import os
import sys

def test_gob_analyzer_functionality():
    """Test if .gob analyzer functionality is properly implemented"""
    print("🔬 Testing .gob File Analyzer Functionality...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for .gob analyzer components
        checks = [
            ('GameObject Analyzer Function', 'analyzeGobFileStructure' in content),
            ('Analysis Button', 'Analyze All .gob Files' in content),
            ('Hex Analysis', 'hexDump' in content and 'magicNumber' in content),
            ('String Pattern Detection', 'strings.push' in content),
            ('Repeated Pattern Detection', 'repeated patterns' in content.lower()),
            ('Data Field Analysis', 'possibleFields' in content),
            ('Modal Display', 'GameObject (.gob) File Analysis' in content),
            ('Analysis Insights', 'Analysis Insights' in content),
            ('Handle Function', 'handleGobAnalysis' in content),
            ('File Structure Analysis', 'fileSize' in content and 'header' in content)
        ]
        
        passed = 0
        for name, check in checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(checks)) * 100
        print(f"📊 .gob Analyzer Check: {passed}/{len(checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ .gob analyzer test failed: {e}")
        return False

def test_gob_analyzer_ui():
    """Test if .gob analyzer UI elements are properly structured"""
    print("\n🎨 Testing .gob Analyzer UI Elements...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for UI elements
        ui_checks = [
            ('Blue Alert Box', 'bg-blue-900 bg-opacity-20' in content),
            ('Analyzer Title', '🔬 .gob File Hex Analyzer' in content),
            ('Critical Info Box', '🔑 Critical: 44,000 GameObjects' in content),
            ('Button Styling', 'border-blue-500' in content),
            ('Modal Structure', 'fixed inset-0 z-50' in content),
            ('Analysis Content', 'gobAnalysisContent' in content),
            ('Color Coding', 'text-yellow-400' in content and 'text-blue-400' in content),
            ('Grid Layout', 'grid grid-cols' in content),
            ('Analysis Summary', 'Analysis Summary' in content),
            ('Expert Advice', 'Morpheus' in content)
        ]
        
        passed = 0
        for name, check in ui_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(ui_checks)) * 100
        print(f"📊 UI Elements Check: {passed}/{len(ui_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ UI elements test failed: {e}")
        return False

def test_hex_analysis_capabilities():
    """Test if hex analysis capabilities are comprehensive"""
    print("\n🔍 Testing Hex Analysis Capabilities...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for analysis features
        analysis_checks = [
            ('Magic Number Detection', 'magicNumber' in content),
            ('Header Analysis', 'hexDump' in content),
            ('String Extraction', 'null-terminated ASCII' in content),
            ('Data Type Detection', 'uint32_le' in content and 'float32' in content),
            ('Pattern Recognition', 'repeated structures' in content),
            ('Offset Analysis', 'commonOffsets' in content),
            ('File Size Analysis', 'fileSize' in content),
            ('Version Detection', 'possibleVersion' in content),
            ('Hex Formatting', 'toString(16)' in content),
            ('Binary Processing', 'ArrayBuffer' in content and 'DataView' in content)
        ]
        
        passed = 0
        for name, check in analysis_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(analysis_checks)) * 100
        print(f"📊 Analysis Capabilities: {passed}/{len(analysis_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ Analysis capabilities test failed: {e}")
        return False

def create_test_gob_file():
    """Create a test .gob file for analysis"""
    print("\n📁 Creating Test .gob File...")
    
    try:
        # Create cache directory if it doesn't exist
        cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        # Create a synthetic .gob file with realistic structure
        gob_file = os.path.join(cache_dir, 'test_gameobject.gob')
        
        with open(gob_file, 'wb') as f:
            # Magic number (fake GameObject signature)
            f.write(b'GOBJ')
            
            # Version
            f.write((1).to_bytes(4, 'little'))
            
            # File size placeholder
            f.write((256).to_bytes(4, 'little'))
            
            # Object ID
            f.write((12345).to_bytes(4, 'little'))
            
            # Position (floats)
            import struct
            f.write(struct.pack('<f', 100.5))  # X
            f.write(struct.pack('<f', 200.0))  # Y
            f.write(struct.pack('<f', 50.25))  # Z
            
            # Rotation (floats)
            f.write(struct.pack('<f', 0.0))    # Pitch
            f.write(struct.pack('<f', 1.5708)) # Yaw (90 degrees)
            f.write(struct.pack('<f', 0.0))    # Roll
            
            # Scale
            f.write(struct.pack('<f', 1.0))
            
            # String data
            object_name = b'TestGameObject\x00'
            f.write(object_name)
            
            class_name = b'Prop\x00'
            f.write(class_name)
            
            script_name = b'default_script.lua\x00'
            f.write(script_name)
            
            # Padding and additional data
            f.write(b'\x00' * (256 - f.tell()))
        
        file_size = os.path.getsize(gob_file)
        print(f"✅ Created test .gob file: {gob_file} ({file_size} bytes)")
        
        # Verify file is accessible via HTTP
        try:
            response = urllib.request.urlopen('http://localhost:8000/cache/test_gameobject.gob', timeout=5)
            if response.getcode() == 200:
                print("✅ Test .gob file accessible via HTTP")
                return True
            else:
                print(f"❌ Test .gob file HTTP error: {response.getcode()}")
                return False
        except Exception as e:
            print(f"❌ Test .gob file not accessible: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Failed to create test .gob file: {e}")
        return False

def run_gob_analyzer_tests():
    """Run all .gob analyzer tests"""
    print("🔬 MOMS .gob File Analyzer Test Suite")
    print("=" * 50)
    
    all_issues = []
    
    # Test 1: Core functionality
    print("\n1. CORE FUNCTIONALITY")
    func_working = test_gob_analyzer_functionality()
    if not func_working:
        all_issues.append("Core .gob analyzer functionality missing")
    
    # Test 2: UI elements
    print("\n2. UI ELEMENTS")
    ui_working = test_gob_analyzer_ui()
    if not ui_working:
        all_issues.append("UI elements missing or incomplete")
    
    # Test 3: Analysis capabilities
    print("\n3. ANALYSIS CAPABILITIES")
    analysis_working = test_hex_analysis_capabilities()
    if not analysis_working:
        all_issues.append("Hex analysis capabilities incomplete")
    
    # Test 4: Test file creation
    print("\n4. TEST FILE CREATION")
    file_created = create_test_gob_file()
    if not file_created:
        all_issues.append("Test .gob file creation failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 .GOB ANALYZER TEST SUMMARY")
    
    if not all_issues:
        print("✅ All .gob analyzer tests passed!")
        print("🎯 Ready to analyze GameObject files")
        print("💡 Navigate to GameObjects tab and click 'Analyze All .gob Files'")
        return True
    else:
        print(f"❌ Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 RECOMMENDATIONS:")
        if any("functionality" in issue for issue in all_issues):
            print("   - Check analyzeGobFileStructure function implementation")
            print("   - Verify handleGobAnalysis function is properly connected")
        
        if any("UI" in issue for issue in all_issues):
            print("   - Check button styling and modal structure")
            print("   - Verify all UI elements are properly rendered")
        
        if any("analysis" in issue for issue in all_issues):
            print("   - Implement missing hex analysis features")
            print("   - Add comprehensive binary data processing")
        
        return False

if __name__ == "__main__":
    success = run_gob_analyzer_tests()
    sys.exit(0 if success else 1)
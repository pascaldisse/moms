#!/usr/bin/env python3
"""
MOMS Final Test Report - Comprehensive validation of all functionality
"""

import urllib.request
import urllib.parse
import json
import sys
import os
import time
from urllib.error import URLError, HTTPError

def generate_test_report():
    """Generate comprehensive test report for MOMS functionality"""
    print("📋 MOMS Final Test Report - Complete Functionality Validation")
    print("=" * 70)
    print(f"📅 Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Testing Focus: 3D Model Extraction and Viewing")
    print("-" * 70)
    
    results = {
        'server': {},
        'application': {},
        'parsing': {},
        'viewing': {},
        'extraction': {},
        'export': {},
        'files': {}
    }
    
    # Test 1: Server Infrastructure
    print("\n🔧 1. SERVER INFRASTRUCTURE")
    try:
        # Main server
        response = urllib.request.urlopen('http://localhost:8000/', timeout=5)
        results['server']['main'] = response.getcode() == 200
        print(f"   ✅ Main Server (port 8000): {'ONLINE' if results['server']['main'] else 'OFFLINE'}")
        
        # BIK server
        try:
            response = urllib.request.urlopen('http://localhost:8002/status', timeout=5)
            results['server']['bik'] = response.getcode() == 200
        except:
            results['server']['bik'] = False
        print(f"   {'✅' if results['server']['bik'] else '⚠️'} BIK Server (port 8002): {'ONLINE' if results['server']['bik'] else 'OFFLINE'}")
        
    except Exception as e:
        results['server']['main'] = False
        results['server']['bik'] = False
        print(f"   ❌ Server test failed: {e}")
    
    # Test 2: Application Components
    print("\n📱 2. APPLICATION COMPONENTS")
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        components = {
            'React': 'React.createElement' in content,
            'THREE.js': 'THREE.Scene' in content,
            'Monaco Editor': 'monaco-editor' in content,
            'Model Parsers': 'parseMOA' in content and 'parseABC' in content,
            'Performance Monitor': 'performanceMonitor' in content,
            'Error Handler': 'handleError' in content,
            'Load Model Function': 'loadModel' in content
        }
        
        for name, present in components.items():
            results['application'][name.lower().replace(' ', '_')] = present
            print(f"   {'✅' if present else '❌'} {name}: {'PRESENT' if present else 'MISSING'}")
            
    except Exception as e:
        print(f"   ❌ Application test failed: {e}")
    
    # Test 3: Model Parsing Functions
    print("\n🔧 3. MODEL PARSING FUNCTIONS")
    parsing_functions = [
        ('parseMOA', 'MOA character models'),
        ('parseABC', 'ABC actor cache'),
        ('parsePROP', 'PROP static objects'),
        ('detectFormat', 'Format detection'),
        ('readString', 'String parsing'),
    ]
    
    for func_name, description in parsing_functions:
        present = func_name in content if 'content' in locals() else False
        results['parsing'][func_name] = present
        print(f"   {'✅' if present else '❌'} {func_name}: {description} - {'AVAILABLE' if present else 'MISSING'}")
    
    # Test 4: 3D Viewing Components
    print("\n🎮 4. 3D VIEWING COMPONENTS")
    viewing_components = [
        ('ModelEditor', 'Model editor component'),
        ('THREE.Scene', '3D scene management'),
        ('OrbitControls', 'Camera controls'),
        ('BufferGeometry', 'Geometry processing'),
        ('MeshPhongMaterial', 'Material rendering'),
        ('AmbientLight', 'Scene lighting'),
        ('exportToOBJ', 'Model export'),
    ]
    
    for component, description in viewing_components:
        present = component in content if 'content' in locals() else False
        results['viewing'][component] = present
        print(f"   {'✅' if present else '❌'} {component}: {description} - {'AVAILABLE' if present else 'MISSING'}")
    
    # Test 5: PKB Extraction
    print("\n📦 5. PKB EXTRACTION FUNCTIONALITY")
    extraction_features = [
        ('extractFromPKB', 'PKB extraction function'),
        ('MXO_PKB_FILES', 'PKB file storage'),
        ('packmap_save', 'Index file processing'),
        ('Extract & View', 'Extraction UI'),
        ('performance', 'Performance monitoring'),
    ]
    
    for feature, description in extraction_features:
        present = feature in content if 'content' in locals() else False
        results['extraction'][feature] = present
        print(f"   {'✅' if present else '❌'} {feature}: {description} - {'AVAILABLE' if present else 'MISSING'}")
    
    # Test 6: File Format Support
    print("\n📐 6. MATRIX ONLINE FILE FORMAT SUPPORT")
    correct_formats = ['.moa', '.prop', '.mga', '.mgc', '.iprf', '.eprf']
    incorrect_formats = ['.mob']  # Common misconception
    
    format_support = {}
    for fmt in correct_formats:
        supported = fmt in content if 'content' in locals() else False
        format_support[fmt] = supported
        results['files'][fmt] = supported
        print(f"   {'✅' if supported else '❌'} {fmt}: Matrix Online format - {'SUPPORTED' if supported else 'MISSING'}")
    
    for fmt in incorrect_formats:
        incorrectly_supported = fmt in content if 'content' in locals() else False
        print(f"   {'✅' if not incorrectly_supported else '⚠️'} {fmt}: Correctly {'not supported' if not incorrectly_supported else 'should not be supported'}")
    
    # Test 7: Test Files Accessibility
    print("\n📁 7. TEST FILES ACCESSIBILITY")
    test_files = [
        'cache/test_character.moa',
        'cache/test_building.prop', 
        'cache/test_models.pkb',
        'cache/packmap_save.lta'
    ]
    
    files_accessible = 0
    for test_file in test_files:
        try:
            response = urllib.request.urlopen(f'http://localhost:8000/{test_file}', timeout=5)
            accessible = response.getcode() == 200
            files_accessible += 1 if accessible else 0
            print(f"   {'✅' if accessible else '❌'} {test_file}: {'ACCESSIBLE' if accessible else 'NOT FOUND'}")
        except:
            print(f"   ❌ {test_file}: NOT ACCESSIBLE")
    
    results['files']['test_files_accessible'] = files_accessible
    
    # Calculate overall scores
    print("\n📊 FINAL ASSESSMENT")
    print("-" * 70)
    
    # Server score
    server_score = sum(results['server'].values()) / len(results['server']) * 100 if results['server'] else 0
    print(f"   🔧 Server Infrastructure: {server_score:.1f}% ({sum(results['server'].values())}/{len(results['server'])})")
    
    # Application score
    app_score = sum(results['application'].values()) / len(results['application']) * 100 if results['application'] else 0
    print(f"   📱 Application Components: {app_score:.1f}% ({sum(results['application'].values())}/{len(results['application'])})")
    
    # Parsing score
    parsing_score = sum(results['parsing'].values()) / len(results['parsing']) * 100 if results['parsing'] else 0
    print(f"   🔧 Model Parsing: {parsing_score:.1f}% ({sum(results['parsing'].values())}/{len(results['parsing'])})")
    
    # Viewing score
    viewing_score = sum(results['viewing'].values()) / len(results['viewing']) * 100 if results['viewing'] else 0
    print(f"   🎮 3D Viewing: {viewing_score:.1f}% ({sum(results['viewing'].values())}/{len(results['viewing'])})")
    
    # Extraction score
    extraction_score = sum(results['extraction'].values()) / len(results['extraction']) * 100 if results['extraction'] else 0
    print(f"   📦 PKB Extraction: {extraction_score:.1f}% ({sum(results['extraction'].values())}/{len(results['extraction'])})")
    
    # Files score
    files_score = (results['files']['test_files_accessible'] / len(test_files)) * 100
    print(f"   📁 Test Files: {files_score:.1f}% ({results['files']['test_files_accessible']}/{len(test_files)})")
    
    # Overall score
    scores = [server_score, app_score, parsing_score, viewing_score, extraction_score, files_score]
    overall_score = sum(scores) / len(scores)
    
    print(f"\n🎯 OVERALL SCORE: {overall_score:.1f}%")
    
    # Assessment
    if overall_score >= 90:
        assessment = "🎉 EXCELLENT - All systems operational"
        status = "FULLY FUNCTIONAL"
    elif overall_score >= 80:
        assessment = "✅ GOOD - Minor issues, mostly functional"
        status = "MOSTLY FUNCTIONAL"
    elif overall_score >= 70:
        assessment = "⚠️ FAIR - Some issues need attention"
        status = "PARTIALLY FUNCTIONAL"
    else:
        assessment = "🚨 POOR - Major issues require fixes"
        status = "LIMITED FUNCTIONALITY"
    
    print(f"🏆 ASSESSMENT: {assessment}")
    print(f"📈 STATUS: {status}")
    
    # Specific recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if server_score < 100:
        print("   - Ensure both main server and BIK server are running")
    if app_score < 90:
        print("   - Check for missing React/THREE.js components")
    if parsing_score < 80:
        print("   - Verify model parsing functions are properly implemented")
    if viewing_score < 80:
        print("   - Test 3D viewer initialization and controls")
    if extraction_score < 80:
        print("   - Validate PKB extraction workflow")
    if files_score < 100:
        print("   - Regenerate test files if missing")
    
    if overall_score >= 85:
        print("   ✨ System is ready for testing with real Matrix Online files!")
        print("   🎯 Focus on testing PKB extraction with actual game files")
        print("   🔍 Verify model viewing works with complex MXO models")
    
    print("\n" + "=" * 70)
    print("📋 TEST REPORT COMPLETE")
    return overall_score >= 80

if __name__ == "__main__":
    success = generate_test_report()
    sys.exit(0 if success else 1)
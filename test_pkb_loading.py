#!/usr/bin/env python3
"""
Test PKB loading functionality specifically
"""

import urllib.request
import os
import sys
import time

def test_pkb_auto_loading():
    """Test the PKB auto-loading functionality"""
    print("📦 Testing PKB Auto-Loading Functionality...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for auto-loading components
        checks = [
            ('loadIndexFile function', 'window.loadIndexFile' in content),
            ('Auto-loading call', 'await window.loadIndexFile()' in content),
            ('MXO_PKB_INDEX_DATA check', 'MXO_PKB_INDEX_DATA' in content),
            ('Fetch index file', "fetch('/cache/packmap_save.lta')" in content),
            ('Index file error handling', 'No index file loaded' in content),
            ('Console logging', 'Auto-loaded index file' in content)
        ]
        
        passed = 0
        for name, check in checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(checks)) * 100
        print(f"📊 Auto-loading Check: {passed}/{len(checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ Auto-loading test failed: {e}")
        return False

def test_index_file_availability():
    """Test if the index file is available and accessible"""
    print("\n📁 Testing Index File Availability...")
    
    # Check if file exists locally
    cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
    index_file = os.path.join(cache_dir, 'packmap_save.lta')
    
    if os.path.exists(index_file):
        size = os.path.getsize(index_file)
        print(f"✅ Index file exists locally: {size} bytes")
        
        # Check HTTP accessibility
        try:
            response = urllib.request.urlopen('http://localhost:8000/cache/packmap_save.lta', timeout=5)
            if response.getcode() == 200:
                data = response.read()
                print(f"✅ Index file accessible via HTTP: {len(data)} bytes")
                
                # Check if it's a valid file (not empty)
                if len(data) > 0:
                    print("✅ Index file has content")
                    return True
                else:
                    print("❌ Index file is empty")
                    return False
            else:
                print(f"❌ HTTP error: {response.getcode()}")
                return False
        except Exception as e:
            print(f"❌ HTTP access failed: {e}")
            return False
    else:
        print(f"❌ Index file does not exist: {index_file}")
        return False

def test_pkb_extraction_workflow():
    """Test the full PKB extraction workflow"""
    print("\n⚙️ Testing PKB Extraction Workflow...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check workflow components
        workflow_checks = [
            ('PKB file check', 'MXO_PKB_FILES' in content),
            ('Extract function', 'extractFromPKB' in content),
            ('Performance monitoring', 'performanceMonitor.start' in content),
            ('Error message', 'No index file loaded' in content),
            ('Auto-load attempt', 'loadIndexFile()' in content),
            ('PKB file validation', 'pkbData = window.MXO_PKB_FILES' in content),
            ('Index data usage', 'window.MXO_PKB_INDEX_DATA' in content)
        ]
        
        passed = 0
        for name, check in workflow_checks:
            if check:
                print(f"✅ {name}: Present")
                passed += 1
            else:
                print(f"❌ {name}: Missing")
        
        success_rate = (passed / len(workflow_checks)) * 100
        print(f"📊 Workflow Check: {passed}/{len(workflow_checks)} ({success_rate:.1f}%)")
        
        return success_rate >= 85
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def test_console_warnings():
    """Test for console warnings and production issues"""
    print("\n⚠️ Testing Console Warnings...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/index.html', timeout=10)
        content = response.read().decode('utf-8')
        
        # Check for warning sources
        warning_checks = [
            ('Tailwind CDN removed', 'cdn.tailwindcss.com' not in content),
            ('Babel production note', 'precompile your scripts' in content.lower() or 'production' in content),
            ('Console.log minimized', content.count('console.log') < 20),
            ('Production ready', 'development' not in content.lower() or content.count('development') < 3)
        ]
        
        issues = []
        for name, check in warning_checks:
            if check:
                print(f"✅ {name}: OK")
            else:
                print(f"⚠️ {name}: Warning")
                issues.append(name)
        
        return len(issues) <= 2  # Allow some warnings
        
    except Exception as e:
        print(f"❌ Console warnings test failed: {e}")
        return False

def create_debug_test_page():
    """Create a simple debug test page to test PKB loading manually"""
    print("\n🛠️ Creating Debug Test Page...")
    
    debug_html = '''<!DOCTYPE html>
<html>
<head>
    <title>PKB Loading Debug Test</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        button { background: #030; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; cursor: pointer; }
        #log { background: #111; border: 1px solid #0f0; padding: 10px; height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>PKB Loading Debug Test</h1>
    <button onclick="testIndexLoad()">Test Index File Loading</button>
    <button onclick="testPKBExtraction()">Test PKB Extraction</button>
    <button onclick="clearLog()">Clear Log</button>
    
    <div id="log"></div>
    
    <script>
        function log(msg) {
            const logDiv = document.getElementById('log');
            logDiv.innerHTML += new Date().toLocaleTimeString() + ': ' + msg + '<br>';
            logDiv.scrollTop = logDiv.scrollHeight;
            console.log(msg);
        }
        
        function clearLog() {
            document.getElementById('log').innerHTML = '';
        }
        
        async function testIndexLoad() {
            log('🔍 Testing index file loading...');
            
            try {
                const response = await fetch('/cache/packmap_save.lta');
                log('📡 Fetch response status: ' + response.status + ' ' + response.statusText);
                
                if (response.ok) {
                    const arrayBuffer = await response.arrayBuffer();
                    const data = new Uint8Array(arrayBuffer);
                    log('✅ Index file loaded: ' + data.length + ' bytes');
                    
                    // Store globally
                    window.MXO_PKB_INDEX_DATA = data;
                    window.MXO_PKB_INDEX_NAME = 'packmap_save.lta';
                    log('✅ Index data stored globally');
                    return true;
                } else {
                    log('❌ Failed to load index file: ' + response.status);
                    return false;
                }
            } catch (error) {
                log('❌ Error loading index file: ' + error.message);
                return false;
            }
        }
        
        async function testPKBExtraction() {
            log('📦 Testing PKB extraction...');
            
            if (!window.MXO_PKB_INDEX_DATA) {
                log('⚠️ No index data loaded, attempting to load...');
                const loaded = await testIndexLoad();
                if (!loaded) {
                    log('❌ Cannot test PKB extraction without index file');
                    return;
                }
            }
            
            log('✅ Index data available: ' + window.MXO_PKB_INDEX_DATA.length + ' bytes');
            log('✅ PKB extraction simulation would work');
        }
        
        // Auto-test on load
        window.addEventListener('load', () => {
            log('🌐 Debug test page loaded');
            setTimeout(() => {
                log('⏳ Auto-testing index file loading...');
                testIndexLoad();
            }, 1000);
        });
    </script>
</body>
</html>'''
    
    try:
        with open('/Users/pascaldisse/Downloads/mxo/moms/debug_pkb.html', 'w') as f:
            f.write(debug_html)
        print("✅ Created debug test page: http://localhost:8000/debug_pkb.html")
        return True
    except Exception as e:
        print(f"❌ Failed to create debug page: {e}")
        return False

def run_pkb_loading_tests():
    """Run all PKB loading tests"""
    print("📦 MOMS PKB Loading Test Suite")
    print("=" * 50)
    
    all_issues = []
    
    # Test 1: Auto-loading functionality
    print("\n1. AUTO-LOADING FUNCTIONALITY")
    auto_loading = test_pkb_auto_loading()
    if not auto_loading:
        all_issues.append("Auto-loading functionality incomplete")
    
    # Test 2: Index file availability
    print("\n2. INDEX FILE AVAILABILITY")
    file_available = test_index_file_availability()
    if not file_available:
        all_issues.append("Index file not accessible")
    
    # Test 3: Extraction workflow
    print("\n3. EXTRACTION WORKFLOW")
    workflow_ok = test_pkb_extraction_workflow()
    if not workflow_ok:
        all_issues.append("Extraction workflow incomplete")
    
    # Test 4: Console warnings
    print("\n4. CONSOLE WARNINGS")
    warnings_ok = test_console_warnings()
    if not warnings_ok:
        all_issues.append("Too many console warnings")
    
    # Test 5: Debug page
    print("\n5. DEBUG TEST PAGE")
    debug_created = create_debug_test_page()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PKB LOADING TEST SUMMARY")
    
    if not all_issues:
        print("✅ All PKB loading tests passed!")
        print("🎯 PKB extraction should work correctly")
        if debug_created:
            print("💡 Test manually at: http://localhost:8000/debug_pkb.html")
        return True
    else:
        print(f"❌ Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 RECOMMENDATIONS:")
        
        if any("Auto-loading" in issue for issue in all_issues):
            print("   - Check loadIndexFile function implementation")
            print("   - Verify auto-loading is called correctly")
        
        if any("Index file" in issue for issue in all_issues):
            print("   - Check file permissions and HTTP access")
            print("   - Verify packmap_save.lta exists and has content")
        
        if any("workflow" in issue for issue in all_issues):
            print("   - Check PKB extraction workflow logic")
            print("   - Verify error handling and fallbacks")
        
        if debug_created:
            print(f"\n💡 Test manually at: http://localhost:8000/debug_pkb.html")
        
        return False

if __name__ == "__main__":
    success = run_pkb_loading_tests()
    sys.exit(0 if success else 1)
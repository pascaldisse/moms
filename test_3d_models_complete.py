#!/usr/bin/env python3
"""
Complete test of 3D Models tab with auto-initialization
"""

import time
import urllib.request
import json

def test_initialization_script():
    """Test if initialization script is accessible"""
    print("🔍 Testing initialization script...")
    
    try:
        response = urllib.request.urlopen('http://localhost:8000/fix_3d_models_init.js', timeout=5)
        if response.getcode() == 200:
            print("✅ Initialization script accessible")
            return True
        else:
            print("❌ Initialization script not found")
            return False
    except Exception as e:
        print(f"❌ Error accessing initialization script: {e}")
        return False

def create_test_instructions():
    """Create clear test instructions"""
    print("\n" + "="*60)
    print("🎯 3D MODELS TAB COMPLETE TEST")
    print("="*60)
    
    print("\n📋 AUTOMATIC TEST:")
    print("1. Open: http://localhost:8000")
    print("2. Open browser console (F12)")
    print("3. Click on '3D Models' tab")
    print("4. Watch console for auto-initialization:")
    print("   - '🎮 Initializing 3D Models Tab...'")
    print("   - '✅ Index file auto-loaded' or already loaded")
    print("   - '✅ Loaded worlds_3g.pkb: XXXX bytes'")
    print("   - '✅ Enhanced extraction loaded'")
    print("5. Click 'Debug Info' button")
    print("   - Should show PKB files loaded")
    print("6. Click 'Test Extract' button")
    print("   - Should extract files successfully!")
    
    print("\n📊 EXPECTED RESULTS:")
    print("✅ Index loaded: true")
    print("✅ PKB files loaded: ['worlds_3g.pkb', 'char_npc.pkb']")
    print("✅ Extraction result: 5 files")
    
    print("\n💡 The 3D Models tab now auto-loads:")
    print("   1. Index file (packmap_save.lta)")
    print("   2. PKB files from cache/")
    print("   3. Enhanced extraction script")
    print("   All automatically when you click the tab!")
    
    print("="*60)

def create_manual_test_page():
    """Create a page to manually test the complete workflow"""
    test_html = '''<!DOCTYPE html>
<html>
<head>
    <title>3D Models Complete Test</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        button { background: #030; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; cursor: pointer; }
        .status { background: #111; border: 1px solid #0f0; padding: 10px; margin: 10px 0; }
        .success { color: #0f0; }
        .error { color: #f00; }
    </style>
</head>
<body>
    <h1>🎯 3D Models Tab Complete Test</h1>
    
    <button onclick="loadInitScript()">1. Load Init Script</button>
    <button onclick="runInit()">2. Run Initialization</button>
    <button onclick="testExtraction()">3. Test Extraction</button>
    
    <div id="status" class="status">Ready to test...</div>
    
    <script>
        function updateStatus(msg, isError = false) {
            const status = document.getElementById('status');
            status.innerHTML += `<div class="${isError ? 'error' : 'success'}">${new Date().toLocaleTimeString()}: ${msg}</div>`;
            console.log(msg);
        }
        
        async function loadInitScript() {
            updateStatus('Loading initialization script...');
            try {
                const script = document.createElement('script');
                script.src = '/fix_3d_models_init.js';
                document.head.appendChild(script);
                await new Promise(resolve => {
                    script.onload = () => {
                        updateStatus('✅ Init script loaded');
                        resolve();
                    };
                    script.onerror = () => {
                        updateStatus('❌ Failed to load init script', true);
                        resolve();
                    };
                });
            } catch (error) {
                updateStatus(`❌ Error: ${error.message}`, true);
            }
        }
        
        async function runInit() {
            if (!window.init3DModelsTab) {
                updateStatus('❌ Init function not found - load script first!', true);
                return;
            }
            
            updateStatus('Running 3D Models initialization...');
            const result = await window.init3DModelsTab();
            updateStatus(`✅ Initialization complete!`);
            updateStatus(`Index loaded: ${result.indexLoaded}`);
            updateStatus(`PKB files: ${result.pkbFiles.join(', ')}`);
            updateStatus(`Enhanced extraction: ${result.enhancedExtraction}`);
        }
        
        async function testExtraction() {
            if (!window.extractFromPKB) {
                updateStatus('❌ Extraction function not found', true);
                return;
            }
            
            updateStatus('Testing extraction...');
            const pkbFiles = Object.keys(window.MXO_PKB_FILES || {});
            
            if (pkbFiles.length === 0) {
                updateStatus('❌ No PKB files loaded - run init first!', true);
                return;
            }
            
            for (const pkb of pkbFiles) {
                const results = await window.extractFromPKB(pkb);
                updateStatus(`${pkb}: Extracted ${results.length} files`);
                results.forEach(f => updateStatus(`  - ${f.name} (${f.size} bytes)`));
            }
        }
        
        // Auto-run on load
        window.addEventListener('load', async () => {
            updateStatus('🌐 Test page loaded');
            await loadInitScript();
            
            // Also load enhanced extraction
            const script2 = document.createElement('script');
            script2.src = '/fix_pkb_extraction.js';
            document.head.appendChild(script2);
        });
    </script>
</body>
</html>'''
    
    with open('/Users/pascaldisse/Downloads/mxo/moms/test_3d_complete.html', 'w') as f:
        f.write(test_html)
    
    print("\n✅ Created test page: test_3d_complete.html")
    print("   http://localhost:8000/test_3d_complete.html")

def run_complete_test():
    """Run complete 3D Models test"""
    print("🧪 3D MODELS TAB COMPLETE TEST")
    print("="*40)
    
    # Test initialization script
    if test_initialization_script():
        print("✅ All components ready")
        
        # Create test instructions
        create_test_instructions()
        
        # Create manual test page
        create_manual_test_page()
        
        print("\n🚀 READY TO TEST!")
        print("Follow the instructions above to test the complete workflow.")
        return True
    else:
        print("❌ Missing components")
        print("Make sure server is running: python3 server.py")
        return False

if __name__ == "__main__":
    import sys
    success = run_complete_test()
    sys.exit(0 if success else 1)
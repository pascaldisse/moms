#!/usr/bin/env python3
"""
Test and apply the enhanced PKB extraction fix
"""

import os
import sys
import shutil
from datetime import datetime

def backup_index_file():
    """Create a backup of index.html before applying fixes"""
    print("📁 Creating backup of index.html...")
    src = '/Users/pascaldisse/Downloads/mxo/moms/index.html'
    dst = f'/Users/pascaldisse/Downloads/mxo/moms/index_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html.bak'
    
    try:
        shutil.copy2(src, dst)
        print(f"✅ Backup created: {dst}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def inject_enhanced_extraction():
    """Inject the enhanced extraction function into index.html"""
    print("\n💉 Injecting enhanced PKB extraction...")
    
    # Read the fix
    with open('/Users/pascaldisse/Downloads/mxo/moms/fix_pkb_extraction.js', 'r') as f:
        fix_code = f.read()
    
    # Read index.html
    with open('/Users/pascaldisse/Downloads/mxo/moms/index.html', 'r') as f:
        content = f.read()
    
    # Find where to inject (after the extractFromPKB function)
    inject_marker = "window.extractFromPKB = async (pkbFileName) => {"
    if inject_marker in content:
        # Find the end of the function
        start_pos = content.find(inject_marker)
        brace_count = 0
        pos = start_pos
        
        # Skip to the opening brace
        while pos < len(content) and content[pos] != '{':
            pos += 1
        
        # Find matching closing brace
        while pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    pos += 1
                    break
            pos += 1
        
        # Find the semicolon after the function
        while pos < len(content) and content[pos] in ' \n\t':
            pos += 1
        if pos < len(content) and content[pos] == ';':
            pos += 1
        
        # Inject our enhanced version after the original
        new_content = content[:pos] + '\n\n' + fix_code + '\n\n' + content[pos:]
        
        # Write back
        with open('/Users/pascaldisse/Downloads/mxo/moms/index.html', 'w') as f:
            f.write(new_content)
        
        print("✅ Enhanced extraction injected successfully")
        return True
    else:
        print("❌ Could not find injection point")
        return False

def add_debug_buttons():
    """Add debug buttons to the 3D Models tab"""
    print("\n🔧 Adding debug buttons...")
    
    with open('/Users/pascaldisse/Downloads/mxo/moms/index.html', 'r') as f:
        content = f.read()
    
    # Find the Extract All Models button
    button_marker = 'onClick={extractAllModels}>Extract All Models</button>'
    
    if button_marker in content:
        # Add debug buttons after it
        debug_buttons = '''
                                <button 
                                    className="bg-green-900 text-green-100 px-4 py-2 rounded ml-2"
                                    onClick={() => {
                                        console.log('🔍 === PKB DEBUG INFO ===');
                                        console.log('Index loaded:', !!window.MXO_PKB_INDEX_DATA);
                                        console.log('Index size:', window.MXO_PKB_INDEX_DATA?.length || 0);
                                        console.log('PKB files loaded:', Object.keys(window.MXO_PKB_FILES || {}));
                                        console.log('PKB sizes:', Object.entries(window.MXO_PKB_FILES || {}).map(([k,v]) => `${k}: ${v.byteLength} bytes`));
                                        console.log('======================');
                                    }}
                                >
                                    Debug Info
                                </button>
                                <button 
                                    className="bg-green-900 text-green-100 px-4 py-2 rounded ml-2"
                                    onClick={async () => {
                                        console.log('🧪 Testing single PKB extraction...');
                                        const pkbs = Object.keys(window.MXO_PKB_FILES || {});
                                        if (pkbs.length > 0) {
                                            const result = await window.extractFromPKB(pkbs[0]);
                                            console.log('Extraction result:', result);
                                        } else {
                                            console.log('❌ No PKB files loaded to test');
                                        }
                                    }}
                                >
                                    Test Extract
                                </button>'''
        
        content = content.replace(button_marker, button_marker + debug_buttons)
        
        with open('/Users/pascaldisse/Downloads/mxo/moms/index.html', 'w') as f:
            f.write(content)
        
        print("✅ Debug buttons added")
        return True
    else:
        print("❌ Could not find button location")
        return False

def create_test_page():
    """Create a comprehensive test page"""
    print("\n📄 Creating comprehensive test page...")
    
    test_html = '''<!DOCTYPE html>
<html>
<head>
    <title>PKB Extraction Test Suite</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        button { background: #030; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; cursor: pointer; }
        button:hover { background: #050; }
        .section { background: #001100; border: 1px solid #0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
        #log { background: #111; border: 1px solid #0f0; padding: 10px; height: 400px; overflow-y: auto; font-size: 12px; }
        .success { color: #0f0; }
        .error { color: #f00; }
        .warning { color: #ff0; }
        .info { color: #0ff; }
    </style>
</head>
<body>
    <h1>🧪 PKB Extraction Test Suite</h1>
    
    <div class="section">
        <h3>📋 Step 1: Load Test Files</h3>
        <button onclick="loadTestIndex()">Load Test Index (packmap_save.lta)</button>
        <button onclick="loadTestPKB('worlds_3g.pkb')">Load worlds_3g.pkb</button>
        <button onclick="loadTestPKB('char_npc.pkb')">Load char_npc.pkb</button>
        <button onclick="checkStatus()">Check Status</button>
    </div>
    
    <div class="section">
        <h3>🔍 Step 2: Test Extraction</h3>
        <button onclick="testExtraction('worlds_3g.pkb')">Extract from worlds_3g.pkb</button>
        <button onclick="testExtraction('char_npc.pkb')">Extract from char_npc.pkb</button>
        <button onclick="testAllExtraction()">Extract All Models</button>
    </div>
    
    <div class="section">
        <h3>🛠️ Step 3: Debug Tools</h3>
        <button onclick="dumpIndexHeader()">Dump Index Header</button>
        <button onclick="dumpPKBHeaders()">Dump PKB Headers</button>
        <button onclick="clearLog()">Clear Log</button>
    </div>
    
    <h3>📝 Activity Log</h3>
    <div id="log"></div>
    
    <script>
        function log(msg, type = 'info') {
            const logDiv = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            const color = {
                success: '#0f0',
                error: '#f00',
                warning: '#ff0',
                info: '#0ff'
            }[type] || '#ccc';
            
            logDiv.innerHTML += `<div style="color: ${color};">[${timestamp}] ${msg}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
            console.log(`[${type.toUpperCase()}] ${msg}`);
        }
        
        function clearLog() {
            document.getElementById('log').innerHTML = '';
            log('Log cleared', 'info');
        }
        
        async function loadTestIndex() {
            log('Loading test index file...', 'info');
            try {
                const response = await fetch('/cache/packmap_save.lta');
                if (response.ok) {
                    const arrayBuffer = await response.arrayBuffer();
                    window.MXO_PKB_INDEX_DATA = new Uint8Array(arrayBuffer);
                    window.MXO_PKB_INDEX_NAME = 'packmap_save.lta';
                    log(`✅ Index loaded: ${window.MXO_PKB_INDEX_DATA.length} bytes`, 'success');
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
            } catch (error) {
                log(`❌ Failed to load index: ${error.message}`, 'error');
            }
        }
        
        async function loadTestPKB(filename) {
            log(`Loading PKB file: ${filename}...`, 'info');
            try {
                const response = await fetch(`/cache/${filename}`);
                if (response.ok) {
                    const arrayBuffer = await response.arrayBuffer();
                    window.MXO_PKB_FILES = window.MXO_PKB_FILES || {};
                    window.MXO_PKB_FILES[filename.toLowerCase()] = arrayBuffer;
                    log(`✅ PKB loaded: ${filename} (${arrayBuffer.byteLength} bytes)`, 'success');
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
            } catch (error) {
                log(`❌ Failed to load PKB: ${error.message}`, 'error');
            }
        }
        
        function checkStatus() {
            log('=== STATUS CHECK ===', 'info');
            log(`Index loaded: ${!!window.MXO_PKB_INDEX_DATA}`, window.MXO_PKB_INDEX_DATA ? 'success' : 'warning');
            
            if (window.MXO_PKB_INDEX_DATA) {
                log(`Index size: ${window.MXO_PKB_INDEX_DATA.length} bytes`, 'info');
            }
            
            const pkbFiles = Object.keys(window.MXO_PKB_FILES || {});
            log(`PKB files loaded: ${pkbFiles.length}`, pkbFiles.length > 0 ? 'success' : 'warning');
            
            pkbFiles.forEach(pkb => {
                const size = window.MXO_PKB_FILES[pkb].byteLength;
                log(`  - ${pkb}: ${size} bytes`, 'info');
            });
            
            log('===================', 'info');
        }
        
        async function testExtraction(pkbFile) {
            log(`\\nTesting extraction from ${pkbFile}...`, 'info');
            
            if (!window.extractFromPKB) {
                log('❌ extractFromPKB function not found!', 'error');
                return;
            }
            
            try {
                const startTime = performance.now();
                const results = await window.extractFromPKB(pkbFile);
                const elapsed = (performance.now() - startTime).toFixed(2);
                
                log(`⏱️ Extraction completed in ${elapsed}ms`, 'info');
                log(`📊 Files extracted: ${results.length}`, results.length > 0 ? 'success' : 'warning');
                
                if (results.length > 0) {
                    log('📄 Extracted files:', 'info');
                    results.forEach((file, i) => {
                        log(`  ${i + 1}. ${file.name} (${file.size} bytes)`, 'success');
                    });
                } else {
                    log('❌ No files were extracted', 'error');
                }
                
                return results;
            } catch (error) {
                log(`❌ Extraction error: ${error.message}`, 'error');
                console.error(error);
            }
        }
        
        async function testAllExtraction() {
            log('\\n=== TESTING ALL EXTRACTIONS ===', 'info');
            
            const pkbFiles = Object.keys(window.MXO_PKB_FILES || {});
            if (pkbFiles.length === 0) {
                log('❌ No PKB files loaded', 'error');
                return;
            }
            
            let totalExtracted = 0;
            for (const pkb of pkbFiles) {
                const results = await testExtraction(pkb);
                if (results) {
                    totalExtracted += results.length;
                }
            }
            
            log(`\\n📊 TOTAL FILES EXTRACTED: ${totalExtracted}`, totalExtracted > 0 ? 'success' : 'error');
        }
        
        function dumpIndexHeader() {
            log('\\n=== INDEX HEADER DUMP ===', 'info');
            
            if (!window.MXO_PKB_INDEX_DATA) {
                log('❌ No index data loaded', 'error');
                return;
            }
            
            const data = window.MXO_PKB_INDEX_DATA;
            const decoder = new TextDecoder('ascii');
            
            // Show first 256 bytes
            const headerSize = Math.min(256, data.length);
            const headerBytes = Array.from(data.slice(0, headerSize));
            
            // Hex dump
            log('Hex dump (first 256 bytes):', 'info');
            for (let i = 0; i < headerSize; i += 16) {
                const hex = headerBytes.slice(i, i + 16).map(b => b.toString(16).padStart(2, '0')).join(' ');
                const ascii = headerBytes.slice(i, i + 16).map(b => (b >= 32 && b < 127) ? String.fromCharCode(b) : '.').join('');
                log(`${i.toString(16).padStart(4, '0')}: ${hex.padEnd(48)} | ${ascii}`, 'info');
            }
            
            // Try to identify format
            const magic = decoder.decode(data.slice(0, 4));
            log(`\\nMagic: "${magic}" (${headerBytes.slice(0, 4).join(', ')})`, 'info');
        }
        
        function dumpPKBHeaders() {
            log('\\n=== PKB HEADERS DUMP ===', 'info');
            
            const pkbFiles = Object.entries(window.MXO_PKB_FILES || {});
            if (pkbFiles.length === 0) {
                log('❌ No PKB files loaded', 'error');
                return;
            }
            
            const decoder = new TextDecoder('ascii');
            
            pkbFiles.forEach(([name, buffer]) => {
                log(`\\n📦 ${name}:`, 'info');
                const data = new Uint8Array(buffer);
                const magic = decoder.decode(data.slice(0, 4));
                log(`Magic: "${magic}"`, 'info');
                
                if (magic === 'PKB\\0' || magic.startsWith('PKB')) {
                    const view = new DataView(buffer);
                    const numFiles = view.getUint32(4, true);
                    log(`Number of files: ${numFiles}`, 'info');
                    
                    // Show first few file entries
                    let offset = 8;
                    for (let i = 0; i < Math.min(3, numFiles); i++) {
                        if (offset + 40 <= buffer.byteLength) {
                            const nameBytes = data.slice(offset, offset + 32);
                            const filename = decoder.decode(nameBytes).replace(/\\0+$/, '');
                            const fileOffset = view.getUint32(offset + 32, true);
                            const fileSize = view.getUint32(offset + 36, true);
                            log(`  File ${i}: ${filename} @ ${fileOffset} (${fileSize} bytes)`, 'info');
                            offset += 40;
                        }
                    }
                } else {
                    log(`Unknown format (first 16 bytes): ${Array.from(data.slice(0, 16)).map(b => b.toString(16).padStart(2, '0')).join(' ')}`, 'warning');
                }
            });
        }
        
        // Auto-load enhanced extraction if available
        window.addEventListener('load', async () => {
            log('🌐 PKB Extraction Test Suite loaded', 'success');
            
            // Load the enhanced extraction script
            try {
                const script = document.createElement('script');
                script.src = '/fix_pkb_extraction.js';
                script.onload = () => log('✅ Enhanced extraction loaded', 'success');
                script.onerror = () => log('❌ Failed to load enhanced extraction', 'error');
                document.head.appendChild(script);
            } catch (error) {
                log(`❌ Error loading enhancement: ${error.message}`, 'error');
            }
            
            // Check initial status
            setTimeout(checkStatus, 500);
        });
    </script>
</body>
</html>'''
    
    with open('/Users/pascaldisse/Downloads/mxo/moms/test_pkb_extraction.html', 'w') as f:
        f.write(test_html)
    
    print("✅ Created test page: test_pkb_extraction.html")
    return True

def run_pkb_fix():
    """Run the complete PKB fix process"""
    print("🔧 MOMS PKB EXTRACTION FIX")
    print("=" * 40)
    
    # Step 1: Backup
    if not backup_index_file():
        print("⚠️ Continuing without backup...")
    
    # Step 2: Inject enhanced extraction
    if not inject_enhanced_extraction():
        print("❌ Failed to inject enhanced extraction")
        return False
    
    # Step 3: Add debug buttons
    if not add_debug_buttons():
        print("⚠️ Could not add debug buttons")
    
    # Step 4: Create test page
    if not create_test_page():
        print("⚠️ Could not create test page")
    
    print("\n✅ PKB EXTRACTION FIX COMPLETE")
    print("\n📋 NEXT STEPS:")
    print("1. Refresh MOMS: http://localhost:8000")
    print("2. Open browser console (F12)")
    print("3. Load Archives tab and click on PKB files")
    print("4. Go to 3D Models tab")
    print("5. Click 'Debug Info' to see loaded files")
    print("6. Click 'Test Extract' to test single extraction")
    print("7. Click 'Extract All Models' to see detailed logs")
    print("\n🧪 TEST PAGE: http://localhost:8000/test_pkb_extraction.html")
    
    return True

if __name__ == "__main__":
    success = run_pkb_fix()
    sys.exit(0 if success else 1)
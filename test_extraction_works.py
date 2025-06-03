#!/usr/bin/env python3
"""
Test if PKB extraction actually works now
"""

import urllib.request
import json
import base64

# JavaScript code to test extraction
test_script = """
async function testPKBExtraction() {
    console.log('🧪 Starting PKB Extraction Test...');
    
    // Step 1: Load index file
    console.log('📋 Loading index file...');
    const indexResponse = await fetch('/cache/packmap_save.lta');
    const indexBuffer = await indexResponse.arrayBuffer();
    window.MXO_PKB_INDEX_DATA = new Uint8Array(indexBuffer);
    console.log('✅ Index loaded:', window.MXO_PKB_INDEX_DATA.length, 'bytes');
    
    // Step 2: Load PKB file
    console.log('📦 Loading worlds_3g.pkb...');
    const pkbResponse = await fetch('/cache/worlds_3g.pkb');
    const pkbBuffer = await pkbResponse.arrayBuffer();
    window.MXO_PKB_FILES = { 'worlds_3g.pkb': pkbBuffer };
    console.log('✅ PKB loaded:', pkbBuffer.byteLength, 'bytes');
    
    // Step 3: Load enhanced extraction if not already loaded
    if (!window.extractFromPKBEnhanced) {
        console.log('📥 Loading enhanced extraction...');
        const script = document.createElement('script');
        script.src = '/fix_pkb_extraction.js';
        document.head.appendChild(script);
        await new Promise(resolve => {
            script.onload = resolve;
            script.onerror = () => {
                console.warn('⚠️ Could not load enhanced extraction');
                resolve();
            };
        });
    }
    
    // Step 4: Test extraction
    console.log('🎯 Testing extraction...');
    const results = await window.extractFromPKB('worlds_3g.pkb');
    
    console.log('\\n📊 EXTRACTION RESULTS:');
    console.log('Files extracted:', results.length);
    
    if (results.length > 0) {
        console.log('✅ EXTRACTION SUCCESS!');
        results.forEach((file, i) => {
            console.log(`  ${i+1}. ${file.name} (${file.size} bytes) @ offset ${file.offset}`);
            // Check file data
            if (file.data && file.data.length > 0) {
                const header = Array.from(file.data.slice(0, 4)).map(b => String.fromCharCode(b)).join('');
                console.log(`     Header: "${header}"`);
            }
        });
        return { success: true, count: results.length, files: results.map(f => f.name) };
    } else {
        console.log('❌ EXTRACTION FAILED - No files extracted');
        return { success: false, count: 0, files: [] };
    }
}

// Run the test
testPKBExtraction().then(result => {
    window.PKB_TEST_RESULT = result;
    console.log('\\n🏁 Test complete:', result);
});
"""

def run_browser_test():
    """Run extraction test in a browser context"""
    print("🌐 Running PKB extraction test in browser context...")
    
    # Create a test HTML page that runs our script
    test_html = f"""<!DOCTYPE html>
<html>
<head><title>PKB Test</title></head>
<body>
<h1>PKB Extraction Test</h1>
<div id="result">Testing...</div>
<script>
{test_script}

// Update UI with results
setTimeout(() => {{
    const result = window.PKB_TEST_RESULT;
    if (result) {{
        document.getElementById('result').innerHTML = 
            result.success ? 
            `✅ SUCCESS: Extracted ${{result.count}} files<br>${{result.files.join('<br>')}}` :
            `❌ FAILED: No files extracted`;
    }}
}}, 3000);
</script>
</body>
</html>"""
    
    # Save test page
    with open('/Users/pascaldisse/Downloads/mxo/moms/browser_test.html', 'w') as f:
        f.write(test_html)
    
    print("✅ Browser test page created: browser_test.html")
    print("\n📋 To run the test:")
    print("1. Open: http://localhost:8000/browser_test.html")
    print("2. Open browser console (F12)")
    print("3. Watch the extraction logs")
    print("4. Check if files are extracted successfully")
    
    return True

def test_extraction_locally():
    """Test extraction logic locally"""
    print("\n🔧 Testing extraction logic locally...")
    
    import struct
    
    # Load files
    with open('/Users/pascaldisse/Downloads/mxo/moms/cache/packmap_save.lta', 'rb') as f:
        index_data = f.read()
    
    with open('/Users/pascaldisse/Downloads/mxo/moms/cache/worlds_3g.pkb', 'rb') as f:
        pkb_data = f.read()
    
    print(f"Index size: {len(index_data)} bytes")
    print(f"PKB size: {len(pkb_data)} bytes")
    
    # Parse index
    if index_data[:4] == b'LTAI':
        print("✅ Valid LTAI index format")
        num_entries = struct.unpack('<I', index_data[4:8])[0]
        print(f"Number of entries: {num_entries}")
        
        # Extract files for worlds_3g.pkb
        extracted = []
        offset = 8
        for i in range(num_entries):
            if offset + 72 <= len(index_data):
                filename = index_data[offset:offset+32].split(b'\x00')[0].decode('ascii')
                pkb_name = index_data[offset+32:offset+64].split(b'\x00')[0].decode('ascii')
                file_offset = struct.unpack('<I', index_data[offset+64:offset+68])[0]
                file_size = struct.unpack('<I', index_data[offset+68:offset+72])[0]
                
                if pkb_name == 'worlds_3g.pkb':
                    print(f"\nExtracting: {filename}")
                    print(f"  Offset: {file_offset}, Size: {file_size}")
                    
                    if file_offset + file_size <= len(pkb_data):
                        data = pkb_data[file_offset:file_offset+file_size]
                        header = data[:4] if len(data) >= 4 else b'????'
                        print(f"  ✅ Extracted {len(data)} bytes, header: {header}")
                        extracted.append(filename)
                    else:
                        print(f"  ❌ Invalid offset/size")
                
                offset += 72
        
        print(f"\n📊 Total extracted: {len(extracted)} files")
        return len(extracted) > 0
    else:
        print("❌ Invalid index format")
        return False

if __name__ == "__main__":
    print("🧪 PKB EXTRACTION VERIFICATION")
    print("=" * 40)
    
    # Test locally first
    local_success = test_extraction_locally()
    
    # Create browser test
    browser_test_created = run_browser_test()
    
    print("\n" + "=" * 40)
    if local_success:
        print("✅ Local extraction test PASSED")
        print("✅ The PKB files are properly structured")
        print("\n🎯 Now test in browser:")
        print("   http://localhost:8000/browser_test.html")
    else:
        print("❌ Local extraction test FAILED")
        print("There may be an issue with the file structure")
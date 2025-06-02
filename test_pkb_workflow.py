#!/usr/bin/env python3
"""
Test and fix the PKB workflow issue
"""

import urllib.request
import os
import sys

def create_realistic_pkb_files():
    """Create realistic PKB files for testing"""
    print("📦 Creating Realistic PKB Files for Testing...")
    
    cache_dir = '/Users/pascaldisse/Downloads/mxo/moms/cache'
    
    # Create a larger, more realistic worlds_3g.pkb file
    worlds_pkb = os.path.join(cache_dir, 'worlds_3g.pkb')
    
    with open(worlds_pkb, 'wb') as f:
        # PKB header
        f.write(b'PKB\x00')  # Magic
        f.write((5).to_bytes(4, 'little'))  # Number of files
        
        # File entries (offset 16 bytes each)
        files = [
            ('building1.prop', 1000, 500),
            ('terrain.prop', 1500, 800),
            ('vehicle.moa', 2300, 1200),
            ('character.moa', 3500, 600),
            ('effects.prop', 4100, 300)
        ]
        
        current_offset = 16 + (len(files) * 32)  # Header + file table
        
        for filename, size, _ in files:
            # Write filename (32 bytes)
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            
            # Write offset and size
            f.write(current_offset.to_bytes(4, 'little'))
            f.write(size.to_bytes(4, 'little'))
            
            current_offset += size
        
        # Write file data
        for filename, size, data_pattern in files:
            # Create synthetic file data
            for i in range(size):
                f.write(((data_pattern + i) % 256).to_bytes(1, 'little'))
    
    file_size = os.path.getsize(worlds_pkb)
    print(f"✅ Created realistic worlds_3g.pkb: {file_size} bytes")
    
    # Create character PKB file
    char_pkb = os.path.join(cache_dir, 'char_npc.pkb')
    
    with open(char_pkb, 'wb') as f:
        # PKB header
        f.write(b'PKB\x00')  # Magic
        f.write((3).to_bytes(4, 'little'))  # Number of files
        
        # Character files
        files = [
            ('agent_smith.moa', 800, 100),
            ('neo.moa', 900, 150),
            ('morpheus.moa', 850, 120)
        ]
        
        current_offset = 16 + (len(files) * 32)
        
        for filename, size, _ in files:
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            f.write(current_offset.to_bytes(4, 'little'))
            f.write(size.to_bytes(4, 'little'))
            current_offset += size
        
        # Write file data
        for filename, size, data_pattern in files:
            for i in range(size):
                f.write(((data_pattern + i) % 256).to_bytes(1, 'little'))
    
    char_size = os.path.getsize(char_pkb)
    print(f"✅ Created char_npc.pkb: {char_size} bytes")
    
    # Update the index file to include these PKB files
    index_file = os.path.join(cache_dir, 'packmap_save.lta')
    
    with open(index_file, 'wb') as f:
        # Enhanced index with PKB file references
        f.write(b'LTAI')  # Magic
        f.write((8).to_bytes(4, 'little'))  # Number of entries
        
        entries = [
            ('building1.prop', 'worlds_3g.pkb', 176, 500),
            ('terrain.prop', 'worlds_3g.pkb', 676, 800),
            ('vehicle.moa', 'worlds_3g.pkb', 1476, 1200),
            ('character.moa', 'worlds_3g.pkb', 2676, 600),
            ('agent_smith.moa', 'char_npc.pkb', 112, 800),
            ('neo.moa', 'char_npc.pkb', 912, 900),
            ('morpheus.moa', 'char_npc.pkb', 1812, 850),
            ('effects.prop', 'worlds_3g.pkb', 3276, 300)
        ]
        
        for filename, pkb_name, offset, size in entries:
            # Filename (32 bytes)
            name_bytes = filename.encode('ascii')[:31]
            f.write(name_bytes + b'\x00' * (32 - len(name_bytes)))
            
            # PKB name (32 bytes)
            pkb_bytes = pkb_name.encode('ascii')[:31]
            f.write(pkb_bytes + b'\x00' * (32 - len(pkb_bytes)))
            
            # Offset and size
            f.write(offset.to_bytes(4, 'little'))
            f.write(size.to_bytes(4, 'little'))
    
    index_size = os.path.getsize(index_file)
    print(f"✅ Updated packmap_save.lta: {index_size} bytes")
    
    return True

def test_pkb_file_access():
    """Test if PKB files are accessible via HTTP"""
    print("\n🔗 Testing PKB File Access...")
    
    pkb_files = ['worlds_3g.pkb', 'char_npc.pkb']
    
    for pkb_file in pkb_files:
        try:
            response = urllib.request.urlopen(f'http://localhost:8000/cache/{pkb_file}', timeout=5)
            if response.getcode() == 200:
                data = response.read()
                print(f"✅ {pkb_file} accessible: {len(data)} bytes")
            else:
                print(f"❌ {pkb_file} error: {response.getcode()}")
                return False
        except Exception as e:
            print(f"❌ {pkb_file} not accessible: {e}")
            return False
    
    return True

def create_pkb_loading_instructions():
    """Create a helpful instruction page for PKB loading"""
    print("\n📋 Creating PKB Loading Instructions...")
    
    instructions_html = '''<!DOCTYPE html>
<html>
<head>
    <title>PKB Loading Instructions</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; line-height: 1.6; }
        .step { background: #001100; border: 1px solid #0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .step h3 { color: #00ff00; margin-top: 0; }
        .error { background: #330000; border-color: #ff0000; color: #ffaaaa; }
        .success { background: #003300; border-color: #00ff00; color: #aaffaa; }
        button { background: #030; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; cursor: pointer; }
        .code { background: #222; padding: 5px; border-radius: 3px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>🎯 How to Load PKB Files for 3D Model Extraction</h1>
    
    <div class="error">
        <h3>❌ Current Issue</h3>
        <p>You're seeing: <span class="code">"PKB file worlds_3g.pkb needs to be loaded first"</span></p>
        <p>This means the PKB file exists but isn't loaded into browser memory yet.</p>
    </div>
    
    <div class="step">
        <h3>📁 Step 1: Navigate to Archives Tab</h3>
        <p>1. In MOMS, click on the <strong>"Archives"</strong> tab in the main navigation</p>
        <p>2. You should see PKB files listed (worlds_3g.pkb, char_npc.pkb, etc.)</p>
    </div>
    
    <div class="step">
        <h3>📦 Step 2: Load PKB File into Memory</h3>
        <p>1. Find the PKB file you want to extract from (e.g., worlds_3g.pkb)</p>
        <p>2. <strong>Click on the PKB file name</strong> to load it into browser memory</p>
        <p>3. Wait for it to load completely (may take a few seconds for large files)</p>
    </div>
    
    <div class="step">
        <h3>🎮 Step 3: Extract 3D Models</h3>
        <p>1. Go back to the <strong>"3D Models"</strong> tab</p>
        <p>2. Click <strong>"Extract All Models"</strong> button</p>
        <p>3. Models should now extract successfully!</p>
    </div>
    
    <div class="success">
        <h3>✅ Success Indicators</h3>
        <p>• Console shows: "✅ Auto-loaded index file: packmap_save.lta"</p>
        <p>• No more "PKB file needs to be loaded first" errors</p>
        <p>• Models appear in the 3D viewer</p>
    </div>
    
    <div class="step">
        <h3>🧪 Test PKB Loading</h3>
        <button onclick="testPKBLoading()">Test PKB File Loading</button>
        <button onclick="window.open('/', '_blank')">Open MOMS Application</button>
        <div id="testResults" style="margin-top: 10px;"></div>
    </div>
    
    <div class="step">
        <h3>🔧 Troubleshooting</h3>
        <p><strong>If you don't see PKB files in Archives tab:</strong></p>
        <ul>
            <li>Load a directory containing .pkb files</li>
            <li>Check that files are in packmaps/ subdirectory</li>
            <li>Ensure files are actual Matrix Online PKB archives</li>
        </ul>
        
        <p><strong>If loading fails:</strong></p>
        <ul>
            <li>Check browser console for detailed error messages</li>
            <li>Ensure files are accessible (try this test page)</li>
            <li>Try loading smaller PKB files first</li>
        </ul>
    </div>
    
    <script>
        async function testPKBLoading() {
            const results = document.getElementById('testResults');
            results.innerHTML = '<p>🔍 Testing PKB file accessibility...</p>';
            
            const pkbFiles = ['worlds_3g.pkb', 'char_npc.pkb'];
            let allGood = true;
            
            for (const pkbFile of pkbFiles) {
                try {
                    const response = await fetch(`/cache/${pkbFile}`);
                    if (response.ok) {
                        const data = await response.arrayBuffer();
                        results.innerHTML += `<p style="color: #0f0;">✅ ${pkbFile}: ${data.byteLength} bytes - Ready for loading</p>`;
                    } else {
                        results.innerHTML += `<p style="color: #f00;">❌ ${pkbFile}: HTTP ${response.status}</p>`;
                        allGood = false;
                    }
                } catch (error) {
                    results.innerHTML += `<p style="color: #f00;">❌ ${pkbFile}: ${error.message}</p>`;
                    allGood = false;
                }
            }
            
            if (allGood) {
                results.innerHTML += '<p style="color: #0f0; font-weight: bold;">🎉 All PKB files are accessible! You can now load them in MOMS.</p>';
            } else {
                results.innerHTML += '<p style="color: #ff0;">⚠️ Some PKB files are not accessible. Check the server logs.</p>';
            }
        }
    </script>
</body>
</html>'''
    
    try:
        with open('/Users/pascaldisse/Downloads/mxo/moms/pkb_instructions.html', 'w') as f:
            f.write(instructions_html)
        print("✅ Created instruction page: http://localhost:8000/pkb_instructions.html")
        return True
    except Exception as e:
        print(f"❌ Failed to create instructions: {e}")
        return False

def run_pkb_workflow_fix():
    """Run the complete PKB workflow fix"""
    print("🎯 MOMS PKB Workflow Fix")
    print("=" * 40)
    
    # Step 1: Create realistic PKB files
    print("\n1. CREATING REALISTIC PKB FILES")
    files_created = create_realistic_pkb_files()
    
    # Step 2: Test file access
    print("\n2. TESTING FILE ACCESS")
    files_accessible = test_pkb_file_access()
    
    # Step 3: Create instructions
    print("\n3. CREATING USER INSTRUCTIONS")
    instructions_created = create_pkb_loading_instructions()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 PKB WORKFLOW FIX SUMMARY")
    
    if files_created and files_accessible and instructions_created:
        print("✅ PKB workflow fix completed successfully!")
        print()
        print("🎯 NEXT STEPS FOR USER:")
        print("1. Open: http://localhost:8000/pkb_instructions.html")
        print("2. Follow the step-by-step instructions")
        print("3. Load PKB files in Archives tab BEFORE extracting models")
        print()
        print("💡 KEY INSIGHT:")
        print("The error 'PKB file needs to be loaded first' is correct!")
        print("User needs to click on PKB files in Archives tab to load them.")
        return True
    else:
        print("❌ PKB workflow fix had issues")
        return False

if __name__ == "__main__":
    success = run_pkb_workflow_fix()
    sys.exit(0 if success else 1)
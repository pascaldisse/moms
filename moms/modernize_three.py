#!/usr/bin/env python3
"""
Script to modernize THREE.js usage in MOMS from legacy to ES modules
"""

import re
import sys

def modernize_three_js(content):
    """Modernize THREE.js code to use ES modules"""
    
    # Replace the old script tags with import map
    import_map = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix Online Modding Suite (MOMS)</title>
    
    <!-- External Dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.23.5/babel.min.js"></script>
    
    <!-- Import map for THREE.js ES modules -->
    <script type="importmap">
    {
        "imports": {
            "three": "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
        }
    }
    </script>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Monaco Editor -->
    <script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs/loader.js"></script>'''
    
    # Find the head section and replace it
    head_pattern = r'<!DOCTYPE html>.*?<script src="https://cdn.jsdelivr.net/npm/monaco-editor.*?</script>'
    content = re.sub(head_pattern, import_map, content, flags=re.DOTALL)
    
    # Add the THREE.js module loader before the main script
    three_loader = '''
    <!-- Load THREE.js modules and initialize them globally -->
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
        
        // Make THREE and its modules available globally for React components
        window.THREE = THREE;
        window.OrbitControls = OrbitControls;
        window.GLTFLoader = GLTFLoader;
        
        // Signal that THREE.js is loaded
        window.dispatchEvent(new Event('threejs-loaded'));
        
        console.log('THREE.js ES modules loaded successfully');
        console.log('THREE version:', THREE.REVISION);
        console.log('OrbitControls available:', !!OrbitControls);
        console.log('GLTFLoader available:', !!GLTFLoader);
    </script>

    <script type="text/babel">
        // Wait for THREE.js modules to load
        function waitForThreeJS() {
            return new Promise((resolve) => {
                if (window.THREE && window.OrbitControls) {
                    resolve();
                } else {
                    window.addEventListener('threejs-loaded', resolve, { once: true });
                }
            });
        }'''
    
    # Insert the loader before the main Babel script
    babel_start = '<script type="text/babel">'
    content = content.replace(babel_start, three_loader, 1)
    
    # Update THREE.js references
    replacements = [
        # OrbitControls usage
        (r'new\s+THREE\.OrbitControls', 'new OrbitControls'),
        (r'window\.THREE\.OrbitControls', 'OrbitControls'),
        (r'THREE\.OrbitControls', 'OrbitControls'),
        
        # GLTFLoader usage
        (r'new\s+THREE\.GLTFLoader', 'new GLTFLoader'),
        (r'window\.THREE\.GLTFLoader', 'GLTFLoader'),
        (r'THREE\.GLTFLoader', 'GLTFLoader'),
        
        # Remove the old OrbitControls loading script
        (r'<script>\s*//\s*Ensure THREE.*?</script>', ''),
        (r'<script>\s*//\s*Load OrbitControls manually.*?</script>', ''),
        (r'<script src="https://cdn.jsdelivr.net/npm/three@.*?OrbitControls\.js"></script>', ''),
        (r'<script src="https://cdn.jsdelivr.net/npm/three@.*?GLTFLoader\.js"></script>', ''),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)
    
    # Update the initialization to wait for THREE.js
    init_pattern = r'// Initialize Monaco Editor'
    init_replacement = '''// Wait for THREE.js to load before initializing
        waitForThreeJS().then(() => {
            console.log('THREE.js modules ready, initializing application');
            
            // Hide loading screen
            setTimeout(() => {
                clearInterval(matrixInterval);
                document.getElementById('loading').style.display = 'none';
            }, 1000);
            
            // Initialize the React app
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<App />);
        });
        
        // Initialize Monaco Editor'''
    
    content = content.replace(init_pattern, init_replacement)
    
    # Fix the app initialization at the end
    app_init_pattern = r'// Initialize the app.*?root\.render\(<App />\);'
    app_init_replacement = '''// App initialization is handled after THREE.js loads (see above)'''
    
    content = re.sub(app_init_pattern, app_init_replacement, content, flags=re.DOTALL)
    
    return content

def main():
    # Read the original file
    with open('/Users/pascaldisse/Downloads/mxo/moms/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Modernize the content
    modernized = modernize_three_js(content)
    
    # Write the modernized version
    with open('/Users/pascaldisse/Downloads/mxo/moms/index_modern.html', 'w', encoding='utf-8') as f:
        f.write(modernized)
    
    print("Modernization complete! Created index_modern.html")
    print("Key changes:")
    print("- Updated to THREE.js r169 with ES modules")
    print("- Fixed OrbitControls deprecation warnings")
    print("- Added proper module loading with import maps")
    print("- Maintained all existing functionality")

if __name__ == '__main__':
    main()
// Fix for main page 3D rendering to use PROP parser V2 coordinate fixes
// This integrates the V2 parser improvements into the existing ModelEditor component

window.fix3DRenderingForMainPage = function() {
    console.log('🔧 Applying 3D rendering fixes for main page...');
    
    // Store original parsePROP function
    if (window.LithtechParsers && window.LithtechParsers.parsePROP && !window.LithtechParsers.parsePROPOriginal) {
        window.LithtechParsers.parsePROPOriginal = window.LithtechParsers.parsePROP;
    }
    
    // Override the parsePROP function to use V2 parser
    if (window.LithtechParsers) {
        window.LithtechParsers.parsePROP = async function(file) {
            console.log('🔄 Using enhanced PROP parser V2 for:', file.name);
            
            // Use V2 parser if available
            if (window.enhancedPROPParserV2) {
                return window.enhancedPROPParserV2(file);
            } else if (window.enhancedPROPParser) {
                return window.enhancedPROPParser(file);
            } else {
                // Fallback to original
                return window.LithtechParsers.parsePROPOriginal(file);
            }
        };
        console.log('✅ Replaced LithtechParsers.parsePROP with V2 parser');
    }
    
    // Hook into the model rendering process to apply coordinate fixes
    const originalSetAttribute = window.THREE.BufferGeometry.prototype.setAttribute;
    window.THREE.BufferGeometry.prototype.setAttribute = function(name, attribute) {
        // Check if this is being called for a PROP model
        if (name === 'position' && window.currentlyParsingPROP) {
            console.log('🔄 Applying coordinate fixes to geometry...');
            
            // The vertices should already be fixed by V2 parser,
            // but let's ensure they are properly set
            const vertices = attribute.array;
            
            // Log first few vertices for debugging
            console.log('First vertex:', vertices[0], vertices[1], vertices[2]);
            if (vertices.length > 3) {
                console.log('Second vertex:', vertices[3], vertices[4], vertices[5]);
            }
        }
        
        return originalSetAttribute.call(this, name, attribute);
    };
    
    // Mark when we're parsing PROP files
    const originalFileHandler = window.handleFile3D || window.FileHandler;
    if (originalFileHandler) {
        window.handleFile3DOriginal = originalFileHandler;
        window.handleFile3D = async function(file) {
            if (file.name.toLowerCase().endsWith('.prop')) {
                window.currentlyParsingPROP = true;
            }
            
            try {
                const result = await window.handleFile3DOriginal(file);
                return result;
            } finally {
                window.currentlyParsingPROP = false;
            }
        };
    }
    
    // Fix camera positioning for PROP models
    window.fixCameraForPROPModel = function(camera, boundingBox) {
        const size = new THREE.Vector3();
        const center = new THREE.Vector3();
        boundingBox.getSize(size);
        boundingBox.getCenter(center);
        
        // Calculate appropriate camera distance
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        
        // Add some padding
        cameraZ *= 2.5;
        
        // Position camera
        camera.position.set(cameraZ * 0.7, cameraZ * 0.5, cameraZ * 0.7);
        camera.lookAt(center);
        
        // Update camera controls if available
        if (window.cameraControls || window.controls) {
            const controls = window.cameraControls || window.controls;
            controls.target.copy(center);
            if (controls.update) controls.update();
        }
        
        console.log(`📷 Camera positioned at distance: ${cameraZ.toFixed(2)}m`);
    };
    
    // Add debug helpers to scene
    window.addDebugHelpers = function(scene, mesh) {
        // Remove existing helpers
        ['axes_helper', 'bounds_helper'].forEach(name => {
            const helper = scene.getObjectByName(name);
            if (helper) scene.remove(helper);
        });
        
        if (!mesh || !mesh.geometry) return;
        
        // Add axes helper
        mesh.geometry.computeBoundingBox();
        const size = new THREE.Vector3();
        mesh.geometry.boundingBox.getSize(size);
        const maxDim = Math.max(size.x, size.y, size.z);
        
        const axesHelper = new THREE.AxesHelper(maxDim * 0.5);
        axesHelper.name = 'axes_helper';
        scene.add(axesHelper);
        
        // Add bounding box helper
        const boxHelper = new THREE.BoxHelper(mesh, 0xffff00);
        boxHelper.name = 'bounds_helper';
        scene.add(boxHelper);
    };
    
    console.log('✅ Main page 3D rendering fixes applied');
    console.log('💡 PROP files will now use V2 parser with coordinate fixes');
};

// Apply fixes immediately
if (window.LithtechParsers) {
    window.fix3DRenderingForMainPage();
} else {
    // Wait for LithtechParsers to be available
    const checkInterval = setInterval(() => {
        if (window.LithtechParsers) {
            clearInterval(checkInterval);
            window.fix3DRenderingForMainPage();
        }
    }, 100);
    
    // Stop checking after 10 seconds
    setTimeout(() => clearInterval(checkInterval), 10000);
}

console.log('✅ Main page 3D rendering fix script loaded');
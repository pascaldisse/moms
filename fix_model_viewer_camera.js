// Fix camera positioning and model centering in the main viewer
// This ensures PROP models are properly centered and viewable

window.fixModelViewerCamera = function() {
    console.log('🎥 Applying model viewer camera fixes...');
    
    // Store the original camera position setter
    if (!window.originalCameraPositionSet) {
        window.originalCameraPositionSet = true;
        
        // Hook into the model loading process
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        // Check if a canvas was added (THREE.js renderer)
                        if (node.tagName === 'CANVAS') {
                            console.log('📷 Canvas detected, applying camera fixes...');
                            setTimeout(() => {
                                applyCameraFix();
                            }, 100);
                        }
                    });
                }
            });
        });
        
        // Start observing
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    function applyCameraFix() {
        // Find the scene and camera
        const canvas = document.querySelector('.webgl-container canvas');
        if (!canvas) return;
        
        // Hook into THREE.js scene updates
        if (window.THREE && window.THREE.Scene) {
            const originalAdd = window.THREE.Scene.prototype.add;
            
            window.THREE.Scene.prototype.add = function(object) {
                const result = originalAdd.call(this, object);
                
                // Check if a mesh was added
                if (object.isMesh || object.isLOD) {
                    console.log('🎯 Model added to scene, fixing camera...');
                    
                    setTimeout(() => {
                        // Find camera in the scene
                        let camera = null;
                        this.traverse((child) => {
                            if (child.isCamera) {
                                camera = child;
                            }
                        });
                        
                        // Use global camera if scene camera not found
                        if (!camera && window.sceneCamera) {
                            camera = window.sceneCamera;
                        }
                        
                        if (camera && object.geometry) {
                            // Compute bounding box
                            object.geometry.computeBoundingBox();
                            const box = object.geometry.boundingBox;
                            const size = new THREE.Vector3();
                            const center = new THREE.Vector3();
                            box.getSize(size);
                            box.getCenter(center);
                            
                            // Log model size for debugging
                            console.log(`📏 Model size: ${size.x.toFixed(2)} x ${size.y.toFixed(2)} x ${size.z.toFixed(2)} meters`);
                            
                            // Center the model
                            object.position.sub(center);
                            
                            // Calculate camera distance
                            const maxDim = Math.max(size.x, size.y, size.z);
                            const fov = camera.fov * (Math.PI / 180);
                            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
                            cameraZ *= 2.5; // Add padding
                            
                            // Position camera at a nice angle
                            camera.position.set(
                                cameraZ * 0.7,
                                cameraZ * 0.5,
                                cameraZ * 0.7
                            );
                            camera.lookAt(0, 0, 0);
                            
                            console.log(`📷 Camera positioned at distance: ${cameraZ.toFixed(2)}m`);
                            
                            // Update controls if available
                            if (window.controls || window.cameraControls) {
                                const controls = window.controls || window.cameraControls;
                                if (controls.target) {
                                    controls.target.set(0, 0, 0);
                                }
                                if (controls.update) {
                                    controls.update();
                                }
                            }
                            
                            // Force render update
                            if (window.rendererRef && window.rendererRef.current) {
                                window.rendererRef.current.render(this, camera);
                            }
                        }
                    }, 50);
                }
                
                return result;
            };
        }
    }
    
    // Apply fix immediately if scene exists
    applyCameraFix();
    
    console.log('✅ Model viewer camera fixes applied');
};

// Auto-apply fixes
window.fixModelViewerCamera();

// Also fix when the 3D Models tab is opened
window.addEventListener('click', (e) => {
    // Check if 3D Models tab was clicked
    if (e.target.textContent === '3D Models' || 
        e.target.closest('[class*="tab"]')?.textContent === '3D Models') {
        setTimeout(() => {
            window.fixModelViewerCamera();
        }, 100);
    }
});

console.log('✅ Model viewer camera fix script loaded');
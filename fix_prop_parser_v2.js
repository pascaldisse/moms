// Enhanced PROP file parser V2 for Matrix Online
// Based on complete documentation and reverse engineering findings

window.enhancedPROPParserV2 = async function(file) {
    console.log(`🔧 Enhanced PROP Parser V2: Processing ${file.name} (${file.size} bytes)`);
    
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const buffer = e.target.result;
                const dataView = new DataView(buffer);
                const uint8Array = new Uint8Array(buffer);
                
                // Log first 256 bytes for analysis
                console.log('📄 PROP file header (first 256 bytes):');
                const headerHex = Array.from(uint8Array.slice(0, 256))
                    .map(b => b.toString(16).padStart(2, '0'))
                    .join(' ');
                console.log(headerHex);
                
                // Check for PROP signature at 0x00
                const signature = String.fromCharCode(...uint8Array.slice(0, 4));
                console.log(`🔮 File signature: "${signature}"`);
                
                // Initialize data arrays
                const vertices = [];
                const indices = [];
                const uvs = [];
                const normals = [];
                
                if (signature === 'PROP') {
                    console.log('✅ Valid PROP signature detected');
                    
                    // Based on documentation:
                    // Header is 136 bytes (0x88)
                    // Vertex count at 0x80
                    // Face count at 0x84
                    
                    const vertexCount = dataView.getUint32(0x80, true);
                    const faceCount = dataView.getUint32(0x84, true);
                    
                    console.log(`📊 Vertex count: ${vertexCount}, Face count: ${faceCount}`);
                    
                    // Validate counts
                    if (vertexCount > 0 && vertexCount < 100000 && faceCount > 0 && faceCount < 100000) {
                        let offset = 0x88; // Start after header
                        
                        // Read vertices (3 floats per vertex)
                        console.log(`📍 Reading ${vertexCount} vertices from offset 0x${offset.toString(16)}`);
                        for (let i = 0; i < vertexCount && offset + 12 <= buffer.byteLength; i++) {
                            let x = dataView.getFloat32(offset, true);
                            let y = dataView.getFloat32(offset + 4, true);
                            let z = dataView.getFloat32(offset + 8, true);
                            
                            // Validate vertex data
                            if (!isNaN(x) && !isNaN(y) && !isNaN(z) && 
                                Math.abs(x) < 100000 && Math.abs(y) < 100000 && Math.abs(z) < 100000) {
                                
                                // CRITICAL FIX 1: Convert from centimeters to meters
                                x *= 0.01;
                                y *= 0.01;
                                z *= 0.01;
                                
                                // CRITICAL FIX 2: Lithtech to three.js coordinate system
                                // Lithtech may use Z-up, three.js uses Y-up
                                // Try swapping Y and Z
                                vertices.push(x, z, -y); // Note: negating Y for proper orientation
                                
                            } else {
                                console.warn(`⚠️ Invalid vertex at index ${i}: (${x}, ${y}, ${z})`);
                            }
                            offset += 12;
                        }
                        
                        // Read face indices
                        console.log(`📐 Reading ${faceCount} faces from offset 0x${offset.toString(16)}`);
                        for (let i = 0; i < faceCount && offset + 12 <= buffer.byteLength; i++) {
                            const a = dataView.getUint32(offset, true);
                            const b = dataView.getUint32(offset + 4, true);
                            const c = dataView.getUint32(offset + 8, true);
                            
                            // Validate indices
                            if (a < vertexCount && b < vertexCount && c < vertexCount) {
                                // CRITICAL FIX 3: Reverse face winding for three.js
                                // Lithtech may use different winding order
                                indices.push(a, c, b); // Reversed from a, b, c
                            } else {
                                console.warn(`⚠️ Invalid face indices at ${i}: (${a}, ${b}, ${c})`);
                            }
                            offset += 12;
                        }
                        
                        // Try to read UV coordinates if space allows
                        if (offset + vertexCount * 8 <= buffer.byteLength) {
                            console.log(`🎨 Reading UV coordinates from offset 0x${offset.toString(16)}`);
                            for (let i = 0; i < vertexCount; i++) {
                                const u = dataView.getFloat32(offset, true);
                                const v = dataView.getFloat32(offset + 4, true);
                                if (!isNaN(u) && !isNaN(v)) {
                                    // UV coordinates might need flipping
                                    uvs.push(u, 1.0 - v); // Flip V coordinate
                                }
                                offset += 8;
                            }
                        }
                        
                        // Try to read normals if space allows
                        if (offset + vertexCount * 12 <= buffer.byteLength) {
                            console.log(`🔦 Reading normals from offset 0x${offset.toString(16)}`);
                            for (let i = 0; i < vertexCount; i++) {
                                let nx = dataView.getFloat32(offset, true);
                                let ny = dataView.getFloat32(offset + 4, true);
                                let nz = dataView.getFloat32(offset + 8, true);
                                
                                // Apply same coordinate transformation as vertices
                                const tempNormal = [nx, nz, -ny];
                                
                                // Normalize
                                const length = Math.sqrt(tempNormal[0]**2 + tempNormal[1]**2 + tempNormal[2]**2);
                                if (length > 0.01) {
                                    normals.push(
                                        tempNormal[0]/length,
                                        tempNormal[1]/length,
                                        tempNormal[2]/length
                                    );
                                }
                                offset += 12;
                            }
                        }
                    }
                } else {
                    console.warn('⚠️ No PROP signature found, file may be corrupted or different format');
                }
                
                // Generate normals if not found
                if (normals.length === 0 && vertices.length > 0 && indices.length > 0) {
                    console.log('🔧 No normals found, will compute in three.js');
                }
                
                console.log(`
📊 === PROP PARSING RESULTS ===
✅ Vertices: ${vertices.length / 3}
✅ Faces: ${indices.length / 3}
✅ UVs: ${uvs.length / 2}
✅ Normals: ${normals.length / 3}
📏 Bounds: ${vertices.length > 0 ? calculateBounds(vertices) : 'N/A'}
🔄 Coordinate system: Converted from Lithtech (Z-up) to three.js (Y-up)
📐 Face winding: Reversed for three.js compatibility
                `);
                
                resolve({
                    type: 'model',
                    vertices: vertices,
                    indices: indices,
                    uvs: uvs,
                    normals: normals,
                    animations: [],
                    materials: [{
                        name: 'default',
                        color: 0x808080,
                        metalness: 0.3,
                        roughness: 0.7,
                        emissive: 0x101010,
                        side: 'double' // Important for debugging
                    }],
                    metadata: {
                        format: 'PROP',
                        description: 'Matrix Online static prop (fixed coordinate system)',
                        vertexCount: vertices.length / 3,
                        faceCount: indices.length / 3,
                        hasUVs: uvs.length > 0,
                        hasNormals: normals.length > 0,
                        engine: 'Modified Lithtech Discovery',
                        scale: 'Converted from cm to meters',
                        coordinateSystem: 'Converted from Lithtech to three.js',
                        signature: signature,
                        fileSize: buffer.byteLength,
                        headerSize: 0x88,
                        vertexOffset: 0x88,
                        exportable: true
                    }
                });
                
            } catch (error) {
                console.error('❌ Error in enhanced PROP parser V2:', error);
                reject(error);
            }
        };
        
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
    });
};

// Helper function to calculate bounds
function calculateBounds(vertices) {
    let minX = Infinity, minY = Infinity, minZ = Infinity;
    let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
    
    for (let i = 0; i < vertices.length; i += 3) {
        minX = Math.min(minX, vertices[i]);
        maxX = Math.max(maxX, vertices[i]);
        minY = Math.min(minY, vertices[i + 1]);
        maxY = Math.max(maxY, vertices[i + 1]);
        minZ = Math.min(minZ, vertices[i + 2]);
        maxZ = Math.max(maxZ, vertices[i + 2]);
    }
    
    return `X: ${minX.toFixed(2)} to ${maxX.toFixed(2)}, Y: ${minY.toFixed(2)} to ${maxY.toFixed(2)}, Z: ${minZ.toFixed(2)} to ${maxZ.toFixed(2)}`;
}

// Enhanced 3D model renderer V2 with debug features
window.renderPROPModelV2 = function(parsedData, scene, camera, renderer, options = {}) {
    console.log('🎮 Rendering PROP model V2 with fixes...');
    
    // Options
    const showWireframe = options.wireframe || false;
    const showAxes = options.axes !== false;
    const showBounds = options.bounds !== false;
    const showNormals = options.normals || false;
    
    // Clear existing model
    const existingModel = scene.getObjectByName('prop_model');
    if (existingModel) {
        scene.remove(existingModel);
    }
    
    // Clear debug helpers
    ['axes_helper', 'bounds_helper', 'grid_helper', 'normals_helper'].forEach(name => {
        const helper = scene.getObjectByName(name);
        if (helper) scene.remove(helper);
    });
    
    // Create geometry
    const geometry = new THREE.BufferGeometry();
    
    // Set vertices
    if (parsedData.vertices && parsedData.vertices.length > 0) {
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(parsedData.vertices, 3));
    } else {
        console.error('No vertices to render!');
        return null;
    }
    
    // Set indices
    if (parsedData.indices && parsedData.indices.length > 0) {
        geometry.setIndex(parsedData.indices);
    }
    
    // Set UVs
    if (parsedData.uvs && parsedData.uvs.length > 0) {
        geometry.setAttribute('uv', new THREE.Float32BufferAttribute(parsedData.uvs, 2));
    }
    
    // Set normals or compute them
    if (parsedData.normals && parsedData.normals.length > 0) {
        geometry.setAttribute('normal', new THREE.Float32BufferAttribute(parsedData.normals, 3));
    } else {
        console.log('Computing vertex normals...');
        geometry.computeVertexNormals();
    }
    
    // Create materials
    const materials = [];
    
    // Main material
    const mainMaterial = new THREE.MeshPhongMaterial({
        color: parsedData.materials?.[0]?.color || 0x00ff00,
        metalness: parsedData.materials?.[0]?.metalness || 0.3,
        roughness: parsedData.materials?.[0]?.roughness || 0.7,
        emissive: parsedData.materials?.[0]?.emissive || 0x101010,
        side: THREE.DoubleSide, // Show both sides for debugging
        flatShading: false,
        transparent: false,
        opacity: 1.0
    });
    materials.push(mainMaterial);
    
    // Wireframe material if requested
    if (showWireframe) {
        const wireframeMaterial = new THREE.MeshBasicMaterial({
            color: 0x00ff00,
            wireframe: true,
            transparent: true,
            opacity: 0.3
        });
        materials.push(wireframeMaterial);
    }
    
    // Create mesh(es)
    const group = new THREE.Group();
    group.name = 'prop_model';
    
    materials.forEach(material => {
        const mesh = new THREE.Mesh(geometry, material);
        group.add(mesh);
    });
    
    // Add to scene
    scene.add(group);
    
    // Compute bounds for camera positioning
    geometry.computeBoundingBox();
    const box = geometry.boundingBox;
    const center = new THREE.Vector3();
    const size = new THREE.Vector3();
    box.getCenter(center);
    box.getSize(size);
    
    // Center the model at origin
    group.position.sub(center);
    
    // Add debug helpers
    if (showAxes) {
        const axesHelper = new THREE.AxesHelper(Math.max(size.x, size.y, size.z) * 0.5);
        axesHelper.name = 'axes_helper';
        scene.add(axesHelper);
    }
    
    if (showBounds) {
        const boxHelper = new THREE.BoxHelper(group, 0xffff00);
        boxHelper.name = 'bounds_helper';
        scene.add(boxHelper);
    }
    
    // Add grid
    const gridSize = Math.max(size.x, size.z) * 2;
    const gridHelper = new THREE.GridHelper(gridSize, 20, 0x444444, 0x222222);
    gridHelper.name = 'grid_helper';
    scene.add(gridHelper);
    
    // Add normal helper if requested
    if (showNormals) {
        const normalHelper = new THREE.VertexNormalsHelper(group.children[0], size.length() * 0.05, 0xff0000);
        normalHelper.name = 'normals_helper';
        scene.add(normalHelper);
    }
    
    // Position camera
    const maxDim = Math.max(size.x, size.y, size.z);
    const distance = maxDim * 2.5;
    camera.position.set(distance * 0.8, distance * 0.6, distance * 0.8);
    camera.lookAt(0, 0, 0);
    
    // Update camera controls if available
    if (window.cameraControls) {
        window.cameraControls.target.set(0, 0, 0);
        window.cameraControls.update();
    }
    
    console.log(`✅ PROP model rendered successfully`);
    console.log(`📏 Model size: ${size.x.toFixed(2)} x ${size.y.toFixed(2)} x ${size.z.toFixed(2)} meters`);
    console.log(`📍 Camera distance: ${distance.toFixed(2)} meters`);
    
    return group;
};

// Auto-replace V1 parser if it exists
if (window.enhancedPROPParser) {
    window.enhancedPROPParserV1 = window.enhancedPROPParser;
    window.enhancedPROPParser = window.enhancedPROPParserV2;
    console.log('✅ Replaced V1 parser with V2');
}

// Auto-replace V1 renderer if it exists
if (window.renderPROPModel) {
    window.renderPROPModelV1 = window.renderPROPModel;
    window.renderPROPModel = window.renderPROPModelV2;
    console.log('✅ Replaced V1 renderer with V2');
}

// Register the enhanced parser
console.log('✅ Enhanced PROP parser V2 loaded with coordinate system fixes');
console.log('💡 Key fixes: Lithtech→three.js coordinates, cm→meters scale, reversed face winding');
console.log('💡 Usage: window.enhancedPROPParserV2(file) or window.renderPROPModelV2(data, scene, camera, renderer, options)');
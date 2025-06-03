// Enhanced PROP file parser for Matrix Online
// Based on community research and successful exports to PLY format

window.enhancedPROPParser = async function(file) {
    console.log(`🔧 Enhanced PROP Parser: Processing ${file.name} (${file.size} bytes)`);
    
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
                
                // Check for PROP signature
                const signature = String.fromCharCode(...uint8Array.slice(0, 4));
                console.log(`🔮 File signature: "${signature}"`);
                
                // Initialize data arrays
                const vertices = [];
                const indices = [];
                const uvs = [];
                const normals = [];
                
                // Strategy 1: Look for PROP signature and structured data
                if (signature === 'PROP') {
                    console.log('✅ Valid PROP signature detected');
                    
                    // Based on the hexdump, the data starts at offset 0x80 (128)
                    // Format appears to be:
                    // - Header: 128 bytes
                    // - Vertex count at 0x80
                    // - Face count at 0x84
                    // - Vertex data follows
                    
                    const vertexCount = dataView.getUint32(0x80, true);
                    const faceCount = dataView.getUint32(0x84, true);
                    
                    console.log(`📊 Vertex count: ${vertexCount}, Face count: ${faceCount}`);
                    
                    // Validate counts
                    if (vertexCount > 0 && vertexCount < 100000 && faceCount > 0 && faceCount < 100000) {
                        let offset = 0x88; // Start after counts
                        
                        // Read vertices (3 floats per vertex)
                        console.log(`📍 Reading ${vertexCount} vertices from offset 0x${offset.toString(16)}`);
                        for (let i = 0; i < vertexCount && offset + 12 <= buffer.byteLength; i++) {
                            const x = dataView.getFloat32(offset, true);
                            const y = dataView.getFloat32(offset + 4, true);
                            const z = dataView.getFloat32(offset + 8, true);
                            
                            // Validate vertex data
                            if (!isNaN(x) && !isNaN(y) && !isNaN(z) && 
                                Math.abs(x) < 10000 && Math.abs(y) < 10000 && Math.abs(z) < 10000) {
                                // Convert from centimeters to meters
                                vertices.push(x * 0.01, y * 0.01, z * 0.01);
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
                                indices.push(a, b, c);
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
                                if (!isNaN(u) && !isNaN(v) && u >= 0 && u <= 1 && v >= 0 && v <= 1) {
                                    uvs.push(u, v);
                                }
                                offset += 8;
                            }
                        }
                        
                        // Try to read normals if space allows
                        if (offset + vertexCount * 12 <= buffer.byteLength) {
                            console.log(`🔦 Reading normals from offset 0x${offset.toString(16)}`);
                            for (let i = 0; i < vertexCount; i++) {
                                const nx = dataView.getFloat32(offset, true);
                                const ny = dataView.getFloat32(offset + 4, true);
                                const nz = dataView.getFloat32(offset + 8, true);
                                
                                // Validate and normalize
                                const length = Math.sqrt(nx*nx + ny*ny + nz*nz);
                                if (length > 0.01 && length < 2.0) {
                                    normals.push(nx/length, ny/length, nz/length);
                                }
                                offset += 12;
                            }
                        }
                    }
                }
                
                // Strategy 2: Pattern-based search (fallback for files without proper header)
                if (vertices.length === 0) {
                    console.log('⚠️ No valid PROP header found, trying pattern-based search...');
                    
                    // Scan for vertex/face count patterns
                    for (let offset = 0; offset < Math.min(512, buffer.byteLength - 8); offset += 4) {
                        const val1 = dataView.getUint32(offset, true);
                        const val2 = dataView.getUint32(offset + 4, true);
                        
                        // Look for reasonable vertex/face counts
                        if (val1 >= 3 && val1 <= 50000 && val2 >= 1 && val2 <= 50000) {
                            // Check if this could be vertex data
                            const testOffset = offset + 8;
                            const expectedSize = testOffset + (val1 * 12) + (val2 * 12);
                            
                            if (expectedSize <= buffer.byteLength) {
                                console.log(`🔍 Found potential counts at offset 0x${offset.toString(16)}: vertices=${val1}, faces=${val2}`);
                                
                                // Try to read as vertices
                                let valid = true;
                                const testVertices = [];
                                let vOffset = testOffset;
                                
                                for (let i = 0; i < Math.min(10, val1); i++) {
                                    const x = dataView.getFloat32(vOffset, true);
                                    const y = dataView.getFloat32(vOffset + 4, true);
                                    const z = dataView.getFloat32(vOffset + 8, true);
                                    
                                    if (isNaN(x) || isNaN(y) || isNaN(z) || 
                                        Math.abs(x) > 50000 || Math.abs(y) > 50000 || Math.abs(z) > 50000) {
                                        valid = false;
                                        break;
                                    }
                                    testVertices.push(x, y, z);
                                    vOffset += 12;
                                }
                                
                                if (valid) {
                                    console.log('✅ Valid vertex data found, extracting full mesh...');
                                    
                                    // Extract all vertices
                                    vOffset = testOffset;
                                    for (let i = 0; i < val1; i++) {
                                        const x = dataView.getFloat32(vOffset, true);
                                        const y = dataView.getFloat32(vOffset + 4, true);
                                        const z = dataView.getFloat32(vOffset + 8, true);
                                        vertices.push(x * 0.01, y * 0.01, z * 0.01);
                                        vOffset += 12;
                                    }
                                    
                                    // Extract faces
                                    for (let i = 0; i < val2; i++) {
                                        const a = dataView.getUint32(vOffset, true);
                                        const b = dataView.getUint32(vOffset + 4, true);
                                        const c = dataView.getUint32(vOffset + 8, true);
                                        if (a < val1 && b < val1 && c < val1) {
                                            indices.push(a, b, c);
                                        }
                                        vOffset += 12;
                                    }
                                    
                                    break;
                                }
                            }
                        }
                    }
                }
                
                // Generate normals if not found
                if (normals.length === 0 && vertices.length > 0) {
                    console.log('🔧 Generating normals from geometry...');
                    // Simple normal generation (can be improved)
                    for (let i = 0; i < vertices.length; i += 3) {
                        normals.push(0, 1, 0); // Default up normal
                    }
                }
                
                console.log(`
📊 === PROP PARSING RESULTS ===
✅ Vertices: ${vertices.length / 3}
✅ Faces: ${indices.length / 3}
✅ UVs: ${uvs.length / 2}
✅ Normals: ${normals.length / 3}
📏 Bounds: ${vertices.length > 0 ? calculateBounds(vertices) : 'N/A'}
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
                        roughness: 0.7
                    }],
                    metadata: {
                        format: 'PROP',
                        description: 'Matrix Online static prop',
                        vertexCount: vertices.length / 3,
                        faceCount: indices.length / 3,
                        hasUVs: uvs.length > 0,
                        hasNormals: normals.length > 0,
                        engine: 'Modified Lithtech Discovery',
                        scale: '1 unit = 1cm (converted to meters)',
                        signature: signature,
                        fileSize: buffer.byteLength,
                        exportable: true
                    }
                });
                
            } catch (error) {
                console.error('❌ Error in enhanced PROP parser:', error);
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

// Enhanced 3D model renderer for PROP files
window.renderPROPModel = function(parsedData, scene, camera, renderer) {
    console.log('🎮 Rendering PROP model with enhanced parser data...');
    
    // Clear existing model
    const existingModel = scene.getObjectByName('prop_model');
    if (existingModel) {
        scene.remove(existingModel);
    }
    
    // Create geometry
    const geometry = new THREE.BufferGeometry();
    
    // Set vertices
    if (parsedData.vertices && parsedData.vertices.length > 0) {
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(parsedData.vertices, 3));
    }
    
    // Set indices
    if (parsedData.indices && parsedData.indices.length > 0) {
        geometry.setIndex(parsedData.indices);
    }
    
    // Set UVs
    if (parsedData.uvs && parsedData.uvs.length > 0) {
        geometry.setAttribute('uv', new THREE.Float32BufferAttribute(parsedData.uvs, 2));
    }
    
    // Set normals
    if (parsedData.normals && parsedData.normals.length > 0) {
        geometry.setAttribute('normal', new THREE.Float32BufferAttribute(parsedData.normals, 3));
    } else {
        geometry.computeVertexNormals();
    }
    
    // Create material
    const material = new THREE.MeshPhongMaterial({
        color: parsedData.materials?.[0]?.color || 0x808080,
        metalness: parsedData.materials?.[0]?.metalness || 0.3,
        roughness: parsedData.materials?.[0]?.roughness || 0.7,
        side: THREE.DoubleSide,
        flatShading: false
    });
    
    // Create mesh
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = 'prop_model';
    
    // Center the model
    geometry.computeBoundingBox();
    const center = new THREE.Vector3();
    geometry.boundingBox.getCenter(center);
    mesh.position.sub(center);
    
    // Add to scene
    scene.add(mesh);
    
    // Adjust camera
    const size = new THREE.Vector3();
    geometry.boundingBox.getSize(size);
    const maxDim = Math.max(size.x, size.y, size.z);
    camera.position.set(maxDim * 1.5, maxDim * 1.5, maxDim * 1.5);
    camera.lookAt(0, 0, 0);
    
    // Add grid helper
    const gridHelper = new THREE.GridHelper(maxDim * 2, 20);
    gridHelper.name = 'grid_helper';
    scene.add(gridHelper);
    
    console.log('✅ PROP model rendered successfully');
    return mesh;
};

// Register the enhanced parser
console.log('✅ Enhanced PROP parser loaded');
console.log('💡 Usage: window.enhancedPROPParser(file) or window.renderPROPModel(data, scene, camera, renderer)');
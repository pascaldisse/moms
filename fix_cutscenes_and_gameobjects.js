// Fix Cutscenes and GameObjects functionality

// Enhanced BIK video handling with better fallback
window.enhancedBikPlayer = async (file) => {
    console.log('🎬 Enhanced BIK player loading...');
    
    // Check if BIK proxy server is available
    const checkBikServer = async () => {
        try {
            const response = await fetch('http://localhost:8002/health', { 
                method: 'GET',
                mode: 'cors',
                signal: AbortSignal.timeout(2000)
            });
            return response.ok;
        } catch (error) {
            console.warn('BIK server not available:', error.message);
            return false;
        }
    };
    
    const bikServerAvailable = await checkBikServer();
    
    if (bikServerAvailable) {
        console.log('✅ BIK server available, using proxy conversion');
        return `http://localhost:8002/convert?file=${encodeURIComponent(file.name)}`;
    } else {
        console.log('⚠️ BIK server not available, showing instructions');
        
        // Create instruction overlay
        const instructions = document.createElement('div');
        instructions.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 17, 0, 0.9);
            border: 2px solid #00ff00;
            padding: 20px;
            color: #00ff00;
            font-family: monospace;
            text-align: center;
            z-index: 1000;
            max-width: 500px;
        `;
        
        instructions.innerHTML = `
            <h3>🎬 BIK Video Player</h3>
            <p>BIK files require a conversion server to play.</p>
            <p><strong>To enable BIK playback:</strong></p>
            <ol style="text-align: left;">
                <li>Start the BIK server:<br>
                    <code style="background: #003300; padding: 5px;">python3 simple-bik-server.py</code>
                </li>
                <li>Make sure FFmpeg is installed:<br>
                    <code style="background: #003300; padding: 5px;">brew install ffmpeg</code>
                </li>
                <li>Refresh this page and try again</li>
            </ol>
            <p style="margin-top: 15px;">
                <strong>File:</strong> ${file.name}<br>
                <strong>Size:</strong> ${(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <button onclick="this.parentElement.remove()" style="background: #030; color: #0f0; border: 1px solid #0f0; padding: 5px 15px; margin-top: 10px; cursor: pointer;">Close</button>
        `;
        
        // Return a container with instructions
        return { instructions, error: 'BIK server not available' };
    }
};

// Fix GameObject properties to actually work with the 3D model
window.connectGameObjectToModel = (mesh) => {
    console.log('🔧 Connecting GameObject properties to model...');
    
    if (!mesh || !mesh.position || !mesh.rotation || !mesh.scale) {
        console.warn('Invalid mesh object');
        return;
    }
    
    // Store original transform
    const originalTransform = {
        position: mesh.position.clone(),
        rotation: mesh.rotation.clone(),
        scale: mesh.scale.clone()
    };
    
    // Create property getters/setters
    window.gameObjectProperties = {
        transform: {
            position: {
                get x() { return mesh.position.x; },
                set x(val) { mesh.position.x = parseFloat(val); },
                get y() { return mesh.position.y; },
                set y(val) { mesh.position.y = parseFloat(val); },
                get z() { return mesh.position.z; },
                set z(val) { mesh.position.z = parseFloat(val); }
            },
            rotation: {
                get x() { return THREE.MathUtils.radToDeg(mesh.rotation.x); },
                set x(val) { mesh.rotation.x = THREE.MathUtils.degToRad(parseFloat(val)); },
                get y() { return THREE.MathUtils.radToDeg(mesh.rotation.y); },
                set y(val) { mesh.rotation.y = THREE.MathUtils.degToRad(parseFloat(val)); },
                get z() { return THREE.MathUtils.radToDeg(mesh.rotation.z); },
                set z(val) { mesh.rotation.z = THREE.MathUtils.degToRad(parseFloat(val)); }
            },
            scale: {
                get x() { return mesh.scale.x; },
                set x(val) { mesh.scale.x = parseFloat(val); },
                get y() { return mesh.scale.y; },
                set y(val) { mesh.scale.y = parseFloat(val); },
                get z() { return mesh.scale.z; },
                set z(val) { mesh.scale.z = parseFloat(val); }
            }
        },
        components: {
            meshRenderer: {
                enabled: mesh.visible,
                castShadow: mesh.castShadow,
                receiveShadow: mesh.receiveShadow
            },
            material: mesh.material,
            geometry: mesh.geometry
        },
        reset: () => {
            mesh.position.copy(originalTransform.position);
            mesh.rotation.copy(originalTransform.rotation);
            mesh.scale.copy(originalTransform.scale);
            console.log('✅ Transform reset to original values');
        }
    };
    
    console.log('✅ GameObject properties connected to model');
    return window.gameObjectProperties;
};

// Enhanced GameObjects analyzer with better categorization
window.enhancedGameObjectAnalyzer = (content, filename) => {
    console.log('🔬 Enhanced GameObject analysis...');
    
    const analysis = {
        overview: {
            filename: filename,
            fileSize: content.length,
            lineCount: content.split('\n').length,
            timestamp: new Date().toISOString()
        },
        gameObjects: [],
        combat: [],
        animations: [],
        network: [],
        abilities: [],
        items: [],
        npcs: [],
        quests: []
    };
    
    // Enhanced patterns for Matrix Online
    const patterns = {
        gameObject: /CreateGoObjAndDistrObjView|GameObject.*created|spawn.*object|instantiate/gi,
        combat: /damage.*\d+|attack.*hit|defend|block|dodge|evade|critical|miss/gi,
        animation: /animation.*play|anim.*state|idle|walk|run|combat_stance/gi,
        network: /packet.*sent|packet.*received|RPC|Protocol.*\d+|network.*event/gi,
        ability: /ability.*use|skill.*activate|power.*cast|hyperboost|hack/gi,
        item: /item.*pickup|loot|inventory.*add|equipment.*equip/gi,
        npc: /NPC.*spawn|mob.*create|enemy.*appear|agent.*smith/gi,
        quest: /quest.*start|mission.*accept|objective.*complete|reward/gi
    };
    
    // Process content line by line
    const lines = content.split('\n');
    lines.forEach((line, index) => {
        const lineNum = index + 1;
        
        // Check each pattern
        Object.entries(patterns).forEach(([category, pattern]) => {
            const matches = line.match(pattern);
            if (matches) {
                const entry = {
                    line: lineNum,
                    content: line.trim(),
                    matches: matches,
                    timestamp: extractTimestamp(line),
                    values: extractValues(line)
                };
                
                // Add to appropriate category
                switch(category) {
                    case 'gameObject':
                        analysis.gameObjects.push(entry);
                        break;
                    case 'combat':
                        analysis.combat.push(entry);
                        break;
                    case 'animation':
                        analysis.animations.push(entry);
                        break;
                    case 'network':
                        analysis.network.push(entry);
                        break;
                    case 'ability':
                        analysis.abilities.push(entry);
                        break;
                    case 'item':
                        analysis.items.push(entry);
                        break;
                    case 'npc':
                        analysis.npcs.push(entry);
                        break;
                    case 'quest':
                        analysis.quests.push(entry);
                        break;
                }
            }
        });
    });
    
    // Helper functions
    function extractTimestamp(line) {
        const timestampMatch = line.match(/\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2}/);
        return timestampMatch ? timestampMatch[0] : null;
    }
    
    function extractValues(line) {
        const values = {};
        
        // Extract damage values
        const damageMatch = line.match(/damage[:\s]+(\d+)/i);
        if (damageMatch) values.damage = parseInt(damageMatch[1]);
        
        // Extract coordinates
        const coordMatch = line.match(/\((-?\d+\.?\d*),\s*(-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)/);
        if (coordMatch) {
            values.position = {
                x: parseFloat(coordMatch[1]),
                y: parseFloat(coordMatch[2]),
                z: parseFloat(coordMatch[3])
            };
        }
        
        // Extract IDs
        const idMatch = line.match(/id[:\s]+(\d+)|#(\d+)/i);
        if (idMatch) values.id = parseInt(idMatch[1] || idMatch[2]);
        
        return values;
    }
    
    // Generate summary
    analysis.summary = {
        totalEvents: Object.values(analysis).filter(v => Array.isArray(v))
            .reduce((sum, arr) => sum + arr.length, 0),
        categories: {
            gameObjects: analysis.gameObjects.length,
            combat: analysis.combat.length,
            animations: analysis.animations.length,
            network: analysis.network.length,
            abilities: analysis.abilities.length,
            items: analysis.items.length,
            npcs: analysis.npcs.length,
            quests: analysis.quests.length
        }
    };
    
    console.log('✅ Enhanced analysis complete:', analysis.summary);
    return analysis;
};

// Fix model parsing to show actual geometry info
window.enhancedModelInfo = (modelData) => {
    if (!modelData || !modelData.vertices) {
        return {
            error: 'No valid model data',
            placeholder: true
        };
    }
    
    const info = {
        format: modelData.metadata?.format || 'Unknown',
        vertices: modelData.vertices.length / 3,
        faces: modelData.indices ? modelData.indices.length / 3 : 0,
        hasUVs: modelData.uvs && modelData.uvs.length > 0,
        hasNormals: modelData.normals && modelData.normals.length > 0,
        hasBones: modelData.bones && modelData.bones.length > 0,
        hasAnimations: modelData.animations && modelData.animations.length > 0,
        boundingBox: calculateBoundingBox(modelData.vertices),
        materials: modelData.materials || [],
        lodLevels: modelData.lodLevels || 1
    };
    
    function calculateBoundingBox(vertices) {
        if (!vertices || vertices.length < 3) return null;
        
        let min = { x: Infinity, y: Infinity, z: Infinity };
        let max = { x: -Infinity, y: -Infinity, z: -Infinity };
        
        for (let i = 0; i < vertices.length; i += 3) {
            min.x = Math.min(min.x, vertices[i]);
            min.y = Math.min(min.y, vertices[i + 1]);
            min.z = Math.min(min.z, vertices[i + 2]);
            max.x = Math.max(max.x, vertices[i]);
            max.y = Math.max(max.y, vertices[i + 1]);
            max.z = Math.max(max.z, vertices[i + 2]);
        }
        
        return {
            min: min,
            max: max,
            size: {
                x: max.x - min.x,
                y: max.y - min.y,
                z: max.z - min.z
            },
            center: {
                x: (min.x + max.x) / 2,
                y: (min.y + max.y) / 2,
                z: (min.z + max.z) / 2
            }
        };
    }
    
    return info;
};

// Add model export functionality
window.exportModel = (mesh, format = 'obj') => {
    console.log(`📤 Exporting model as ${format.toUpperCase()}...`);
    
    if (!mesh || !mesh.geometry) {
        console.error('No valid mesh to export');
        return;
    }
    
    let exportData = '';
    
    if (format === 'obj') {
        // Export as Wavefront OBJ
        exportData = '# Exported from MOMS - Matrix Online Modding Suite\n';
        exportData += `# ${new Date().toISOString()}\n\n`;
        
        const geometry = mesh.geometry;
        const vertices = geometry.attributes.position;
        const normals = geometry.attributes.normal;
        const uvs = geometry.attributes.uv;
        
        // Export vertices
        for (let i = 0; i < vertices.count; i++) {
            exportData += `v ${vertices.getX(i)} ${vertices.getY(i)} ${vertices.getZ(i)}\n`;
        }
        
        // Export normals if available
        if (normals) {
            for (let i = 0; i < normals.count; i++) {
                exportData += `vn ${normals.getX(i)} ${normals.getY(i)} ${normals.getZ(i)}\n`;
            }
        }
        
        // Export UVs if available
        if (uvs) {
            for (let i = 0; i < uvs.count; i++) {
                exportData += `vt ${uvs.getX(i)} ${uvs.getY(i)}\n`;
            }
        }
        
        // Export faces
        if (geometry.index) {
            for (let i = 0; i < geometry.index.count; i += 3) {
                const a = geometry.index.getX(i) + 1;
                const b = geometry.index.getX(i + 1) + 1;
                const c = geometry.index.getX(i + 2) + 1;
                exportData += `f ${a} ${b} ${c}\n`;
            }
        }
    }
    
    // Download the file
    const blob = new Blob([exportData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `model_export.${format}`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('✅ Model exported successfully');
};

console.log('✅ Cutscenes and GameObjects fixes loaded');
console.log('💡 New functions available:');
console.log('   - window.enhancedBikPlayer() - Better BIK video handling');
console.log('   - window.connectGameObjectToModel() - Connect UI to 3D model');
console.log('   - window.enhancedGameObjectAnalyzer() - Better log analysis');
console.log('   - window.exportModel() - Export 3D models as OBJ');
// Fix for 3D Models tab initialization - Auto-load index and PKB files

// Enhanced initialization for 3D Models tab
window.init3DModelsTab = async () => {
    console.log('🎮 Initializing 3D Models Tab...');
    
    // Step 1: Auto-load index file if not loaded
    if (!window.MXO_PKB_INDEX_DATA) {
        console.log('📋 Auto-loading index file...');
        const loaded = await window.loadIndexFile();
        if (loaded) {
            console.log('✅ Index file auto-loaded');
        } else {
            console.log('⚠️ No index file found in cache/');
        }
    } else {
        console.log('✅ Index already loaded');
    }
    
    // Step 2: Check for PKB files in cache and auto-load them
    if (!window.MXO_PKB_FILES || Object.keys(window.MXO_PKB_FILES).length === 0) {
        console.log('📦 Checking for PKB files to auto-load...');
        
        const pkbFilesToLoad = ['worlds_3g.pkb', 'char_npc.pkb'];
        let loadedCount = 0;
        
        for (const pkbFile of pkbFilesToLoad) {
            try {
                console.log(`📥 Attempting to load ${pkbFile}...`);
                const response = await fetch(`/cache/${pkbFile}`);
                
                if (response.ok) {
                    const arrayBuffer = await response.arrayBuffer();
                    if (!window.MXO_PKB_FILES) {
                        window.MXO_PKB_FILES = {};
                    }
                    window.MXO_PKB_FILES[pkbFile.toLowerCase()] = arrayBuffer;
                    console.log(`✅ Loaded ${pkbFile}: ${arrayBuffer.byteLength} bytes`);
                    loadedCount++;
                } else {
                    console.log(`⚠️ ${pkbFile} not found in cache/`);
                }
            } catch (error) {
                console.log(`❌ Error loading ${pkbFile}:`, error.message);
            }
        }
        
        if (loadedCount > 0) {
            console.log(`✅ Auto-loaded ${loadedCount} PKB files`);
        } else {
            console.log('⚠️ No PKB files found in cache/');
            console.log('💡 To load PKB files: Go to Archives tab and click on PKB files');
        }
    } else {
        console.log(`✅ PKB files already loaded: ${Object.keys(window.MXO_PKB_FILES).join(', ')}`);
    }
    
    // Step 3: Load enhanced extraction if available
    if (!window.extractFromPKBEnhanced) {
        try {
            const script = document.createElement('script');
            script.src = '/fix_pkb_extraction.js';
            document.head.appendChild(script);
            await new Promise((resolve) => {
                script.onload = () => {
                    console.log('✅ Enhanced extraction loaded');
                    resolve();
                };
                script.onerror = () => {
                    console.log('⚠️ Enhanced extraction not available');
                    resolve();
                };
            });
        } catch (error) {
            console.log('⚠️ Could not load enhanced extraction');
        }
    }
    
    console.log('🎯 3D Models tab ready!');
    
    // Return status
    return {
        indexLoaded: !!window.MXO_PKB_INDEX_DATA,
        pkbFiles: Object.keys(window.MXO_PKB_FILES || {}),
        enhancedExtraction: !!window.extractFromPKBEnhanced
    };
};

// Auto-initialize when switching to 3D Models tab
console.log('✅ 3D Models initialization function ready');
console.log('💡 Call window.init3DModelsTab() when opening 3D Models tab');
// Fix to show extracted files in UI with viewing capability

// Store extracted files globally for easy access
window.MXO_EXTRACTED_FILES = window.MXO_EXTRACTED_FILES || {};

// Enhanced extraction that stores files for viewing
window.extractFromPKBWithUI = async (pkbFileName) => {
    console.log(`🎯 Extracting from ${pkbFileName} with UI support...`);
    
    // Use the enhanced extraction
    const extractedFiles = await window.extractFromPKB(pkbFileName);
    
    if (extractedFiles.length > 0) {
        console.log(`✅ Extracted ${extractedFiles.length} files, preparing for UI...`);
        
        // Store extracted files globally
        if (!window.MXO_EXTRACTED_FILES[pkbFileName]) {
            window.MXO_EXTRACTED_FILES[pkbFileName] = [];
        }
        
        extractedFiles.forEach(file => {
            // Create proper file object for UI
            const blob = new Blob([file.data], { type: 'application/octet-stream' });
            const fileObj = new File([blob], file.name, {
                lastModified: Date.now()
            });
            
            // Store with metadata
            window.MXO_EXTRACTED_FILES[pkbFileName].push({
                name: file.name,
                size: file.size,
                offset: file.offset,
                file: fileObj,
                data: file.data,
                pkb: pkbFileName
            });
        });
        
        console.log(`📦 Files ready for viewing in UI`);
    }
    
    return extractedFiles;
};

// Function to display extracted files in a nice UI
window.showExtractedFilesUI = () => {
    console.log('📋 Showing extracted files UI...');
    
    const allExtracted = window.MXO_EXTRACTED_FILES;
    const totalFiles = Object.values(allExtracted).flat().length;
    
    if (totalFiles === 0) {
        console.log('❌ No extracted files to show');
        return;
    }
    
    // Create modal or panel to show files
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #001100;
        border: 2px solid #00ff00;
        padding: 20px;
        max-width: 80%;
        max-height: 80%;
        overflow-y: auto;
        z-index: 1000;
        font-family: monospace;
        color: #00ff00;
    `;
    
    let html = '<h2>📦 Extracted Files</h2>';
    html += `<p>Total: ${totalFiles} files</p>`;
    html += '<button onclick="this.parentElement.remove()" style="float: right; background: #030; color: #0f0; border: 1px solid #0f0; padding: 5px;">Close</button>';
    html += '<div style="clear: both; margin-top: 10px;">';
    
    Object.entries(allExtracted).forEach(([pkbName, files]) => {
        html += `<h3>📦 ${pkbName} (${files.length} files)</h3>`;
        html += '<ul style="list-style: none; padding: 0;">';
        
        files.forEach((file, index) => {
            const ext = file.name.split('.').pop().toLowerCase();
            const icon = ext === 'moa' ? '🧍' : ext === 'prop' ? '🏠' : '📄';
            
            html += `<li style="padding: 5px; border-bottom: 1px solid #003300;">`;
            html += `${icon} <strong>${file.name}</strong> `;
            html += `<span style="color: #00aa00;">(${file.size} bytes)</span> `;
            html += `<button onclick="window.viewExtractedFile('${pkbName}', ${index})" style="background: #030; color: #0f0; border: 1px solid #0f0; padding: 2px 8px; margin-left: 10px;">View</button>`;
            html += `</li>`;
        });
        
        html += '</ul>';
    });
    
    html += '</div>';
    modal.innerHTML = html;
    document.body.appendChild(modal);
};

// Function to view a specific extracted file
window.viewExtractedFile = (pkbName, fileIndex) => {
    const file = window.MXO_EXTRACTED_FILES[pkbName]?.[fileIndex];
    if (!file) {
        console.error('File not found');
        return;
    }
    
    console.log(`👁️ Viewing: ${file.name}`);
    
    // Check file type
    const ext = file.name.split('.').pop().toLowerCase();
    
    if (ext === 'moa' || ext === 'prop') {
        // For 3D models, trigger the model viewer
        console.log('🎮 Opening in 3D viewer...');
        
        // Find the file select handler
        if (window.handleFileSelect) {
            window.handleFileSelect(file.name, { type: 'file', file: file.file });
            
            // Switch to explorer view by clicking the tab
            const tabs = document.querySelectorAll("div[class*='cursor-pointer'][class*='rounded-t']");
            for (const tab of tabs) {
                if (tab.textContent.trim() === 'File Explorer') {
                    tab.click();
                    break;
                }
            }
        } else {
            console.error('File select handler not found');
        }
    } else {
        // For other files, show hex dump or text
        const data = file.data;
        const text = Array.from(data.slice(0, 256))
            .map(b => b.toString(16).padStart(2, '0'))
            .join(' ');
        
        alert(`File: ${file.name}\nSize: ${file.size} bytes\nFirst 256 bytes (hex):\n${text}`);
    }
};

// Enhanced Extract All Models button
window.extractAllModelsWithUI = async () => {
    console.log('🎯 Extracting all models with UI support...');
    
    const pkbFiles = Object.keys(window.MXO_PKB_FILES || {});
    if (pkbFiles.length === 0) {
        alert('No PKB files loaded. Click on PKB files in Archives tab first.');
        return;
    }
    
    // Clear previous extractions
    window.MXO_EXTRACTED_FILES = {};
    
    let totalExtracted = 0;
    for (const pkbFile of pkbFiles) {
        const files = await window.extractFromPKBWithUI(pkbFile);
        totalExtracted += files.length;
    }
    
    if (totalExtracted > 0) {
        console.log(`✅ Total extracted: ${totalExtracted} files`);
        // Show the UI
        window.showExtractedFilesUI();
    } else {
        alert('No files were extracted. Check console for details.');
    }
};

console.log('✅ Extracted files UI enhancement loaded');
console.log('💡 Functions available:');
console.log('   - window.extractAllModelsWithUI() - Extract and show UI');
console.log('   - window.showExtractedFilesUI() - Show extracted files');
console.log('   - window.viewExtractedFile(pkb, index) - View specific file');
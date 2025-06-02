# File Restoration Instructions

The JavaScript files (components.js and app.js) have been deleted from the split-version directory.

## To Restore the Files

Since the git repository appears to be in a parent directory that I cannot access due to security restrictions, you'll need to restore the files manually.

### Option 1: From Git (Recommended)
```bash
cd /Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN
git checkout moms/split-version/components.js
git checkout moms/split-version/app.js
git checkout moms/split-version/components_compiled.js
git checkout moms/split-version/app_compiled.js
git checkout moms/split-version/mxo-protocol-parser.js
git checkout moms/split-version/mxo-protocol-parser-v2.js
git checkout moms/split-version/bik-decoder.js
git checkout moms/split-version/build.sh
```

### Option 2: From Backup
If you have a backup of the MOMS project, copy these files:
- components.js (main UI components, ~3000 lines)
- app.js (main application logic, ~2000 lines)
- mxo-protocol-parser.js
- mxo-protocol-parser-v2.js
- bik-decoder.js
- build.sh

### Option 3: From Another Location
Check if the files exist elsewhere:
```bash
find ~ -name "components.js" -path "*/moms/*" -type f 2>/dev/null
```

## Current Status
✅ Servers are running:
- Main server: http://localhost:8000 (PID: 41102)
- BIK proxy: http://localhost:8002 (PID: 41103)

❌ Missing files:
- components.js
- app.js
- Other supporting JavaScript files

## What Was Lost
The missing files contained:
1. **components.js**: React components for UI, packet analysis, file browser, video player
2. **app.js**: Main application logic, packet parsing, combat analysis
3. **Protocol parsers**: Matrix Online packet decoding logic
4. **Build scripts**: Compilation tools

Without these files, the application cannot function.
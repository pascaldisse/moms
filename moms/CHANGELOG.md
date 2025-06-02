# Changelog

All notable changes to the Matrix Online Modding Suite (MOMS) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-06-02

### Added
- Enhanced GameObjects & Combat Analyzer with support for 30+ combat patterns
- XML/JSON parsing for structured combat data files
- Combat value extraction (damage numbers, percentages, dice rolls)
- Support for config files (.cfg, .ini, .dat, .csv)
- "Toggle Lights" button in 3D viewer for scene lighting control
- "Export OBJ" button with comprehensive Wavefront OBJ export functionality
- Enhanced lighting system with ambient, directional, point, and fill lights
- Improved material properties with specular and shininess settings
- Shadow mapping and tone mapping for better visual quality
- WebGL context loss/restore handling for stability
- parseMGA parser for model group/collection files (.mga/.mgc)
- Comprehensive technical documentation (TECHNICAL.md)
- Detailed README with usage instructions

### Changed
- **CRITICAL**: Corrected model file format support (Matrix Online does NOT use .mob files)
- Updated supported model formats: .moa, .prop, .iprf, .eprf, .mga, .mgc
- Renamed parseMOB to parseMOA to reflect correct format
- Enhanced file categorization with combat, animation, mission categories
- Improved pattern matching for Matrix Online specific terms
- Updated UI to show correct file format information and descriptions
- Enhanced metadata with engine details and scale information

### Fixed
- Syntax error in analyzeLogFile function (missing closing brace)
- Model format descriptions now accurately reflect MXO file types
- File type detection for actual Matrix Online model formats

### Technical Details
- Engine: Modified Lithtech Discovery (unique to MXO)
- Scale: 1 unit = 1 centimeter
- Model formats properly documented with LOD and bone weight information

## [2.0.0] - 2025-06-02 (Earlier Session)

### Added
- GameObjects Log Analyzer for Matrix Online server/client logs
- Pattern recognition for GameObject creation, RPC calls, and combat events
- Multi-file upload support for log analysis
- Real-time statistics dashboard
- Advanced filtering and sorting capabilities
- THREE.js ES module migration (r153 to r169)

### Changed
- Migrated from deprecated THREE.js builds to ES modules
- Enhanced MOB parser with magic number detection
- Improved 3D viewer controls (WADR movement system)

### Fixed
- THREE.js deprecation warnings
- OrbitControls loading issues (with fallback)
- MOB file parsing vertex validation

## [1.0.0] - 2025-06-02 (Initial Session)

### Added
- Initial MOMS restoration from single-file application
- Basic 3D model viewing (.abc, .mob files)
- Texture viewer for DTX, DDS formats
- Code editor with Monaco Editor
- BIK video support with FFmpeg proxy
- File browser with directory loading
- Matrix-themed UI

### Known Issues
- THREE.js OrbitControls may fail to load
- BIK video path hardcoded in proxy server
- Large files cause performance issues
- Single-file architecture (5000+ lines)

---

## Version History

- **3.0.0** - Major update with correct MXO file format support and enhanced combat analyzer
- **2.0.0** - Added GameObjects analyzer and THREE.js modernization
- **1.0.0** - Initial restoration of MOMS application
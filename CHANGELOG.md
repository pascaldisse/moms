# Changelog

All notable changes to the Matrix Online Modding Suite (MOMS) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-06

### Added
- **Comprehensive Test Suite** (`test_suite.html`) with automated testing for all components
- **Performance Monitoring** system with real-time memory and processing time tracking
- **Global Error Handler** with user-friendly messages and GitHub issue reporting
- **PKB Archive Extraction** with individual file extraction buttons for each PKB
- **Enhanced Combat Analyzer** with XML/JSON parsing and value extraction (damage numbers, percentages, dice rolls)
- **Three.js ES Modules Support** in `index_modern.html` (THREE.js r169)
- **Export Functionality** for 3D models to Wavefront OBJ format with proper vertex/normal/UV data
- **Advanced Pattern Recognition** for combat logs (30+ combat types including crowd control, buffs/debuffs)

### Fixed
- **THREE.js Loading Issues** - Fixed "Cannot add property OrbitControls, object is not extensible" error
- **Event Handler Scope Issues** - Properly declared variables to prevent undefined errors in cleanup
- **PKB File Processing** - Now stores PKB data globally for extraction when index is available
- **Model Format Corrections** - Fixed misconception about .mob files (MXO uses .moa, .prop, etc.)
- **OrbitControls Initialization** - Added fallback manual camera controls when OrbitControls fails

### Changed
- **Camera Controls** - Updated movement keys to W=Forward, A=Left, D=Backward, R=Right
- **Enhanced Lighting System** - Multiple light sources with shadows and tone mapping
- **File Type Detection** - Corrected Matrix Online file format support (.moa, .prop, .mga, .mgc)
- **Combat Log Analysis** - Expanded from basic patterns to structured data parsing with value extraction
- **UI Improvements** - Added individual PKB extraction buttons with status feedback

### Documentation
- **README.md** - Completely rewritten with comprehensive feature list and current status
- **CLAUDE.md** - Updated with all session changes and technical implementation details
- **TECHNICAL.md** - Enhanced with correct Matrix Online file format specifications

## [2.0.0] - 2025-01-05

### Added
- **GameObjects Tab** with transform controls, component management, tags & layers
- **Enhanced 3D Viewer** with toggle lights and material controls
- **PKB Archive Support** with proper index file handling
- **BIK Video Integration** with real-time FFmpeg conversion
- **Combat Log Analyzer** with advanced pattern recognition
- **Model Statistics** showing counts of visible models, MOA files, PROP files

### Fixed
- **Scale Conversion** for Matrix Online models (1 unit = 1cm → 0.01m for THREE.js)
- **Model Format Support** - Added proper .moa, .prop, .iprf, .eprf, .mga, .mgc parsing
- **THREE.js Deprecation Warnings** - Began migration from deprecated build files

### Changed
- **File Extensions** - Corrected Matrix Online model formats (removed .mob misconception)
- **3D Viewer Lighting** - Enhanced with ambient, directional, point, and fill lights
- **Archive Handling** - Added PKB archive alerts and extraction guidance

## [1.2.0] - 2025-01-04

### Added
- **Archive Browser Tab** for exploring REZ, LTA, LTB, PKB files
- **Cutscenes Browser Tab** for BIK video files
- **Audio Browser Tab** for sound files
- **Multiple File Format Support** including animations, assemblies, logs

### Fixed
- **File Type Detection** improvements
- **Error Handling** for unsupported file types
- **Memory Management** for large files

### Changed
- **UI Layout** with tabbed interface for different file types
- **File Browser** organization and navigation

## [1.1.0] - 2025-01-03

### Added
- **Monaco Editor Integration** for script editing with syntax highlighting
- **3D Model Viewer** with THREE.js and OrbitControls
- **Texture Viewer** with support for various image formats
- **File Type Icons** and improved visual indicators

### Fixed
- **CORS Issues** with proper server configuration
- **File Reading** for binary formats
- **Performance Issues** with large directory structures

### Changed
- **Server Architecture** - Separated into main server and BIK proxy server
- **Component Structure** - Modularized React components

## [1.0.0] - 2025-01-02

### Added
- **Initial Release** of Matrix Online Modding Suite
- **Basic File Browser** with directory loading
- **Single-file Application** architecture
- **Server Components** (`server.py`, `simple-bik-server.py`)
- **Matrix-themed UI** with green-on-black styling

### Features
- File type detection and categorization
- Basic 3D model support
- Archive file exploration
- Video file handling
- Script file viewing

## [0.9.0] - 2025-01-01

### Added
- **Project Initialization** from Matrix Online Modding Suite requirements
- **File Structure** setup with documentation
- **Basic React Application** with component architecture
- **THREE.js Integration** for 3D rendering

### Infrastructure
- Git repository initialization
- Server setup scripts
- Basic documentation structure
- Development environment configuration

---

## Version History Summary

- **v2.1.0** (Current) - Comprehensive testing, performance monitoring, error handling
- **v2.0.0** - Major feature additions (GameObjects, PKB support, combat analyzer)
- **v1.2.0** - Multi-tab interface and file format expansion
- **v1.1.0** - Monaco Editor and 3D viewer implementation
- **v1.0.0** - Initial stable release
- **v0.9.0** - Project foundation and basic functionality

## Development Notes

### Breaking Changes
- **v2.0.0**: File format corrections (removed .mob support, added .moa/.prop)
- **v1.2.0**: UI restructure with tabbed interface
- **v1.0.0**: Single-file architecture establishment

### Migration Guide
- **From v1.x to v2.x**: Update file type expectations (.mob → .moa/.prop)
- **From v0.x to v1.x**: Use new tabbed interface, update server startup scripts

### Future Versions
- **v2.2.0** (Planned) - CNB cutscene viewer and texture mapping
- **v2.3.0** (Planned) - Animation system and timeline controls  
- **v3.0.0** (Planned) - Modular architecture and build system

---

*For detailed technical information about each release, see [CLAUDE.md](CLAUDE.md)*
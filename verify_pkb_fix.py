#!/usr/bin/env python3
"""
Verify the PKB extraction fix is working
"""

import urllib.request
import json
import time

def test_enhanced_extraction():
    """Test if the enhanced extraction is loaded"""
    print("🧪 Testing Enhanced PKB Extraction...")
    
    try:
        # Check if fix_pkb_extraction.js is accessible
        response = urllib.request.urlopen('http://localhost:8000/fix_pkb_extraction.js', timeout=5)
        if response.getcode() == 200:
            print("✅ Enhanced extraction script accessible")
        else:
            print("❌ Enhanced extraction script not found")
            return False
            
        # Check if test page is accessible
        response = urllib.request.urlopen('http://localhost:8000/test_pkb_extraction.html', timeout=5)
        if response.getcode() == 200:
            print("✅ Test page accessible")
        else:
            print("❌ Test page not found")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error accessing files: {e}")
        return False

def display_test_instructions():
    """Display clear testing instructions"""
    print("\n" + "="*60)
    print("🎯 PKB EXTRACTION TESTING INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 METHOD 1: Using the Test Page (Recommended)")
    print("1. Open: http://localhost:8000/test_pkb_extraction.html")
    print("2. Click buttons in order:")
    print("   - 'Load Test Index' (loads packmap_save.lta)")
    print("   - 'Load worlds_3g.pkb'")
    print("   - 'Check Status' (verify files loaded)")
    print("   - 'Test Extract' (see detailed extraction logs)")
    print("3. Check the Activity Log for detailed information")
    
    print("\n📋 METHOD 2: Using Main MOMS Application")
    print("1. Open: http://localhost:8000")
    print("2. Open browser console (F12)")
    print("3. Go to Archives tab")
    print("4. Click on 'worlds_3g.pkb' to load it")
    print("5. Watch console for: '✅ Loaded PKB file into memory'")
    print("6. Go to 3D Models tab")
    print("7. Click 'Debug Info' button - check PKB files are loaded")
    print("8. Click 'Test Extract' button - see extraction logs")
    print("9. Click 'Extract All Models' - see comprehensive logs")
    
    print("\n🔍 WHAT TO LOOK FOR IN CONSOLE:")
    print("- '✅ Index data available: XXX bytes'")
    print("- '✅ PKB data available: XXX bytes'")
    print("- '🔧 Step 3: Parsing index file...'")
    print("- '📊 === EXTRACTION RESULTS ==='")
    print("- Details about extracted files or why extraction failed")
    
    print("\n⚠️ COMMON ISSUES:")
    print("1. If no files extracted: Check console for format detection")
    print("2. If PKB not loaded: Make sure you clicked on it in Archives")
    print("3. If index not loaded: Check packmap_save.lta is in cache/")
    
    print("\n💡 The enhanced logging will show EXACTLY why extraction")
    print("   is failing and what format the files are using.")
    print("="*60)

def run_verification():
    """Run the verification process"""
    print("🔍 PKB Extraction Fix Verification")
    print("="*40)
    
    # Test enhanced extraction
    if test_enhanced_extraction():
        print("\n✅ All files deployed successfully!")
        
        # Display instructions
        display_test_instructions()
        
        print("\n🚀 READY TO TEST!")
        print("Follow the instructions above to test PKB extraction.")
        return True
    else:
        print("\n❌ Some files are missing")
        print("Make sure the server is running: python3 server.py")
        return False

if __name__ == "__main__":
    import sys
    success = run_verification()
    sys.exit(0 if success else 1)
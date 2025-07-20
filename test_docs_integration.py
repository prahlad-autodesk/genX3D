#!/usr/bin/env python3
"""
Test script to verify documentation integration
"""
import os
import subprocess
import time
import requests

def test_documentation_files():
    """Test that documentation files are in place"""
    print("🔍 Testing documentation files...")
    
    # Check if docs directory exists
    docs_dir = "static/docs"
    if not os.path.exists(docs_dir):
        print("❌ Documentation directory not found")
        return False
    
    # Check if index.html exists
    index_file = os.path.join(docs_dir, "index.html")
    if not os.path.exists(index_file):
        print("❌ Documentation index.html not found")
        return False
    
    print("✅ Documentation files are in place")
    return True

def test_backend_integration():
    """Test backend integration"""
    print("\n🔍 Testing backend integration...")
    
    # Check if main.py has the docs mount
    with open("backend/main.py", "r") as f:
        content = f.read()
        if "app.mount(\"/documentation\"" in content:
            print("✅ Documentation mount found in main.py")
        else:
            print("❌ Documentation mount not found in main.py")
            return False
    
        # Check if root redirect is configured
        if "RedirectResponse(url=\"/documentation/\")" in content:
            print("✅ Root redirect to docs configured")
        else:
            print("❌ Root redirect not configured")
            return False
    
    return True

def test_frontend_integration():
    """Test frontend integration"""
    print("\n🔍 Testing frontend integration...")
    
    # Check if docs button is in the HTML
    with open("frontend/CascadeStudio/index.html", "r") as f:
        content = f.read()
        if "📚 Docs" in content:
            print("✅ Documentation button found in frontend")
        else:
            print("❌ Documentation button not found in frontend")
            return False
        
        if 'href="/documentation"' in content:
            print("✅ Documentation link configured correctly")
        else:
            print("❌ Documentation link not configured correctly")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing genx3D Documentation Integration")
    print("=" * 50)
    
    # Test documentation files
    docs_ok = test_documentation_files()
    
    # Test backend integration
    backend_ok = test_backend_integration()
    
    # Test frontend integration
    frontend_ok = test_frontend_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Documentation Files: {'✅ PASS' if docs_ok else '❌ FAIL'}")
    print(f"Backend Integration: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Frontend Integration: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if all([docs_ok, backend_ok, frontend_ok]):
        print("\n🎉 All tests passed! Documentation integration is ready.")
        print("\n📋 Next steps:")
        print("1. Start your backend server: cd backend && python -m uvicorn main:app --reload --port 8000")
        print("2. Access your app at: http://localhost:8000/app/")
        print("3. Click the '📚 Docs' button to open documentation")
        print("4. Or access docs directly at: http://localhost:8000/documentation/")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 
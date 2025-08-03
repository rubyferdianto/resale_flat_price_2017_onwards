#!/usr/bin/env python3
"""
Setup Script for Singapore Resale Flat Price Analysis Project
This script helps set up the environment and dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_conda():
    """Check if conda is available."""
    try:
        subprocess.run(['conda', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False

def setup_conda_environment():
    """Set up conda environment."""
    print("\n🔧 Setting up Conda environment...")
    
    if not check_conda():
        print("❌ Conda not found. Please install Anaconda or Miniconda first.")
        print("Download from: https://docs.conda.io/en/latest/miniconda.html")
        return False
    
    # Create environment
    if run_command("conda env create -f environment.yml", "Creating conda environment"):
        print("✅ Conda environment 'resale-flat-analysis' created successfully")
        print("\n🎯 To activate the environment, run:")
        print("   conda activate resale-flat-analysis")
        return True
    else:
        print("❌ Failed to create conda environment")
        return False

def setup_pip_environment():
    """Set up pip environment."""
    print("\n🔧 Setting up pip environment...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  It's recommended to use a virtual environment")
        print("   Create one with: python -m venv venv")
        print("   Activate with: source venv/bin/activate (macOS/Linux) or venv\\Scripts\\activate (Windows)")
        
        response = input("\nContinue with global installation? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Install requirements
    if run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("✅ Python packages installed successfully")
        return True
    else:
        print("❌ Failed to install Python packages")
        return False

def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import pandas as pd
        import numpy as np
        import streamlit as st
        import plotly.express as px
        import requests
        
        print("✅ All required packages imported successfully")
        
        # Test data fetcher
        from data_fetcher import ResaleFlatDataFetcher
        fetcher = ResaleFlatDataFetcher()
        print("✅ Data fetcher module loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("SINGAPORE RESALE FLAT PRICE ANALYSIS - SETUP")
    print("=" * 60)
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Check what files exist
    print("\n📁 Checking project files...")
    required_files = [
        'environment.yml',
        'requirements.txt',
        'data_fetcher.py',
        'streamlit_app.py',
        'data_analysis.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        print("Please ensure all project files are present.")
        sys.exit(1)
    
    # Choose installation method
    print("\n🚀 Choose installation method:")
    print("1. Conda (Recommended)")
    print("2. Pip")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    success = False
    if choice == "1":
        success = setup_conda_environment()
    elif choice == "2":
        success = setup_pip_environment()
    else:
        print("❌ Invalid choice. Please run the script again.")
        sys.exit(1)
    
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Test installation (only for pip, conda needs activation first)
    if choice == "2":
        if test_installation():
            print("\n🎉 Setup completed successfully!")
        else:
            print("\n❌ Setup completed but testing failed. Please check your installation.")
            sys.exit(1)
    
    # Final instructions
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    
    if choice == "1":
        print("\n🎯 Next steps:")
        print("1. Activate the environment: conda activate resale-flat-analysis")
        print("2. Test the installation: python run_analysis.py")
        print("3. Start the dashboard: streamlit run streamlit_app.py")
    else:
        print("\n🎯 Next steps:")
        print("1. Test the installation: python run_analysis.py")
        print("2. Start the dashboard: streamlit run streamlit_app.py")
    
    print("\n📚 Documentation:")
    print("- Project overview: New_Readme.md")
    print("- Original notes: readme.md")
    
    print("\n🌐 Dashboard URL (after running streamlit):")
    print("   http://localhost:8501")

if __name__ == "__main__":
    main()

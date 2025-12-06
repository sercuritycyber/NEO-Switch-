#!/bin/bash
# NeoSwitch Build Script
# Builds standalone executable using PyInstaller

set -e  # Exit on error

echo "🚀 NeoSwitch Build Script"
echo "=========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
OS=$(uname -s)
echo -e "${BLUE}📋 Detected OS: ${OS}${NC}"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ ${PYTHON_VERSION} found${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip3 install --upgrade pyinstaller customtkinter psutil --break-system-packages || {
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
}
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Clean previous builds
echo ""
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build dist __pycache__ *.spec
echo -e "${GREEN}✓ Cleaned${NC}"

# Build directly with pyinstaller
echo ""
echo -e "${YELLOW}🔨 Building executable (this may take a few minutes)...${NC}"

pyinstaller --onefile \
    --windowed \
    --name neoswitch \
    --hidden-import customtkinter \
    --hidden-import psutil \
    --hidden-import tkinter \
    --hidden-import threading \
    --hidden-import subprocess \
    --hidden-import platform \
    --hidden-import stat \
    --collect-data customtkinter \
    vpngui.py || {
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
}

# Check output
echo ""
if [ "$OS" = "Darwin" ]; then
    if [ -f "dist/neoswitch" ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        echo ""
        echo -e "${BLUE}📦 Output:${NC}"
        echo -e "   ${GREEN}dist/neoswitch${NC}"
        echo ""
        echo -e "${BLUE}🚀 Run with:${NC}"
        echo -e "   ${YELLOW}sudo ./dist/neoswitch${NC}"
        echo ""
        echo -e "${BLUE}💡 Tip:${NC} Install system-wide:"
        echo -e "   ${YELLOW}sudo cp dist/neoswitch /usr/local/bin/${NC}"
    else
        echo -e "${RED}❌ Build completed but output not found${NC}"
        exit 1
    fi
else
    if [ -f "dist/neoswitch" ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        echo ""
        echo -e "${BLUE}📦 Output:${NC}"
        echo -e "   ${GREEN}dist/neoswitch${NC}"
        echo ""
        
        # Make executable
        chmod +x dist/neoswitch
        
        echo -e "${BLUE}🚀 Run with:${NC}"
        echo -e "   ${YELLOW}sudo ./dist/neoswitch${NC}"
        echo ""
        echo -e "${BLUE}💡 Tip:${NC} Install system-wide:"
        echo -e "   ${YELLOW}sudo cp dist/neoswitch /usr/local/bin/${NC}"
        
        # Get size
        SIZE=$(du -h dist/neoswitch | cut -f1)
        echo ""
        echo -e "${BLUE}📊 File size:${NC} ${SIZE}"
    else
        echo -e "${RED}❌ Build completed but output not found${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}✨ Done!${NC}"
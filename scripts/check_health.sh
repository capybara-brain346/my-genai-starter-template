#!/usr/bin/env bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN} $1${NC}"
    else
        echo -e "${RED} $1${NC}"
    fi
}

check_command() {
    if command -v $1 >/dev/null 2>&1; then
        print_status "$1 is installed" 0
        return 0
    else
        print_status "$1 is not installed" 1
        return 1
    fi
}

echo -e "${YELLOW}Starting Health Check...${NC}"
echo "=========================="

echo -e "\n${YELLOW}Checking Python Installation:${NC}"
check_command python
PYTHON_VERSION=$(python --version 2>&1)
echo "Python Version: $PYTHON_VERSION"

echo -e "\n${YELLOW}Checking Dependencies:${NC}"
if [ -f "requirements.txt" ]; then
    print_status "requirements.txt exists" 0
    
    key_packages=("fastapi" "google-generativeai")
    for package in "${key_packages[@]}"; do
        if pip show $package > /dev/null 2>&1; then
            print_status "$package is installed" 0
        else
            print_status "$package is not installed" 1
        fi
    done
else
    print_status "requirements.txt not found" 1
fi

echo -e "\n${YELLOW}Checking Environment Variables:${NC}"
if [ -f ".env" ]; then
    print_status ".env file exists" 0
    if grep -q "GOOGLE_API_KEY" .env; then
        if grep -q "GOOGLE_API_KEY=\"\"" .env || grep -q "GOOGLE_API_KEY=$" .env; then
            print_status "GOOGLE_API_KEY is empty" 1
        else
            print_status "GOOGLE_API_KEY is set" 0
        fi
    else
        print_status "GOOGLE_API_KEY not found in .env" 1
    fi
else
    print_status ".env file not found" 1
fi

# Check if FastAPI server can start
echo -e "\n${YELLOW}Checking FastAPI Server:${NC}"
if pgrep -f "fastapi" > /dev/null; then
    print_status "FastAPI server is running" 0
else
    print_status "FastAPI server is not running" 1
    echo -e "${YELLOW}Tip: Start the server using the start_server script${NC}"
fi

# Check disk space
echo -e "\n${YELLOW}Checking System Resources:${NC}"
df -h . | awk 'NR==2 {print "Disk Space: " $4 " available"}'

echo -e "\n${YELLOW}Health Check Complete${NC}"
echo "=========================="

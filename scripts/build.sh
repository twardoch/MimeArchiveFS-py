#!/bin/bash
# this_file: scripts/build.sh
# Build script for the package

set -e

echo "🏗️ Building package..."

# Change to the project root directory
cd "$(dirname "$0")/.."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "📦 Building package..."
hatch build

echo "✅ Package built successfully!"
echo "📦 Built files:"
ls -la dist/
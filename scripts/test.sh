#!/bin/bash
# this_file: scripts/test.sh
# Test script for the package

set -e

echo "🧪 Running tests..."

# Change to the project root directory
cd "$(dirname "$0")/.."

# Run linting and formatting checks
echo "📋 Running linting and formatting checks..."
hatch run lint:style

# Run tests with coverage
echo "🔍 Running tests with coverage..."
hatch run test

echo "✅ All tests passed!"
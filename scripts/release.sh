#!/bin/bash
# this_file: scripts/release.sh
# Release script for the package

set -e

echo "🚀 Preparing release..."

# Change to the project root directory
cd "$(dirname "$0")/.."

# Check if we're on the main branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
    echo "⚠️  Warning: You are not on the main branch. Current branch: $BRANCH"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Release cancelled."
        exit 1
    fi
fi

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Please commit or stash changes."
    git status --short
    exit 1
fi

# Run tests first
echo "🧪 Running tests before release..."
./scripts/test.sh

# Build the package
echo "🏗️ Building package..."
./scripts/build.sh

# Get the current version from git
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "📋 Current version: $CURRENT_VERSION"

# Prompt for new version
echo "🏷️  Enter new version (format: vX.Y.Z):"
read NEW_VERSION

# Validate version format
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Invalid version format. Use vX.Y.Z (e.g., v1.0.0)"
    exit 1
fi

# Check if tag already exists
if git tag --list | grep -q "^$NEW_VERSION$"; then
    echo "❌ Tag $NEW_VERSION already exists."
    exit 1
fi

# Create and push tag
echo "🏷️  Creating and pushing tag $NEW_VERSION..."
git tag "$NEW_VERSION"
git push origin "$NEW_VERSION"

echo "✅ Release $NEW_VERSION created successfully!"
echo "🎉 GitHub Actions will now build and publish the release."
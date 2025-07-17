#!/bin/bash
# this_file: scripts/dev-setup.sh
# Development environment setup script

set -e

echo "🔧 Setting up development environment..."

# Change to the project root directory
cd "$(dirname "$0")/.."

# Check if hatch is installed
if ! command -v hatch &> /dev/null; then
    echo "📦 Installing hatch..."
    if command -v pipx &> /dev/null; then
        pipx install hatch
    else
        echo "Installing pipx first..."
        python -m pip install --user pipx
        python -m pipx ensurepath
        pipx install hatch
    fi
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚡ Installing uv..."
    if command -v pipx &> /dev/null; then
        pipx install uv
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
fi

# Configure hatch to use uv
echo "⚙️  Configuring hatch to use uv..."
hatch config set dirs.env.virtual.uv "$(command -v uv)"

# Create development environment
echo "🏠 Creating development environment..."
hatch env create

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
hatch run pre-commit install

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  • Run tests: ./scripts/test.sh"
echo "  • Build package: ./scripts/build.sh"
echo "  • Enter development shell: hatch shell"
echo "  • Run linting: hatch run lint:style"
#!/bin/bash
# Script to run the AIKB agent with proper environment setup

echo "🤖 Starting AIKB Agent..."

# Store the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: python -m venv .venv"
    echo "   Then install dependencies: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activating virtual environment..."
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Check if dependencies are installed
if ! python -c "import google.adk" 2>/dev/null; then
    echo "❌ Dependencies not installed!"
    echo "   Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "❌ Configuration file not found!"
    echo "   Please copy .env.example to .env and add your API key"
    echo "   Command: cp .env.example .env"
    exit 1
fi

# Run the agent from project root (so relative paths work correctly)
cd "$PROJECT_ROOT"
python src/agent.py

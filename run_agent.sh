#!/bin/bash
# Simple script to run the AIKB agent

echo "🤖 Starting AIKB Agent..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: python -m venv .venv"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Configuration file not found!"
    echo "   Please copy .env.example to .env and add your API key"
    echo "   Command: cp .env.example .env"
    exit 1
fi

# Run the agent
cd src
python agent.py

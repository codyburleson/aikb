# Python Project Files Explained

This document explains the purpose of each configuration file in your Python project.

## 📋 requirements.txt

**What it is:** A simple text file listing all the Python packages your project needs.

**Why you need it:** Makes it easy for anyone to install all dependencies with one command:
```bash
pip install -r requirements.txt
```

**When to update it:** When you add a new Python library to your project, add it to this file.

## ⚙️ pyproject.toml

**What it is:** A modern Python project configuration file (PEP 518 standard).

**Why you need it:** It's the new standard way to configure Python projects. It contains:
- Project metadata (name, version, description)
- Dependencies (same as requirements.txt, but more structured)
- Build system configuration
- Tool settings for linters, formatters, etc.

**Advantage over setup.py:** More standardized, easier to read, and supports modern Python packaging tools.

**When to update it:**
- When you change project metadata
- When you add/remove dependencies
- When you configure new development tools

## 🔐 .env and .env.example

**What they are:**
- `.env` - Contains your actual API keys and secrets (NEVER commit this to git!)
- `.env.example` - A template showing what variables are needed (safe to commit)

**Why you need them:**
- Keeps sensitive information out of your code
- Makes it easy for new developers to know what configuration they need
- Different people can have different API keys without code conflicts

**How to use:**
1. Copy `.env.example` to `.env`
2. Fill in your real API keys in `.env`
3. The `.gitignore` file prevents `.env` from being committed

## 🚀 start.sh

**What it is:** A convenience script to start your agent with safety checks.

**Why you need it:** Instead of remembering all the commands, just run:
```bash
./start.sh
```

It automatically:
- Checks if virtual environment exists
- Activates the virtual environment
- Checks if .env file is configured
- Runs the main agent

## 📦 Virtual Environment (.venv)

**What it is:** An isolated Python environment for your project.

**Why you need it:**
- Keeps your project dependencies separate from other projects
- Prevents version conflicts between different projects
- Makes your project portable and reproducible

**How to use:**
```bash
# Create it (once)
python -m venv .venv

# Activate it (every time you work on the project)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate when done
deactivate
```

## 🗂️ src/ folder

**What it is:** Contains your actual source code.

**Why you need it:** Python best practice to separate your code from:
- Documentation (docs/)
- Tests (tests/)
- Configuration files
- README, LICENSE, etc.

This makes your project cleaner and more professional.

## Quick Reference

| File | Purpose | Safe to commit? |
|------|---------|----------------|
| `requirements.txt` | List of dependencies | ✅ Yes |
| `pyproject.toml` | Project configuration | ✅ Yes |
| `.env.example` | Template for secrets | ✅ Yes |
| `.env` | Your actual secrets | ❌ NO! |
| `start.sh` | Convenience script | ✅ Yes |
| `.venv/` | Virtual environment | ❌ No (too large) |
| `src/` | Your source code | ✅ Yes |

## Common Commands

```bash
# First time setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# (edit .env with your API key)

# Run the main agent
./start.sh

# Or manually
cd src
python agent.py

# Update dependencies after adding new packages
pip freeze > requirements.txt
```

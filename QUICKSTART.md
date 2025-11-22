# 🚀 AIKB Quick Start Guide

Get up and running with the AIKB agent in 5 minutes!

## Prerequisites

- **Python 3.8+** installed on your system
- **Google AI API key** ([Get one free here](https://ai.google.dev/))

## Setup Steps

### 1. Clone & Navigate

```bash
git clone https://github.com/codyburleson/aikb.git
cd aikb
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

> 💡 **Tip:** You'll see `(.venv)` appear in your terminal prompt when activated.

### 4. ⚠️ CRITICAL: Install Dependencies

```bash
pip install -r requirements.txt
```

> **Important:** Don't skip this step! The virtual environment is empty until you install the dependencies. This is the most common cause of errors.

### 5. Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

In the `.env` file, replace:
```
GOOGLE_API_KEY=your_api_key_here
```

with your actual API key from [Google AI Studio](https://ai.google.dev/).

### 6. Run the Agent

**Easy way (recommended):**
```bash
./run_agent.sh
```

If you get a "Permission denied" error:
```bash
chmod +x run_agent.sh
./run_agent.sh
```

**Manual way:**
```bash
python src/agent.py
```

## Verify It's Working

You should see output like this:

```
🤖 Initializing AIKB Agent ...
📚 Knowledge Base Detected: 29 Markdown files found in './reference-vault'
📝 Creating new session: session_01...
✨ Connected! (Memory & Session Active)
Enter your commands ("quit" to exit).

You:
```

## Try It Out

Once the agent is running, try these commands:

```
You: What can you do?
You: Search for information about AIKB
You: Create a note about today's meeting
You: quit
```

## Common Issues

### ❌ "ModuleNotFoundError: No module named 'google'"

**Problem:** Dependencies not installed in virtual environment.

**Fix:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### ❌ "No such file or directory: .env"

**Problem:** Environment file not created.

**Fix:**
```bash
cp .env.example .env
# Then edit .env and add your API key
```

### ❌ Script runs but can't find reference-vault

**Problem:** Expected folder structure missing.

**Fix:** The repository should already have a `reference-vault` folder. If not:
```bash
mkdir reference-vault
```

### ❌ "Permission denied: ./run_agent.sh"

**Problem:** Script not executable.

**Fix:**
```bash
chmod +x run_agent.sh
```

## Next Steps

1. **Explore the reference vault:** Check out `reference-vault/` to see example knowledge notes
2. **Read the specification:** See `docs/aikb-spec.md` for details on the AIKB standard
3. **Customize:** Modify `src/agent.py` to add your own tools and capabilities

## Daily Usage

Every time you start a new terminal session:

```bash
cd aikb
source .venv/bin/activate  # Activate the environment
./run_agent.sh             # Run the agent
```

When done:
```bash
deactivate  # Exit the virtual environment
```

## Need More Help?

- See [PYTHON_SETUP_GUIDE.md](PYTHON_SETUP_GUIDE.md) for detailed explanations
- Check the main [README.md](README.md) for comprehensive documentation
- Open an issue on GitHub if you're still stuck

---

**Happy Knowledge Managing! 🎉**

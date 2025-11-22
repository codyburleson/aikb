# Agent-Interoperable Knowledge Base (AIKB)

<p>
<strong>Ready to level-up your personal knowledge management?</strong><br>
Transform your notes into an AI-ready ecosystem where multiple agents work together to understand, organize, and enhance your thinking.
</p>

![Status](https://img.shields.io/badge/Status-Alpha-yellow)
![License](https://img.shields.io/badge/License-CC%20BY%E2%88%92SA%204.0-green)
![Course](https://img.shields.io/badge/Google_AI_Agents-Capstone-blue)

As our [Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project) for the [5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)](https://www.kaggle.com/learn-guide/5-day-agents) we present a novel approach to personal knowledge management (PKM) in a system comprised of the following parts:

- **[The AIKB Specification (Working Draft)](https://github.com/codyburleson/aikb/blob/main/docs/aikb-spec.md)**: Proposed standards and guidelines to enable agent interoperability with personal knowledge management systems (PKMs).
- **[Reference Vault](https://github.com/codyburleson/aikb/tree/main/reference-vault)**: A knowledge base repository with templates, schemas, knowledge documents, and other knowledge artifacts demonstrating our proposed standards in practice. Use this as a starting point for your own knowledge base and to test the agents. We recommend using [Obsidian](https://obsidian.md/) to manage your knowledge vault, but any other tool that can read and write markdown files will work.
- **[Agent Base](https://github.com/codyburleson/aikb/tree/main/src)**: Executable source code for a core set of interoperable agents implementing various AIKB use cases.

## What Can AIKB Do?

Imagine asking your AI assistant:

- "What should I be working on?"
- "Summarize all my meeting notes and completed activities from last week; just those related to the ACME project."
- etc.
- etc.

### Example Use Case

```yaml
User: "Create a weekly review from my journal entries"
Agent: Analyzes 7 daily notes following AIKB metadata standards
Output: Structured weekly summary with trends, achievements, and action items
```

## Getting Started

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Google AI API Key** - [Get your free API key](https://ai.google.dev/)

### Quick Setup (5 minutes)

1. **Clone the repository**

   With HTTPS:
   ```bash
   git clone https://github.com/codyburleson/aikb.git
   ```

   ...or SSH:
   ```bash
   git clone git@github.com:codyburleson/aikb.git
   ```

   Change into the project directory:
   ```bash
   cd aikb
   ```

2. **Create a Python virtual environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it (macOS/Linux)
   source .venv/bin/activate

   # Or on Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit the .env file and add your Google AI API key
   # You can use any text editor, for example:
   nano .env
   ```

   Replace `your_api_key_here` with your actual API key from [Google AI Studio](https://ai.google.dev/).

5. **Run the agent**
   ```bash
   cd src
   python agent.py
   ```

That's it! You should see the agent start up and you can begin chatting with it.

### Example Session

```
🤖 Initializing AIKB Agent ...
📚 Knowledge Base Detected: 29 Markdown files found in './reference-vault'
📝 Creating new session: session_01...
✨ Connected! (Memory & Session Active)
Enter your commands ("quit" to exit).

You: What can you do?
Agent: I can help you with a few things:

*   **Tell time**: I can tell you the current time in any specified city.
*   **Remember past conversations**: I can recall information from our previous discussions.
*   **Search your Knowledge Vault**: I can search your local reference vault for information on specific topics, people, or projects.
*   **Create notes**: I can create new Markdown files in your reference vault to save summaries, meeting notes, or ideas.
```

### Troubleshooting

**Problem: `ModuleNotFoundError`**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt` again

**Problem: API key not working**
- Verify your API key is correctly copied into `.env` (in the project root)
- Make sure there are no extra spaces or quotes around the key

**Problem: Can't find reference vault**
- The agent expects a `reference-vault` folder in the project root
- Create one if needed: `mkdir reference-vault`

## Acknowledgments

- [5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)](https://www.kaggle.com/learn-guide/5-day-agents)
- [Obsidian](https://obsidian.md/) community for PKM inspiration

# Agent-Interoperable Knowledge Base (AIKB)

> Transform your personal knowledge into an AI-ready ecosystem where multiple agents can understand, organize, and enhance your notes.

Ever wished your AI assistants could actually understand your Obsidian vault? Or that different AI tools could work together on your personal knowledge base? AIKB makes this possible.

![Status](https://img.shields.io/badge/Status-Alpha-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Course](https://img.shields.io/badge/Google_AI_Agents-Capstone-blue)

**🚧 This is a [Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project) in active development**

This Capstone Project, part of the [5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)](https://www.kaggle.com/learn-guide/5-day-agents) proposes and demonstrates a novel approach to personal knowledge management (PKM) in a system comprised of the following parts:

- **[The AIKB Specification (Working Draft)](./specs/aikb-0.1.md)**: A proposal for a set of formal standards and guidelines to enable agent interoperability with personal knowledge management systems (PKMs).
  - For the purpose of the Capstone Project, the scope has been limited to PKMs comprised of locally sourced markdown documents and media files, which can be easily managed by users using freely available and cross-platform tools like [Obsidian](https://obsidian.md/), [Visual Studio Code](https://code.visualstudio.com/), standard OS features and widely available text editors.
  - 🚧 AIKB Specification Draft v0.1 (in development)
- **Reference Vault**: A repository of markdown document templates implementing metadata standards, comprehensive guidelines ("Principles, Patterns, and Practices for Knowledge Management"), and example documents that demonstrate the standards in practice.
  - The reference vault is hosted publicly on GitHub and intended for access by users and agents.
  - 🚧 Reference Vault (coming soon)
- **Agent Base** - a core set of interoperable and autonomous agents that implement various AIKB use cases.
  - For the purpose of the Capstone Project, the scope of AI software and services has centered around the use of Google's Agent Development Kit and the Google Cloud Platform, though, as a matters of principle, we seek to keep this solution open to community contribution, open source, based on open standards, flexible and free of vendor lock-in.
  - 🚧 Agent Base (in development)
- **CLI (or MCP servers for the Gemini CLI)** - a command line interface enabling users to interact with agents and resources in their personal "knowledge vault" via text input, shell scripts, and Python. (in development)
- **Obsidian Plugin** - a chat user interface plugin enabling Obsidian users to manage their notebook and knowledge with support from AIKB's agents and popular language models.
  - 📋 Obsidian Plugin (planned)

## What Can AIKB Do?

Imagine asking your AI assistant:

- "What should I be working on?"
- "Summarize all my meeting notes and completed activities from last week; just those related to the ACME project."
- etc.
- etc.

...and having it work across ALL your AI tools, not just one.

### Example Use Case

```yaml
User: "Create a weekly review from my journal entries"
Agent: Analyzes 7 daily notes following AIKB metadata standards
Output: Structured weekly summary with trends, achievements, and action items
```

## Project Status

This is a **proof of concept** developed for the Google AI Agents Intensive Course.

- [ ] Core specification drafted
- [ ] Conceptual framework defined
- [ ] Reference implementation
- [ ] CLI tool functional
- [ ] Community feedback incorporated
- [ ] Production-ready release

## Installation

(Coming soon - currently in development)

## Contributing

We welcome feedback on the specification! See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) Attribution-ShareAlike 4.0 International

## Acknowledgments

- [5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)](https://www.kaggle.com/learn-guide/5-day-agents)
- [Obsidian](https://obsidian.md/) community for PKM inspiration

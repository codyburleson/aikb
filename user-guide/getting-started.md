# User Getting Started

## 1. Install the Gemini CLI

The [Gemini command line interface (CLI)](https://geminicli.com/) is an open source AI agent that provides access to Gemini directly in your terminal. The Gemini CLI uses a reason and act (ReAct) loop with your built-in tools and local or remote MCP servers to complete complex use cases like fixing bugs, creating new features, and improving test coverage. While the Gemini CLI excels at coding, it's also a versatile local utility that you can use for a wide range of tasks, from content generation and problem solving to deep research and task management.

Gemini Code Assist for individuals, Standard, and Enterprise each provide quotas for using the Gemini CLI. Note that these quotas are shared between Gemini CLI and Gemini Code Assist agent mode.

Developers, note: This is the main interface through which you can interact with your knowledge vault, I'm thinking. We'll make our agents available via MCP or tools to this CLI, and so, one will access our Agent Base ultimately through the Gemini CLI as a mediator. The user guide will therefor need to provide instructions for installing Gemini and configuring it to recognize the our agents/MCPs/tools. We need to install the CLI and soon after PoC the easiest way to get some component of our own configured with it. I've done this before using a custom MCP with Anthropic Claud, but in respect for this Google sponsored capstone, we'll use their software and services.

## References

- [Gemini CLI](https://developers.google.com/gemini-code-assist/docs/gemini-cli)

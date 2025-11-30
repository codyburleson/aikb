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

## What Can the Agent Base Do?

Right now, the AIKB Agent (Code) Base can create, read, update, and delete markdown notes. It can also query and search for notes based on their metadata or content. It can use templates to create new notes and organize them into folders. It can also summarize notes if they are too long. But this is just a foundation for the beginning of a greater vision.

Imagine having a Life Operating System ("Life OS") and an agent that truly understands you as a person, not just the context of your current comversation. With conformance to certain AIKB standards and guidelines, this becomes possible.

Imagine, for example, if you ask, "What should I be working on?"

In the current state, the Agent will respond with your TO-DO list (instances of the Task template/type); a simple tool. But imagine when the Agent can utilize a personal formula that incorprates your values, goals, projects, and schedule, among other things. Even your current mood can be a factor in your personal formula. With the AIKB standards and guidelines, truly smart responses become possible so that your personal knowledge base becomes the foundation for Agent truly useful Agent services, rather than just a personal notebook.

### Example Use Case

```yaml
User: "Create a weekly review from my journal entries"
Agent: Analyzes 7 daily notes following AIKB metadata standards
Output: Structured weekly summary with trends, achievements, and action items
```

## Automated Actor-Critic Evaluation

AIKB includes a **Critic Agent** pipeline. During regression testing, a secondary LLM instance acts as a judge, analyzing the notes created by the main agent to score them on coherence and formatting quality before they are committed to the vault.

## Getting Started

> 🚀 **Want to get started immediately?** Check out our [QUICKSTART.md](QUICKSTART.md) for a streamlined setup process!

### Example Session

```
🤖 Starting AIKB Agent...
🤖 System Startup: Initializing AIKB...
📂 Loading Templates...
   - Loaded: default
   - Loaded: dailynote
   - Loaded: project
   - Loaded: creativework
   - Loaded: person
   - Loaded: event
   - Loaded: place
   - Loaded: task
   - Loaded: pattern
   - Loaded: organization
✅ Template System Ready: 10 templates loaded.
📝 Context Loaded: Templates=[default, dailynote, project, creativework, person, event, place, task, pattern, organization] | Folders=[25 folders loaded]
📋 Global instructions loaded from ./reference-vault/.aikb/global-instructions.md

👉 You: What can you do?
🤖 Agent: I can create, read, update, and delete markdown notes. I can also query and search for notes based on their metadata or content. I can use templates to create new notes and organize them into folders. I can also summarize notes if they are too long.

👉 You: new task: Complete performance review by Nov 30
🤖 Agent: OK. I have created a new task: "Complete performance review by Nov 30" in the "3 Resources/Tasks/To Do" folder.

👉 You: Rank the task: 5
🤖 Agent: I have updated the rank of the task "Complete performance review by Nov 30" to 5.

👉 You: Order new pants, size 34/34 (or 34/33 if they exist)
🤖 Agent: It seems like there was an issue creating the note, possibly due to the characters in the filename "Order new pants, size 34/34 (or 34/33 if they exist)". The "/" character can sometimes be interpreted as a folder separator.

Would you like me to create the task with a simpler filename, such as "Order new pants size 34/34" or "Order new pants" and then add the details to the content, or save it to '0 Inbox' with the original filename?

👉 You: use a simpler file name and move pants size to content body
🤖 Agent: Okay, I have created a new task "Order new pants" in the "3 Resources/Tasks/To Do" folder. The content of the note includes "Order new pants, size 34/34 (or 34/33 if they exist)".

👉 You: What should I be working on?
🤖 Agent: You should be working on the following tasks:

*   Complete performance review by Nov 30
*   Create a banner for my LinkedIn profile
*   Order new pants
```

## Acknowledgments

- [5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)](https://www.kaggle.com/learn-guide/5-day-agents)
- [Obsidian](https://obsidian.md/) community for PKM inspiration

## Want to Know More?

Here are some additional resources to help you get started:

- [Developer Guide](docs/developer-guide/developer-guide.md)
- [Obsidian Guide](docs/obsidian-guide/obsidian-guide.md)
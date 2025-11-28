# AIKB System Flowchart

This flowchart shows the overall workflow from application startup through the user interaction loop.

## Overview

The system follows these main phases:
1. **Initialization**: Load environment, templates, and scan vault structure
2. **Configuration**: Create agent, configure tools, initialize services
3. **Runtime**: User interaction loop with agent processing and tool invocation

## Diagram

```mermaid
flowchart TD
    Start([Application Start]) --> LoadEnv[Load Environment Variables]
    LoadEnv --> LoadTemplates[Load Templates from Vault]
    LoadTemplates --> ScanFolders[Scan Vault Folder Structure]
    ScanFolders --> BuildContext[Build Context: Templates & Folders]

    BuildContext --> CreateAgent[Create LlmAgent with System Instructions]
    CreateAgent --> ConfigAgent[Configure Agent with Tools:<br/>- create_markdown<br/>- read_markdown<br/>- query_metadata<br/>- search_notes<br/>- update_content<br/>- update_frontmatter<br/>- delete_note]

    ConfigAgent --> InitServices[Initialize Services:<br/>- SessionService<br/>- MemoryService<br/>- LoggingPlugin]
    InitServices --> CreateRunner[Create Runner]
    CreateRunner --> StartSession[Create Session for User]

    StartSession --> ChatLoop{User Input Loop}
    ChatLoop -->|User Input| CheckExit{Exit Command?}
    CheckExit -->|Yes| End([Application End])
    CheckExit -->|No| ProcessMessage[Send Message to Agent]

    ProcessMessage --> AgentThink[Agent Analyzes Intent]
    AgentThink --> DecideAction{Action Needed?}

    DecideAction -->|Tool Call| InvokeTool[Invoke Markdown Operation Tool]
    InvokeTool --> FileOp[Perform File System Operation]
    FileOp --> ReturnResult[Return Result to Agent]

    DecideAction -->|Direct Response| GenerateResponse[Generate Text Response]
    ReturnResult --> GenerateResponse

    GenerateResponse --> DisplayToUser[Display Response to User]
    DisplayToUser --> ChatLoop

    style LoadTemplates fill:#e1f5ff
    style ConfigAgent fill:#e1f5ff
    style InvokeTool fill:#fff4e1
    style FileOp fill:#fff4e1
    style ChatLoop fill:#f0f0f0
```

## Key Points

- **Blue nodes**: Template and configuration phases (one-time setup)
- **Yellow nodes**: Tool invocation and file operations (runtime actions)
- **Gray node**: Main user interaction loop
- The chat loop continues until user enters "exit" or "quit"
- Agent can either invoke tools or respond directly based on user intent

## Related Files

- [`src/agent.py`](file:///Users/dev/repos/aikb/src/agent.py) - Main application entry point
- [`src/tools/markdown_ops.py`](file:///Users/dev/repos/aikb/src/tools/markdown_ops.py) - Tool implementations

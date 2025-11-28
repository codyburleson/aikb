# AIKB Sequence Diagram - Agent Tool Interaction

This diagram shows the detailed interaction flow when a user requests to create a note.

## Overview

This sequence illustrates:
- How the application initializes and loads templates
- The message flow from user input to agent response
- Conditional logic for folder validation
- File system operations through the tools layer

## Diagram

```mermaid
sequenceDiagram
    actor User
    participant Main as main()
    participant Agent as LlmAgent
    participant Runner
    participant Tools as markdown_ops
    participant FS as File System

    User->>Main: Start Application
    Main->>Tools: load_templates(vault_path)
    Tools->>FS: Scan Templates folder
    FS-->>Tools: Template files
    Tools->>Tools: Parse templates into LOADED_TEMPLATES
    Tools-->>Main: Templates loaded

    Main->>Main: Scan vault folders
    Main->>Agent: Create with system instructions
    Main->>Runner: Initialize with agent & services
    Main->>Runner: Create session

    rect rgb(240, 248, 255)
        Note over User,FS: User Interaction Loop
        User->>Main: "Create a person note for John Doe"
        Main->>Runner: run_async(message)
        Runner->>Agent: Process message

        Agent->>Agent: Analyze intent<br/>(Person note needed)
        Agent->>Agent: Check folder exists<br/>in context

        alt Folder exists
            Agent->>Tools: create_markdown(filename="John Doe",<br/>folder="Persons",<br/>template_name="person")
            Tools->>Tools: Get safe path
            Tools->>Tools: Load template from LOADED_TEMPLATES
            Tools->>Tools: Generate UUID & timestamp
            Tools->>FS: Write file with frontmatter + content
            FS-->>Tools: Success
            Tools-->>Agent: "Note created: Persons/John Doe.md"
        else Folder missing
            Agent-->>User: "Folder 'Persons' doesn't exist.<br/>Create it or use '0 Inbox'?"
        end

        Agent->>Runner: Response event
        Runner-->>Main: Event stream
        Main-->>User: Display response
    end

    User->>Main: "exit"
    Main->>Main: Break loop
    Main->>User: Application ends
```

## Key Interactions

### Startup Phase
1. Templates are loaded from the vault into memory cache
2. Vault folder structure is scanned for context
3. Agent is created with dynamic system instructions
4. Session is initialized for the user

### Runtime Phase
1. User sends natural language request
2. Agent analyzes intent and determines required template
3. Agent validates folder exists in scanned context
4. Tool creates note with proper frontmatter and content
5. Response is streamed back to user

## Security Features

- **Folder Validation**: Agent checks if target folder exists before creating notes
- **Path Safety**: `_get_safe_path()` prevents path traversal attacks
- **Template Caching**: Templates loaded once at startup, not on every request

## Related Files

- [`src/agent.py`](file:///Users/dev/repos/aikb/src/agent.py) - Orchestrates the interaction flow
- [`src/tools/markdown_ops.py`](file:///Users/dev/repos/aikb/src/tools/markdown_ops.py) - Implements the tools called by the agent

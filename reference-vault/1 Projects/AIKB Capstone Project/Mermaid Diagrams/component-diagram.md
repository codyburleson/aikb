# AIKB Component Diagram

This diagram shows the structural organization and relationships between components in the AIKB system.

## Overview

The architecture follows a layered approach:
- **Orchestration Layer**: `AgentMain` coordinates startup and runtime
- **Agent Layer**: Google ADK's `LlmAgent` and `Runner` handle AI processing
- **Service Layer**: Session, Memory, and Logging services support the agent
- **Tool Layer**: `MarkdownOps` provides file system abstraction
- **Storage Layer**: File system operations for vault management

## Diagram

```mermaid
classDiagram
    class AgentMain {
        +main() async
        -vault_path: str
        -USER_ID: str
        -SESSION_ID: str
    }

    class LlmAgent {
        +model: str
        +name: str
        +instruction: str
        +tools: list
    }

    class Runner {
        +agent: LlmAgent
        +app_name: str
        +session_service: SessionService
        +memory_service: MemoryService
        +plugins: list
        +run_async() async
    }

    class SessionService {
        +create_session()
        +get_session()
    }

    class MemoryService {
        +store_memory()
        +retrieve_memory()
    }

    class LoggingPlugin {
        +log_events()
    }

    class MarkdownOps {
        +LOADED_TEMPLATES: dict
        +VAULT_ROOT: str
        +load_templates(vault_path)
        +create_markdown(filename, content, folder, template_name)
        +read_markdown(path)
        +query_metadata(key, value)
        +update_frontmatter(path, updates_json)
        +update_content(path, new_content)
        +search_notes(query)
        +delete_note(filename, folder)
        -_get_safe_path(filename_or_path)
        -_sanitize_metadata(metadata)
    }

    class FileSystem {
        <<external>>
        +read_file()
        +write_file()
        +walk_directory()
    }

    AgentMain --> LlmAgent : creates
    AgentMain --> Runner : creates
    AgentMain --> SessionService : creates
    AgentMain --> MemoryService : creates
    AgentMain --> LoggingPlugin : creates (conditional)
    AgentMain --> MarkdownOps : imports tools

    Runner --> LlmAgent : uses
    Runner --> SessionService : uses
    Runner --> MemoryService : uses
    Runner --> LoggingPlugin : uses

    LlmAgent --> MarkdownOps : calls tools
    MarkdownOps --> FileSystem : interacts with

    note for AgentMain "Entry point\nOrchestrates startup\nManages chat loop"
    note for MarkdownOps "Tool layer\nHandles all file operations\nProvides vault security"
    note for LlmAgent "Google ADK Agent\nProcesses user intent\nCalls appropriate tools"
```

## Component Responsibilities

### AgentMain
- Application entry point and orchestrator
- Loads templates and scans vault structure
- Creates and configures all components
- Manages the user interaction loop

### LlmAgent
- Google ADK's AI agent (Gemini 2.5 Flash)
- Analyzes user intent and decides on actions
- Invokes appropriate tools based on context
- Follows system instructions for safety and validation

### Runner
- Manages agent execution lifecycle
- Handles session and memory persistence
- Streams events back to the application
- Integrates plugins (e.g., logging)

### MarkdownOps
- Abstracts all file system operations
- Provides secure vault access (path validation)
- Manages template cache (`LOADED_TEMPLATES`)
- Implements CRUD operations for markdown files

### Services
- **SessionService**: Manages user sessions
- **MemoryService**: Stores conversation history
- **LoggingPlugin**: Provides observability (conditional on `DEBUG` flag)

## Design Patterns

- **Dependency Injection**: Services injected into Runner
- **Template Method**: Templates loaded once, reused many times
- **Tool Pattern**: Agent uses declarative tools, not direct file access
- **Security Layer**: All file operations validated through `_get_safe_path()`

## Related Files

- [`src/agent.py`](file:///Users/dev/repos/aikb/src/agent.py) - Contains `AgentMain` and orchestration logic
- [`src/tools/markdown_ops.py`](file:///Users/dev/repos/aikb/src/tools/markdown_ops.py) - Contains `MarkdownOps` tool implementations

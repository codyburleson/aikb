import asyncio
import os
from dotenv import load_dotenv

# Google ADK Imports
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)

# Import the tools (keeping the main file clean)
from src.tools.markdown_ops import (
    load_templates,
    create_markdown,
    read_markdown,
    query_metadata,
    update_content,
    update_frontmatter,
    search_notes,
    delete_note,
    LOADED_TEMPLATES
)

load_dotenv()

# Application Configuration
APP_NAME = "aikb_local"

# --- Main Execution ---
async def main():
    print("🤖 System Startup: Initializing AIKB...")

    # Load templates first - can't do much without them
    load_templates("./reference-vault")

    # Create a clean list of template names
    available_templates = ", ".join(LOADED_TEMPLATES.keys())
    if not available_templates:
        available_templates = "default"

    # Scan the folder structure so the agent isn't flying blind
    # We list actual directories to prevent hallucinated folders
    vault_path = "./reference-vault"
    existing_folders = []
    if os.path.exists(vault_path):
        for root, dirs, files in os.walk(vault_path):
             # Filter out hidden folders (like .git or .obsidian) in place
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for d in dirs:
                # Get the relative path (e.g., "3 Resources/Persons")
                full_path = os.path.join(root, d)
                rel_path = os.path.relpath(full_path, vault_path)
                existing_folders.append(rel_path)

    folder_context = "\n".join([f"       - {f}" for f in existing_folders])
    print(f"📝 Context Loaded: Templates=[{available_templates}] | Folders=[{len(existing_folders)} folders loaded]")

    # Define the agent with some strict safety rules
    system_instruction = f"""
    You are an intelligent Knowledge Base Manager.

    --- DYNAMIC RESOURCES ---
    1. AVAILABLE TEMPLATES: [{available_templates}]
    2. EXISTING FOLDERS:
{folder_context}

    --- INTERPRETATION RULES ---
    1. ANALYZE INTENT: Determine the type of note (Person, Project, etc.).
    2. MATCH TEMPLATE:
       - If User asks for "Person" -> use 'template_name="person"'.
       - If User asks for "Project" -> use 'template_name="project"'.
       - If User asks for "Event" -> use 'template_name="event"'.
       - Default -> 'template_name="default"'.

    --- FOLDER SAFETY PROTOCOL (CRITICAL) ---
    1. PREFERRED MAPPING:
       - Template "person"  -> prefer folder "Persons"
       - Template "project" -> prefer folder "Projects"
       - Template "book"    -> prefer folder "Books"

    2. VERIFICATION RULE (STOP & ASK):
       - Before calling 'create_markdown', check if your target 'folder' exists in the [EXISTING FOLDERS] list above.
       - IF EXISTS: Proceed immediately.
       - IF MISSING: Do NOT create the note yet.
         Reply to the user: "I notice the folder '[Target Folder]' does not exist. Do you want me to create it, or save this in '0 Inbox'?"

    3. EXCEPTION: If the user explicitly says "Create a new folder" or "Yes", then you may proceed.

    --- DISPLAY PROTOCOL (CRITICAL) ---
    1. READ MODE:
       - When using 'read_markdown', return ONLY the file 'content' by default.
       - Do NOT show the Metadata/YAML Frontmatter (tags, UUIDs, dates) unless the user explicitly asks for it.
       - If the user asks "Show me the metadata" or "What are the tags?", THEN show the full details.

    --- SEARCH STRATEGY ---
    - First, try 'query_metadata' (e.g., key="type", value="Person").
    - Second, use 'search_notes' for text content.
    """

    # Note: LlmAgent does not accept app_name parameter (Pydantic validation error)
    # The app name mismatch warning that appears is expected and harmless
    root_agent = LlmAgent(
        model='gemini-2.5-flash',
        name='AIKB_Agent',
        instruction=system_instruction,
        tools=[
            create_markdown,
            read_markdown,
            query_metadata,
            search_notes,
            update_content,
            update_frontmatter,
            delete_note
        ]
    )

    # ... (Rest of your Runner/Session code follows here) ...
    # Spin up the services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()


    # Conditionally enable debug logging based on DEBUG environment variable
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    plugins = [LoggingPlugin()] if DEBUG else []

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
        plugins=plugins,  # Handles standard Observability logging across ALL agents (when DEBUG=true)
    )

    # Let's go!
    USER_ID = "user_01"
    SESSION_ID = "session_01"

    print(f"✨ AIKB Ready! (Session: {SESSION_ID})")
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # Main chat loop
    while True:
        try:
            user_input = await asyncio.to_thread(input, "\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            message = types.Content(role="user", parts=[types.Part(text=user_input)])

            async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Agent: {part.text}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
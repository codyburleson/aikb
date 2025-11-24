from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory  # <--- The tool that lets the agent READ memory
from google.genai import types
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#GLOBAL CACHE
_VAULT_CACHE = {}

# --- Tool Definitions ---
# A tool to get "current" (hard-coded) time for simple agent tool testing
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

#######################################################################################
# KB Tool to search and read reference vaults
# -------------------------------------------------------------------------------------
#
# Appears to read all content into memory, which is not ideal for large vaults.
# We'll need to improve this in the future. Also walks and we already walk on startup,
# so we can probably optimize down to one walk that does some sort of indexing, or
# better yet, maybe only by entity type as we converse with the agent.
#######################################################################################
def search_knowledge_vault(query: str) -> dict:
    """
    Searches local reference vault folder for markdown files.
    Useful for answering questions about the 'AIKB' project, documentation, or specs.
    Uses Smart Caching: Only re-reads files if they have been modified since the last search.
    """
    vault_path = "./reference-vault"
    global _VAULT_CACHE
    indexed_files = {}

    if not os.path.exists(vault_path):
        return {"status": "error", "message": f"Directory '{vault_path}' not found."}

    print(f"   [Tool: Smart-Scanning '{vault_path}' for '{query}'...]")

    files_scanned = 0
    files_updated = 0

    # Recursively read all .md files in the vault_path
    file_count = 0
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                files_scanned += 1
                file_path = os.path.join(root, file)
                try:
                    current_mtime = os.path.getmtime(file_path)

                    if (file_path not in _VAULT_CACHE) or (_VAULT_CACHE[file_path]["mtime"] != current_mtime):
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        _VAULT_CACHE[file_path] = {
                            "mtime": current_mtime,
                            "content": content
                        }
                        files_updated += 1
                except Exception as e:
                    print(f"   [Skipped {file}: {e}]")

    # 2. SEARCH MEMORY
    print(f"   [Cache Stats] Total: {files_scanned} | Updated/Read: {files_updated}")

    # Search for the query in the indexed files
    results = {}
    for path, data in _VAULT_CACHE.items():
        # If the file was deleted from disk, we might want to handle that cleanup,
        # but for now we just search what's in memory.(A valid point to consider for future versions)
        if query.lower() in data["content"].lower():
            results[path] = data["content"]

    if not results:
        return {"status": "no_results", "message": f"No matches for '{query}' in {file_count} files."}
    return {"status": "success", "results": results}




from src.tools.markdown_ops import read_markdown, create_markdown, update_frontmatter, update_content

# ... (existing imports)

# --- Agent Definition ---
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time and remembers user details.",
    # Updated instructions to tell the agent to use memory
    instruction="\n".join([
        "You are a helpful AI assistant managing a personal knowledge base.",
        "The knowledge base is a collection of Markdown files in a 'reference-vault' directory.",
        "You can search for notes, read them, create new ones, and update them.",
        "When asked to update a note's content, read it first, then rewrite the content as needed and use the update_content tool.",
        "Always check if a file exists before trying to read or update it.",
        "Use the 'Inbox' folder for new notes unless specified otherwise."
    ]),
    # Add load_memory to the tools list so the agent can use it
    tools=[
        get_current_time,
        load_memory,
        search_knowledge_vault,
        create_markdown,
        read_markdown,
        update_frontmatter,
        update_content
    ]
)

# --- Execution Logic (Only runs when you execute this file directly) ---
async def main():
    print("🤖 Initializing AIKB Agent ...")

    vault_path = "./reference-vault"

    #######################################################################################
    # Startup Check: Verify and Walk Vault
    # This is a simple check to ensure the vault exists and contains files.
    # In the future, we might be able to use this also to build up some kind of index of
    # the vault contents, or some kind of cache preload. For example,
    # the search_knowledge_vault tool does this same walk, so... at the moment, this is
    # redundant; we could probably optimize here.
    # -------------------------------------------------------------------------------------
    # The Python os.walk() function is a generator that recursively traverses a directory
    # tree, providing information about each directory it visits. For each step, it yields
    # a 3-tuple (dirpath, dirnames, filenames).
    #######################################################################################

    if os.path.exists(vault_path):
        count = 0
        for (dirpath, dirnames, filenames) in os.walk(vault_path):
            for file in filenames:
                if file.endswith('.md'):
                    count += 1
                    full_path = os.path.join(dirpath, file)
                    print(f"[{count}] Markdown file: {full_path}")
        print(f"📚 Knowledge Base Detected: {count} Markdown files found in '{vault_path}'")
    else:
        print(f"⚠️ Warning: '{vault_path}' folder not found!")
    # ---------------------------------------

    # 1. Initialize the Services
    # SessionService: Remembers the current conversation flow (Short-term)

    # The InMemorySessionService is the default session storage mechanism in the
    # Agent Development Kit (ADK), designed for local development and testing.
    # It stores all session data, including conversation history and state, directly
    # in the application's memory.
    #
    # Transient Data: All session data is stored in RAM and is lost if the application or
    # process restarts, crashes, or ends. This makes it unsuitable for production
    # environments where session persistence is required.
    # Ease of Use: It is the default option and requires no external setup or database management,
    # making it easy to use for prototyping and simple testing scenarios.
    # Functionality: It acts as a central manager for the entire lifecycle of conversation sessions,
    # handling the creation, retrieval, updating (with new events), and deletion of sessions.
    # Shared State: For agents to share state and memory during a local run, the same instance of
    # the InMemorySessionService must be shared across all runners.

    session_service = InMemorySessionService()


    # MemoryService: Stores facts for later retrieval ("Long-term Memory")
    # Not really "Long-term Memory"; it's not persistent across sessions

    # The InMemoryMemoryService in the Google Agent Development Kit (ADK) is a simple, non-persistent
    # memory implementation designed for prototyping, local development, and basic testing. It is
    # automatically used by InMemoryRunner if no other memory service is specified, requires no
    # setup, and stores session events directly in application memory.
    # No External Dependencies: The InMemoryMemoryService works out of the box without requiring any
    # external services or Google Cloud configuration, making it ideal for quick local testing and
    # development.
    # Non-Persistent: Data stored in the InMemoryMemoryService is lost when the application or session
    # restarts. It is not suitable for production applications that need reliable, long-term memory.
    # Basic Keyword Matching: The service performs simple keyword-based matching to retrieve relevant
    # information from past sessions, rather than advanced semantic search.
    # Stores Full Conversations: Unlike more advanced services that extract and consolidate memories,
    # this service treats entire conversations as memory units, which helps preserve conversational
    # flow during development.
    # For production environments, the VertexAiMemoryBankService or VertexAiRagMemoryService
    # (which offer persistent, scalable memory with advanced semantic search capabilities) are
    # recommended alternatives.

    memory_service = InMemoryMemoryService()

    # Constants for our session
    APP_NAME = "agents"
    USER_ID = "user_01"
    SESSION_ID = "session_01"

    # Create Session
    print(f"📝 Creating new session: {SESSION_ID}...")
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # Create a Runner (The "Manager")
    # The Runner connects your Agent to the Memory and Session services
    # Remember: For agents to share state and memory during a local run, the same instance of the
    # InMemorySessionService must be shared across all runners.
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    print("✨ Connected! (Memory & Session Active)")
    print('Enter your commands ("exit" or "quit" to exit).')

    # Chat Loop
    while True:
        try:
            user_input = await asyncio.to_thread(input, "\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            # Created the structured Message Object
            message_object = types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )

            # This returns a generator, so we loop through events as they arrive
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=message_object
            ):
                # Check if the event has text content to display
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Agent: {part.text}")
            # After the conversation turn is done, we grab the session and save it to memory.
            # This updates the "Long Term Memory" so load_memory can find it next time.
            current_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID
            )
            await memory_service.add_session_to_memory(current_session)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory  # <--- The tool that lets the agent READ memory
from google.genai import types
import asyncio
import os


#GLOBAL CACHE
_VAULT_CACHE = {}

# --- Tool Definitions ---
#testing tool to get current time
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

# Knowledge Base Tool to search and read reference vaults
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


# --- 3. Note Creation Tool (Writer) ---
def create_knowledge_note(filename: str, content: str, folder: str = "Inbox") -> dict:
    """
    Creates a new Markdown file in the reference vault.
    """
    base_path = "./reference-vault"
    target_dir = os.path.join(base_path, folder)

    if not filename.endswith(".md"):
        filename += ".md"

    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except OSError as e:
            return {"status": "error", "message": f"Could not create folder: {e}"}

    file_path = os.path.join(target_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # OPTIONAL: Pre-load into cache so it's immediately searchable
        global _VAULT_CACHE
        _VAULT_CACHE[file_path] = {
            "mtime": os.path.getmtime(file_path),
            "content": content
        }

        print(f"   [Tool: Created new note at '{file_path}']")
        return {"status": "success", "file_path": file_path, "message": "Note created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- Agent Definition ---
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time and remembers user details.",
    # Updated instructions to tell the agent to use memory
    instruction=(
        "You are the AIKB (Agent-Interoperable Knowledge Base) Assistant. "
            "Your goal is to help the user manage their Knowledge Vault.\n\n"
            "OPERATIONAL MANUAL:\n"
            "1. **TIME CHECKING**: Want to Know Time of any City ? \n"
            "2. **MEMORY RECALL**: Remember past conversation .\n"
            "3. **READING KNOWLEDGE**: If the user asks about specific topics, people (like Geoffrey Hinton), or projects stored in their files, "
            "use `search_knowledge_vault`. \n"
            "   - *Tip:* Hey Search for specific keywords (e.g., 'Hinton') rather than full sentences.\n"
            "4. **WRITING NOTES**: If the user asks to save a summary, meeting note, or idea, use `create_knowledge_note`. \n"
            "   - *Format:* Ensure the content is written in clean Markdown.\n"
    ),
    # Add load_memory to the tools list so the agent can use it
    tools=[get_current_time, load_memory, search_knowledge_vault, create_knowledge_note],
)

# --- Execution Logic (Only runs when you execute this file directly) ---
async def main():
    print("🤖 Initializing AIKB Agent ...")

    # --- Startup Check: Verify Resources ---
    vault_path = "./reference-vault"
    if os.path.exists(vault_path):
        count = sum(len([f for f in files if f.endswith('.md')]) for r, d, files in os.walk(vault_path))
        print(f"📚 Knowledge Base Detected: {count} Markdown files found in '{vault_path}'")
    else:
        print(f"⚠️ Warning: '{vault_path}' folder not found!")
    # ---------------------------------------

    # 1. Initialize the Services
    # SessionService: Remembers the current conversation flow (Short-term)
    session_service = InMemorySessionService()

    # MemoryService: Stores facts for later retrieval (Long-term)
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
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    print("✨ Connected! (Memory & Session Active)")
    print("Enter your commands (Ctrl+C to exit).")

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
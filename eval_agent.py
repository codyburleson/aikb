import asyncio
import os
import frontmatter
from dotenv import load_dotenv
from google.genai import types
from google.adk.models.google_llm import Gemini # Or standard GenAI SDK

# Import your main agent's tools to test them
from src.tools.markdown_ops import create_markdown, read_markdown, delete_note, load_templates

load_dotenv()

async def run_evaluation():
    print("🧪 Starting AIKB Multi-Agent Evaluation...")
    
    # Load templates first
    load_templates()
    
    # SETUP
    test_file = "Evaluation_Test_Note"
    test_folder = "0 Inbox"
    content_to_write = "Python is a high-level programming language. It is great for AI."
    
    # --- PHASE 1: THE ACTOR (Your Main System) ---
    print(f"\n[Actor Agent] Creating note '{test_file}'...")
    result = create_markdown(test_file, content_to_write, folder=test_folder)
    
    if result['status'] != 'success':
        print("❌ CRITICAL FAIL: Actor could not create file.")
        return

    # Read the file back to get what was actually written
    file_data = read_markdown(f"{test_folder}/{test_file}.md")
    actual_content = file_data.get('content', '')
    
    # --- PHASE 2: THE CRITIC (The Second Agent) ---
    print("\n[Critic Agent] Reviewing the work...")
    
    # We create a temporary LLM instance for the critic
    # You can use the standard google-genai SDK here for simplicity
    from google import genai
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    critic_prompt = f"""
    You are a strict Content Quality Control Agent.
    Your job is to evaluate the following Markdown note content.
    
    CRITERIA:
    1. Is the content coherent?
    2. Is it free of hallucinations?
    3. Does it follow standard text formatting?
    
    CONTENT TO REVIEW:
    "{actual_content}"
    
    OUTPUT FORMAT:
    Return strictly a JSON: {{"score": 1-10, "reason": "short explanation"}}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=critic_prompt
    )
    
    print(f"🧐 Critic's Verdict:\n{response.text}")
    
    # --- PHASE 3: CLEANUP ---
    delete_note(test_file, test_folder)
    print("\n✅ Evaluation Cycle Complete.")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
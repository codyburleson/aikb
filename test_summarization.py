import os
import sys
from dotenv import load_dotenv

# Ensure src is in path
sys.path.append(os.getcwd())

from src.tools.markdown_ops import create_markdown, read_markdown, delete_note, load_templates

def test_summarization():
    load_dotenv()
    
    # Load templates first
    load_templates()
    
    print("🚀 Starting Context Compaction Test...")
    
    filename = "LargeTestNote"
    content = """
    # The History of Artificial Intelligence
    
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    
    AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).
    
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    
    Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding. AI research has tried and discarded many different approaches since its founding, including simulating the brain, modeling human problem solving, formal logic, large databases of knowledge and imitating animal behavior. In the first decades of the 21st century, highly mathematical-statistical machine learning has dominated the field, and this technique has proved highly successful, helping to solve many challenging problems throughout industry and academia.
    """
    
    # 1. Create a large note
    print(f"📝 Creating note '{filename}'...")
    create_result = create_markdown(filename, content, folder="0 Inbox")
    print(f"DEBUG: create_result = {create_result}")
    
    # 2. Read normally
    print("📖 Reading normally...")
    normal_result = read_markdown(f"0 Inbox/{filename}.md")
    print(f"DEBUG: normal_result = {normal_result}")
    print(f"   Normal Length: {len(normal_result['content'])} chars")
    
    # 3. Read as summary
    print("Testing summarization (this calls the LLM)...")
    summary_result = read_markdown(f"0 Inbox/{filename}.md", as_summary=True)
    summary_content = summary_result['content']
    
    print(f"   Summary Length: {len(summary_content)} chars")
    print(f"   Summary Content Preview: {summary_content[:100]}...")
    
    # 4. Verify
    if "[SUMMARY]" in summary_content and len(summary_content) < len(normal_result['content']):
        print("✅ SUCCESS: Content was summarized.")
    else:
        print("❌ FAILURE: Content was not summarized properly.")
        print(f"   Content: {summary_content}")

    # Cleanup
    delete_note(filename, "0 Inbox")
    print("🧹 Cleanup done.")

if __name__ == "__main__":
    test_summarization()

import os
import shutil
import json
from src.tools.markdown_ops import create_markdown, read_markdown, update_frontmatter, update_content

def verify_tools():
    print("Starting verification...")

    # Setup
    test_filename = "AIKB Markdown Ops Test Note"
    test_folder = "0 Inbox"
    full_path = os.path.abspath(f"./reference-vault/{test_folder}/{test_filename}.md")

    if os.path.exists(full_path):
        os.remove(full_path)

    # 1. Create Markdown
    print(f"\n1. Testing create_markdown...")
    content = "# Test Note\n\nThis is a test paragraph."
    metadata = {"tags": ["test", "verification"], "status": "draft"}
    result = create_markdown(test_filename, content, test_folder, json.dumps(metadata))
    print(f"Create Result: {result}")

    if result["status"] != "success" or not os.path.exists(full_path):
        print("FAILED: File creation failed.")
        return

    # 2. Read Markdown
    print(f"\n2. Testing read_markdown...")
    read_result = read_markdown(full_path)
    print(f"Read Result: {read_result}")

    if read_result["metadata"].get("status") != "draft":
        print("FAILED: Metadata mismatch.")
        return

    # 3. Update Frontmatter
    print(f"\n3. Testing update_frontmatter...")
    update_result = update_frontmatter(full_path, json.dumps({"status": "published", "author": "Agent"}))
    print(f"Update Result: {update_result}")

    read_again = read_markdown(full_path)
    if read_again["metadata"].get("status") != "published":
        print("FAILED: Metadata update failed.")
        return

    # 4. Update Content
    print(f"\n4. Testing update_content...")
    new_content = "# Updated Test Note\n\nThis content was updated directly."
    update_content_result = update_content(full_path, new_content)
    print(f"Update Content Result: {update_content_result}")

    if update_content_result["status"] != "success":
        print("FAILED: Content update failed.")
        return

    # Verify content change
    final_read = read_markdown(full_path)
    if "Updated Test Note" not in final_read["content"]:
        print("FAILED: Content update verification failed.")
        print(f"Content: {final_read['content']}")
        return

    # Verify metadata preserved
    if final_read["metadata"].get("status") != "published":
         print("FAILED: Metadata lost during content update.")
         return

    print("\nSUCCESS: All verification steps passed!")

    # Cleanup
    # shutil.rmtree(f"./reference-vault/{test_folder}")

if __name__ == "__main__":
    verify_tools()

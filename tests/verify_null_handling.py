import os
import sys
import frontmatter

# Add the repository root to sys.path
sys.path.append(os.getcwd())

from src.tools.markdown_ops import create_markdown, delete_note, load_templates

def test_null_handling():
    # Load templates first
    vault_root = os.getenv("VAULT_ROOT", "./reference-vault")
    load_templates(vault_root)

    filename = "Test Null Handling"
    folder = "3 Resources/Persons"

    # Clean up if exists
    delete_note(filename, folder)

    # Create note using Person template which has empty fields (None in python)
    print(f"Creating note '{filename}'...")
    result = create_markdown(
        filename=filename,
        content="Test content",
        folder=folder,
        template_name="person"
    )

    if result["status"] != "success":
        print(f"❌ Creation failed: {result['message']}")
        return

    file_path = result["file_path"]
    print(f"Note created at: {file_path}")

    # Read file content directly to check for "null"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("\n--- File Content Preview ---")
    print(content[:200]) # Show first 200 chars
    print("----------------------------")

    if "null" in content:
        print("❌ Found 'null' in file content. Fix failed.")
    else:
        print("✅ No 'null' found in file content. Fix verified.")

    # Cleanup
    delete_note(filename, folder)
    print("Test note deleted.")

if __name__ == "__main__":
    test_null_handling()

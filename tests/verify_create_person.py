import os
import sys
import frontmatter

# Add the repository root to sys.path
sys.path.append(os.getcwd())

from src.tools.markdown_ops import create_markdown, delete_note, load_templates

def test_create_person_fix():
    # Load templates first
    vault_root = os.getenv("VAULT_ROOT", "./reference-vault")
    load_templates(vault_root)

    filename = "Test Person Fix"
    folder = "3 Resources/Persons"
    email = "test@example.com"
    frontmatter_yaml = f"email: {email}"

    # Clean up if exists
    delete_note(filename, folder)

    print(f"Creating note '{filename}' with frontmatter: {frontmatter_yaml}")
    result = create_markdown(
        filename=filename,
        content="Test content",
        folder=folder,
        template_name="person",
        frontmatter_yaml=frontmatter_yaml
    )

    if result["status"] != "success":
        print(f"❌ Creation failed: {result['message']}")
        return

    file_path = result["file_path"]
    print(f"Note created at: {file_path}")

    # Verify content
    post = frontmatter.load(file_path)
    metadata = post.metadata

    # Check 1: Email should be in frontmatter
    if metadata.get("email") == email:
        print("✅ Email correctly set in frontmatter.")
    else:
        print(f"❌ Email missing or incorrect. Got: {metadata.get('email')}")

    # Check 2: birthDate should be empty (None or empty string)
    birth_date = metadata.get("birthDate")
    if not birth_date:
        print("✅ birthDate is correctly empty.")
    else:
        print(f"❌ birthDate should be empty but is: {birth_date}")

    # Check 3: created/updated should be populated
    if metadata.get("created") and metadata.get("updated"):
        print("✅ created and updated timestamps are populated.")
    else:
        print("❌ created or updated timestamps are missing.")

    # Cleanup
    delete_note(filename, folder)
    print("Test note deleted.")

if __name__ == "__main__":
    test_create_person_fix()

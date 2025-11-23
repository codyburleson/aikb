import os
import frontmatter
import json

def read_markdown(path: str) -> dict:
    """
    Reads a markdown file and returns its metadata and content.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"File not found: {path}"}

    try:
        post = frontmatter.load(path)
        return {
            "status": "success",
            "metadata": post.metadata,
            "content": post.content,
            "path": path
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_markdown(filename: str, content: str, folder: str = "0 Inbox", metadata_json: str = "{}") -> dict:
    """
    Creates a new markdown file with optional metadata (provided as JSON string).
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
        metadata = json.loads(metadata_json) if metadata_json else {}
        post = frontmatter.Post(content, **metadata)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"status": "success", "file_path": file_path, "message": "Note created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_frontmatter(path: str, updates_json: str) -> dict:
    """
    Updates the frontmatter metadata of an existing markdown file.
    updates_json: JSON string containing the metadata updates.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"File not found: {path}"}

    try:
        updates = json.loads(updates_json)
        post = frontmatter.load(path)
        post.metadata.update(updates)

        with open(path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"status": "success", "message": "Metadata updated.", "metadata": post.metadata}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_content(path: str, new_content: str) -> dict:
    """
    Updates the content (body) of a markdown file while preserving the existing frontmatter.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"File not found: {path}"}

    try:
        # Load existing file to get metadata
        post = frontmatter.load(path)

        # Update content
        post.content = new_content

        # Write back
        with open(path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"status": "success", "message": "Content updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

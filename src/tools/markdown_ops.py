import os
import frontmatter
import json
from datetime import datetime, date

# Global cache for templates
# This dictionary acts as a high-speed cache for your templates.
# It is populated once when the application starts.
LOADED_TEMPLATES = {}

VAULT_ROOT = os.path.abspath("./reference-vault")

# Security check: prevent path traversal (e.g. accessing ../../../etc/passwd)
def _get_safe_path(filename_or_path: str) -> str:
    """
    Ensures the Agent cannot access files outside the vault.
    """
    # Normalize path separators
    clean_path = os.path.normpath(filename_or_path)
    
    # Check if it's already an absolute path
    if os.path.isabs(clean_path):
        # If it's absolute, it MUST start with VAULT_ROOT
        if not clean_path.startswith(VAULT_ROOT):
             raise ValueError(f"Security Alert: Access denied to {clean_path}")
        return clean_path

    # Remove any leading path separators (./ or /) to force relative path
    if clean_path.startswith(os.sep) or clean_path.startswith("."):
        clean_path = clean_path.lstrip(os.sep).lstrip(".")

    # Join with root and resolve absolute path
    full_path = os.path.abspath(os.path.join(VAULT_ROOT, clean_path))
    
    # The final check: Does the resolved path start with our vault root?
    if not full_path.startswith(VAULT_ROOT):
        raise ValueError(f"Security Alert: Access denied to {full_path}")
    
    return full_path

# Load templates dynamically from the folder
def load_templates(vault_path: str = VAULT_ROOT):
    """
    Scans the 'Templates' folder and loads all Markdown files into memory.
    This allows you to add new templates (e.g., 'Meeting.md') just by creating a file.
    """
    templates_dir = os.path.join(vault_path, "3 Resources", "Templates")
    global LOADED_TEMPLATES
    LOADED_TEMPLATES.clear() # Reset cache on reload

    if not os.path.exists(templates_dir):
        print(f"⚠️  Warning: 'Templates' folder not found at {templates_dir}")
        return

    count = 0
    print("📂 Loading Templates...")
    for filename in os.listdir(templates_dir):
        if filename.endswith(".md"):
            # Template name becomes the key (e.g., 'person.md' -> 'person')
            key = filename.replace(".md", "").lower()
            try:
                path = os.path.join(templates_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    LOADED_TEMPLATES[key] = f.read()
                print(f"   - Loaded: {key}")
                count += 1
            except Exception as e:
                print(f"   ❌ Failed to load {filename}: {e}")
    
    print(f"✅ Template System Ready: {count} templates loaded.")    

# Helper to fix JSON serialization issues with dates
def _sanitize_metadata(metadata: dict) -> dict:
    """
    Converts non-JSON-serializable objects (like dates) to strings.
    """
    clean_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, (datetime, date)):
            clean_metadata[key] = value.isoformat()
        elif isinstance(value, dict):
            clean_metadata[key] = _sanitize_metadata(value)
        elif isinstance(value, list):
            clean_metadata[key] = [
                item.isoformat() if isinstance(item, (datetime, date)) else item 
                for item in value
            ]
        else:
            clean_metadata[key] = value
    return clean_metadata

def read_markdown(path: str) -> dict:
    """
    Reads a markdown file and returns its metadata and content.
    """
    try:
        full_path = _get_safe_path(path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}

        post = frontmatter.load(full_path)
        return {
            "status": "success",
            "metadata": _sanitize_metadata(post.metadata),
            "content": post.content
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_markdown(filename: str, content: str, folder: str = "0 Inbox", template_name: str = "default") -> dict:
    """
    Creates a new note using a template found in the Templates folder.
    
    Args:
        filename: Title of the note.
        content: The core information to insert into the note.
        folder: Target folder.
        template_name: The name of the template file to use.
    """
    try:
        # 1. Prepare Path
        if not filename.endswith(".md"):
            filename += ".md"
        
        # Security: Ensure folder is safe, but we construct the full path manually to create dirs
        safe_folder_path = _get_safe_path(folder)
        if not os.path.exists(safe_folder_path):
            os.makedirs(safe_folder_path)
            
        full_path = os.path.join(safe_folder_path, filename)
        
        if os.path.exists(full_path):
            return {"status": "error", "message": f"File '{filename}' already exists."}

        # 2. Load Template
        # Fallback to a basic string if the requested template is missing
        template_key = template_name.lower()
        raw_tmpl = LOADED_TEMPLATES.get(template_key, 
            "---\ntype: note\ncreated: {date}\n---\n# {title}\n\n{content}")

        # 3. Inject Data (Simple String Formatting)
        # Note: If your templates use {{Jinja}} style braces for other things, this might break.
        # For simple use, standard python formatting {key} is sufficient.
        final_content = raw_tmpl.replace("{title}", filename.replace(".md", "")) \
                                .replace("{date}", datetime.now().strftime("%Y-%m-%d")) \
                                .replace("{content}", content)

        # 4. Write File
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        return {"status": "success", "file_path": full_path, "message": f"Created note using '{template_key}' template."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Search metadata (like a mini-SQL for the vault)
def query_metadata(key: str, value: str) -> dict:
    """
    Searches for notes where a specific YAML frontmatter key matches a value.
    Supports substring matching (useful for [[Wikilinks]]).
    
    Args:
        key: The metadata field (e.g., 'type', 'company', 'tags').
        value: The value to look for (e.g., 'Person', 'Google').
    """
    matches = {}
    scanned_count = 0
    search_val = value.lower()

    # Walk the entire vault
    for root, _, files in os.walk(VAULT_ROOT):
        for file in files:
            if file.endswith(".md"):
                scanned_count += 1
                full_path = os.path.join(root, file)
                
                try:
                    # frontmatter.load is efficient; it only reads the header
                    post = frontmatter.load(full_path)
                    if not post.metadata: 
                        continue

                    # Check if key exists
                    if key in post.metadata:
                        field_val = post.metadata[key]
                        is_match = False

                        # LOGIC: Handle Lists (tags: [a, b]) vs Strings (type: "[[Person]]")
                        if isinstance(field_val, list):
                            # Check if search_val is inside any of the list items
                            if any(search_val in str(item).lower() for item in field_val):
                                is_match = True
                        else:
                            # Substring match (Handles "[[Person]]" matching "Person")
                            if search_val in str(field_val).lower():
                                is_match = True

                        if is_match:
                            # Return relative path for cleaner agent context
                            rel_path = os.path.relpath(full_path, VAULT_ROOT)
                            matches[rel_path] = _sanitize_metadata(post.metadata)

                except Exception:
                    continue # Skip unreadable files

    if not matches:
        return {"status": "no_results", "message": f"No notes found where '{key}' contains '{value}'."}

    return {
        "status": "success", 
        "query": f"{key} ~= {value}",
        "count": len(matches),
        "results": matches
    }

def update_frontmatter(path: str, updates_json: str) -> dict:
    """
    Updates the frontmatter metadata of an existing markdown file.
    updates_json: JSON string containing the metadata updates.
    """
    try:
        full_path = _get_safe_path(path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}

        updates = json.loads(updates_json)
        post = frontmatter.load(full_path)
        post.metadata.update(updates)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"status": "success", "message": "Metadata updated.", "metadata": _sanitize_metadata(post.metadata)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_content(path: str, new_content: str) -> dict:
    """
    Updates the content (body) of a markdown file while preserving the existing frontmatter.
    """
    try:
        full_path = _get_safe_path(path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}

        # Load existing file to get metadata
        post = frontmatter.load(full_path)

        # Update content
        post.content = new_content

        # Write back
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"status": "success", "message": "Content updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_notes(query: str) -> dict:
    """
    Performs a text search across all notes. 
    Use this ONLY if query_metadata fails to find what you need.
    """
    matches = {}
    
    # Walk the vault
    for root, _, files in os.walk(VAULT_ROOT):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Simple case-insensitive search
                    if query.lower() in content.lower():
                        # Optimization: Return a snippet, not the whole file
                        rel_path = os.path.relpath(full_path, VAULT_ROOT)
                        snippet_index = content.lower().find(query.lower())
                        start = max(0, snippet_index - 50)
                        end = min(len(content), snippet_index + 150)
                        matches[rel_path] = "..." + content[start:end] + "..."
                        
                except Exception:
                    continue
                    
    if not matches:
        return {"status": "no_results"}
        
    return {"status": "success", "matches": matches}

def delete_note(filename: str, folder: str) -> dict:
    """
    Deletes a markdown note from the vault.
    
    Args:
        filename: The name of the file to delete (e.g., "Meeting Notes").
        folder: The folder containing the file (e.g., "Inbox").
    """
    try:
        if not filename.endswith(".md"):
            filename += ".md"
            
        safe_folder_path = _get_safe_path(folder)
        full_path = os.path.join(safe_folder_path, filename)
        
        # Verify path is safe and exists
        safe_full_path = _get_safe_path(full_path)
        
        if not os.path.exists(safe_full_path):
            return {"status": "error", "message": f"File not found: {safe_full_path}"}
            
        os.remove(safe_full_path)
        return {"status": "success", "message": f"Deleted note: {filename}"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

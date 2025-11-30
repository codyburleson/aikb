import os
import frontmatter
import json
import yaml
from datetime import datetime, date
from zoneinfo import ZoneInfo
from google import genai

# Global cache for templates
# This dictionary acts as a high-speed cache for your templates.
# It is populated once when the application starts.
LOADED_TEMPLATES = {}

VAULT_ROOT = os.path.abspath(os.path.expanduser(os.getenv("VAULT_ROOT", "./reference-vault")))

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

# Helper to prepare metadata for function return values
def _sanitize_metadata(metadata: dict) -> dict:
    """
    Converts non-serializable objects (like datetime objects) to strings
    for safe return in function responses.
    """
    result = {}
    for key, value in metadata.items():
        if isinstance(value, (datetime, date)):
            result[key] = value.isoformat() if isinstance(value, datetime) else str(value)
        elif isinstance(value, list):
            result[key] = [
                v.isoformat() if isinstance(v, (datetime, date)) else v
                for v in value
            ]
        else:
            result[key] = value
    return result

def read_markdown(path: str, as_summary: bool = False) -> dict:
    """
    Reads a markdown file and returns its metadata and content.
    
    Args:
        path: The path to the markdown file.
        as_summary: If True, returns a summary of the content instead of the full text.
    """
    try:
        full_path = _get_safe_path(path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}

        post = frontmatter.load(full_path)
        content = post.content

        if as_summary and content.strip():
            try:
                client = genai.Client()
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Summarize the following note concisely, capturing key points and context:\n\n{content}"
                )
                if response.text:
                    content = f"[SUMMARY]\n{response.text}"
            except Exception as e:
                print(f"⚠️ Summarization failed: {e}")
                # Fallback to full content if summarization fails
                pass

        return {
            "status": "success",
            "metadata": _sanitize_metadata(post.metadata),
            "content": content
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_markdown(filename: str, content: str, folder: str = "0 Inbox", template_name: str = "default", frontmatter_yaml: str = None) -> dict:
    """
    Creates a new note using a template found in the Templates folder.

    Args:
        filename: Title of the note.
        content: The core information to insert into the note.
        folder: Target folder.
        template_name: The name of the template file to use.
        frontmatter_yaml: Optional YAML string to populate frontmatter fields.
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
        template_key = template_name.lower()
        if template_key not in LOADED_TEMPLATES:
            return {"status": "error", "message": f"Template '{template_name}' not found. Available: {', '.join(LOADED_TEMPLATES.keys())}"}

        # Parse template frontmatter
        template_post = frontmatter.loads(LOADED_TEMPLATES[template_key])
        metadata = dict(template_post.metadata)
        body_template = template_post.content

        # Merge provided frontmatter (if any)
        if frontmatter_yaml:
            try:
                custom_metadata = yaml.safe_load(frontmatter_yaml)
                if custom_metadata:
                    metadata.update(custom_metadata)
            except Exception as e:
                print(f"Warning: Could not parse frontmatter_yaml: {e}")

        # 3. Load JSON Schema (if available)
        schema_path = os.path.join(VAULT_ROOT, ".aikb", "schemas", f"{template_name.capitalize()}.json")
        schema = None
        if os.path.exists(schema_path):
            try:
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load schema {schema_path}: {e}")

        # 4. Populate Empty Fields Based on Schema
        # Timezone Logic
        configured_tz = os.getenv("TIMEZONE", "")
        try:
            now = datetime.now(ZoneInfo(configured_tz)) if configured_tz else datetime.now()
        except Exception:
            now = datetime.now()

        for key, value in metadata.items():
            # Skip if already populated
            if value:
                continue

            # Check if we have schema information for this field
            if schema and "properties" in schema and key in schema["properties"]:
                prop_schema = schema["properties"][key]
                field_type = prop_schema.get("type", "string")
                field_format = prop_schema.get("format", "")

                # Populate based on type and format
                # ONLY auto-populate created/updated timestamps.
                # Do NOT auto-populate generic dates like birthDate, startDate, etc.
                if key in ["created", "updated"] and field_format == "date-time":
                    metadata[key] = now.isoformat()
                elif key == "name":
                    # Use the filename (without .md) as the name
                    metadata[key] = filename.replace(".md", "")
                # Other empty fields remain empty (will be filled by user or other agents)
            else:
                # Fallback for fields without schema (backward compatibility)
                if key in ["created", "updated"]:
                    metadata[key] = now.strftime("%Y-%m-%d")
                elif key == "name":
                    metadata[key] = filename.replace(".md", "")

        # 5. Create Final Post
        # Ensure no None values exist in metadata (convert to empty string)
        # This prevents "key: null" in the YAML output
        for key, value in metadata.items():
            if value is None:
                metadata[key] = ""

        post = frontmatter.Post(content, **metadata)

        # 6. Write File
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {
            "status": "success",
            "file_path": full_path,
            "message": f"Created note using '{template_key}' template with schema-based field population."
        }

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

def update_frontmatter(path: str, updates_yaml: str) -> dict:
    """
    Updates the frontmatter metadata of an existing markdown file.
    updates_yaml: YAML string containing the metadata updates.
    """
    try:
        full_path = _get_safe_path(path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File not found: {path}"}

        updates = yaml.safe_load(updates_yaml)
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

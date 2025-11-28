import unittest
import os
import shutil
import json
import tempfile
from src.tools.markdown_ops import (
    load_templates,
    create_markdown,
    read_markdown,
    query_metadata,
    update_frontmatter,
    update_content,
    search_notes,
    VAULT_ROOT,
    LOADED_TEMPLATES
)

class TestMarkdownOps(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the vault
        self.test_dir = tempfile.mkdtemp()
        # Mock the VAULT_ROOT in the module (this is a bit hacky but works for simple scripts)
        # Since we can't easily change the global VAULT_ROOT in the imported module without
        # refactoring the module to a class or using a config, we will try to use the
        # real vault root but use a specific test folder to avoid messing up real data.
        # NOTE: The module uses VAULT_ROOT = os.getenv("VAULT_ROOT", "./reference-vault")
        # We use the VAULT_ROOT from the module and create a dedicated test folder within it.


        self.test_folder = "Test_Zone_Automated"
        self.full_test_folder_path = os.path.join(VAULT_ROOT, self.test_folder)

        if os.path.exists(self.full_test_folder_path):
            shutil.rmtree(self.full_test_folder_path)
        os.makedirs(self.full_test_folder_path)

        # Ensure templates are loaded
        load_templates()

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.full_test_folder_path):
            shutil.rmtree(self.full_test_folder_path)

    def test_create_and_read_markdown(self):
        filename = "test_note"
        content = "This is a test note."
        metadata = {"type": "test", "status": "active"}

        # Create
        # Note: create_markdown expects json string for metadata?
        # Wait, looking at the code for create_markdown:
        # def create_markdown(filename: str, content: str, folder: str = "0 Inbox", template_name: str = "default") -> dict:
        # It DOES NOT take metadata as an argument in the signature I saw earlier!
        # Let's re-read the code in step 14.
        # It takes: filename, content, folder, template_name.
        # It does NOT take metadata directly. It uses a template.

        result = create_markdown(filename, content, self.test_folder)
        self.assertEqual(result["status"], "success")

        # Read
        file_path = result["file_path"]
        read_result = read_markdown(file_path)
        self.assertEqual(read_result["status"], "success")
        self.assertIn(content, read_result["content"])

    def test_update_frontmatter(self):
        filename = "update_fm_test"
        create_markdown(filename, "Content", self.test_folder)
        full_path = os.path.join(self.full_test_folder_path, filename + ".md")

        updates = json.dumps({"new_field": "value", "status": "updated"})
        result = update_frontmatter(full_path, updates)
        self.assertEqual(result["status"], "success")

        read_result = read_markdown(full_path)
        self.assertEqual(read_result["metadata"]["new_field"], "value")
        self.assertEqual(read_result["metadata"]["status"], "updated")

    def test_update_content(self):
        filename = "update_content_test"
        create_markdown(filename, "Original Content", self.test_folder)
        full_path = os.path.join(self.full_test_folder_path, filename + ".md")

        new_content = "Updated Content"
        result = update_content(full_path, new_content)
        self.assertEqual(result["status"], "success")

        read_result = read_markdown(full_path)
        self.assertEqual(read_result["content"], new_content)

    def test_query_metadata(self):
        # Create a file with specific metadata
        # Since create_markdown doesn't let us set metadata easily without a template,
        # we'll create it and then update it.
        filename = "query_test"
        create_markdown(filename, "Content", self.test_folder)
        full_path = os.path.join(self.full_test_folder_path, filename + ".md")

        update_frontmatter(full_path, json.dumps({"project": "Apollo", "tags": ["space", "moon"]}))

        # Query
        result = query_metadata("project", "Apollo")
        self.assertEqual(result["status"], "success")
        self.assertGreater(result["count"], 0)

        # Verify the file is in results
        # The keys in results are relative paths
        rel_path = os.path.relpath(full_path, VAULT_ROOT)
        self.assertIn(rel_path, result["results"])

    def test_search_notes(self):
        filename = "search_test"
        unique_string = "Supercalifragilisticexpialidocious"
        create_markdown(filename, f"This note contains {unique_string}", self.test_folder)

        result = search_notes(unique_string)
        self.assertEqual(result["status"], "success")

        full_path = os.path.join(self.full_test_folder_path, filename + ".md")
        rel_path = os.path.relpath(full_path, VAULT_ROOT)
        self.assertIn(rel_path, result["matches"])

if __name__ == '__main__':
    unittest.main()

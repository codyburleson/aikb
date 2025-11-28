from src.tools.markdown_ops import load_templates, LOADED_TEMPLATES, VAULT_ROOT, create_markdown
import os

def debug_templates():
    print(f"VAULT_ROOT: {VAULT_ROOT}")
    
    # 1. Load Templates
    load_templates(VAULT_ROOT)
    
    # 2. Check CreativeWork template
    key = "creativework"
    if key in LOADED_TEMPLATES:
        print(f"\n--- Template: {key} ---")
        print(LOADED_TEMPLATES[key])
        print("-----------------------")
        
        if "{content}" in LOADED_TEMPLATES[key]:
            print("SUCCESS: Template contains {content} placeholder.")
        else:
            print("FAILURE: Template MISSING {content} placeholder.")
    else:
        print(f"FAILURE: Template {key} not found in {list(LOADED_TEMPLATES.keys())}")

    # 3. Test Creation
    print("\n--- Testing Creation ---")
    filename = "Debug_Harry_Potter"
    content = "This is the debug content."
    folder = "3 Resources/Creative Works/Books"
    
    result = create_markdown(filename, content, folder, template_name="CreativeWork")
    print(f"Creation Result: {result}")
    
    if result["status"] == "success":
        with open(result["file_path"], "r") as f:
            created_content = f.read()
            print("\n--- Created File Content ---")
            print(created_content)
            print("----------------------------")
            
            if content in created_content:
                print("SUCCESS: Content was injected correctly.")
            else:
                print("FAILURE: Content was NOT injected.")
                
    # Cleanup
    if result["status"] == "success" and os.path.exists(result["file_path"]):
        os.remove(result["file_path"])

if __name__ == "__main__":
    debug_templates()

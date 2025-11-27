from src.tools.markdown_ops import load_templates, LOADED_TEMPLATES, VAULT_ROOT

def verify_templates():
    print(f"Loading templates from: {VAULT_ROOT}")
    load_templates(VAULT_ROOT)
    
    if LOADED_TEMPLATES:
        print(f"SUCCESS: Loaded {len(LOADED_TEMPLATES)} templates.")
        print(f"Templates: {list(LOADED_TEMPLATES.keys())}")
    else:
        print("FAILURE: No templates loaded.")

if __name__ == "__main__":
    verify_templates()

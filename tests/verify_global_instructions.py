import os
import sys

# Add the repository root to sys.path
sys.path.append(os.getcwd())

from src.agent import load_global_instructions

def test_load_global_instructions():
    vault_path = os.getenv("VAULT_ROOT", "./reference-vault")
    instructions = load_global_instructions(vault_path)

    expected_path = os.path.join(vault_path, ".aikb", "global-instructions.md")
    with open(expected_path, "r", encoding="utf-8") as f:
        expected_content = f.read()

    if instructions == expected_content:
        print("✅ Verification Successful: Global instructions loaded correctly.")
        print("Content Preview:")
        print(instructions[:100] + "...")
    else:
        print("❌ Verification Failed: Loaded content does not match file content.")
        print(f"Expected length: {len(expected_content)}, Got: {len(instructions)}")

if __name__ == "__main__":
    test_load_global_instructions()

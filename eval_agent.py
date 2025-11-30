import subprocess
import time
import os
import shutil

def run_evaluation():
    print("🚀 Starting Agent Evaluation...")

    # Define the test scenario
    test_note_name = "EvalTestNote"
    test_content = "This is a test note created by the evaluation script."
    expected_file = f"reference-vault/0 Inbox/{test_note_name}.md"
    
    # Ensure clean state
    if os.path.exists(expected_file):
        os.remove(expected_file)

    # Start the agent process
    # We use the virtual environment's python to ensure dependencies are met
    process = subprocess.Popen(
        [".venv/bin/python3", "-m", "src.agent"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd()
    )

    try:
        # Wait for agent to initialize (simple sleep for now, could be more robust by reading stdout)
        time.sleep(5) 

        # Send command to create a note
        command = f"Create a note called '{test_note_name}' with content '{test_content}'\n"
        print(f"📤 Sending command: {command.strip()}")
        process.stdin.write(command)
        process.stdin.flush()

        # Wait for processing
        time.sleep(5)

        # Send exit command
        process.stdin.write("exit\n")
        process.stdin.flush()
        
        # Wait for process to finish
        stdout, stderr = process.communicate(timeout=5)
        
        print("\n--- Agent Output ---")
        print(stdout)
        if stderr:
            print("\n--- Agent Errors ---")
            print(stderr)
        print("--------------------\n")

        # Verify file creation
        possible_paths = [
            f"reference-vault/0 Inbox/{test_note_name}.md",
            f"reference-vault/Inbox/{test_note_name}.md"
        ]
        
        found_file = None
        for path in possible_paths:
            if os.path.exists(path):
                found_file = path
                break
        
        if found_file:
            print(f"✅ SUCCESS: File '{found_file}' was created.")
            with open(found_file, "r") as f:
                content = f.read()
                if test_content in content:
                    print("✅ SUCCESS: Content verification passed.")
                else:
                    print(f"❌ FAILURE: Content mismatch. Found:\n{content}")
            
            # Cleanup
            os.remove(found_file)
            print("🧹 Cleanup: Removed test file.")
        else:
            print(f"❌ FAILURE: File '{test_note_name}.md' was NOT created in any expected inbox.")

    except Exception as e:
        print(f"❌ ERROR: Evaluation failed with exception: {e}")
        process.kill()

if __name__ == "__main__":
    run_evaluation()

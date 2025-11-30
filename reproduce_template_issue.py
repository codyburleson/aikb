from src.tools.markdown_ops import create_markdown, load_templates, VAULT_ROOT
import os
import shutil

def test_templates():
    print(f"VAULT_ROOT: {VAULT_ROOT}")
    load_templates(VAULT_ROOT)

    # Test Event Template
    print("\n--- Testing Event Template ---")
    res_event = create_markdown("Test_Event", "Event Content", "0 Inbox", template_name="Event")
    print(f"Result: {res_event}")
    if res_event["status"] == "success":
        with open(res_event["file_path"], "r") as f:
            print(f"Content:\n{f.read()}")
        os.remove(res_event["file_path"])

    # Test DailyNote Template (Exact Match)
    print("\n--- Testing DailyNote Template (Exact) ---")
    res_daily = create_markdown("Test_Daily", "Daily Note Content", "0 Inbox", template_name="DailyNote")
    print(f"Result: {res_daily}")
    if res_daily["status"] == "success":
        with open(res_daily["file_path"], "r") as f:
            print(f"Content:\n{f.read()}")
        os.remove(res_daily["file_path"])

    # Test Daily Note Template (Space - should fallback to hardcoded)
    print("\n--- Testing Daily Note Template (Space) ---")
    res_daily_space = create_markdown("Test_Daily_Space", "Daily Note Space Content", "0 Inbox", template_name="Daily Note")
    print(f"Result: {res_daily_space}")
    if res_daily_space["status"] == "success":
        with open(res_daily_space["file_path"], "r") as f:
            print(f"Content:\n{f.read()}")
        os.remove(res_daily_space["file_path"])

if __name__ == "__main__":
    test_templates()

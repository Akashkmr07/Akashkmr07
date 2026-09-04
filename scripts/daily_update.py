import os
import sys
import datetime
import re

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(repo_root, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}", file=sys.stderr)
        sys.exit(1)
        
    start_tag = "<!-- AUTO-UPDATE-START -->"
    end_tag = "<!-- AUTO-UPDATE-END -->"
    
    if start_tag not in content or end_tag not in content:
        print(f"Error: {start_tag} or {end_tag} not found in README.md", file=sys.stderr)
        sys.exit(1)
        
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    new_section = f"{start_tag}\n\nLast automated maintenance: {now}\n\n{end_tag}"
    
    pattern = re.compile(f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    new_content = pattern.sub(lambda m: new_section, content)
    
    if new_content == content:
        print("No update needed. README.md is already up to date.")
        sys.exit(0)
        
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"Error writing to {readme_path}: {e}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Successfully updated README.md with date {now}.")

if __name__ == "__main__":
    main()

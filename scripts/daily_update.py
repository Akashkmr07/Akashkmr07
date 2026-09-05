import os
import sys
import datetime
import re
import urllib.request
import json

def get_quote():
    try:
        url = "https://api.quotable.io/random?tags=technology|programming"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return f'"{data["content"]}"\n— *{data["author"]}*'
    except Exception as e:
        print(f"Failed to fetch quote from quotable API: {e}. Falling back to default list.")
        import random
        quotes = [
            '"Talk is cheap. Show me the code."\n— *Linus Torvalds*',
            '"Programs must be written for people to read, and only incidentally for machines to execute."\n— *Harold Abelson*',
            '"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."\n— *Martin Fowler*',
            '"First, solve the problem. Then, write the code."\n— *John Johnson*',
            '"Experience is the name everyone gives to their mistakes."\n— *Oscar Wilde*',
            '"In order to be irreplaceable, one must always be different"\n— *Coco Chanel*',
            '"Knowledge is power."\n— *Francis Bacon*',
            '"Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday\'s code."\n— *Dan Salomon*'
        ]
        return random.choice(quotes)

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
        
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    quote = get_quote()
    
    new_section = f"{start_tag}\n\n### 💡 Developer Quote of the Day\n\n> {quote.replace(chr(10), chr(10)+'> ')}\n\n<p align=\"right\" style=\"color: #8b949e; font-size: 0.8em;\">Last automated maintenance: {now}</p>\n\n{end_tag}"
    
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

import os
import sys
import datetime
import subprocess
import random

def run_cmd(cmd, cwd=None, env=None):
    # Merge existing environment with new env vars
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    result = subprocess.run(cmd, shell=True, cwd=cwd, env=run_env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running '{cmd}': {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dummy_file = os.path.join(repo_root, "retro_commits_dummy.txt")
    
    print("Welcome to the Retroactive Commits Generator!")
    print("This script will create past commits to fill your GitHub contribution graph.")
    print("It modifies a dummy file (retro_commits_dummy.txt) and creates commits backdated in time.")
    print("WARNING: This will create a large number of commits in your local history.")
    
    confirm = input("\nDo you want to proceed? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        sys.exit(0)
        
    days = input("How many days back do you want to generate commits for? (default 365): ")
    try:
        days = int(days) if days.strip() else 365
    except ValueError:
        print("Invalid number of days.")
        sys.exit(1)
        
    max_commits_per_day = input("Maximum commits per day? (default 5): ")
    try:
        max_commits_per_day = int(max_commits_per_day) if max_commits_per_day.strip() else 5
    except ValueError:
        print("Invalid maximum commits.")
        sys.exit(1)
        
    print(f"\nGenerating up to {max_commits_per_day} commits per day for the last {days} days...")
    
    now = datetime.datetime.now()
    
    commits_made = 0
    for i in range(days, -1, -1):
        date = now - datetime.timedelta(days=i)
        
        num_commits = random.randint(1, max_commits_per_day)
        
        for j in range(num_commits):
            commit_time = date.replace(
                hour=random.randint(9, 23), 
                minute=random.randint(0, 59), 
                second=random.randint(0, 59)
            )
            
            with open(dummy_file, "a") as f:
                f.write(f"Commit on {commit_time.isoformat()}\n")
            
            run_cmd(f'git add "{dummy_file}"', cwd=repo_root)
            
            date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
            env_vars = {
                'GIT_AUTHOR_DATE': date_str,
                'GIT_COMMITTER_DATE': date_str
            }
            cmd = f'git commit -m "Retroactive contribution {commit_time.date()}"'
            run_cmd(cmd, cwd=repo_root, env=env_vars)
            
            commits_made += 1
            
    print(f"\nDone! Made {commits_made} retroactive commits.")
    print("\nTo push these to GitHub, simply run:")
    print("git push origin main")

if __name__ == "__main__":
    main()

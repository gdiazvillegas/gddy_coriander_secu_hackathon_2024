import json
import subprocess
import os
import re
import sys

def check_commit_exists(repo_path, commit):
    try:
        subprocess.run(['git', '-C', repo_path, 'cat-file', '-e', commit],
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_diff(repo_path, commit1, commit2):
    if not os.path.exists(repo_path):
        return f"Error: The specified repository path does not exist: {repo_path}"
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return f"Error: The specified path is not a git repository: {repo_path}"
    if not check_commit_exists(repo_path, commit1):
        return f"Error: Commit not found: {commit1}"
    if not check_commit_exists(repo_path, commit2):
        return f"Error: Commit not found: {commit2}"
    try:
        result = subprocess.run(['git', '-C', repo_path, 'diff', commit1, commit2], 
                                capture_output=True, 
                                text=True, 
                                check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred while running git diff: {e.stderr}"

def format_diff(diff_output):
    files = diff_output.split('diff --git')[1:]  # Split by file, ignore the first empty part
    formatted_output = ""
    for file_diff in files:
        lines = file_diff.split('\n')
        file_name = lines[0].split()[-1].lstrip('b/')
        
        # Find the start of the actual diff content
        diff_start = next(i for i, line in enumerate(lines) if line.startswith('@@'))
        
        # Extract added lines and count total changes
        added_lines = [line[1:] for line in lines[diff_start:] if line.startswith('+') and not line.startswith('+++')]
        total_changes = sum(1 for line in lines[diff_start:] if line.startswith(('+', '-')) and not line.startswith(('+++ b', '--- a')))
        
        if added_lines:
            formatted_output += f"# {file_name}: {total_changes} change{'s' if total_changes > 1 else ''}\n"
            formatted_output += '\n'.join(added_lines) + '\n\n'
    print("???????????????")
    print(formatted_output.strip())
    print("???????????????")
    return formatted_output.strip()

# Get the PR base and head SHAs
#github_context = json.loads(os.environ['GITHUB_CONTEXT'])
print("#####")
print(dict(os.environ))
print("#####......")
try:
    print("#####......1")
    print(os.getenv('GITHUB_ENV'))    
except e:
    print(e)
try:
    print("#####......2")
    print(os.getenv('GITHUB_OUTPUT'))    
except e:
    print(e)
try:
    print("#####......3")
    print(sys.argv)    
except e:
    print(e)
#pr_base_sha = sys.argv[0]
#pr_head_sha = sys.argv[1]
#repo_path = os.getcwd()
#pr_base_sha = ""#${{ env.BASE_SHA }}
#$BASE_SHA#github_context['event']['pull_request']['base']['sha']#os.environ['BASE_SHA']
#pr_head_sha = ""#${{ env.HEAD_SHA}}
#$HEAD_SHA#github_context['event']['pull_request']['head']['sha']#os.environ['HEAD_SHA']

#repo_path = os.environ['GITHUB_WORKSPACE']
#repo_path = "GITHUB_WORKSPACE"
print("33333334333333333333333")
#print(f": repo_path: {repo_path}")
#print(f"pr_base_sha: {pr_base_sha}")
#print(f": pr_head_sha{pr_head_sha}")
print("33333334333333333333333")
#diff = get_git_diff(repo_path, pr_base_sha, pr_head_sha)
print("222222")
#print(f"diff: {diff}")
print("222222")
#formatted_diff = format_diff(diff)
#print(formatted_diff)

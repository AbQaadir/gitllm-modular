import os
import base64
import requests
from langchain_core.tools import tool
from .config import get_github_token


def get_repo_name_owner(github_repo_url: str) -> tuple:
    """Extract repository owner and name from a GitHub URL."""
    
    if not github_repo_url:
        raise ValueError("GitHub URL not provided")
    
    parts = github_repo_url.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    
    return parts[-2], parts[-1]

def detect_project_type(contents) -> str:
    """Detect project type based on file extensions in the repository."""
    FILE_EXTENSIONS = {
        'python': ['.py'],
        'java': ['.java'],
        'ballerina': ['.bal'],
        'react': ['.js', '.tsx']
    }
    
    extension_counts = {project: 0 for project in FILE_EXTENSIONS}
    
    for item in contents:
        if item['type'] == 'file':
            for project, extensions in FILE_EXTENSIONS.items():
                if any(item['name'].endswith(ext) for ext in extensions):
                    extension_counts[project] += 1
    
    dominant_type = max(extension_counts.items(), key=lambda x: x[1], default=('java', 0))[0]
    return dominant_type if extension_counts[dominant_type] > 0 else 'all'

def get_repo_structure(repo_link: str, path="", depth=0, is_last=False, prefix="", project_type=None):
    """Generate a tree structure of the files and directories in a GitHub repository
    with automatic project type detection and filtered source files, pruning empty dirs."""
    
    FILE_EXTENSIONS = {
        'python': ['.py'],
        'java': ['.java'],
        'ballerina': ['.bal'],
        'react': ['.js', '.tsx'],
        'all': None
    }

    repo_owner, repo_name = get_repo_name_owner(repo_link)
    tree_structure = ""

    # Initialize root directory name at depth 0
    if depth == 0:
        tree_structure += repo_name + "\n"

    # Construct GitHub API URL for the current path
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    
    github_token = get_github_token()  # Assuming this function exists elsewhere
    
    if not github_token:
        return "GitHub token missing (set GITHUB_TOKEN env variable)"
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        
        # Detect project type only at root level
        if depth == 0:
            project_type = detect_project_type(contents)
        
        # Filter contents to only include directories and relevant source files
        if FILE_EXTENSIONS[project_type]:
            relevant_extensions = FILE_EXTENSIONS[project_type]
        else:
            relevant_extensions = ('.py', '.java', '.bal', '.js', '.tsx')

        filtered_contents = []
        dir_subtrees = []

        # Process items and collect subtrees for directories
        for item in contents:
            if item['type'] == 'file' and any(item['name'].endswith(ext) for ext in relevant_extensions):
                filtered_contents.append(item)
            elif item['type'] == 'dir':
                # Recursively get the subtree for this directory
                subtree = get_repo_structure(repo_link, item['path'], depth + 1, False, "", project_type)
                if subtree.strip():  # Only include directory if its subtree has relevant content
                    filtered_contents.append(item)
                    dir_subtrees.append((item['name'], subtree))

        num_items = len(filtered_contents)

        # Build the tree structure
        for index, item in enumerate(filtered_contents):
            is_last_item = (index == num_items - 1)
            connector = "   " if is_last_item else "│  "
            tree_structure += prefix + ("└── " if is_last_item else "├── ") + item['name'] + "\n"

            # Append the subtree for directories
            if item['type'] == 'dir':
                for dir_name, subtree in dir_subtrees:
                    if dir_name == item['name']:
                        tree_structure += prefix + connector + subtree.replace('\n', '\n' + prefix + connector, -1).rstrip()
                        break

    else:
        tree_structure += f"Failed to fetch contents: {response.status_code}\n"
    
    return tree_structure


@tool
def get_file_content(github_repo_url: str, file_path: str) -> str:
    """Fetch and decode content of a file from a GitHub repository."""
    # Get repo details
    repo_owner, repo_name = get_repo_name_owner(github_repo_url)
    github_token = get_github_token()
    
    if not github_token:
        return "GitHub token missing (set GITHUB_TOKEN env variable)"
    
    # Build and call API
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if not response.ok:
        return f"Failed to fetch file: {response.status_code}"
    
    # Decode content
    file_data = response.json()
    content = file_data.get('content', '')
    
    if not content:
        return "No content found in file"
    
    return base64.b64decode(content.replace('\n', '')).decode('utf-8')


# Tool usage: 
if __name__ == "__main__":
    
    file_content = get_file_content.invoke({
        "github_repo_url": os.getenv("GITHUB_REPOSITORY"),
        "file_path": "README.md"
    })
    
    print(file_content)
    
    
    repo_structure = get_repo_structure(
        repo_link=os.getenv("GITHUB_REPOSITORY")
        )
    
    print(repo_structure)
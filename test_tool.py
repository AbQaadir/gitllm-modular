# import requests
# from src.config import get_github_token


# import requests

# def get_repo_name_owner(github_repo_url: str) -> tuple:
#     """Extract repository owner and name from a GitHub URL."""
#     if not github_repo_url:
#         raise ValueError("GitHub URL not provided")
    
#     parts = github_repo_url.strip('/').split('/')
#     if len(parts) < 2:
#         raise ValueError("Invalid GitHub URL format")
    
#     return parts[-2], parts[-1]





# if __name__ == "__main__":
    
#     # repo_link = "https://github.com/AbQaadir/chainlit_choreo"
#     repo_link = "https://github.com/wx-yz/ai-gateway"
    
#     tree_structure = get_repo_structure(repo_link)
#     print(tree_structure)
    
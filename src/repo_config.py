# repo_config.py

class RepoHolder:
    def __init__(self, url):
        self.url = url

# Initialize with a default URL (optional)
repo_holder = RepoHolder("https://github.com/uthaiyashankar/2025-02-devant-samples")

def get_repo_url():
    """Get the current repository URL."""
    return repo_holder.url

def set_repo_url(url: str):
    """Set a new repository URL dynamically."""
    repo_holder.url = url
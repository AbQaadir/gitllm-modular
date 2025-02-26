class RepoHolder:
    def __init__(self, url):
        self.url = url

repo_holder = RepoHolder("https://github.com/uthaiyashankar/2025-02-devant-samples")

def get_repo_url():
    return repo_holder.url

if __name__ == "__main__":
    from src.graph import app
    from src.tools import get_repo_structure
    
    tree_structure = get_repo_structure(
        repo_link=get_repo_url()
    )
    
    print(tree_structure)
    
    task = f"Review the code in the given project directory. file structure: \n\n {tree_structure}"
    
    for s in app.stream({"task" : task}, stream_mode="debug"):
        print(s)
        print("\n\n")

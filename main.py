# main.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Generator

# Import from the new module
from src.repo_config import get_repo_url, set_repo_url

# Assuming these imports work in your project
from src.graph import app
from src.tools import get_repo_structure

# FastAPI app instance
app_fastapi = FastAPI()

# Add CORS middleware to the app
app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the request body model
class RepoRequest(BaseModel):
    repo_url: str

# Function to generate stream content in a readable format
def generate_stream_content(repo_url: str) -> Generator[str, None, None]:
    try:
        # Set the repo URL in the shared config
        set_repo_url(repo_url)
        
        # Get the repository structure using the shared URL
        tree_structure = get_repo_structure(repo_link=get_repo_url())
        
        # Prepare the task
        task = f"Review the code in the given project directory. file structure: \n\n {tree_structure}"
        
        # Stream the file structure first
        yield f"Repository File Structure:\n{tree_structure}\n\n"
        yield "Processing review steps...\n\n"

        # Stream meaningful parts of the app.stream output with stream_mode="updates"
        for s in app.stream({"task": task}, stream_mode="updates"):
            if 'plan' in s:
                yield "📝 Plan Update:\n"
                for step in s['plan']['steps']:
                    yield f"  - {step[0]}\n"  # Stream step description
                yield "\n"
            elif 'tool' in s:
                yield "🛠️ Tool Update:\n"
                for key, value in s['tool']['results'].items():
                    yield f"  - {key}: {value}\n"  # Stream tool result key-value pairs
                yield "\n"
            elif 'solve' in s:
                yield "✅ Final Result:\n"
                yield f"{s['solve']['result']}\n\n"  # Stream the final solved content
            yield "---\n"  # Separator between updates
    
    except Exception as e:
        yield f"Error: {str(e)}\n\n"

# FastAPI POST streaming endpoint
@app_fastapi.post("/review-repo")
async def review_repo(request: RepoRequest):
    # Return a StreamingResponse with the generator
    return StreamingResponse(
        generate_stream_content(request.repo_url),
        media_type="text/plain"
    )

# Run the app (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)
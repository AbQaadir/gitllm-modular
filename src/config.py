# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_github_token():
    return os.getenv("GITHUB_TOKEN")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

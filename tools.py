#tools.py
import os
import re
from dotenv import load_dotenv
from crewai_tools import GithubSearchTool
from langchain_groq import ChatGroq
from github import Github
from github.GithubException import GithubException
from langchain_huggingface import HuggingFaceEmbeddings


# Load environment variables
load_dotenv()

# Get GitHub token and Groq API key from environment variables
github_token = os.getenv("GITHUB_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")

if not github_token:
    raise EnvironmentError("GITHUB_TOKEN is not set in the environment or .env file")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set in the environment or .env file")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama2-70b-4096",
    temperature=0.7,
)

def validate_repo_url(repo_url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL format")
    return match.groups()

def create_github_search_tool(repo_url):
    try:
        owner, repo = validate_repo_url(repo_url)
        
        # Verify repository exists and is accessible
        g = Github(github_token)
        repo_obj = g.get_repo(f"{owner}/{repo}")
        
        # If we get here, the repository exists and is accessible
        return GithubSearchTool(
            github_repo=repo_url,
            content_types=['code', 'issue'],
            gh_token=github_token,
            config=dict(
                llm=dict(
                    provider="groq",
                    config=dict(
                        model="llama2-70b-4096",
                        api_key=groq_api_key,
                    ),
                ),
                embedder=dict(
                    provider="huggingface",
                    config=dict(
                        model="sentence-transformers/all-MiniLM-L6-v2",
                    ),
                ),
            )
        )
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
    except GithubException as e:
        if e.status == 404:
            print(f"Error: Repository not found or you don't have permission to access it.")
        else:
            print(f"GitHub API Error: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    
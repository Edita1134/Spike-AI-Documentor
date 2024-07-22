#agents.py
from dotenv import load_dotenv
load_dotenv()
import os
from crewai import Agent
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama2-70b-4096",
    temperature=0.5,
)

github_agent = Agent(
    role='GitHub Researcher and Documentation Writer',
    goal='Interact with GitHub repositories to fetch files, analyze code, and write documentation',
    backstory='You are an expert in understanding complex codebases, their architectures, and writing clear, concise documentation.',
    verbose=True,
    llm=llm
)
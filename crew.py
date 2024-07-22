#crew.py
from crewai import Crew
from agents import github_agent
from tasks import create_tasks

class DocumentationCrew:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.tasks = create_tasks(self.repo_url)
        if not self.tasks:
            raise ValueError("No tasks could be created. Please check the repository URL and your permissions.")
        self.crew = Crew(
            agents=[github_agent],
            tasks=self.tasks,
            verbose=2
        )

    def run(self):
        result = self.crew.kickoff()
        return result
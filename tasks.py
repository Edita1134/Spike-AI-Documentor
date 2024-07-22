#tasks.py
from crewai import Task
from agents import github_agent
from tools import create_github_search_tool

def create_tasks(repo_url):
    github_search_tool = create_github_search_tool(repo_url)
    
    if github_search_tool is None:
        return []  # Return an empty list if the tool couldn't be created

    analyze_code_task = Task(
        description=f'Analyze the structure and relationships between different files in the repository: {repo_url}',
        expected_output='A detailed analysis of the code structure and relationships between files.',
        agent=github_agent,
        tools=[github_search_tool]
    )

    write_documentation_task = Task(
        description='Write clear and concise documentation for each file based on the analysis.',
        expected_output='Comprehensive documentation for each analyzed file.',
        agent=github_agent,
        tools=[github_search_tool]
    )

    review_documentation_task = Task(
        description='Review and improve the generated documentation. Ensure accuracy, clarity, and completeness.',
        expected_output='Reviewed and improved documentation for each file.',
        agent=github_agent,
        tools=[github_search_tool]
    )

    show_updated_repo_task = Task(
        description=f'Show the updated repository structure and list of files with their new documentation: {repo_url}',
        expected_output='A comprehensive overview of the updated repository, including file structure and new documentation references.',
        agent=github_agent,
        tools=[github_search_tool]
    )

    return [analyze_code_task, write_documentation_task, review_documentation_task, show_updated_repo_task]
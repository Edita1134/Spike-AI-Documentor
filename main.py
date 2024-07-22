#main.py
import os
from dotenv import load_dotenv
from crew import DocumentationCrew

def main():
    load_dotenv()

    required_vars = ['GITHUB_TOKEN', 'GROQ_API_KEY']
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"{var} is not set in the environment or .env file")

    repo_url = input("Enter the GitHub repository URL: ")
    
    try:
        doc_crew = DocumentationCrew(repo_url)
        result = doc_crew.run()

        print("\nDocumentation update summary:")
        print(result)
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

    print("\nIf you encountered any errors, please check the following:")
    print("1. Ensure your GitHub token has the necessary permissions to access the repository.")
    print("2. Verify that the repository URL is correct and the repository exists.")
    print("3. Make sure the specified files exist in the repository.")
    print("4. Check your internet connection and try again.")

if __name__ == "__main__":
    main()
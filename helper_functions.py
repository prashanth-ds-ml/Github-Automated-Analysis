import requests
import openai
import keys
from github import Github


# Set up OpenAI GPT API credentials
openai.api_key = keys.OPENAI_API_KEY


def fetch_user_repositories(github_url):
    # Extract the username from the GitHub URL
    username = github_url.split('/')[-1]

    # Authenticate with GitHub using a personal access token
    g = Github(keys.GITHUB_ACCESS_TOKEN)

    try:
        # Get the user object based on the username
        user = g.get_user(username)

        # Retrieve all the repositories of the user
        repositories = user.get_repos()

        # Create a list to store repository names and associated code files
        repository_files = []

        # Iterate over each repository
        for repo in repositories:
            # Fetch the code files for the current repository
            code_files = fetch_code_files(repo)

            # Only include repositories with code files
            if code_files:
                # Append the repository name and code files to the list
                repository_files.append((repo.name, code_files))

        # Return the list of repository names and associated code files
        return repository_files
    except Exception as e:
        # Handle any exceptions that might occur
        print(f"An error occurred: {str(e)}")
        return []


def fetch_code_files(repo):
    code_files = []
    try:
        files = repo.get_contents("")
        for file in files:
            # Filter code files based on their extensions
            if file.name.endswith(('.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.js')):
                file_content = fetch_file_content(file.download_url)
                code_files.append((file.name, file_content))
        return code_files
    except Exception as e:
        raise Exception(f"Failed to fetch code files. Error: {str(e)}")


def fetch_file_content(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch file content. Status code: {response.status_code}")


def assess_code_complexity_and_generate_justification(code_text):
    prompt = "Evaluate the technical complexity and justify it using 100 words or less:\n\n"
    input_text = prompt + code_text

    # Truncate code snippet to fit within the context limit
    max_code_length = 4096
    truncated_code = input_text[:max_code_length]

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=truncated_code,
        max_tokens=200,
        temperature=0.5,
        n=1,
        best_of=1,
    )
    complexity_and_justification = response.choices[0].text.strip()
    return complexity_and_justification


def extract_detailed_justification(complexity_and_justification):
    split_text = complexity_and_justification.split('\n', 1)
    if len(split_text) > 1:
        detailed_justification = split_text[1]
    else:
        detailed_justification = ""
    return detailed_justification


def remove_comments(code):
    import re
    # Remove single-line comments
    code = re.sub(r"\/\/.*", "", code)
    # Remove multi-line comments
    code = re.sub(r"\/\*.*?\*\/", "", code, flags=re.DOTALL)
    return code


def remove_extra_spaces(code):
    # Remove leading and trailing spaces
    code = code.strip()
    # Replace multiple spaces with a single space
    code = ' '.join(code.split())
    return code


def identify_most_complex_repository(repositories):
    max_complexity = -1
    most_complex_repo = None

    for repo_name, code_files in repositories:
        code_text = ""

        for _, file_content in code_files:
            # Remove comments and extra spaces from the code to reduce noise
            code_without_comments = remove_comments(file_content)
            code_without_spaces = remove_extra_spaces(code_without_comments)

            # Append the code to the code_text
            code_text += code_without_spaces

        # Assess code complexity and generate justification for the entire code
        complexity_and_justification = assess_code_complexity_and_generate_justification(code_text)
        detailed_justification = extract_detailed_justification(complexity_and_justification)

        # Check if the current repository has higher complexity than the previous maximum
        if len(detailed_justification) > max_complexity:
            max_complexity = len(detailed_justification)
            most_complex_repo = (repo_name, detailed_justification)

    return most_complex_repo

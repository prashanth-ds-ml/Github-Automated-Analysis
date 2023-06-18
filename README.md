# Github-Automated-Analysis

### helper_function.py module

- Here i have defined a helper_function module to define various functions that will help in automated analysis

1. **Importing Required Modules:**
   - The script begins by importing the necessary modules: `requests` for making HTTP requests, `openai` for interacting with the OpenAI GPT API, `keys` for storing API keys, and `Github` from the `github` library for interacting with the GitHub API.

2. **Setting OpenAI API Key:**
   - The OpenAI API key is set using the value stored in `keys.OPENAI_API_KEY`.

3. **Function: fetch_user_repositories(github_url):**
   - This function takes a GitHub URL as input and retrieves repositories and their code files associated with the given username.
   - It extracts the username from the GitHub URL and authenticates with GitHub using a personal access token stored in `keys.GITHUB_ACCESS_TOKEN`.
   - It retrieves all the repositories of the user and creates an empty list to store the repository names and their associated code files.
   - It iterates over each repository, fetches the code files for each repository using the `fetch_code_files` function, and appends the repository name and code files to the `repository_files` list.
   - It returns the list of repository names and associated code files. If an exception occurs, it catches the exception, prints an error message, and returns an empty list.

4. **Function: fetch_code_files(repo):**
   - This function takes a repository object as input and retrieves code files from the repository.
   - It creates an empty list to store the code files.
   - It fetches all the files from the repository using the `get_contents` method.
   - It filters the code files based on their extensions (e.g., `.py`, `.java`, `.cpp`, etc.).
   - For each code file, it fetches the file content using the `fetch_file_content` function and appends the filename and content to the `code_files` list.
   - It returns the list of code files. If an exception occurs, it raises an exception with an error message.

5. **Function: fetch_file_content(file_url):**
   - This function takes a file URL as input and fetches the file content using the `requests` module.
   - It makes an HTTP GET request to the file URL and checks if the response status code is 200 (indicating a successful request).
   - If the request is successful, it returns the text content of the file. Otherwise, it raises an exception with an error message.

6. **Function: assess_code_complexity_and_generate_justification(code_text):**
   - This function takes a code text as input and assesses the technical complexity of the code by generating a justification using the OpenAI GPT API.
   - It constructs a prompt with a predefined message and appends the code text to it.
   - To fit within the context limit of 4096 characters, it truncates the combined text if necessary.
   - It uses the OpenAI API's `Completion` class to generate a completion for the truncated code.
   - It retrieves the complexity and justification from the response and returns it.

7. **Function: extract_detailed_justification(complexity_and_justification):**
   - This function takes the complexity and justification text as input and extracts the detailed justification from it.
   - It splits the complexity and justification text at the first occurrence of a newline character (`\n`).
   - If the split results in more than one part, it assigns the second part (detailed justification) to the `detailed_justification` variable.
   - If the split results in only one part (no newline character found), it assigns an empty string

 to `detailed_justification`.
   - The function returns the detailed justification.

8. **Function: remove_comments(code):**
   - This function takes a code text as input and removes both single-line and multi-line comments from the code.
   - It uses regular expressions (`re`) to remove single-line comments starting with `//` and multi-line comments enclosed within `/*` and `*/`.
   - The function returns the code without comments.

9. **Function: remove_extra_spaces(code):**
   - This function takes a code text as input and removes leading and trailing spaces using the `strip` method.
   - It replaces multiple consecutive spaces with a single space by splitting the code into a list of words using `split()` and joining them back with a single space using `' '.join()`.
   - The function returns the code without extra spaces.

10. **Function: identify_most_complex_repository(repositories):**
    - This function takes a list of repositories and their code files as input and identifies the repository with the highest code complexity.
    - It initializes `max_complexity` with -1 and `most_complex_repo` with `None`.
    - It iterates over each repository and code files and calculates the code complexity by concatenating the code files after removing comments and extra spaces.
    - It uses the `assess_code_complexity_and_generate_justification` function to assess the code complexity and generate a justification for the entire code.
    - It extracts the detailed justification using the `extract_detailed_justification` function.
    - It compares the length of the detailed justification with the maximum complexity seen so far and updates the maximum complexity and the most complex repository accordingly.
    - Finally, it returns the repository with the highest complexity as a tuple.

### app.py

1. **Importing Required Modules:**
   - The code begins by importing the necessary modules:
     - `Flask` from the `flask` module to create the Flask application.
     - `render_template` from the `flask` module to render HTML templates.
     - `request` from the `flask` module to handle HTTP requests.

2. **Creating the Flask Application:**
   - The Flask application is created using `Flask(__name__)`. The `__name__` argument represents the name of the current module.

3. **Route: "/" - Index Page:**
   - `@app.route("/", methods=["GET", "POST"])` decorates the function `index()` and associates it with the URL route "/".
   - The function handles both GET and POST requests to the root URL.
   - If the request method is POST, the function retrieves the GitHub URL from the submitted form data.
   - It calls the `fetch_user_repositories` function to retrieve the repositories and their code files associated with the given GitHub URL.
   - If repositories are found, it calls the `identify_most_complex_repository` function to identify the most complex repository.
   - If a most complex repository is found, it extracts the repository name, complexity, and generates the GitHub link for that repository.
   - The function renders the "index.html" template, passing the repository name as the title, complexity as the script, and the GitHub link as the link.

4. **Route: "/" - GET Request:**
   - If the request method is GET (i.e., accessing the root URL without form submission), the function renders the "index.html" template without any data.

5. **Running the Flask Application:**
   - The code checks if the current module is the main module (`__name__ == "__main__"`) to ensure that the application is being run directly and not imported.
   - It calls `app.run()` to run the Flask application.
   - The application runs with `debug=False` and `host='0.0.0.0'`, which means it runs in production mode and listens on all available network interfaces.

This Flask application serves a single route at the root URL ("/"). When accessed, it renders the "index.html" template, which is responsible for displaying the most complex repository information based on a GitHub URL submitted via a form. The application makes use of helper functions `fetch_user_repositories` and `identify_most_complex_repository` to fetch and process the repositories' data.

Please note that this code assumes the presence of an "index.html" template and the `helper_functions` module, which should contain the required helper functions. Ensure that these files are present and properly implemented for the code to run successfully.
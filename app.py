from flask import Flask, render_template, request
from helper_functions import fetch_user_repositories, identify_most_complex_repository

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        github_url = request.form["github_url"]
        repositories = fetch_user_repositories(github_url)

        if repositories:
            most_complex_repo = identify_most_complex_repository(repositories)
            if most_complex_repo:
                repo_name, repo_complexity = most_complex_repo
                repo_link = f"{github_url}/{repo_name}"
                return render_template("index.html", title=repo_name, script=repo_complexity, link=repo_link)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')

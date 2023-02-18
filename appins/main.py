import pathlib
import subprocess

from typer import Typer

app = Typer()


@app.command()
def init(template_url: str):
    """
    Create a new project from a template.
    template_url: The url of the template to use.
    """
    print(f"Creating new project from {template_url}...")
    subprocess.run(["cookiecutter", template_url])


@app.command()
def get_app(url: str):
    """
    Clone a repository from GitHub into apps directory.
    url: The url of the repository to clone.
    """
    print(f"Cloning {url}...")
    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    subprocess.run(["git", "clone", url, apps_directory + "/" + url.split("/")[-1]])


@app.command()
def remove_app(app_name: str):
    """
    Remove an app from the apps directory.
    app_name: The name of the app to remove.
    """
    print(f"Removing {app_name}...")
    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    subprocess.run(["rm", "-rf", apps_directory + "/" + app_name])


@app.command()
def start(server_path: str = "core.backend.src.main:app"):
    """
    Start the FastAPI server.
    server_path: The path to the FastAPI server. default: core.backend.src.main:app
    """
    print(f"Starting {server_path}...")
    subprocess.run(["uvicorn", server_path, "--reload"])

import pathlib
import subprocess

from typer import Typer

app = Typer()


@app.command(help="Create a new project from a template.")
def init():
    print(f"Creating new project...")
    template_url = "git@github.com:0xsirsaif/enabled-project-template.git"
    subprocess.run(["cookiecutter", template_url])


@app.command(help="Clone an app repository from GitHub into apps directory.")
def clone_app(app_url: str):
    """
    Clone an app repository from GitHub into apps directory.
    url: The url of the repository to clone.
    """
    print(f"Cloning {app_url}...")
    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    subprocess.run(
        ["git", "clone", app_url, apps_directory + "/" + app_url.split("/")[-1]]
    )


@app.command(help="Remove an app from the apps directory.")
def remove_app(app_name: str):
    """
    Remove an app from the apps directory.
    app_name: The name of the app to remove.
    """
    print(f"Removing {app_name}...")
    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    removed_app = pathlib.Path(apps_directory + "/" + app_name)
    subprocess.run(["rm", "-rf", removed_app])


@app.command(help="Create a new app.")
def create_new_app():
    print("Creating new app from...")
    new_app_template = "git@github.com:0xsirsaif/enabled-app-template.git"
    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    subprocess.run(["cookiecutter", new_app_template, "--output-dir", apps_directory])


@app.command()
def start(server_path: str = "core.backend.src.main:app"):
    """
    Start the FastAPI server.
    server_path: The path to the FastAPI server. default: core.backend.src.main:app
    """
    print(f"Starting {server_path}...")
    is_inside_apps = True if pathlib.Path.cwd().name == "apps" else False
    server_path = server_path if is_inside_apps else f"apps.{server_path}"
    subprocess.run(["uvicorn", server_path, "--reload"])


@app.command()
def install_app(app_name: str):
    """
    Install app requirements.
    app_name: The name of the app to install.
    """
    print(f"Installing {app_name}...")


@app.command()
def update_app(app_name: str):
    """
    Update an app.
    app_name: The name of the app to update.
    """
    print(f"Updating {app_name}...")


@app.command()
def create_migration():
    """
    Create a new migration.
    """
    print("Creating new migration...")


@app.command()
def apply_migration():
    """
    Apply all migrations.
    """
    print("Applying migrations...")

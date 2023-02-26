import pathlib
import subprocess

from cookiecutter.main import cookiecutter

import typer

app = typer.Typer()


@app.command(help="Create a new project from a template.")
def init():
    print("Creating new project...")
    template_url = "git@github.com:0xsirsaif/enabled-project-template.git"

    # typer to ask for project name
    project_name = typer.prompt("Project name", default="Base project")
    project_slug = typer.prompt("Project slug", default=project_name.lower().replace(" ", "_"))
    author = typer.prompt("Author", default="enabled")

    # cookiecutter to create project
    cookiecutter(
        template_url,
        no_input=True,
        extra_context={
            "project_name": project_name,
            "project_slug": project_slug,
            "author": author,
        },
    )

    cwd = pathlib.Path.cwd()
    apps_dir = cwd / project_slug / "apps"

    core_app_url = "git@github.com:enabledu/enabled.git"
    print(f"Cloning {core_app_url}...")

    subprocess.run(["git", "clone", core_app_url, apps_dir / "enabled"])


@app.command(help="Clone an app repository from GitHub into apps directory.")
def clone_app(app_url: str):
    """
    Clone an app repository from GitHub into apps directory. and install requirements.
    url: The url of the repository to clone.
    """
    print(f"Cloning {app_url}...")

    apps_directory = "." if pathlib.Path.cwd().name == "apps" else "./apps"
    app_to_clone = app_url.split("/")[-1].replace(".git", "")

    subprocess.run(["git", "clone", app_url, apps_directory + "/" + app_to_clone])


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

    cookiecutter(new_app_template, no_input=True, output_dir=apps_directory)


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
def install_requirements():
    """
    Install app requirements.
    app_name: The name of the app to install.
    """
    print(f"Installing requirements")
    cwd = pathlib.Path.cwd()
    is_apps_besides = True if (cwd / "apps").exists() else False
    if is_apps_besides:
        apps_dir = cwd / "apps"
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir():
                requirements_file = app_dir / "requirements.txt"
                if requirements_file.exists():
                    subprocess.run(["python", "-m", "pip", "install", "-r", requirements_file])
    else:
        print(
            "No apps directory found. Make sure you are in the project root directory."
        )


@app.command()
def merge_esdl():
    """
    Merge all apps `.esdl` files into dbschema global directory.
    """
    cwd = pathlib.Path.cwd()
    is_dbschema_besides = True if (cwd / "dbschema").exists() else False
    if is_dbschema_besides:
        global_dbschema = cwd / "dbschema"
        apps_directory = cwd / "apps"
        for app_dir in apps_directory.iterdir():
            if app_dir.is_dir():
                try:
                    app_dbschema = app_dir / "dbschema"
                    esdl_files = app_dbschema.glob("*.esdl")
                    for esdl_file in esdl_files:
                        subprocess.run(
                            [
                                "cp",
                                esdl_file,
                                global_dbschema / f"{app_dir.name}_{esdl_file.name}",
                            ]
                        )
                except FileNotFoundError as e:
                    print(f"FileNotFoundError: {e}")

    else:
        print("No dbschema directory found. Please got to the project root directory.")

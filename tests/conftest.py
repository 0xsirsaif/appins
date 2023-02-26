import shutil

import pytest


@pytest.fixture
def temp_enabled_project(tmp_path):
    enabled_project_dir = tmp_path / "enabled"
    enabled_global_schema = enabled_project_dir / "dbschema"
    enabled_app_1_schema = enabled_project_dir / "apps" / "my_app" / "dbschema"
    enabled_app_2_schema = enabled_project_dir / "apps" / "my_app_2" / "dbschema"

    enabled_project_dir.mkdir()
    enabled_global_schema.mkdir(parents=True)
    enabled_app_1_schema.mkdir(parents=True)
    enabled_app_2_schema.mkdir(parents=True)

    yield enabled_project_dir

    shutil.rmtree(enabled_project_dir)


@pytest.fixture
def cwd(mocker, temp_enabled_project):
    mocker.patch("pathlib.Path.cwd", return_value=temp_enabled_project)
    yield temp_enabled_project


@pytest.fixture
def project_slug(tmp_path):
    project_slug = tmp_path / "my_project"
    project_slug.mkdir()

    yield project_slug

    shutil.rmtree(project_slug)


@pytest.fixture
def apps_dir(project_slug):
    apps_dir = project_slug / "apps"
    apps_dir.mkdir()

    yield apps_dir

    shutil.rmtree(apps_dir)
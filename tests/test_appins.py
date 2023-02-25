from appins.main import merge_esdl


def test_merge_esdl_no_dbschema(mocker, temp_enabled_project):
    mocker.patch("pathlib.Path.cwd", return_value=temp_enabled_project)
    dbschema_dir = temp_enabled_project / "dbschema"

    merge_esdl()

    assert len(list(dbschema_dir.iterdir())) == 0


def test_merge_esdl_with_dbschema(cwd, temp_enabled_project):
    dbschema_dir = temp_enabled_project / "dbschema"
    my_app_dir = temp_enabled_project / "apps" / "my_app" / "dbschema"
    (my_app_dir / "default.esdl").touch()

    merge_esdl()

    assert (dbschema_dir / "my_app_default.esdl").exists()
    assert len(list(dbschema_dir.iterdir())) == 1


def test_merge_esdl_with_multiple_apps(cwd, temp_enabled_project):
    dbschema = temp_enabled_project / "dbschema"
    my_app_dir = temp_enabled_project / "apps" / "my_app" / "dbschema"
    my_app_2_dir = temp_enabled_project / "apps" / "my_app_2" / "dbschema"
    (my_app_dir / "default.esdl").touch()
    (my_app_2_dir / "default.esdl").touch()

    merge_esdl()

    assert (dbschema / "my_app_default.esdl").exists()
    assert (dbschema / "my_app_2_default.esdl").exists()
    assert len(list(dbschema.iterdir())) == 2

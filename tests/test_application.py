from repertoire.application import create_app


def test_application_constructor():
    uut = create_app()
    assert uut is not None

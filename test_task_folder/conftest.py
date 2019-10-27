import pytest


@pytest.fixture(scope="session", autouse=True)
def resource_setup():
    print("\n------Start Unit tests------")
    yield
    print("\n------End Unit tests------")

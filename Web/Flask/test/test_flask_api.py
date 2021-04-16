import pytest
from src import create_app
from flask.helpers import url_for


@pytest.fixture(scope="function")
def client(request):
    app = create_app("testing")
    context = app.test_request_context()
    context.push()
    client = app.test_client()
    print("create context")
    yield client
    context.pop()
    print("context pop")

@pytest.mark.website
def test_1(client):
    response = client.get(
        url_for("companies_access_rules", cid="test"), follow_redirects=True
    )
    print(response)

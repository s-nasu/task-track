import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

cors_header = "access-control-allow-origin"


@pytest.mark.parametrize(
    "url, status_code, should_contain_cors_header",
    [
        ("http://localhost:3000", status.HTTP_200_OK, True),
        ("http://disallowed.origin.com", status.HTTP_400_BAD_REQUEST, False),
    ],
)
def test_cors(url, status_code, should_contain_cors_header):
    headers = {"Origin": url, "Access-Control-Request-Method": "GET"}
    response = client.options("/", headers=headers)
    cors_header_value = response.headers.get(cors_header, None)

    assert response.status_code == status_code

    assert (cors_header_value == url) is should_contain_cors_header

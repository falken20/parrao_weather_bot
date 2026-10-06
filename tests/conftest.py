import os

import pytest
import requests

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import db  # noqa: E402
import main  # noqa: E402
import models  # noqa: E402,F401


class FakeTwitterClient:
    def get_me(self):
        return {"data": {"id": "test-user"}}

    def create_tweet(self, text):
        return {"data": {"id": "test-tweet"}}


@pytest.fixture(autouse=True)
def isolate_external_services(monkeypatch):
    def fake_get_auth():
        if not main.ACCESS_TOKEN:
            raise requests.RequestException("Twitter credentials are missing")
        return FakeTwitterClient()

    monkeypatch.setattr(main, "get_auth", fake_get_auth)
    yield
    db.session.rollback()


def pytest_configure():
    db.Base.metadata.create_all(db.engine)

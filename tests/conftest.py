import os

import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db  # noqa: E402
import models  # noqa: E402,F401
import telegram_client  # noqa: E402


class FakeTelegramResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"ok": True, "result": {"message_id": 1}}


@pytest.fixture(autouse=True)
def isolate_external_services(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001234567890")
    monkeypatch.setattr(
        telegram_client.requests,
        "post",
        lambda *args, **kwargs: FakeTelegramResponse(),
    )
    yield
    db.session.rollback()


def pytest_configure():
    db.Base.metadata.create_all(db.engine)

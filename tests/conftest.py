import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    engine = create_engine("sqlite:///:memory:")
    db.Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    monkeypatch.setattr(db, "engine", engine)
    monkeypatch.setattr(db, "Session", session_factory)
    monkeypatch.setattr(db, "session", session)
    try:
        yield
    finally:
        session.rollback()
        session.close()
        engine.dispose()

import pytest
from src.config import Config
from pydantic import ValidationError


@pytest.mark.parametrize(
    ("url", "username", "password"),
    [
        ("http://localhost:420/send_sms", "user1", "1234567890"),
        ("http://localhost:80/send_sms", "mc", ""),
        ("http://localhost:420/send_sms", "", ""),
    ],
)
def test_init_config(url, username, password):
    config = Config(url=url, username=username, password=password)
    assert config.url == url
    assert config.username == username
    assert config.password.get_secret_value() == password

@pytest.mark.parametrize(
    ("url"),
    [
        ("invalid_url"),
        ("http://localhost:420/send"),
        ("http://localhost:420/"),
        ("http://localhost:420"),
        ("http://localhost/send_sms"),
        ("localhost:420/send_sms"),
        ("http://:420/send_sms"),
    ]
)
def test_invalid_url(url):
    with pytest.raises(ValidationError):
        Config(url=url, username="user", password="secret")

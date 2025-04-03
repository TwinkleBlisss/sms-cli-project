import pytest
from src.sender import Sender

@pytest.mark.parametrize(
    ("sender", "recepient", "message"),
    [
        ("123", "456", "Hi!"),
        ("+345879643123", "+546079456", "Hi! Как у тебя дела?"),
        ("090998", "12356", "1+5=6-2*2+2^2"),
    ],
)
def test_send_sms(sender, recepient, message):
    status, body = Sender(sender, recepient, message).send_sms()
    assert status == "HTTP/1.1 200 OK"
    assert body == '{"status":"success","message_id":"123456"}'
    
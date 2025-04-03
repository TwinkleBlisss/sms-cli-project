from src.http_classes import HttpRequest, PostHttpRequest, HttpResponse

def test_http_request():
    request = HttpRequest("POST", "/send_sms", {"Content-Type": "application/json"}, '{"msg": "hello"}')
    assert b"POST /send_sms HTTP/1.1" in request.to_bytes()

def test_post_http_request():
    request = PostHttpRequest("123", "456", "Hello", "http://localhost:420/send_sms", "user", "pass")
    assert request.method == "POST"
    assert "Authorization" in request.headers
    assert request.headers["Authorization"].startswith("Basic")

def test_http_response():
    response_data = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"
    response = HttpResponse.from_bytes(response_data)
    assert response.status_line == "HTTP/1.1 200 OK"
    assert response.body == '{"status": "success"}'

import base64

class HttpRequest:
    """
    Класс, реализующий HTTP-запрос.
    """

    def __init__(self, method: str, path: str, headers: dict, body: str):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
    
    def to_bytes(self) -> bytes:
        """
        Cоздает бинарный HTTP-запрос из данных, сохранённых в экземпляре класса.
        """
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        
        # .encode('cp1251') - из-за проблем с кириллицей
        return (request_line + headers + "\r\n" + self.body).encode('cp1251')

class PostHttpRequest(HttpRequest):
    """
    Класс для создания POST-запроса к API отправки SMS.
    """
    def __init__(
            self, sender: str, recipient: str, message: str, 
            url: str, username: str, password: str
        ):
        host_port, path = url.replace("http://", "").split("/")
        host, port = host_port.split(":")
        
        body = self._create_sms_body(sender, recipient, message)
        headers = {
            "Host": host,
            "Content-Type": "application/json",
            "Authorization": self._create_auth_header(username, password),
            "Content-Length": str(len(body))
        }
        self.host = host
        self.port = port
        super().__init__("POST", f"/{path}", headers, body)

    @staticmethod
    def _create_auth_header(username: str, password: str) -> str:
        auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return f"Basic {auth_token}"

    @staticmethod
    def _create_sms_body(sender: str, recipient: str, message: str) -> str:
        return f'{{"sender": "{sender}", "recipient": "{recipient}", "message": "{message}"}}'


class HttpResponse:
    """
    Класс, реализующий HTTP-ответ.
    """
    def __init__(self, status_line: str, headers: dict, body: str):
        self.status_line = status_line
        self.headers = headers
        self.body = body
    
    @classmethod
    def from_bytes(cls, binary_data: bytes):
        """
        Метод класса, преобразующий последовательность 
        байт в объект HTTP-ответа.
        """
        data = binary_data.decode()
        lines = data.split("\r\n")
        status_line = lines[0]
        headers = {}
        body_index = 0

        for i, line in enumerate(lines[1:]):
            if line == "":
                body_index = i + 2
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        
        body = "\r\n".join(lines[body_index:])
        return cls(status_line, headers, body)

import socket
import logging

from src.config import config
from src.http_classes import PostHttpRequest, HttpResponse

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(message)s", 
    filename="sms_client.log"
)

class Sender:
    """
    Класс для создания запроса и его отправки.
    """
    def __init__(self, sender: str, recipient: str, message: str):
        self.request = PostHttpRequest(
            sender, recipient, message,
            config.api.url, config.api.username,
            config.api.password.get_secret_value()
        )

    def _send_http_request(self):
        with socket.create_connection((self.request.host, self.request.port)) as sock:
            sock.sendall(self.request.to_bytes())

            print("REQUEST", self.request.to_bytes())

            response_data = sock.recv(4096)
        return HttpResponse.from_bytes(response_data)

    def send_sms(self) -> tuple[str, str]:
        """
        Функция отправляет Http-запрос, а затем получает Http-ответ.
        """
        response = self._send_http_request()
        logging.info(f"Response: {response.status_line} {response.body}")
        return response.status_line, response.body

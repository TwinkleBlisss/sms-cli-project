import argparse
import logging
from src.sender import Sender

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(message)s", 
    filename="sms_client.log"
)


def main():
    parser = argparse.ArgumentParser(description="SMS Client CLI")
    parser.add_argument("sender", help="Sender phone number")
    parser.add_argument("recipient", help="Recipient phone number")
    parser.add_argument("message", help="Message text")

    args = parser.parse_args()

    logging.info(f"Parsed args: {args}")

    status, body = Sender(args.sender, args.recipient, args.message).send_sms()
    print("Код ответа:", status)
    print("Тело ответа:", body)


if __name__ == "__main__":
    main()

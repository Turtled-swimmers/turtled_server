from typing import List

from firebase_admin import credentials, initialize_app, messaging
from firebase_admin.exceptions import FirebaseError

from turtled_backend.config.config import Config
from turtled_backend.config.log import logger


class FirebaseCloudMessageService:
    def __init__(self) -> None:
        self.cred = credentials.Certificate(Config.MESSAGING_CREDENTIAL_PATH)

    def init(self):
        initialize_app(self.cred)

    def send(self, title: str, body: str, tokens: List[str]) -> messaging.BatchResponse:
        notification = messaging.Notification(title=title, body=body)

        message = messaging.MulticastMessage(tokens=tokens, notification=notification)
        try:
            batch_response = messaging.send_each_for_multicast(message, dry_run=True)
            logger.info(f"sent message to {batch_response.success_count} device(s)")
            return batch_response
        except (FirebaseError, ValueError) as err:
            logger.exception("exception occur when sending message using firebase admin sdk")


firebase_manager = FirebaseCloudMessageService()

from fbchat import Client, log
from fbchat.models import *
import os
from os.path import join, dirname
from dotenv import load_dotenv


class myBot(Client):
    def onMessage(
            self,
            author_id=None,
            message_object=None,
            thread_id=None,
            thread_type=ThreadType.USER,
            **kwargs
    ):
        self.markAsRead(author_id)

        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
        msgText = message_object.text

        reply = "Busy right now.. Please contact him through other social media." \
                "\n- BOT"

        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

        self.markAsDelivered(author_id, thread_id)


# replace the email and password
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("PASS")
client = myBot(EMAIL, PASS)
client.listen()

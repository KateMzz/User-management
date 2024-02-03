import json
from datetime import datetime

import aio_pika

from settings import settings
from utils.logconf import logger


async def publish_reset_password_message(email):
    connection = await aio_pika.connect_robust(
        settings.RABBIT_MQ,
    )
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue("reset-password-stream")
        message = {
            "email": email,
            "subject": "Reset Password",
            "body": "Click the link to reset your password.",
            "publish_datetime": str(datetime.now()),
        }

        # Convert the message to JSON
        message_json = json.dumps(message)

        # Publish the message to the queue
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_json.encode()), routing_key="reset-password-stream"
        )
        logger.info("message sent to '%s'", email)

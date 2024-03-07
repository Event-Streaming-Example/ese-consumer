import pika
import json

from components.mailer.configs import MailerViewConfig, Mail

def send_email(config:MailerViewConfig, mail: Mail):
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.queue_url))
    channel = connection.channel()

    message = json.dumps(mail.to_json())

    channel.queue_declare(queue=config.channel)
    channel.basic_publish(
        exchange="",
        routing_key=config.channel,
        body=message
    )
    connection.close()
from confluent_kafka import Producer
import json
import time

def config_producer():
    # CONFIG SERVER AND SETTINGS
    config = {
        'bootstrap.servers': 'kafka_host:9093'
    }

    # CREATE INSTANCE OF PRODUCER
    producer = Producer(config)
    return producer


# MANAGE THE DELIVERY MESSAGES
def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()} [{msg.partition()}]')


def create_message(signature_user_vote, uuid):
    # CREATE MESSAGE
  
    message_value = signature_user_vote

    key = uuid
    topic = 'vote_passthrough'
    return topic, key, message_value


async def send_to_kafka(signature_user_vote, uuid):
    producer = config_producer()
    topic, key, message_value = create_message(signature_user_vote, uuid)

    # SEND THE MESSAGE
    producer.produce(topic, key=key, value=message_value, callback=delivery_report)

    # WAIT UNTIL ALL THE MESSAGES ARRIVES
    producer.flush() 
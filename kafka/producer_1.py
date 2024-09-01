from confluent_kafka import Producer
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CONFIG SERVER AND SETTINGS
def config_producer():
    try:
        config = {
            'bootstrap.servers': 'kafka_host:9093'
        }

        # CREATE INSTANCE OF PRODUCER
        producer = Producer(config)
        return producer
    except Exception as e:
        logger.error(f'Error: failed in the configuration of the kafka broker - {str(e)}')
        raise e


# MANAGE THE DELIVERY MESSAGES
def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()} [{msg.partition()}]')


# CREATE MESSAGE
def create_message(signature_user_vote, uuid):
    try:
        if not isinstance(signature_user_vote, bytes) or not isinstance(uuid, str):
            logger.error(f'Error: The signature must be in bytes and uui in string format')
            raise TypeError
        
        message_value = signature_user_vote
        key = uuid
        topic = 'vote_passthrough'

        return topic, key, message_value
    except Exception as e:
        logger.error(f'Error: The message could not created - {str(e)}')
        raise e


# INIT THE PRODUCER
async def send_to_kafka(signature_user_vote, uuid):
    try:
        producer = config_producer()
        topic, key, message_value = create_message(signature_user_vote, uuid)

        # SEND THE MESSAGE
        producer.produce(topic, key=key, value=message_value, callback=delivery_report)

        # WAIT UNTIL ALL THE MESSAGES ARRIVES
        producer.flush() 
    except Exception as e:
        logger.error(f'Error: To send the message to kafka producer - {str(e)}')
        raise e
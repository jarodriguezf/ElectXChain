from confluent_kafka import Consumer, KafkaError
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CONFIGURATION
def config_consumer():
    try:
        config = {
            'bootstrap.servers': 'kafka_host:9093',
            'group.id': 'vote_consumer_group', 
            'auto.offset.reset': 'earliest',    
            'enable.auto.commit': False         
        }

        consumer = Consumer(config)
        return consumer
    except Exception as e:
        logger.error(f'Error: In the configuration of consumer: {str(e)}')
        raise e


# INIT THE CONSUMER
def consume_messages():
    try:
        consumer = config_consumer()
        topic = 'vote_passthrough'
        
        # SUBSCRIBE TO THE TOPIC
        consumer.subscribe([topic])
        logger.info(f"getting messages for topic: {topic}")

        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # END OF THE PARTITION
                    logger.info(f"End of the partition: {msg.partition()}")
                else:
                    logger.error(f"Error: In the consumition of the partition: {msg.error()}")
                continue
            
            # PASS THE KEY AS STRING AND THE MESSAGE AS BYTES (DEFAULT)
            key = msg.key().decode('utf-8') if msg.key() else None
            value = msg.value()

            # SHOW THE KEY AND THE MESSAGE
            logger.info(f"Message received correctly")
            logger.debug(f"Message: key={key}, value={value}")

    except Exception as e:
        logger.error(f'Error: In the consumition of the messages: {str(e)}')
    finally:
        consumer.close()


if __name__ == "__main__":
    consume_messages()

const { Kafka } = require('kafkajs');
const logger = require('pino')({ level: 'debug' });

// CONFIG SERVER AND SETTINGS
async function configProducer() {
    try {
        const kafka = new Kafka({
            clientId: 'producer_2',
            brokers: ['kafka_host:9093'],
            producer: {
                maxMessageSize: 1048576
            }
        });

        const producer = kafka.producer();
        await producer.connect();
        return producer;
    } catch (error) {
        logger.error(`Error: failed in the configuration of the kafka broker - ${error.message}`);
        throw error;
    }
}

// MANAGE THE DELIVERY MESSAGES
function deliveryReport(err, topic, partition) {
    if (err) {
        logger.error(`Error to send the message: ${err.message}`);
    } else {
        logger.info(`Message sent in ${topic} : [${partition}]`);
    }
}

// CREATE MESSAGE
function createMessage(key, value) {
    try {
        if (typeof key !== 'string' || !Buffer.isBuffer(value)) {
            logger.error('Error: The value and the key must be in bytes and string fotmat');
            throw new TypeError('The value and the key must be in bytes and string fotmat');
        }

        const message = {
            topic: 'vote_result',
            messages: [
                { key, value }
            ]
        };

        return message;
    } catch (error) {
        logger.error(`Error: The message could not be created - ${error.message}`);
        throw error;
    }
}

// INIT THE PRODUCER
async function sendToKafka(key, value) {
    try {
       // console.debug(`Size of value before sending kafka topic_2: ${value.length} bytes`);
        const producer = await configProducer();
        const message = createMessage(key, value);

        // SEND THE MESSAGE
        const recordMetadata = await producer.send(message);

        recordMetadata.forEach(({ topic, partition, offset }) => {
            deliveryReport(null, topic, partition, offset);
        });

        // DISCONNECT THE PRODUCER AFTER FLUSHING
        await producer.disconnect();
    } catch (error) {
        logger.error(`Error: To send the message to kafka producer - ${error.message}`);
        throw error;
    }
}

// EXPORT THE FUNCTION
module.exports = { sendToKafka };

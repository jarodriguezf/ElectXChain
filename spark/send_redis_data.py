import redis
import logging
import binascii

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host='redis_host', port=6379, db=0)

def store_in_redis(df, epoch_id):
    try:
        rows = df.collect()

        for row in rows:
            key = row['key']
            value = row['value']
            
            if isinstance(value, bytearray):
                value = bytes(value)

            #original_length = len(value)
            #logger.debug(f"Original length of value (key: {key}): {original_length}")

            redis_client.set(key, value)

            # VERIFY THE LEN OF THE VALUE 
            # stored_value = redis_client.get(key)
            # if stored_value:
            #     hex_representation = binascii.hexlify(stored_value).decode('ascii')
            #     logger.debug(f"Hexadecimal length representation: {len(hex_representation)}")
            #     logger.debug(f"Hexadecimal representation: {hex_representation}")
        
        logger.info(f'Stored {len(rows)} rows in Redis.')
    except Exception as e:
        logger.error(f'Error: To send the data in redis - {str(e)}')
        raise e
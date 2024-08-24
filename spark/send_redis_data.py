import redis
import json
import logging

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

            redis_client.set(key, value)
        logger.info(f'Stored {len(rows)} rows in Redis.')
    except Exception as e:
        logger.error(f'Error: To send the data in redis - {str(e)}')
        raise e
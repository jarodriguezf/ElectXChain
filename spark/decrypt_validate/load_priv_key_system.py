from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_private_system_key(system_private_key_pem):
    try:
        with open(system_private_key_pem, 'rb') as key_file:
            system_private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
            return system_private_key
    except FileNotFoundError as e:
        logger.error(f'Error: File not found - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'Error: In the process od the key PEM- {str(e)}')
        raise e
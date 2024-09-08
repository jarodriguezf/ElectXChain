import cryptography
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_encryption(encrypted_data, system_private_key_pem, user_public_key_der, original_message):
    try:
        # logger.debug(f'len of the encrypted_data: {len(encrypted_data)}')
        # logger.debug(f'representation of the encrypted_data: {encrypted_data}')
        
        encrypted_aes_key = encrypted_data[:256]
        encrypted_signature = encrypted_data[256:]

        # DECRYPT AES USING THE PRIVATE KEY OS THE SYSTEM
        try:
            aes_key = system_private_key_pem.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise ValueError(f"Error decrypting AES key: {str(e)}")


        # CHECK THE LENGTH OF THE AES KEY
        if len(aes_key) != 32:  # 256 bits = 32 bytes
            raise ValueError("Decrypted AES key length is incorrect")
        
        # DECRYPT THE SIGN USING THE KEY AES AND THE IV (INITIALIZE VECTOR)
        if len(encrypted_signature) < 16:
            raise ValueError("Encrypted signature is too short to contain IV")

        iv = encrypted_signature[:16]
        encrypted_signature_data = encrypted_signature[16:]

        # VERIFY THE LENGTH OF THE ENCRYPTED SIGNATURE DATA
        if len(encrypted_signature_data) % 16 != 0:  # Check if length is a multiple of block size (16 bytes)
            raise ValueError("Encrypted signature data length is incorrect")

        try:
            cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            signature = decryptor.update(encrypted_signature_data) + decryptor.finalize()
            #logger.debug(f'signature: {signature}')
        except Exception as e:
            raise ValueError(f"Error decrypting signature: {str(e)}")


        # LOAD THE PUBLIC KEY OF THE USER IN DER FORMAT (BINARY)
        try:
            user_public_key = serialization.load_der_public_key(
                user_public_key_der,
                backend=default_backend()
            )
        except Exception as e:
            raise ValueError(f"Error loading user's public key: {str(e)}")


        # CAST THE ORIGINAL MESSAGE INTO BYTES
        if isinstance(original_message, str):
            #logger.debug(f'original hash vote user: {original_message}')
            try:
                original_message_bytes = bytes.fromhex(original_message)
                #logger.debug('Original message is a hexadecimal string converted to bytes.')
            except ValueError as e:
                logger.error(f'Error converting original message to bytes: {e}')
                raise
        elif isinstance(original_message, bytes) and len(original_message) == 32:
            original_message_bytes = original_message
            #logger.debug('Original mesage is a binary format')
        else:
            raise TypeError("Original message must be a string or bytes")


        # VERIFY THE MESSAGE USING THE PUBLIC KEY OS THE USER AND THE ORIGINAL MESSAGE
        try:
            user_public_key.verify(
                signature,
                original_message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            logger.info('Signature Successfully validated')
            return True
        except cryptography.exceptions.InvalidSignature as e:
            logger.error(f"Signature is invalid - {str(e)}")
            raise ValueError(f"Signature is invalid - {str(e)}")
        except Exception as e:
            logger.error(f"Error verifying the signature: {str(e)}")
            raise ValueError(f"Error verifying the signature: {str(e)}")
        
    except (ValueError, TypeError, cryptography.exceptions.InvalidSignature) as e:
        logger.error(f'Signature validation failed: {str(e)}')
    except Exception as e:
        logger.error(f'Error: Processing of validation failed - {str(e)}')
    return False
    

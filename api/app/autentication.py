import time
import pyotp
import os
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def manager_key():
    key = os.getenv('MANAGER_KEY_OTP', 'default_key')
    if key == 'default_key':
        logger.error('Error: The manager key is not configured')
        return
    return key

def topt_instance(key, digits=6, interval=120):
    return pyotp.TOTP(key, digits=6, interval=120)
    

# RETURN THE 2FA TOKEN
def get_token() -> str:
    key = manager_key()
    if not key:
        raise Exception('Error: Cant generated the OTP code.')
    totp = topt_instance(key, digits=6, interval=120)
    return totp.now()

    
# VALIDATE THE CODE 2FA
def validate_token(input_token: str) -> bool:
    key = manager_key()
    if not key:
        raise Exception('Error: Cant validated the OTP code.')
    
    totp = topt_instance(key, digits=6, interval=120)
    if not totp.verify(input_token):
        logger.error('Error: In the verification of the code') 
        return False
    logger.info('Code successfully verified')
    return True

import os
from dotenv import load_dotenv
from utils.Logger import logger

load_dotenv(encoding="ascii")



secret_key = os.getenv('SECRET_KEY', None)
authorization = os.getenv('AUTHORIZATION', False)
domain_chatgpt = os.getenv('DOMAIN_CHATGPT', '')



logger.info("-" * 60)
logger.info(f"Chat-Share | https://github.com/h88782481/Chat-Share")
logger.info("-" * 60)
logger.info("Environment variables:")
logger.info("SECRET_KEY:        " + str(secret_key))
logger.info("AUTHORIZATION:     " + str(authorization))
logger.info("DOMAIN_CHATGPT:          " + str(domain_chatgpt))
logger.info("-" * 60)

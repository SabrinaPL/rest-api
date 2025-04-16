from loguru import logger
import sys
import os

# Remove default logging handler
logger.remove()

# Configure Loguru
logger.add(
    sys.stdout,  # Print logs to the console
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO",
    enqueue=True,
)

# Ensure the logs directory exists
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logger.add(
    "logs/app.log",  # Log to a file
    rotation="7 days",  # Automatically rotate logs
    retention="10 days",  # Keep logs for 10 days
    compression="zip",  # Compress old logs
    level="INFO",
    enqueue=True,
)

def get_logger():
    return logger

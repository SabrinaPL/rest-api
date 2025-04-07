"""
Configuration for MongoEngine.
"""
import logging
from mongoengine import connect

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def connect_to_database(mongo_uri):
    """
    Establishes a connection to the MongoDB database using MongoEngine.
    """
    try:
        connect(host=mongo_uri)
        logger.info("MongoEngine connected to MongoDB.")
    except Exception as e:
        logger.error(f"MongoEngine connection error: {e}")
        raise

# Handle process exit signals
import signal
import sys

def close_connection(signal_received, frame):
    """
    Closes the MongoDB connection when the app is shutting down.
    """
    logger.info(f"MongoEngine disconnected from MongoDB due to {signal.strsignal(signal_received)}.")
    sys.exit(0)

for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, close_connection)

import logging

def setup_logging():
    logging.basicConfig(
        filename='/home/pi/pump.log',  # Log file location
        level=logging.INFO,            # Minimum logging level
        format='%(asctime)s %(levelname)s: %(message)s'  # Log format
    )
import logging
import os
from datetime import datetime

# Create a unique log file name based on current datetime
LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

# Create logs directory if it doesn't exist
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

# Full path for the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)
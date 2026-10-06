import logging
import json
import os

def setup_logger(config_path="config/config.json"):
    log_file = "logs/app.log"
    log_level = logging.INFO

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                log_file = config.get("log_file_path", log_file)
                level_str = config.get("log_level", "INFO").upper()
                log_level = getattr(logging, level_str, logging.INFO)
        except Exception as e:
            print(f"Failed to load logging config: {e}")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("SIS_Logger")
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()
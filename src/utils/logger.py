import logging
import os
from datetime import datetime


def get_logger():

    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    log_dir = os.path.join(
        os.getcwd(),
        "logs"
    )

    os.makedirs(
        log_dir,
        exist_ok=True
    )

    log_file_path = os.path.join(
        log_dir,
        log_file
    )

    logging.basicConfig(
        level=logging.INFO,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                log_file_path,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("EduGenie")
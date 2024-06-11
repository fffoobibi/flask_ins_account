import logging
import os
from pathlib import Path

__all__ = ("logger",)

log_path = Path(__file__).parent.joinpath("./logs")
if not log_path.exists():
    log_path.mkdir(parents=True)

log_level = os.environ.get("DEBUG", "DEBUG")
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

formater = logging.Formatter(
    "%(asctime)s - [P: %(process)d, T: %(threadName)s] %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)
file_handler = logging.FileHandler(
    "./logs/app.log",
    encoding="utf8",
)
file_handler.setLevel(log_level)
file_handler.setFormatter(formater)
logger.addHandler(file_handler)

st_handler = logging.StreamHandler()
st_handler.setLevel(log_level)
st_handler.setFormatter(formater)
logger.addHandler(st_handler)

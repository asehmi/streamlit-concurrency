import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s - %(funcName)s: %(message)s",
    # datefmt="%Y-%m-%d %H:%M:%S",
)

for info_loggers in ["asyncio", "streamlit"]:
    logging.getLogger(info_loggers).setLevel(logging.INFO)

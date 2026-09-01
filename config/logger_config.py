import logging
import sys

try:
    from loguru import logger
except ImportError:
    # Fallback standard library logging with loguru-like interface
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s"
    )
    logger = logging.getLogger("pipecat_hexagonal")

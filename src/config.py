import os
import sys
import logging

logger = logging.getLogger(__name__)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        logger.error(f"Missing required: {name}")
        sys.exit(1)
    return value


FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key-change-in-prod")
PORT = int(os.getenv("PORT", "5000"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bp_helper.db")

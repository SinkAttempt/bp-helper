import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

from flask import Flask
from src.config import FLASK_SECRET_KEY, PORT
from src.database import init_db
from src.routes import bp

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.register_blueprint(bp)

init_db()

if __name__ == "__main__":
    logger.info(f"STARTUP BP Helper on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)

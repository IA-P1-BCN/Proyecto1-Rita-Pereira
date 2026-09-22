import logging
import os

def configurar_logger():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/taximetro.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger("taximetro")
from local_llama.settings import Settings
import logging


logger = logging.getLogger(__name__)
if not logger.hasHandlers():  # do only once
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)  # works downstream to all subpackages


settings = Settings()

if not settings.save_folder.exists():
    settings.save_folder.mkdir()

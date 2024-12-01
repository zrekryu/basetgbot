from dataclasses import dataclass
import logging
import os
import textwrap

from dotenv import load_dotenv

from .metadata import (
    __author__,
    __version__
    )

load_dotenv()

@dataclass
class Config:
    INTRO_STRING: str = textwrap.dedent(
        f"""\
        Base Telegram Bot - Version {__version__}.
        Author: {__author__}.
        """
        )
    
    CLIENT_NAME: str = os.getenv("CLIENT_NAME", "tgbot")
    API_ID: int = int(os.getenv("API_ID"))
    API_HASH: str = os.getenv("API_HASH")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    
    LOG_LEVEL: int = int(os.getenv("LOG_LEVEL", logging.INFO))
    LOG_FILE: str = os.getenv("LOG_FILE", "tgbot.log")
    LOG_FILE_MODE: str = os.getenv("LOG_FILE_MODE", "w+")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s")
    LOG_DATEFMT: str = os.getenv("LOG_DATEFMT", "%y/%m/%d %H:%M:%S")
    
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DBNAME: str = os.getenv("MONGO_DBNAME", "tgbot")
    
    STRICT_CMD_PY_SUFFIX: bool = True
import asyncio
import logging
from typing import Self

from .bot import Bot
from .config import Config
from .mongodb import mongo_client

class Runner:
    def __init__(self: Self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self.loop = loop
        
        self.bot: Bot = Bot(
            name=Config.CLIENT_NAME,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            strict_cmd_py_suffix=Config.STRICT_CMD_PY_SUFFIX
            )
        
        self.setup_logger()
    
    def get_logger(self: Self) -> logging.Logger:
        logger: logging.Logger = logging.getLogger(Config.LOGGER_NAME)
        logger.setLevel(Config.LOG_LEVEL)
        
        logger.propagate = False
        
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        file_handler: logging.FileHandler = logging.FileHandler(filename=Config.LOG_FILE, mode=Config.LOG_FILE_MODE)
        
        formatter = logging.Formatter(Config.LOG_FORMAT, datefmt=Config.LOG_DATEFMT)
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        return logger
    
    def setup_logger(self: Self) -> None:
        self.get_logger()
    
    async def setup_mongodb(self: Self) -> None:
        await mongo_client.setup()
    
    def print_intro(self: Self) -> None:
        print(Config.INTRO_STRING)
    
    async def run_bot(self: Self) -> None:
        await self.setup_mongodb()
        
        self.bot.import_commands()
        
        await self.bot.start()
        
        await self.bot.idle()
        
        await self.bot.stop()
    
    def run_bot_in_loop(self: Self, loop: asyncio.AbstractEventLoop) -> None:
        try:
            loop.run_until_complete(self.run_bot())
        finally:
            loop.close()
    
    @staticmethod
    def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
        loop: asyncio.AbstractEventLoop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop
    
    def run(self: Self) -> None:
        if self.loop:
            self.run_bot_in_loop(self.loop)
        else:
            self.run_bot_in_loop(self.get_or_create_event_loop())

def run(loop: asyncio.AbstractEventLoop | None = None) -> None:
    runner: Runner = Runner(loop=loop)
    runner.print_intro()
    
    runner.run()
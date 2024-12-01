import asyncio
import logging
from typing import Self

from .bot import Bot
from .config import Config

class Runner:
    def __init__(self: Self, config: Config, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self.config = config
        self.loop = loop
        
        self.bot: Bot = Bot(
            name=self.config.CLIENT_NAME,
            api_id=self.config.API_ID,
            api_hash=self.config.API_HASH,
            bot_token=self.config.BOT_TOKEN,
            strict_cmd_py_suffix=self.config.STRICT_CMD_PY_SUFFIX
            )
        
        self.setup_logger()
    
    def get_logger(self: Self) -> logging.Logger:
        logger: logging.Logger = logging.getLogger("tgbot")
        logger.setLevel(self.config.LOG_LEVEL)
        
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        file_handler: logging.FileHandler = logging.FileHandler(filename=self.config.LOG_FILE, mode=self.config.LOG_FILE_MODE)
        
        formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(name)s - %(message)s", datefmt="%d/%m/%y %H:%M:%S")
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        return logger
    
    def setup_logger(self: Self) -> None:
        self.get_logger()
    
    def print_intro(self: Self) -> None:
        print(self.config.INTRO_STRING)
    
    async def run_bot(self: Self) -> None:
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

def run(config: Config = Config, loop: asyncio.AbstractEventLoop | None = None) -> None:
    runner: Runner = Runner(config=config, loop=loop)
    runner.print_intro()
    
    runner.run()
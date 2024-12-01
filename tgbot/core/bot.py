import logging
import importlib
import os
from types import ModuleType
from typing import Self

from pyrogram.handlers.handler import Handler
from pyrogram.handlers import (
    MessageHandler
    )
from pyrogram import Client, idle

logger: logging.Logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(
        self: Self,
        name: str,
        api_id: int,
        api_hash: str,
        bot_token: str,
        strict_cmd_py_suffix: bool
        ) -> None:
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.strict_cmd_py_suffix = strict_cmd_py_suffix
        
        super().__init__(
            name=self.name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token
            )
    
    async def start(self: Self) -> None:
        logger.info("Bot is starting...")
        await super().start()
        logger.info("Bot has been started!")
    
    async def stop(self: Self) -> None:
        logger.info("Bot is stopping...")
        await super().stop()
        logger.info("Bot stopped!")
    
    async def idle(self: Self) -> None:
        logger.info("Bot is idling...")
        await idle()
    
    def add_message_handler(self: Self, message_handler: MessageHandler) -> None:
        super().add_handler(message_handler)
    
    def import_command(self: Self, name: str) -> tuple[ModuleType, str, Handler] | None:
        module: ModuleType = importlib.import_module(name)
        
        try:
            command_name: Handler = module.command_name
        except AttributeError:
            raise AttributeError(f"Command module '{file}' has no attribute 'command_name'")
        
        try:
            command_handler: Handler = module.command_handler
        except AttributeError:
            raise AttributeError(f"Command module '{file}' has no attribute 'command_handler'")
        
        if isinstance(command_handler, MessageHandler):
            self.add_message_handler(command_handler)
        else:
            super().add_handler(command_handler)
        
        return module, command_name, command_handler
    
    def import_commands(self: Self) -> None:
        logger.info("Importing commands...")
        for file in os.listdir(os.path.join(os.path.dirname(__file__), "commands")):
            if file.startswith("__") or not file.endswith(".py"):
                continue
            if not file.endswith("_cmd.py") and self.strict_cmd_py_suffix:
                raise ValueError(f"Command file '{file}' does not ends with '_cmd.py'")
            
            name: str = f"{__name__[:-3]}commands.{file[:-3]}"
            
            module: ModuleType
            command_name: str
            command_handler: Handler
            module, command_name, command_handler = self.import_command(name)
            
            logger.debug(f"Imported command: {command_name}")
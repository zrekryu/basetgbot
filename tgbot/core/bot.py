import importlib
import logging
from pathlib import Path
from types import ModuleType
from typing import Self

from pyrogram.filters import Filter
from pyrogram.handlers.handler import Handler
from pyrogram.handlers import (
    MessageHandler,
    CallbackQueryHandler
    )
from pyrogram import Client, idle

from .registers import (
    CommandRegister,
    CallbackQueryRegister
    )

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
        logger.info("Bot has stopped idling!")
    
    @staticmethod
    def command_register(name: str, filters: Filter, group: int = 0) -> CommandRegister:
        return CommandRegister.as_decorator(name, filters, group)
    
    def import_commands(self: Self) -> None:
        logger.info("Importing commands...")
        commands_dir: Path = Path(__file__).parent / "commands"
        imported_commands: list[tuple[ModuleType, CommandRegister]] = self.import_commands_from_path(commands_dir)
        
        imported_command_names: str = ", ".join(
            cmd_reg.name for _, cmd_regs in imported_commands
            for cmd_reg in cmd_regs
            )
        logger.info(f"Imported command names: {imported_command_names}.")
    
    def import_commands_from_path(self: Self, path: Path) -> list[tuple[ModuleType, CommandRegister]]:
        imported_commands: list[tuple[ModuleType, CommandRegister]] = []
        for file in path.iterdir():
            if file.name.startswith("__") or file.suffix != ".py":
                continue
            if file.is_dir():
                imported_commands.extend(
                    self.import_commands_from_path(file)
                    )
                continue
            if not file.name.endswith("_cmd.py") and self.strict_cmd_py_suffix:
                raise ValueError(f"Command file '{file.name}' does not ends with '_cmd.py'")
            
            logger.debug(f"Importing command file: {file.name}.")
            
            name: str = f"{__name__[:-3]}commands.{file.stem}"
            
            module: ModuleType
            registers: list[CommandRegister]
            module, registers = self.import_command_registers_from_module(name)
            
            logger.debug(f"Imported command file: {file.name}.")
            
            self.add_command_registers(registers)
            imported_commands.append((module, registers))
        
        return imported_commands
    
    def import_command_registers_from_module(self: Self, name: str) -> tuple[ModuleType, list[CommandRegister]]:
        module: ModuleType = importlib.import_module(name)
        registers: list[CommandRegister] = []
        
        # Import command registers from list.
        if hasattr(module, "registers"):
            for register in module.registers:
                if not isinstance(register, CommandRegister):
                    raise TypeError(f"Command register '{register}' must be an instance of CommandRegister")
                
                registers.append(register)
        
        # Find and import command registers from module.
        for value in vars(module).values():
            if isinstance(value, CommandRegister):
                registers.append(value)
        
        if not registers:
            raise RuntimeError(f"Command module '{name}' does not define any registers")
        
        return (module, registers)
    
    def add_command_registers(self: Self, registers: list[CommandRegister]) -> None:
        for register in registers:
            if not isinstance(register, CommandRegister):
                raise TypeError(f"Command register '{register}' must be an instance of CommandRegister")
            
            self.add_message_handler(register.handler, register.group)
    
    def add_callback_query_registers(self: Self, registers: list[CommandRegister]) -> None:
        for register in registers:
            if not isinstance(register, CommandRegister):
                raise TypeError(f"CallbackQuery register '{register}' must be an instance of CallbackQueryRegister")
            
            self.add_callback_query_handler(register.handler, self.group)
    
    def add_message_handler(self: Self, handler: MessageHandler, group: int = 0) -> None:
        super().add_handler(handler, group)
    
    def add_callback_query_handler(self: Self, handler: CallbackQueryHandler, group: int = 0) -> None:
        super().add_handler(handler, group)
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters

from ..bot import Bot

async def on_start_command(_: Bot, message: Message) -> None:
    await message.reply("Hello, there!")

command_name: str = "START"
command_handler: MessageHandler = MessageHandler(
    callback=on_start_command,
    filters=filters.command("start")
)

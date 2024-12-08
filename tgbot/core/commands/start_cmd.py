from pyrogram.types import Message
from pyrogram import filters

from ..bot import Bot

@Bot.command_register(
    name="START",
    filters=filters.command("start")
    )
async def on_start_command(bot: Bot, message: Message) -> None:
    if message.from_user:
        await message.reply(f"Hello, {message.from_user.first_name}!")
    else:
        await message.reply("Hello there!")
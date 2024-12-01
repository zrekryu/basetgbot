import time

from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters

from ..bot import Bot

async def on_ping_command(_: Bot, message: Message) -> None:
    start_time = time.perf_counter()
    pong_msg: Message = await message.reply("Pong!")
    end_time = time.perf_counter()
    
    latency_ms = (end_time - start_time) * 1000
    await pong_msg.edit(f"Pong! `{latency_ms:.3f}` ms".format(latency_ms=latency_ms))

command_name: str = "PING"
command_handler: MessageHandler = MessageHandler(
    callback=on_ping_command,
    filters=filters.command("ping")
    )
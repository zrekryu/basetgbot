from typing import Any, Callable, Self

from pyrogram.filters import Filter
from pyrogram.handlers import MessageHandler

class CallbackQueryRegister:
    def __init__(
        self: Self,
        name: str,
        filters: Filter,
        callback: Callable[[Any], Any]
        ) -> None:
        self.name = name
        self.filters = filters
        self.callback = callback
    
    def get_handler(self: Self) -> MessageHandler:
        return CallbackQueryHandler(
            filters=self.filters,
            callback=self.callback
            )
    
    def __repr__(self: Self) -> str:
        return (
            "CallbackQueryRegister("
            f"name={self.name}"
            f"filters={self.filters}"
            f"callback={self.callback}"
            ")"
            )
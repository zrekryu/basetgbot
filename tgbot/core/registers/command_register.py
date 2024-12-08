from typing import Callable, Self

from pyrogram.filters import Filter
from pyrogram.handlers import MessageHandler

class CommandRegister:
    def __init__(
        self: Self,
        name: str,
        callback: Callable,
        filters: Filter,
        group: int = 0
        ) -> None:
        self.name = name
        self.callback = callback
        self.filters = filters
        self.group = group
    
    @classmethod
    def as_decorator(cls: type[Self], name: str, filters: Filter, group: int = 0) -> Callable:
        def decorator(func: Callable) -> Self:
            return cls(name, func, filters, group)
        
        return decorator
    
    @property
    def handler(self: Self) -> MessageHandler:
        return MessageHandler(
            callback=self.callback,
            filters=self.filters
            )
    
    def __repr__(self: Self) -> str:
        return (
            "CommandRegister("
            f"name={self.name}, "
            f"callback={self.callback}, "
            f"filters={self.filters}, "
            f"group={self.group}"
            ")"
            )
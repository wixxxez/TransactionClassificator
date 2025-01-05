from typing import Any, Awaitable, Callable, Dict
from aiogram import types
from aiogram  import BaseMiddleware
from aiogram.types import Message
from ...utils.ConfigLoader import load_config

class WhiteListMiddleware(BaseMiddleware):
 
    def __init__(self, cfg) -> None:
            self.config = cfg

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
        ) -> Any:
            id = event.from_user.id
            if self.is_user_banned(id):
                await event.reply("You are not allowed to use this bot.")
                return 
            return await handler(event, data)

    def is_user_banned(self, id: int) -> bool:
        # Implement your logic to check if the user is banned
        

        whitelist = self.config['whitelist']
        
        whitelist_users = [id for id in whitelist ]

        return id in whitelist_users
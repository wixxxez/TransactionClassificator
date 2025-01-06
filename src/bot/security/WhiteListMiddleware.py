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
            if self.is_user_not_allowed(id):
                await event.reply(f"You are not allowed to use this bot. ID {id} not in white list. ")
                return 
            return await handler(event, data)

    def is_user_not_allowed(self, id: int) -> bool:


        whitelist = self.config['whitelist']
        
        whitelist_users = [id for id in whitelist ]

        users = [i['id'] for i in whitelist ]
        
       
        return id not in users
from backend import Backend
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from asyncio import sleep
from random import uniform as rand_float
import logging as log


class Response:
    def __init__(self, app: Client, message: Message) -> None:
        self.app = app
        self.message = message

    @property
    async def _process(self) -> None:
        data = await Backend(self.message.text).get
        if data:
            message = self.message
            await self._response(data, message)
        else:
            return

    async def _response(self, data: str, message: Message) -> None or Exception:
        try:
            if self._need_response:
                await self._call_sleep(prepare=True)
                await self.app.mark_chat_unread(message.chat.id)
                await self._call_sleep(prepare=False)
                # actions after sleep
                await self.app.send_chat_action(
                    chat_id=message.chat.id, action=ChatAction.TYPING)
                await sleep(rand_float(2, 5))
                await message.reply(data)
        except Exception as e:
            log.error("Error response. Details: %s" % e)
            return e

    @staticmethod
    async def _call_sleep(prepare: bool) -> sleep:
        return \
            await sleep(rand_float(0, 5) + rand_float(5, 20)
                        if rand_float(0, 1) > 0.95 else 0) \
            if prepare \
            else await sleep(
                rand_float(0, 2) + rand_float(2, 8)
                if rand_float(0, 1) > 0.8 else 0)

    @staticmethod
    def _need_response() -> bool:
        return True if rand_float(0, 1) > 0.7 else False

    @property
    async def begin(self) -> None:
        return await self._process

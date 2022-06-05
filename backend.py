from typing import Coroutine, Any

from aiohttp import ClientSession
import logging as log


class Backend:
    def __init__(self, text: str) -> None:
        self.host = "xu.su"
        self.path = "api/send"

        self.json = {
            "uid": None,
            "bot": "main",
            "text": text
        }

    @property
    async def _request(self) -> Coroutine[dict, Any, Any] or None:
        async with ClientSession() as session:
            try:
                async with session.post(
                        f"https://{self.host}/{self.path}", json=self.json
                ) as response:
                    if response.status >= 200 < 205:
                        log.debug("Success response backend.")
                        return await response.json()
                    else:
                        log.warning(f"Error code backend: {response.status}.\n{'-'*15}\n"
                                    f"Detail response:\n{response.text}")
            except Exception as e:
                log.error("Error send request to backend. Details: %s" % e)

    @staticmethod
    async def _parser(json_body: dict) -> str or None:
        try:
            return json_body["text"] if json_body["ok"] else None
        except Exception as e:
            log.error("Backend json parser error. Details: %s" % e)

    @property
    async def get(self) -> str or None:
        body = await self._request
        return await self._parser(body if body else {})

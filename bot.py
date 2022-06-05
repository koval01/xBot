import logging

from pyrogram import Client, filters
from os import getenv
from response import Response
import logging as log

app = Client(
    "bot_session",
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    phone_number=getenv("PHONE_NUMBER"),
    # in_memory=True
)
log.basicConfig(level=log.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@app.on_message(filters.text & filters.group)
async def main_handler(client, message):
    log.info("Call %s" % main_handler.__name__)
    return await Response(app, message).begin


@app.on_message(filters.text & filters.group & filters.reply)
async def reply_handler(client, message):
    log.info("Call %s" % reply_handler.__name__)
    return await Response(app, message, reply=True).begin


@app.on_message(filters.private & filters.chat(int(getenv("OWNER_ID"))))
async def owner_private_handler(client, message):
    log.info("Call %s" % owner_private_handler.__name__)
    return await Response(app, message, reply=True).begin


logging.info("Starting bot...")
app.run()

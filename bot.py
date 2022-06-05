from pyrogram import Client, filters
from os import getenv
from response import Response

app = Client(
    "bot_session",
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    phone_number=getenv("PHONE_NUMBER"),
    # in_memory=True
)


@app.on_message(filters.text & filters.group)
async def main_handler(client, message):
    return await Response(app, message).begin


@app.on_message(filters.text & filters.group & filters.reply)
async def reply_handler(client, message):
    return await Response(app, message, reply=True).begin

app.run()

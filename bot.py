from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, date
import zoneinfo
from settings import *
import os
import pygsheets

zone = zoneinfo.ZoneInfo("Europe/Moscow")
app = Client("bot", api_id=api_id, api_hash=api_hash)
gc = pygsheets.authorize(service_account_file='sheets_key.json')

ws = gc.open('База писывших людей').worksheet()
@app.on_message()
async def on_new_message(client, message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id == user_id:
        i = 1
        while True:
            if str(ws.cell(f'A{i}').value) == str(chat_id):
                break
            if ws.cell(f'A{i}').value == '':
                ws.cell(f'A{i}').value = chat_id
                ws.cell(f'B{i}').value = message.from_user.first_name
                ws.cell(f'C{i}').value = message.from_user.last_name
                ws.cell(f'D{i}').value = message.from_user.username
                ws.cell(f'E{i}').value = message.from_user.phone_number
                ws.cell(f'F{i}').value = str(datetime.now(zone).date())
                break
            i += 1

app.run()
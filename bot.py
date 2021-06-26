# Made with python3
# (C) @FayasNoushad
# Copyright permission under GNU General Public License v3.0
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Telegraph-Uploader-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file

FayasNoushad = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Hallo {}, Kami akan upload media anda ke telegra.ph link (uploader bot).

- Hanya mengupload media dibawah 5MB (mungkin)
- Kami akan mendownloadnya
- Setelah kami mendownloadnya kami akan mengupload ke telegra.ph link

Made by @s4nyt
"""

# start command
@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=START_TEXT.format(update.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Channel ⚙', url='https://telegram.me/FayasNoushad'), InlineKeyboardButton('⚙ Group ⚙', url='https://telegram.me/FayasChat')]]),
        reply_to_message_id=update.message_id
    )

# Main function
@FayasNoushad.on_message(filters.media & filters.private)
async def getmedia(bot, update):
    medianame = "./DOWNLOADS/" + "FayasNoushad/FnTelegraphBot"
    text = await bot.send_message(
        chat_id=update.chat.id,
        text="<code>Downloading server ...</code>",
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<code>Downloading Selesai. Sekarang kami akan upload ke telegra.ph Link ...</code>"
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True
        )
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @s4nyt",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"), InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}"),],
                                           [InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url="https://telegram.me/s4ncg")]])
    )
    try:
        os.remove(medianame)
    except:
        pass

FayasNoushad.run()

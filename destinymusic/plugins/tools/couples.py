import os 
import random
from datetime import datetime 
from telegraph import upload_file
from PIL import Image, ImageDraw
from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import *

#BOT FILE NAME
from destinymusic import app as app
from destinymusic.mongo.couples_db import _get_image, get_couple

POLICE = [
    [
        InlineKeyboardButton(
            text="ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ  🥀",
            url=f"https://t.me/crush_hu_tera",
        ),
    ],
]


def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list
    

def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a

tomorrow = str(dt_tom())
today = str(dt()[0])

@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")
    try:
        msg = await message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴏᴜᴘʟᴇs ɪᴍᴀɢᴇ...")
        
        # Get list of users
        list_of_users = []
        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        if len(list_of_users) < 2:
            return await msg.edit_text("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴏᴜᴘʟᴇs.")

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        try:
            photo1 = (await app.get_chat(c1_id)).photo
            photo2 = (await app.get_chat(c2_id)).photo
            N1 = (await app.get_users(c1_id)).mention 
            N2 = (await app.get_users(c2_id)).mention
            
            # Download profile photos
            try:
                p1 = await app.download_media(photo1.big_file_id, file_name=f"pfp_{cid}_1.png")
            except Exception:
                p1 = "destinymusic/assets/upic.png"
            try:
                p2 = await app.download_media(photo2.big_file_id, file_name=f"pfp_{cid}_2.png")
            except Exception:
                p2 = "destinymusic/assets/upic.png"
                
            # Process images
            img1 = Image.open(p1)
            img2 = Image.open(p2)
            img = Image.open("destinymusic/assets/cppicbranded.jpg")

            img1 = img1.resize((437,437))
            img2 = img2.resize((437,437))

            # Create circular masks
            mask = Image.new('L', img1.size, 0)
            draw = ImageDraw.Draw(mask) 
            draw.ellipse((0, 0) + img1.size, fill=255)

            mask1 = Image.new('L', img2.size, 0)
            draw = ImageDraw.Draw(mask1) 
            draw.ellipse((0, 0) + img2.size, fill=255)

            img1.putalpha(mask)
            img2.putalpha(mask1)

            draw = ImageDraw.Draw(img)
            img.paste(img1, (116, 160), img1)
            img.paste(img2, (789, 160), img2)

            output_path = f'couple_{cid}.png'
            img.save(output_path)
        
            TXT = f"""
**ᴛᴏᴅᴀʏ's ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ :

{N1} + {N2} = 💚

ɴᴇxᴛ ᴄᴏᴜᴘʟᴇs ᴡɪʟʟ ʙᴇ sᴇʟᴇᴄᴛᴇᴅ ᴏɴ {tomorrow} !!**
"""
            await message.reply_photo(
                output_path,
                caption=TXT,
                reply_markup=InlineKeyboardMarkup(POLICE)
            )
            await msg.delete()

            # Upload to telegraph
            a = upload_file(output_path)
            for x in a:
                img = "https://graph.org/" + x
                couple = {"c1_id": c1_id, "c2_id": c2_id}
                # await save_couple(cid, today, couple, img)

        except Exception as e:
            await msg.edit_text(f"ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ɪᴍᴀɢᴇs: {str(e)}")
            return

    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {str(e)}")
        return

    finally:
        # Cleanup files
        try:
            os.remove(f"pfp_{cid}_1.png")
            os.remove(f"pfp_{cid}_2.png")
            os.remove(f"couple_{cid}.png")
        except Exception:
            pass
         

__mod__ = "COUPLES"
__help__ = """
**» /couples** - Get Todays Couples Of The Group In Interactive View
"""





    




    

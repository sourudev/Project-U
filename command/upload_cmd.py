import discord
import io
import aiohttp
import discord
import hashlib
import random
from util.function import print_in_color,save_uploaded_file_count

async def _upload(ctx, attachment: discord.Attachment,responses,media_content_types,uploaded_file_count):
    await ctx.defer()
    random_msg = random.choice(responses)
    message = await ctx.send("เริ่มกระบวนการขนส่งวิญญาณ..")
    file_data = await attachment.read()
    file_name = f"{attachment.filename}"
    file_type = file_name.split(".")[-1] if "." in file_name else "ไฟล์ปริศนา"
    print_in_color(f"กำลังอัปโหลดไฟล์ {file_name}", "32")
    await message.edit(content="กำลังเข้ารหัสไฟล์")
    hash_value = hashlib.sha256(file_data).hexdigest()
    await message.edit(content=f"การเข้ารหัสของไฟล์: {hash_value}")
    bytes_io = io.BytesIO(file_data)
    await message.edit(content="คำนวนขนาดของไฟล์ ")
    bytes_size = len(bytes_io.getbuffer())
    mb_size = bytes_size / (1024 * 1024)  # Convert bytes to megabytes
    gb_size = mb_size / 1024  # Convert megabytes to gigabytes

    if gb_size >= 1:
        size_text = f"{gb_size:.2f} GB"
    elif mb_size >= 1:
        size_text = f"{mb_size:.2f} MB"
    else:
        size_text = f"{bytes_size} bytes"

    await message.edit(content=f"ขนาดไฟล์: {size_text}")



    file = (file_name, bytes_io)

    try:
        await message.edit(content="กำลังลองอัปโหลดไฟล์...")
        
        data = aiohttp.FormData()
        data.add_field('file', file[1], filename=file[0])
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://0x0.st", data=data) as response:
                if response.status == 200:
                    file_url = await response.text()
                    is_nsfw = "#nsfw" in file_url
                    color = 0xff0000 if is_nsfw else discord.Color.random()
                    footer_text = random_msg if is_nsfw else random_msg
                    description = ""
                    preview_length = 100
                    file_preview = file_data.decode(errors="ignore")[:preview_length]
                 
                     # ...

                    uploaded_file_count += 1
                    if uploaded_file_count % 3 == 0:
                        save_uploaded_file_count(uploaded_file_count)

                    if attachment.content_type not in media_content_types:
                        description = f"```{file_type}\n{file_preview}[...]```"

                    embed = discord.Embed(title="ผลลัพท์", description=description, color=color)
                    embed.add_field(name="การเข้ารหัสของไฟล์ (sha256)", value=hash_value, inline=False)
                    embed.add_field(name="ชื่อไฟล์", value=file_name, inline=True)
                    embed.add_field(name="ประเภทไฟล์", value=file_type, inline=True)
                    embed.add_field(name="ขนาดไฟล์", value=f"{size_text}", inline=True)
                    if is_nsfw:
                        embed.add_field(name="ลิงค์ 0x0 ของไฟล์", value=f"||{file_url}||", inline=False)
                    else:
                        embed.add_field(name="ลิงค์ 0x0 ของไฟล์", value=file_url, inline=True)
                        embed.set_image(url=attachment.url)
                    embed.set_footer(text=footer_text)
                    
                    view = discord.ui.View()
                    view.add_item(discord.ui.Button(label="เปิดไฟล์", url=file_url))
                    view.add_item(discord.ui.Button(label="ตรวจสอบVirus", url=f"https://www.virustotal.com/gui/search/{hash_value}"))
                    await message.edit(content="", embed=embed, view=view)
                else:
                    error_message = await response.text()
                    embed = discord.Embed(title="ผลลัพท์", color=0xff0000)
                    embed.add_field(name="ความผิดพลาดของการอัปโหลด", value=f"```{error_message}```", inline=False)
                    await message.edit(content="", embed=embed)
           
    except Exception as e:
        embed = discord.Embed(title="ขนส่งวิญญาณผิดพลาด", color=0xff0000)
        embed.add_field(name="ความผิดพลาดของการอัปโหลด", value=str(e), inline=False)
        await message.edit(content="", embed=embed)
    return uploaded_file_count   
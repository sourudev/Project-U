import os
import io
import aiohttp
import discord
import hashlib
import random
import json
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Set up the Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=60)
TOKEN = os.getenv('DISCORD_TOKEN')
media_content_types = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'video/mp4',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-matroska'
]

def print_in_color(text, color):
    print(f"\033[{color}m{text}\033[0m")

def load_responses(url):
    response = json.loads(requests.get(url).content)["responses"]
    return response

responses = load_responses(
    "https://raw.githubusercontent.com/sourudev/Project-U/main/fact.JSON"
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(),
        scopes=("bot", "applications.commands")
    )

    os.system('clear' if os.name == 'posix' else 'cls')
    
    print_in_color(f"{bot.user} is ready to upload!", "1;97")
    print_in_color(f"Invite link: {invite_link}", "1;36")

@bot.hybrid_command(name="upload", description="อัปโหลดไฟล์")
async def upload(ctx, attachment: discord.Attachment):
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
    await message.edit(content=f"ขนาดbytesของไฟล์: {bytes_size}")
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
                    if attachment.content_type not in media_content_types:
                        description = f"```{file_type}\n{file_preview}[...]```"

                    embed = discord.Embed(title="ผลลัพท์", description=description, color=color)
                    embed.add_field(name="การเข้ารหัสของไฟล์ (sha256)", value=hash_value, inline=False)
                    embed.add_field(name="ชื่อไฟล์", value=file_name, inline=True)
                    embed.add_field(name="ประเภทไฟล์", value=file_type, inline=True)
                    embed.add_field(name="ขนาดไฟล์", value=f"{bytes_size} bytes", inline=True)
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

if __name__ == "__main__":
    bot.run(TOKEN)

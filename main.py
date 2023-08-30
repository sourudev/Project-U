import os
import discord
from util.function import load_responses
from command.on_ready_cmd import _on_ready
from command.upload_cmd import _upload
from command.status_cmd import _status_command
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

responses = load_responses(
    "https://raw.githubusercontent.com/sourudev/Project-U/main/fact.JSON"
)


@bot.event
async def on_ready():
    global uploaded_file_count
    await _on_ready(bot,uploaded_file_count)


@bot.hybrid_command(name="upload", description="อัปโหลดไฟล์")
async def upload(ctx, attachment: discord.Attachment):
    global uploaded_file_count
    await _upload(ctx, attachment,responses,media_content_types,uploaded_file_count)

@bot.hybrid_command(name="status", description="แสดงการอัปโหลดและปิง")
async def status(ctx):
    global uploaded_file_count  # Ensure you have a global variable for uploaded_file_count
    await _status_command(ctx, uploaded_file_count)

if __name__ == "__main__":
    bot.run(TOKEN)

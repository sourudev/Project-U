import json
import requests
import discord
import asyncio
def print_in_color(text, color):
    print(f"\033[{color}m{text}\033[0m")

def load_responses(url):
    response = json.loads(requests.get(url).content)["responses"]
    return response

def save_uploaded_file_count(count):
    data = {"uploaded_file_count": count}
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

def load_uploaded_file_count():
    try:
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
            return data.get("uploaded_file_count", 0)  # Default to 0 if "count" key doesn't exist
    except (FileNotFoundError, json.JSONDecodeError):
        return 0  # Return 0 if file is not found or invalid JSON
    

async def update_status(bot):
    global uploaded_file_count
    while True:
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"อัปโหลดไปแล้ว {uploaded_file_count} ไฟล์")
        await bot.change_presence(activity=activity)
        await asyncio.sleep(5)  # Sleep for 5 seconds before updating again
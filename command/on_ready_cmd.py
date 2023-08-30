import os
import discord
from util.function import print_in_color,load_uploaded_file_count,update_status   # Import any custom functions you need

async def _on_ready(bot):
    await bot.tree.sync()
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(),
        scopes=("bot", "applications.commands")
    )

    os.system('clear' if os.name == 'posix' else 'cls')

    global uploaded_file_count
    uploaded_file_count = load_uploaded_file_count()  # Load the count from the JSON file

    # Start the status update coroutine as a background task
    bot.loop.create_task(update_status(bot))

    print_in_color(f"{bot.user} is ready to upload!", "1;97")
    print_in_color(f"Invite link: {invite_link}", "1;36")
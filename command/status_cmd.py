import discord

async def _status_command(ctx, uploaded_file_count):
    ping = round(ctx.bot.latency * 1000)  # Convert to milliseconds
    embed = discord.Embed(title="<a:alert:982206199757955082> สถานะของบอท", color=0xff0000)
    embed.add_field(name="อัปโหลดไปแล้ว:", value=f"{uploaded_file_count}", inline=False)
    embed.add_field(name="Ping:", value=f"{ping} ms", inline=False)
    await ctx.send(content="", embed=embed)
# from discord.ext import commands
# import asyncio
#
#
# class Timers(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.Cog.listener()
#     async def on_message(self, message):
#         author, channel, content = message.author, message.channel, message.content
#         if channel.id == self.bot.config()["channels"]["fishing"]:
#             if content in ["?fish", "t!fish"]:
#                 def check(m):
#                     return m.author.id == 172002275412279296 and m.channel == channel
#                 try:
#                     tatsu = await self.bot.wait_for("message", timeout=30, check=check)
#                 except asyncio.TimeoutError:
#                     return
#                 if tatsu:
#                     if "you caught" in tatsu.content:
#                         await asyncio.sleep(30)
#                         msg = await channel.send(f"{author.mention} you can fish again!")
#                         await asyncio.sleep(10)
#                         return await msg.delete()
#                     return
#                 return
#
#
# def setup(bot):
#     bot.add_cog(Timers(bot))

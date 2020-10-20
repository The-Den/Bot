import json
import os

import discord
from discord.ext import commands


class ReadyHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        await self.bot.change_presence(
            activity=discord.Game(name="Booting..", type=discord.ActivityType.playing), status=discord.Status.dnd)
        self.bot.gateway_server_name = json.loads(self.bot.ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.ws._trace[0])[1]["calls"][0]

    @commands.Cog.listener()
    async def on_resumed(self):
        self.bot.gateway_server_name = json.loads(self.bot.ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.ws._trace[0])[1]["calls"][0]

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.gateway_server_name = json.loads(self.bot.ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.ws._trace[0])[1]["calls"][0]
        info = f"\nConnected ⚡\n" \
            f"Gateway server: {self.bot.gateway_server_name}\n" \
            f"Session server: {self.bot.session_server_name}\n" \
            f"\nLogged in 📡\n" \
            f"User: {self.bot.user} ({self.bot.user.id})\n" \
            f"Avatar: {self.bot.user.avatar_url_as(static_format='png', size=512)}\n" \
            f"\nInformation ℹ\n" \
            f"Bot version: {self.bot.version['bot']}\n" \
            f"Lib version: {self.bot.version['discord.py']}\n" \
            f"Python version: {self.bot.version['python']}"
        self.bot.log.info(info)
        if len(self.bot.cogs) == 1:
            self.starter_modules()
        await self.bot.change_presence(
            activity=discord.Game(name="with Kanin | !help", type=discord.ActivityType.playing),
            status=discord.Status.online)
        self.bot.log.info("Logged in and ready!")

    def starter_modules(self):
        paths = ["modules/Events", "modules/Commands"]
        blacklist = ["modules/Events/Ready"]
        if self.bot.debug:
            blacklist.append("modules/Events/Timers")
        for path in paths:
            loaded, failed = 0, 0
            name = path.split("/")[-1]
            for file in os.listdir(path):
                try:
                    if file.endswith(".py"):
                        to_load = f"{path}/{file[:-3]}"
                        if to_load not in blacklist:
                            self.bot.load_extension(to_load.replace("/", "."))
                            loaded += 1
                except Exception as e:
                    failed += 1
                    self.bot.log.error(f"Failed to load {path}/{file}: {repr(e)}")
            message = f"Loaded {loaded} {name}"
            if failed > 0:
                message += f" | Failed to load {failed} {name}"
            self.bot.log.info(message)


def setup(bot):
    bot.add_cog(ReadyHandler(bot))

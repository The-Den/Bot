import json
import discord


class ReadyHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_connect(self):
        await self.bot.change_presence(
            activity=discord.Game(name="Booting..", type=discord.ActivityType.playing), status=discord.Status.dnd)
        self.bot.gateway_server_name = json.loads(self.bot.ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.ws._trace[0])[1]["calls"][0]

    async def on_resumed(self):
        self.bot.gateway_server_name = json.loads(self.bot.ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.ws._trace[0])[1]["calls"][0]

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
            f"Bot version: {self.bot.version}\n" \
            f"Lib version: {self.bot.lib_version}\n" \
            f"Python version: {self.bot.python_version}"
        self.bot.log.info(info)
        await self.bot.change_presence(
            activity=discord.Game(name="with Kanin | !help", type=discord.ActivityType.playing),
            status=discord.Status.online)
        self.bot.log.info("Logged in and ready!")


def setup(bot):
    events = [ReadyHandler(bot).on_ready, ReadyHandler(bot).on_connect, ReadyHandler(bot).on_resumed]
    for event in events:
        bot.event(event)
        bot.log.info(f"Event loaded: {event}")

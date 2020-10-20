import asyncio
import atexit
import os
from os.path import join, dirname

import discord
from discord.ext.commands import Bot as DiscordBot
from dotenv import load_dotenv

from utils import setup
from utils.ctx import CustomContext
from config import config

description = "A Discord bot"


class Bot(DiscordBot):
    def __init__(self):
        load_dotenv(join(dirname(__file__), "config/.env"))
        atexit.register(lambda: asyncio.ensure_future(self.logout()))
        super().__init__(command_prefix=["!"], description=description, case_insensitive=True, intents=config.intents)
        setup.bot(self)
        try:
            self.loop.run_until_complete(self.start(os.getenv("TOKEN")))
        except discord.errors.LoginFailure or discord.errors.HTTPException as e:
            self.log.error(f"Shit: {repr(e)}", exc_info=False)
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.pool.close())
            self.loop.run_until_complete(self.logout())

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or CustomContext)

    if __name__ != "__main__":
        setup.logger()


if __name__ == "__main__":
    setup.logger()
    Bot()

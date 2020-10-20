import datetime
import logging
import os
import sys
from collections import Counter

import aiohttp
import asyncpg
import discord
import psutil

from utils.config.config import get_icon
from config import config


def setup_bot(bot):
    # Argument Handling
    bot.debug = any("debug" in arg.lower() for arg in sys.argv)

    # Logging
    discord_log = logging.getLogger("discord")
    discord_log.setLevel(logging.CRITICAL if not bot.debug else logging.INFO)
    log = logging.getLogger("bot")
    bot.log = log
    log.info(f"\n{get_icon()}\nLoading....")

    # Load modules
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    bot.load_extension("modules.Events.Ready")

    # Database
    credentials = {
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASS"),
        "database": os.getenv("POSTGRES_DATABASE"),
        "host": os.getenv("POSTGRES_HOST"),
    }
    bot.pool = bot.loop.run_until_complete(asyncpg.create_pool(**credentials))
    bot.log.info(f"Postgres connected to database ({bot.pool._working_params.database})"
                 f" under the ({bot.pool._working_params.user}) user")

    # Config
    bot.config = config
    bot.uptime = datetime.datetime.utcnow()
    bot.version = {
        "bot": config.version,
        "python": sys.version.split(" ")[0],
        "discord.py": discord.__version__
    }
    bot.counter = Counter()
    bot.commands_used = Counter()
    bot.process = psutil.Process()
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    bot.color = bot.config.colors["main"]
    bot.error_color = bot.config.colors["error"]

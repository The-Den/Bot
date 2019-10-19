import datetime
import coloredlogs
import discord
import logging
import sys
import os
import yaml
import asyncpg
from collections.__init__ import Counter
from utils.config.config import get_icon, get_config

import aiohttp
import psutil

logger = logging.getLogger()


def setup_logger():
    with open("config/logging.yml", "r") as log_config:
        config = yaml.safe_load(log_config)

    coloredlogs.install(level="INFO", logger=logger, fmt=config["formats"]["console"],
                        datefmt=config["formats"]["datetime"], level_styles=config["levels"],
                        field_styles=config["fields"])

    file = logging.FileHandler(filename=f"logs/bot.log", encoding="utf-8", mode="w")
    file.setFormatter(logging.Formatter(config["formats"]["file"]))
    logger.addHandler(file)
    return logger


def setup_bot(bot):
    discord_log = logging.getLogger("discord")
    log = logging.getLogger("bot")
    discord_log.setLevel(logging.CRITICAL)
    bot.log = log
    log.info(f"\n{get_icon()}\nLoading....")
    bot.debug = any("debug" in arg.lower() for arg in sys.argv)
    starter_modules(bot)
    credentials = {
        "user": os.environ["PG_USER"],
        "password": os.environ["PG_PASS"],
        "database": "theden",
        "host": "localhost"
    }
    bot.pool = bot.loop.run_until_complete(asyncpg.create_pool(**credentials))
    bot.config = get_config
    bot.log.info(f"Postgres connected to database ({bot.pool._working_params.database})"
                 f" under the ({bot.pool._working_params.user}) user")
    bot.uptime = datetime.datetime.utcnow()
    bot.version = {
        "bot": "1.0.0",
        "python": sys.version.split(" ")[0],
        "discord.py": discord.__version__
    }
    bot.counter = Counter()
    bot.commands_used = Counter()
    bot.process = psutil.Process()
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    bot.color = 11533055
    bot.error_color = 15158332
    if bot.debug:
        discord_log.setLevel(logging.INFO)


def starter_modules(bot):
    paths = ["modules/Events", "modules/Commands"]
    for path in paths:
        for file in os.listdir(path):
            try:
                if file.endswith(".py"):
                    file_name = file[:-3]
                    path = path.replace("/", ".")
                    bot.load_extension(f"{path}.{file_name}")
            except Exception as e:
                bot.log.error(f"Failed to load {file}: {e}")

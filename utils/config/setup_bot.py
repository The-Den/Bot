import datetime
import coloredlogs
import discord
import logging
import sys
import os
import yaml
from collections.__init__ import Counter
from utils.config.config import get_icon

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
    bot.uptime = datetime.datetime.utcnow()
    bot.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    bot.version = "1.0.0"
    bot.lib_version = discord.__version__
    bot.counter = Counter()
    bot.commands_used = Counter()
    bot.process = psutil.Process()
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    bot.conn = ""  # TODO: database
    bot.color = 11533055
    bot.error_color = 15158332
    if bot.debug:
        discord_log.setLevel(logging.INFO)


def starter_modules(bot):
    for file in os.listdir("modules"):
        try:
            if file.endswith(".py"):
                file_name = file[:-3]
                bot.load_extension(f"modules.{file_name}")
        except Exception as e:
            bot.log.error(f"Failed to load {file}: {e}")

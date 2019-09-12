import discord
import inspect
from discord.ext import commands


class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    @staticmethod
    async def send_cmd_help(self):
        channel = self.channel
        prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
        command = self.invoked_subcommand if self.invoked_subcommand else self.command
        em = discord.Embed(color=discord.Color.red())
        em.title = "Missing required argument ❌"
        em.description = f"{prefix}{command.qualified_name} {command.signature}\n{command.description}"
        await channel.send(embed=em)

    @staticmethod
    async def send_error(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Error ❌")
        em.description = str(content)
        await channel.send(embed=em)

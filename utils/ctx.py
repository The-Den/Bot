import re

import discord
from discord.ext import commands
from discord.ext.commands import converter as converters


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
        em.description = f"{prefix}{command.qualified_name} {self.command_signature(self, command)}\n{command.description}"
        await channel.send(embed=em)

    @staticmethod
    async def send_error(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Error ❌")
        em.description = str(content)
        await channel.send(embed=em)

    @staticmethod
    def command_signature(self, command: commands.Command = None):
        command = command if command else self.command
        if command.usage:
            return command.usage

        params = command.clean_params
        if not params:
            return ""

        result = []
        for name, param in params.items():
            greedy = isinstance(param.annotation, converters._Greedy)
            if param.kind == param.VAR_POSITIONAL:
                result.append(f"[{self.clean_param(param)}...]")
            elif greedy:
                result.append(f"[{self.clean_param(param)}]...")
            elif command._is_typing_optional(param.annotation):
                result.append(f"[{self.clean_param(param)}]")
            else:
                result.append(f"<{self.clean_param(param)}>")

        return ' '.join(result)

    @staticmethod
    def clean_param(param):
        if not param.annotation:
            return param.name

        clean = str(param)
        clean = clean.replace(" ", "")
        clean = clean.replace("=None", "")
        if "Union" in clean:
            args = clean.split(":")
            args1 = args[1].replace("Union[", "").replace("]", "")
            args1 = " or ".join([re.search(r".*(?=\.)\.(.*)", item).group(1) for item in args1.split(",")])
            clean = f"{args[0]}:{args1}"
        if ":" in clean:
            parts = clean.split(":")
            reg = re.search(r".*(?=\.)\.(.*)", parts[1])
            clean = f"{parts[0]}:{reg.group(1)}" if reg else clean
        clean = clean.replace("str", "Text")
        clean = clean.replace("int", "Number")
        return clean

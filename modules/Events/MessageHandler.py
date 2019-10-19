import discord
from discord.ext import commands
from utils.checks.bot_checks import can_send, can_embed, can_react
from utils.ctx import CustomContext


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.is_ready():
            return
        author = message.author
        # Adding some statistics
        self.bot.counter["messages"] += 1
        # Checking if the author of the message is a bot
        if author.bot:
            return
        # Mention the bot to list prefixes
        mentions = [self.bot.user.mention]
        if not isinstance(message.channel, discord.DMChannel):
            mentions.append(message.guild.me.mention)
        if message.content in mentions:
            await message.channel.send(f"My prefix here is:\n!")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        message, command = ctx.message, ctx.command

        cmd = command.qualified_name.replace(" ", "_")
        self.bot.commands_used[cmd] += 1
        self.bot.counter["commands_ran"] += 1

        destination = "Private Message" if isinstance(ctx.channel, discord.DMChannel) else \
            f"#{message.channel.name} ({message.guild.name})"

        self.bot.log.info(f"{message.author} in {destination}: {message.content}")


def setup(bot):
    bot.add_cog(MessageHandler(bot))

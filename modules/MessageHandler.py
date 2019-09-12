import discord

from utils.checks.bot_checks import can_send, can_embed, can_react
from utils.ctx import CustomContext


class MessageHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command(self, ctx):
        cmd = ctx.command.qualified_name.replace(" ", "_")
        self.bot.commands_used[cmd] += 1
        self.bot.counter["commands_ran"] += 1

        message = ctx.message
        destination = "Private Message" if isinstance(ctx.channel, discord.DMChannel) else\
            f"#{message.channel.name} ({message.guild.name})"

        self.bot.log.info(f"{message.author} in {destination}: {message.content}")

    async def process_commands(self, message: discord.Message):
        ctx = await self.bot.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        if not isinstance(message.channel, discord.DMChannel):
            if not can_send(ctx) or not can_embed(ctx):
                if can_react(ctx):
                    return await message.add_reaction("❌")
                try:
                    return await ctx.author.send("Missing permissions to `Send Messages` and/or `Embed Links`!")
                except discord.Forbidden:
                    return self.bot.log.error("Could not respond to command, all checks failed!")

        await self.bot.invoke(ctx)

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
        # Processing the commands
        await self.process_commands(message)


def setup(bot):
    events = [MessageHandler(bot).on_message, MessageHandler(bot).on_command]
    for event in events:
        bot.event(event)
        bot.log.info(f"Event loaded: {event}")

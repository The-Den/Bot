from datetime import timedelta
from discord.ext import commands


class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def format_retry_after(retry_after):
        delta = timedelta(seconds=int(round(retry_after, 0)))
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days:
            fmt = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"
        elif hours:
            fmt = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
        elif minutes:
            fmt = f"{minutes} minutes and {seconds} seconds"
        else:
            fmt = f"{seconds} seconds"
        return f"You can try again in {fmt}"

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(self.format_retry_after(error.retry_after))
        ctx.command.reset_cooldown(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_cmd_help(ctx)
        else:
            self.bot.log.error(error)
            return await ctx.send_error(ctx, error)


def setup(bot):
    bot.event(ErrorHandler(bot).on_command_error)

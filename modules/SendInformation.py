import discord
import yaml
from discord.ext import commands
from utils.checks import checks

with open("config/reactroles.yml", "r") as reactroles:
    reactroles = yaml.safe_load(reactroles)


class SendInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.group(aliases=["rr"], hidden=True)
    async def reactroles(self, ctx):
        if not ctx.invoked_subcommand:
            return ctx.send_cmd_help(ctx)

    @reactroles.command(name="colors")
    async def reactroles_colors(self, ctx):
        colors = ""
        for key, value in reactroles["colors"].items():
            emoji = self.bot.get_emoji(value["emoji"])
            role = ctx.guild.get_role(value["role"])
            colors += f"{emoji} | {role.mention}\n"
        em = discord.Embed(description=colors, color=self.bot.color)
        em.set_author(name="Colors")
        em.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=1024))
        em.set_footer(text="React to this message with the emoji beside the color you want")
        await ctx.send(embed=em)
        colors2 = ""
        for key, value in reactroles["colors2"].items():
            emoji = self.bot.get_emoji(value["emoji"])
            role = ctx.guild.get_role(value["role"])
            colors2 += f"{emoji} | {role.mention}\n"
        em = discord.Embed(description=colors2, color=self.bot.color)
        em.set_footer(text="React to this message with the emoji beside the color you want")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(SendInfo(bot))

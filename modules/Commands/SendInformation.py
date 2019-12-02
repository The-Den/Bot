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
            return await ctx.send_help(ctx.command)

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

    @reactroles.command(name="registered")
    async def reactroles_registered(self, ctx):
        await ctx.message.delete()
        male = ctx.guild.get_role(602614563283664897)
        female = ctx.guild.get_role(602614563732717588)
        nobin = ctx.guild.get_role(602614564344954900)
        pronouns = discord.Embed(color=self.bot.color)
        pronouns.set_author(name="Pronouns")
        pronouns.description = f"👨 | {male.mention}\n" \
                               f"👩 | {female.mention}\n" \
                               f"🤷 | {nobin.mention}"
        pronouns.set_footer(text="React to this message with the emoji beside the role you want")
        pronouns.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=1024))
        await ctx.send(embed=pronouns)
        open = ctx.guild.get_role(384814700032163861)
        closed = ctx.guild.get_role(384814700124307466)
        ask = ctx.guild.get_role(535808392426553374)
        dms = discord.Embed(color=self.bot.color)
        dms.set_author(name="DM status")
        dms.description = f"📬 | {open.mention}\n" \
                          f"📪 | {closed.mention}\n" \
                          f"📫 | {ask.mention}"
        dms.set_footer(text="React to this message with the emoji beside the role you want")
        await ctx.send(embed=dms)
        yes = ctx.guild.get_role(384814697540485130)
        no = ctx.guild.get_role(384814697817571328)
        yes_emoji = self.bot.get_emoji(628243476311572531)
        no_emoji = self.bot.get_emoji(628243211122638898)
        mention = discord.Embed(color=self.bot.color)
        mention.set_author(name="Mentions")
        mention.description = f"{yes_emoji} | {yes.mention}\n" \
                              f"{no_emoji} | {no.mention}"
        mention.set_footer(text="React to this message with the emoji beside the role you want")
        await ctx.send(embed=mention)

    @reactroles.command(name="nsfw")
    async def reactroles_nsfw(self, ctx):
        await ctx.message.delete()
        nsfw = ctx.guild.get_role(629135128018550784)
        nudes = ctx.guild.get_role(629135697353244683)
        nude_emoji = self.bot.get_emoji(629145734859587601)
        lewd = discord.Embed(color=self.bot.color)
        lewd.set_author(name="NSFW")
        lewd.description = f"🔞 | {nsfw.mention}\n" \
                           f"{nude_emoji} | {nudes.mention}"
        lewd.set_footer(text="React to this message with the emoji beside the role you want")
        lewd.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=1024))
        await ctx.send(embed=lewd)


def setup(bot):
    bot.add_cog(SendInfo(bot))

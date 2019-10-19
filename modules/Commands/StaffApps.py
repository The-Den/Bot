import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from modules.Commands.Info import get_relative_delta

roles = {
    "staff": 365262621642850304,
    "banned": 433274330164756480,
    "applicant": 433270619388248084
}

out_channel = 622080645262475264


class StaffApplications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(description="Apply to be a part of the staff team!")
    async def apply(self, ctx):
        """
        {"permissions": {"user": [], "bot": [embed_links]}}
        """
        guild, author = ctx.guild, ctx.author
        banned = guild.get_role(roles["banned"])
        if banned in author.roles:
            return await ctx.send_error(ctx, "You're banned from staff!")
        applicant = guild.get_role(roles["applicant"])
        if applicant in author.roles:
            return await ctx.send_error(ctx, "You've already applied! Please be patient!")
        staff = guild.get_role(roles["staff"])
        if staff in author.roles:
            return await ctx.send_error(ctx, "You're already staff!")

        start = discord.Embed(color=self.bot.color,
                              description=f"{author.mention} I will be messaging you to collect your info!")
        await ctx.send(embed=start)
        try:
            await author.send("Let's get started, how old are you? Be honest!")
        except discord.Forbidden:
            return await ctx.send_error(ctx, "It looks like you have DMs disabled!")

        def check(m):
            return m.channel == author.dm_channel and m.author == author

        em = discord.Embed(color=author.color)
        em.set_author(name=f"Staff application for: {author}")
        em.set_footer(text=f"{author.id} • {datetime.now().strftime('%A, %B %d %Y @ %I:%M%p %Z')}")
        avatar = author.avatar_url_as(static_format="png") if author.avatar else author.default_avatar_url
        em.set_thumbnail(url=avatar)
        desc = author.mention + "\n\n"
        positions = ["Moderator", "Partner Manager", "Bot Support", "Translator"]

        while True:
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await author.send("Timed out")

            content = response.content
            if not content.isdigit():
                await author.send("Your response must be a number!")
            else:
                content = int(content)
                if content < 16:
                    return await author.send("Sorry but we're only accepting people who are 16+!")
                em.add_field(name="Age:", value=str(content))
                break
            if not response:
                return
        while True:
            await author.send(f"Okay, what is the MAIN position you would be applying for?\n"
                              f"{', '.join(positions)}")
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await author.send("Timed out")

            content = response.content.title()
            if content not in positions:
                await author.send(f"Your response **MUST** be one of:\n"
                                  f"{', '.join(positions)}")
            else:
                em.add_field(name="Main position:", value=content)
                positions.remove(content)
                break
            if not response:
                return
        while True:
            await author.send(f"Would you like to apply for any other position? (Just say no if not,"
                              f" please separate positions with commas)\n"
                              f"{', '.join(positions)}")
            try:
                response = await ctx.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                return await author.send("Timed out")

            content = response.content.title()
            if content == "No":
                break
            else:
                em.add_field(name="Other positions:", value=content)
                break
        while True:
            await author.send("Now, tell us why you deserve the position(s) you're applying for!"
                              " Tell us a little about you!")
            try:
                response = await ctx.bot.wait_for("message", timeout=600, check=check)
            except asyncio.TimeoutError:
                return await author.send("Timed out")

            content = response.content
            desc += content
            em.description = desc
            break
        em.add_field(name="Other info:",
                     value=f"**Joined the server:**\n"
                           f"{get_relative_delta(author.joined_at)}")
        await guild.get_channel(out_channel).send(embed=em)
        await guild.get_member(author.id).add_roles(applicant, reason="Applied for staff!")
        await author.send("Thank you for applying! Please be patient and wait for your applications to be voted on!")
        return


def setup(bot):
    bot.add_cog(StaffApplications(bot))

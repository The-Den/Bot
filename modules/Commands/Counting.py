import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

from utils.checks import checks

emojis = {
    1: "🏆",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:",
    7: ":seven:",
    8: ":eight:",
    9: ":nine:",
    10: "🔟"
}


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.mod_or_permissions()
    @commands.command(description="Setup counting!")
    async def countsetup(self, ctx):
        """
        {"permissions": {"user": ["manage_guild", "manage_webhooks"], "bot": ["embed_links"]}}
        """
        guild = ctx.guild
        async with self.bot.pool.acquire() as db:
            guild_info = await db.fetchrow(
                """SELECT channel FROM counting_settings WHERE guild_id=$1""",
                guild.id
            )
            if guild_info:
                return await ctx.send(f"Counting has already been set up in <#{guild_info['channel']}>!")
            count_channel = await guild.create_text_channel("counting", topic="**Next count:** 1", slowmode_delay=2,
                                                            reason=f"[ {ctx.author} ] is setting up counting")
            hook = await count_channel.create_webhook(name="Counting",
                                                      reason=f"[ {ctx.author} ] is setting up counting")
            await db.execute(
                """INSERT INTO counting_settings (guild_id, channel, webhook_url)
                 VALUES ($1, $2, $3) ON CONFLICT DO NOTHING""",
                guild.id, count_channel.id, hook.url
            )
            await ctx.send(f"Counting has been set up in <#{count_channel.id}>!")

    @commands.guild_only()
    @commands.command(description="View the leaderboard for counting")
    async def counttop(self, ctx):
        """
        {"permissions": {"user": [], "bot": ["embed_links"]}}
        """
        async with self.bot.pool.acquire() as db:
            rows = await db.fetch(
                """SELECT user_id, user_count FROM counting WHERE guild_id=$1 ORDER BY user_count DESC LIMIT 10""",
                ctx.guild.id
            )
            user = await db.fetchrow(
                """SELECT * FROM (
                SELECT row_number() OVER (
                PARTITION BY guild_id ORDER BY user_count DESC
                ) AS rank, * FROM counting ORDER BY user_count DESC
                ) AS _ WHERE user_id = $1""",
                ctx.author.id
            )
            msg = ""
            index = 0
            for row in rows:
                index += 1
                msg += f"{emojis[index]} `{row['user_count']:,}`: <@{row['user_id']}>\n"
            em = discord.Embed(description=msg, color=self.bot.color)
            em.set_author(name="Top counters!")
            em.add_field(name="Your Rank:", value=f"**{user['rank']:,}.** Count: `{user['user_count']:,}`")
            em.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=em)

    async def update_counting_info(self, message):
        async with self.bot.pool.acquire() as db:
            user = await db.fetchrow(
                """SELECT user_id FROM counting WHERE guild_id=$1 AND user_id=$2""",
                message.guild.id, message.author.id
            )
            if not user:
                await db.execute(
                    """INSERT INTO counting (guild_id, user_id) VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    message.guild.id, message.author.id
                )
            else:
                await db.execute(
                    """UPDATE counting SET user_count=user_count + 1 WHERE guild_id=$1 AND user_id=$2""",
                    message.guild.id, message.author.id
                )
            await db.execute(
                "UPDATE counting_settings SET current_count=$1, last_counter=$2 WHERE guild_id=$3",
                int(message.content), message.author.id, message.guild.id
            )

    async def get_counting_info(self, message):
        async with self.bot.pool.acquire() as db:
            guild_info = await db.fetchrow(
                """SELECT current_count, channel, roles, last_counter, webhook_url
                 FROM counting_settings WHERE guild_id=$1""",
                message.guild.id
            )

            if not guild_info:
                return

            users = await db.fetch(
                """SELECT user_id, user_count FROM counting WHERE guild_id=$1""",
                message.guild.id
            )

            return {
                "channel": guild_info["channel"],
                "count": guild_info["current_count"],
                "roles": guild_info["roles"],
                "last_counter": guild_info["last_counter"],
                "webhook_url": guild_info["webhook_url"],
                "users": users
            }

    @commands.Cog.listener()
    async def on_message(self, message):
        # Variables
        guild, author, channel, content = message.guild, message.author, message.channel, message.content
        avatar = author.avatar_url if author.avatar else author.default_avatar_url

        # Checks
        if not message.guild:
            return
        settings = await self.get_counting_info(message)
        if not settings:
            return
        if not settings["channel"] or message.channel.id != settings["channel"]:
            return
        if message.author.bot:
            if message.author.discriminator != "0000":
                return await message.delete()
            return
        if not message.content.isdigit():
            return await message.delete()
        content = int(message.content)
        if not content == settings["count"] + 1 or message.author.id == settings["last_counter"]:
            return await message.delete()

        # Update the data
        await self.update_counting_info(message)

        # Change channel topic
        # await message.channel.edit(topic=f"**Next count:** {content + 1}")

        # Delete the original message and resend it as a webhook to prevent deleting
        hook = Webhook.from_url(settings["webhook_url"],
                                adapter=AsyncWebhookAdapter(self.bot.session))
        await message.delete()
        await hook.send(content, username=str(author), avatar_url=avatar)


def setup(bot):
    bot.add_cog(Counting(bot))

from discord.ext import commands, tasks
from random import randint


class Rainbow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_id = 621710507157487656
        self.colors = [16768511, 16761035, 16744685, 13413085, 9699539, 7340203, 4915330, 7506394, 2490561, 13430527,
                       3158212, 65535, 32896, 415029, 13434845, 2541350, 8453888, 16777164, 16776960, 16760576,
                       16770484, 16768460, 16744192, 16728064, 16768477, 13185329, 10944512, 6636321, 0]
        self.index = 0
        self.rainbow_role.start()

    def cog_unload(self):
        self.rainbow_role.stop()

    @tasks.loop(seconds=300)
    async def rainbow_role(self, ctx):
        print(1)
        role = ctx.guild.get_role(self.role_id)
        print(role)
        await role.edit(color=self.colors[self.index])
        print(role)
        if self.index > len(self.colors):
            self.index = 0
        else:
            self.index += 1
        print(self.index)

    @rainbow_role.before_loop
    async def before_rainbow_role(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Rainbow(bot))

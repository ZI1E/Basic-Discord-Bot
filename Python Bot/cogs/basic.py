import logging

from discord.ext import commands

logger = logging.getLogger(f"discord.{__name__}")


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latency(self, ctx):
        """Prints the current latency"""
        await ctx.send(f"Current Latency: {self.bot.latency} seconds")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello")


def setup(bot):
    logger.info(f"Loaded {__name__}")
    bot.add_cog(Basic(bot))

import discord
import asyncio

from discord.ext import commands
from random import choice
from concurrent.futures import ProcessPoolExecutor

import holopearl.helpers

class HoloPearlCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.loop = asyncio.get_event_loop()

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... this feels familiar.')
        self._last_member = member

    @commands.command()
    async def suggestion(self, ctx):
        """Logs a suggestion"""
        if self.bot.store_suggestion(suggestion_message=ctx.message):
            await ctx.send("Thanks! I've logged your suggestion.")
        else:
            await ctx.send("Sorry! I couldn't log your suggestion.")

    @commands.command()
    async def challenge(self, ctx):
        """Challenge HoloPearl to a duel!"""
        options = [
            "Do you wish to engage in combat?",
            "You've already made a mistake by challenging me!",
            "Commencing duel.", "Training mode initiated. Level 1. Begin!",
            "Parry! Parry! Thrust!",
            "You've drawn your sword in vain!"
        ]
        await ctx.send(choice(options))

    @commands.command()
    async def download(self, ctx):
        """Download a video"""
        urls = holopearl.helpers.find_urls_in_string(string_to_parse=ctx.message.content)
        if urls:
            await ctx.send(f"Downloading videos.")
            await self.ytdlp_loop(urls=urls)
        else:
            await ctx.send(f"I couldn't find any URLs in your message :C")

    async def ytdlp_loop(self, urls: list):
        executor = ProcessPoolExecutor(max_workers=1)
        await self.loop.run_in_executor(
                executor, holopearl.helpers.yt_download, urls, self.bot.base_path
            )

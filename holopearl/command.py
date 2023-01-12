import discord
import asyncio
import qrcode

from discord import File
from discord.ext import commands
from io import BytesIO
from random import choice
from functools import partial

import holopearl.helpers

class HoloPearlCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        self.loop = asyncio.get_event_loop()

    @commands.command()
    async def hello(self, ctx: commands.Context, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... this feels familiar.')
        self._last_member = member

    @commands.command()
    async def suggestion(self, ctx: commands.Context):
        """Logs a suggestion"""
        if self.bot.store_suggestion(suggestion_message=ctx.message):
            await ctx.send("Thanks! I've logged your suggestion.")
        else:
            await ctx.send("Sorry! I couldn't log your suggestion.")

    @commands.command()
    async def challenge(self, ctx: commands.Context):
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
    async def qrcode(self, ctx: commands.Context):
        """Create a QR Code from a string of text!"""
        qr_obj = qrcode.make(ctx.message.content.replace("!qrcode ",""))
        with BytesIO() as image_binary:
            qr_obj.save(image_binary)
            image_binary.seek(0)
            await ctx.send(file=File(fp=image_binary, filename="image.png"))

    @commands.command()
    @commands.max_concurrency(number=1, per=commands.BucketType(1), wait=True)
    async def download(self, ctx: commands.Context):
        """Download a video!"""
        await ctx.message.add_reaction("👀")
        urls = holopearl.helpers.find_urls_in_string(string_to_parse=ctx.message.content)
        if urls:
            exec_func = partial(
                holopearl.helpers.yt_download,
                urls, self.bot.base_path,
            )
            await asyncio.to_thread(exec_func)
        else:
            await ctx.send(f"I couldn't find any URLs in your message :C")
            await ctx.message.remove_reaction("👀", self.bot.user)

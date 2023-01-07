import logging
from collections import namedtuple
from importlib import reload
import os

import discord
from discord.ext import commands

from holopearl.command import HoloPearlCommands
from holopearl import exception
import config

class HoloPearl(commands.Bot):
    def __init__(self, bot_environment="dev"):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents, command_prefix='!')
        reload(config)

        if bot_environment == 'dev':
            self.config = config.DevelopmentConfig()
        elif bot_environment == 'prod':
            self.config = config.ProductionConfig()

        env_bot_token = os.getenv(key="HOLOPEARL_BOT_TOKEN")
        if env_bot_token:
            self.bot_token = env_bot_token

        else:
            raise exception.HoloError("Bot token not supplied as environment variable.")

        self._logger = logging.getLogger('HoloPearl')
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self._logger.addHandler(log_handler)
        self._logger.setLevel(self.config.LOG_LEVEL)
        self.next_anime_host = None
        self.next_anime_date = None
        self.base_path = "/holodata"

    def run(self):
        super().run(self.bot_token)

    # TODO: store suggestions somewhere besides local disk - file in S3?
    def store_suggestion(self, suggestion_message: discord.Message) -> bool:
        write_line = f"{suggestion_message.author} suggested: {suggestion_message.content.lstrip('!suggestion')}\n"
        filepath = os.path.join(self.base_path, 'suggestions.txt')
        try:
            with open(filepath, 'a+') as suggestion_file:
                suggestion_file.write(write_line)
        except IOError as e:
            return False

        return True

    #broken
    @staticmethod
    async def process_mention(mention_message: discord.Message):
        await mention_message.add_reaction("👀")

    async def on_ready(self):
        self._logger.debug(f"Logged in as {self.user.name}:{self.user.id}")
        self._logger.info(f"{self.user.name} is ready!")

        await self.add_cog(HoloPearlCommands(self))

        self._logger.info(f"Loaded Cogs!")
        self._logger.debug(f"Available commands:\n{[command.name for command in self.commands]}")

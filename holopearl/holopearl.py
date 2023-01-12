import logging
import os

import discord
from discord.ext import commands

from holopearl.command import HoloPearlCommands
from holopearl.exception import HoloError
import config

class HoloPearl(commands.Bot):
    def __init__(self, bot_environment="dev"):
        intents = discord.Intents.default()
        intents.message_content = True

        if bot_environment == 'dev':
            self.config = config.DevelopmentConfig()
        elif bot_environment == 'prod':
            self.config = config.ProductionConfig()

        env_bot_token = os.getenv(key="HOLOPEARL_BOT_TOKEN")
        if env_bot_token:
            self.bot_token = env_bot_token
        else:
            raise HoloError("Bot token not supplied as environment variable.")

        if self.config.LOG_ROOT:
            self._logger = logging.getLogger()
        else:
            self._logger = logging.getLogger('HoloPearl')

        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self._logger.addHandler(log_handler)
        self._logger.setLevel(self.config.LOG_LEVEL)

        self.next_anime_host = None
        self.next_anime_date = None
        self.base_path = "/holodata"
        super().__init__(intents=intents, command_prefix=self.config.COMMAND_PREFIX)
        self.add_listener(self.command_completion, 'on_command_completion')

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

    async def on_command_error(self, context, exception: BaseException) -> None:
        self._logger.error(exception)
        await context.reply(f"Oops. That didn't work. Please see {self.config.COMMAND_PREFIX}help for information on command usage.")
        raise exception

    async def on_message(self, context: discord.Message):
        if not context.author == self.user:
            if self.user in context.mentions:
                await context.add_reaction("👀")
        await self.process_commands(context)

    async def on_ready(self):
        self._logger.debug(f"Logged in as {self.user.name}:{self.user.id}")
        self._logger.info(f"{self.user.name} is ready!")

        await self.add_cog(HoloPearlCommands(self))

        self._logger.info(f"Loaded Cogs!")
        self._logger.debug(f"Available commands:\n{[command.name for command in self.commands]}")

    async def command_completion(self, ctx: commands.Context):
        if ctx.command.name == 'download':
            await ctx.message.remove_reaction("👀", member=self.user)
            await ctx.message.add_reaction("✔️")
        else:
            pass

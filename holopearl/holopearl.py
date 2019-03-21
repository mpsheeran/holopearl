import logging
from random import randint
import datetime
from collections import namedtuple
from dateutil import parser as date_parser
from importlib import reload

import discord

# import holopearl.command  # TODO: put commands here
from holopearl import exception
import config


class HoloPearl(discord.Client):
	def __init__(self, environment="dev"):
		super().__init__()
		reload(config)

		if environment == 'dev':
			self.config = config.DevelopmentConfig()
		elif environment == 'prod':
			self.config = config.ProductionConfig()

		if self.config.DISCORD_BOT_KEY:
			if self.config.DISCORD_BOT_KEY.endswith("TOKEN_GOES_HERE"):
				raise exception.HoloError("Bot key not updated from default value.")
			else:
				self.bot_token = self.config.DISCORD_BOT_KEY
		else:
			raise exception.HoloError("Bot key blank or missing from configuration file.")

		self._logger = logging.getLogger('HoloPearl')
		log_handler = logging.StreamHandler()
		log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
		self._logger.addHandler(log_handler)
		self._logger.setLevel(self.config.LOG_LEVEL)
		self.next_anime_host = None
		self.next_anime_date = None

	def run(self):
		super().run(self.bot_token)

	# TODO: store suggestions somewhere besides local disk - file in S3?
	def store_suggestion(self, suggestion_message: discord.Message) -> bool:
		write_line = f"{suggestion_message.author} suggested: {suggestion_message.content.lstrip('!suggestion')}\n"
		try:
			with open('suggestions.txt', 'a+') as suggestion_file:
				suggestion_file.write(write_line)
		except IOError as e:
			return False

		return True

	# TODO: find a collection in which to store all possible commands
	# TODO: have '!help' dump all possible commands
	def process_bang_command(self, bang_message: discord.Message) -> str:
		try:
			full_command = bang_message.content.split(' ')
			command_word = full_command[0]

			if command_word == '!help':
				message_to_send = "This is a help message."

			elif command_word == '!suggestion':
				if self.store_suggestion(suggestion_message=bang_message):
					message_to_send = "Thanks! I've logged your suggestion."
				else:
					message_to_send = "Sorry! I couldn't log your suggestion."

			elif command_word == '!japan':
				future = datetime.date(year=2019, month=3, day=31)
				today = datetime.date.today()
				diff = future - today
				message_to_send = f"{diff.days} days until Japan!"

			elif command_word == '!challenge':
				options = [
					"Do you wish to engage in combat?",
					"You've already made a mistake by challenging me!",
					"Commencing duel.", "Training mode initiated. Level 1. Begin!",
					"Parry! Parry! Thrust!",
					"You've drawn your sword in vain!"
				]
				message_to_send = options[randint(0, len(options) - 1)]
			elif command_word == '!anime':
				anime_tuple = self.get_next_anime_night()
				if not (anime_tuple.next_anime_host or anime_tuple.next_anime_date):
					message_to_send = f"Next anime night is unset! Please use the command `!setanime` to plan it."
				elif not anime_tuple.next_anime_host:
					message_to_send = f"The next anime night is scheduled for {anime_tuple.next_anime_date}; we don't know where!"
				elif not anime_tuple.next_anime_date:
					message_to_send = f"The next anime night is scheduled at {anime_tuple.next_anime_host.name}'s house; we don't know when!"
				else:
					message_to_send = f"The next anime night is scheduled for {anime_tuple.next_anime_date} at {anime_tuple.next_anime_host.name}'s house."
			elif command_word == '!setanime':
				next_anime_host = bang_message.mentions[0]
				next_anime_date = date_parser.parse(full_command[1]).date()
				self.next_anime_host = next_anime_host
				self.next_anime_date = next_anime_date
				message_to_send = f"OK! Set the next anime date to {next_anime_date} and the next anime host to {next_anime_host.name}"
			else:
				message_to_send = f"Sorry, \"{command_word}\" is not a recognized command. Try `!help` for a list of available commands."
		except IndexError as e:
			pass

		except ValueError as e:
			pass

		finally:
			return message_to_send

	@staticmethod
	async def process_mention(mention_message: discord.Message):
		await mention_message.add_reaction("👀")

	async def on_ready(self):
		self._logger.debug(f"Logged in as {self.user.name}:{self.user.id}")
		self._logger.info(f"{self.user.name} is ready!")
		# TODO: chat into a debug channel?

	# TODO
	def get_next_anime_night(self) -> namedtuple:
		AnimeNight = namedtuple(typename="AnimeNight", field_names=["next_anime_date", "next_anime_host"])
		# if self.next_anime_date < datetime.date.today():
		# 	pass # TODO: maybe default to next Friday?

		next_night = AnimeNight(next_anime_date= self.next_anime_date, next_anime_host= self.next_anime_host)
		return next_night  # this CAN return None for either or both of the fields

	# TODO
	def set_next_anime_night(self, user: discord.User = None, date: datetime.date = None) -> bool:
		if not (user or date):
			self._logger.debug("set_next_anime_night was called with no arguments.")
			return False
		if user:
			self.next_anime_host = user
		if date:
			self.next_anime_date = date

		return True

	async def on_message(self, message):
		if message.author == self.user:
			return

		if message.content.startswith('!'):
			message_to_send = self.process_bang_command(message)
			await message.channel.send(message_to_send)
			self._logger.debug(f"Processed command: {message.content}; sent message \"{message_to_send}\"")

		elif self.user in message.mentions:
			await self.process_mention(mention_message=message)
			self._logger.debug(f"Reacted to message: {message.content}")


if __name__ == "__main__":
	client = HoloPearl()
	client.run()

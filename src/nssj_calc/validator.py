import re
from dataclasses import dataclass
from enum import Enum

from nssj_calc.config import CONFIG, TrainingPlan, WeightCategory


@dataclass
class Validator:
	@classmethod
	def __input(cls, message: str, *options: str) -> str:
		if message != "":
			print(message)

		# Stripped lowercase, for matching later
		options = tuple[str](opt.strip().lower() for opt in options)

		for option in options:
			print(f"-	{option}")

		while True:
			value = input("> ").strip()

			# Simple validation if options
			if options and value not in options:
				print("Invalid choice. Please choose from the given options.")
				continue

			return value

	def __str(self, message: str) -> str:
		return self.__input(message)

	def __int(self, message: str) -> int:
		while True:
			try:
				return int(self.__input(message))
			except ValueError, TypeError:
				print("Please enter a valid numerical value.")
				continue

	def __float(self, message: str) -> float:
		while True:
			try:
				return float(self.__input(message))
			except ValueError, TypeError:
				print("Please enter a valid numerical value.")
				continue

	def __bool(self, message: str) -> bool:
		while True:
			value = self.__input(message).lower()

			if value in ("yes", "y", "true", "t", "1"):
				return True
			elif value in ("no", "n", "false", "f", "0"):
				return False
			else:
				print("Please enter one of (y/n).")
				continue

	def __enum[E: Enum](self, cls: type[E], message: str) -> E:
		members = {member.name.upper(): member for member in cls}
		if not members:
			raise ValueError(f"{cls.__name__} has no options!")

		options = tuple(members.keys())
		choice = self.__input(message, *options).strip().upper()
		return members[choice]

	def name(self, message: str) -> str:
		# Used https://regex101.com/ for testing the regex validity and such
		# Must start with unicode character
		# Check for initials (matching '.')
		# Check for more unicode characters again
		# Must end with character, no special characters
		regex = re.compile(r"^[^\W\d_]+\.?(?: [^\W\d_]+\.?)*$")

		while True:
			value = self.__str(message)
			if regex.fullmatch(value):
				return value
			else:
				print("Enter a valid name! Remove any special characters and such.")

	def weight(self, message: str) -> float:
		while True:
			value = self.__float(message)
			if (
				CONFIG.validation.weight.max != 0.0
				and CONFIG.validation.weight.min
				<= value
				<= CONFIG.validation.weight.max
				or CONFIG.validation.weight.min <= value
			):
				return value
			else:
				print("Enter a valid weight! Must be numerical and positive.")

	def training_plan(self, message: str) -> TrainingPlan:
		return self.__enum(TrainingPlan, message)

	def weight_category(self, message: str) -> WeightCategory:
		return self.__enum(WeightCategory, message)

	def competitions(self, message: str) -> int:
		while True:
			value = self.__int(message)
			if (
				CONFIG.validation.competitions.min
				<= value
				<= CONFIG.validation.competitions.max
			):
				return value
			else:
				print(
					f"The number of competitions you can enter is between {CONFIG.validation.competitions.min} and {CONFIG.validation.competitions.max} only!"
				)

	def private_coaching(self, message: str) -> int:
		while True:
			value = self.__int(message)
			if (
				CONFIG.validation.coaching.min
				<= value
				<= CONFIG.validation.coaching.max
			):
				return value
			else:
				print(
					f"Private coaching can only be within {CONFIG.validation.coaching.min} to {CONFIG.validation.coaching.max} hours!"
				)

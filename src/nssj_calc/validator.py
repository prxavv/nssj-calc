import re
from dataclasses import dataclass
from enum import Enum

from nssj_calc.config import CONFIG, TrainingPlan, WeightCategory


@dataclass
class Validator:
	"""The primary validator class. Contains MANY methods to validate inputs in many different levels.
	There are three levels:
	- Input & Option Validation: Validates if the input matches given options if any.
	- Type Validation: Make sure inputs are of the type they're requested.
	- Value Range Validation: Final validation level, to check if all inputs are within the correct range.

	All levels prompt repeatedly until the correct values are entered, so all inputs are air-tight."""

	@classmethod
	def __input(cls, message: str, *options: str) -> str:
		"""Takes inputs and returns them.
		Sort of replaces the default `input` function, by repeated inputs, different formatting,
		options validating if any, and such.

		Level 1 fn.

		Args:
			message: Takes a message to print before taking inputs.
			*options: Optional options to match. If no matches, it forces a re-entry.

		Returns:
			A string of the entered value. Type validation is level 2."""
		if message != "":
			print(message)

		# Stripped lowercase, for matching later
		options = tuple(opt.strip().lower() for opt in options)

		for option in options:
			print(f"-	{option}")

		while True:
			value = input("> ").strip().lower()

			# Simple validation if options
			if options and value not in options:
				print("Invalid choice. Please choose from the given options.")
				continue

			return value

	def __str(self, message: str) -> str:
		"""Takes a message and returns inputs as a string.
		Acts as an abstraction layer over the `__input` function.

		Level 2 abstracted fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			`str`."""
		return self.__input(message)

	def __int(self, message: str) -> int:
		"""Takes a message and returns inputs as an int.
		Acts as an abstraction layer over the `__input` function.

		Level 2 abstracted fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			`int`."""
		while True:
			try:
				return int(self.__input(message))
			except ValueError, TypeError:
				print("Please enter a valid numerical value.")
				continue

	def __float(self, message: str) -> float:
		"""Takes a message and returns inputs as a float.
		Acts as an abstraction layer over the `__input` function.

		Level 2 abstracted fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			`float`."""
		while True:
			try:
				return float(self.__input(message))
			except ValueError, TypeError:
				print("Please enter a valid numerical value.")
				continue

	def __bool(self, message: str) -> bool:
		"""Takes a message and returns inputs as a bool.
		Acts as an abstraction layer over the `__input` function.

		Level 2 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			`bool`."""
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
		"""Takes a message and returns inputs as an enum.
		Acts as an abstraction layer over the `__input` function.

		Level 2 abstracted fn.

		Args:
			cls: Takes an enum class for `__input` `*options`.
			message: Takes a message for parameter drilling.

		Returns:
			The type of enum you provided will be returned."""
		members = {member.name.upper(): member for member in cls}
		if not members:
			raise ValueError(f"{cls.__name__} has no options!")

		options = tuple(members.keys())
		choice = self.__input(message, *options).strip().upper()
		return members[choice]

	def name(self, message: str) -> str:
		"""Takes a message and returns inputs as a string.
		Acts as an abstraction layer over the `__str` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Name `str`."""
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
		"""Takes a message and returns inputs as a float.
		Acts as an abstraction layer over the `__float` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Weight `float`."""
		while True:
			value = self.__float(message)

			if (
				CONFIG.validation.weight.max == 0.0
				or value <= CONFIG.validation.weight.max
			) and CONFIG.validation.weight.min <= value:
				return value
			else:
				if CONFIG.validation.weight.max == 0.0:
					print(
						f"Enter a valid weight! Must be numerical and above {CONFIG.validation.weight.min}"
					)
				else:
					print(
						f"Enter a valid weight! Must be numerical and between {CONFIG.validation.weight.min} and {CONFIG.validation.weight.max}."
					)

	def training_plan(self, message: str) -> TrainingPlan:
		"""Takes a message and returns inputs as `TrainingPlan`.
		Acts as an abstraction layer over the `__enum` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Enum `TrainingPlan`."""
		return self.__enum(TrainingPlan, message)

	def weight_category(self, message: str) -> WeightCategory:
		"""Takes a message and returns inputs as `WeightCategory`.
		Acts as an abstraction layer over the `__enum` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Enum `WeightCategory`."""
		return self.__enum(WeightCategory, message)

	def competitions(self, message: str) -> int:
		"""Takes a message and returns inputs as an int.
		Acts as an abstraction layer over the `__int` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Competitions `int`."""
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
		"""Takes a message and returns inputs as an int.
		Acts as an abstraction layer over the `__int` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			Private Coaching `int`."""
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

	def add_athlete(self, message: str) -> bool:
		"""Takes a message and returns inputs as a bool.
		Acts as an abstraction layer over the `__bool` function.

		Level 3 abstraction fn.

		Args:
			message: Takes a message for parameter drilling.

		Returns:
			`bool`."""
		return self.__bool(message)

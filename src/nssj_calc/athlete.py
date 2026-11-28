from dataclasses import dataclass
from typing import override

from nssj_calc.config import CONFIG, TrainingPlan, WeightCategory

# pyright: reportAny=false


@dataclass
class Athlete:
	"""The primary athlete class. Contains all the details, calculations, etc."""

	name: str
	weight: float
	weight_category: WeightCategory
	training_plan: TrainingPlan
	competitions: int
	private_coaching: int

	def __fmt_row(self, width: int, label: str, value: object) -> str:
		"""Format any given value based on width.

		Args:
			width: Width of the entire row.
			label: The left hand side's value.
			value: The right hand side's value.

		Returns:
			Formatted `str`."""
		value = str(value)
		remaining = max(0, width - len(label))
		return f"{label}{value:>{remaining}}"

	def __calculate_weight_cat(self):
		"""Calculates the weight category based on the athlete's weight.

		Returns:
			`WeightCategory` of the athlete's weight."""
		ordered_desc = sorted(WeightCategory, key=lambda cat: cat.value, reverse=True)
		matched = next((cat for cat in ordered_desc if self.weight >= cat.value), None)
		if matched is not None:
			return matched

		# Default to fly_weight or the first one.
		return ordered_desc[-1]

	def __weight_difference(self) -> str:
		"""Calculates and returns the difference in weight between
		the athlete's current weight and their target weight
		category.

		Returns:
			A `str` value of the amount of weight to be lost or
			gained to reach the desired weight category. Can be
			converted to a `float`."""

		weight = self.weight
		target = self.weight_category
		current_category = self.__calculate_weight_cat()

		# If their target category was to reach the category they're
		# currently in, return 0.00 kgs change
		if current_category == target:
			return f"{0.0:.2f}"

		ordered = sorted(WeightCategory, key=lambda cat: cat.value)
		idx = ordered.index(target)
		upper_bound: float | None = (
			ordered[idx + 1].value if idx + 1 < len(ordered) else None
		)

		# Calculate bounds and return with change sign
		if upper_bound is not None and weight >= upper_bound:
			difference = upper_bound - weight
			return f"{difference:+.2f}"

		if weight < target.value:
			difference = target.value - weight
			return f"{difference:+.2f}"

		# Unnecessary fallback (better safe than sorry)
		return f"{0.0:.2f}"

	@override
	def __str__(self) -> str:
		# Overriding the default __str__ method, so whenever print is
		# called on an instance of this class, it's formatted nicely.

		# fmt: off
		header	= "- - - - - - - - - - - - Athlete Information - - - - - - - - - - - -"
		costs	= "- - - - - - - - - - - - - - Total Costs - - - - - - - - - - - - - -"
		divider	= "-------------------------------------------------------------------"
		# fmt: on
		width = len(header)

		# Pre-calculate all values necessary
		training_plan: float = self.training_plan.value.price * 4.0
		private_coaching: float = (
			self.private_coaching * 4 * CONFIG.validation.coaching.price
		)
		competitions: float = self.competitions * CONFIG.validation.competitions.price

		total = training_plan + private_coaching + competitions

		# Complex calculations are separated into functions and
		# called inside this array
		lines = [
			header,
			self.__fmt_row(width, "Athlete Name:", self.name),
			self.__fmt_row(width, "Current Weight:", f"{self.weight:.2f} kg"),
			"",
			self.__fmt_row(
				width, "Current Weight Category:", self.__calculate_weight_cat().name
			),
			self.__fmt_row(width, "Target Weight Category:", self.weight_category.name),
			self.__fmt_row(
				width, "Weight Difference:", f"{self.__weight_difference()} kg"
			),
			"",
			costs,
			self.__fmt_row(width, "Training Plan:", f"£ {training_plan:.2f}"),
			self.__fmt_row(width, "Private Coaching:", f"£ {private_coaching:.2f}"),
			self.__fmt_row(width, "Competition Fees:", f"£ {competitions:.2f}"),
			divider,
			self.__fmt_row(width, "Total", f"£ {total:.2f}"),
		]

		# Join and return; Fully formatted.
		return "\n".join(lines)

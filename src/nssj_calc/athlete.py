from dataclasses import dataclass
from typing import override

from nssj_calc.config import CONFIG, TrainingPlan, WeightCategory


@dataclass
class Athlete:
	name: str
	weight: float
	weight_category: WeightCategory
	training_plan: TrainingPlan
	competitions: int
	private_coaching: int

	def __fmt_row(self, width: int, label: str, value: object) -> str:
		value = str(value)
		remaining = max(0, width - len(label))
		return f"{label}{value:>{remaining}}"

	def __calculate_weight_cat(self):
		ordered_desc = sorted(WeightCategory, key=lambda cat: cat.value, reverse=True)
		matched = next((cat for cat in ordered_desc if self.weight >= cat.value), None)
		if matched is not None:
			return matched

		return ordered_desc[-1]

	def __weight_difference(self) -> float:
		current = self.weight
		target = self.weight_category
		ordered = sorted(WeightCategory, key=lambda cat: cat.value)
		
		idx = ordered.index(target)
		upper_bound = ordered[idx + 1].value if idx + 1 < len(ordered) else None

		if current < target.value:
			return round(target.value - current, 2)

		if upper_bound is not None and current > upper_bound:
			return round(current - upper_bound, 2)

		return 0.0

	@override
	def __str__(self) -> str:
		header	= "- - - - - - - - - - - - Athlete Information - - - - - - - - - - - -"
		costs	= "- - - - - - - - - - - - - - Total Costs - - - - - - - - - - - - - -"
		divider	= "-------------------------------------------------------------------"
		width = len(header)

		training_plan: float = self.training_plan.value.price * 4.0
		private_coaching: float = self.private_coaching * 4 * CONFIG.validation.coaching.price
		competitions: float = self.competitions * CONFIG.validation.competitions.price

		total = training_plan + private_coaching + competitions

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
				width, "Weight Difference:", f"{self.__weight_difference():.2f} kg"
			),
			"",
			costs,
			self.__fmt_row(width, "Training Plan:", f"£ {training_plan:.2f}"),
			self.__fmt_row(width, "Private Coaching:", f"£ {private_coaching:.2f}"),
			self.__fmt_row(width, "Competition Fees:", f"£ {competitions:.2f}"),
			divider,
			self.__fmt_row(width, "Total", f"£ {total:.2f}")
		]

		return "\n".join(lines)

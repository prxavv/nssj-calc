from nssj_calc.athlete import Athlete
from nssj_calc.validator import Validator

# pyright: reportAny=false


def onboarding() -> Athlete:
	"""Orchestrates the program, by taking all inputs, and returning an `Athlete`.

	Returns:
		`Athlete` after all inputs."""
	vdt = Validator()

	name = vdt.name("What's your name?")
	weight = vdt.weight("And your current weight?")
	weight_category = vdt.weight_category("Which weight category are you applying for?")
	training_plan = vdt.training_plan("Enter the plan you'd like to join")

	competitions = 0
	if training_plan.value.competition_validity:
		competitions = vdt.competitions(
			"You're eligible to enter competitions.\nHow many competitions would you like to enter?"
		)

	private_coaching = vdt.private_coaching(
		"How many extra hours of classes would you like (per week; 0 is an option too)?"
	)

	return Athlete(
		name, weight, weight_category, training_plan, competitions, private_coaching
	)


def main() -> None:
	"""Entrypoint to the application.
	Repeats until terminated or quit."""
	loop = True
	while loop:
		print(onboarding())

		validator = Validator()
		loop = validator.add_athlete("Would you like to add another athlete? (y/n)")


if __name__ == "__main__":
	main()

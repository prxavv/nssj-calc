import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseModel

from nssj_calc.utils import (
	DEFAULT_CONFIG,
)


@dataclass(frozen=True)
class PlanCost:
	sessions: int
	price: float
	competition_validity: bool


class MinMax[T: (int, float)](BaseModel):
	min: T
	max: T


class Weight(MinMax[float]):
	pass


class Competitions(MinMax[int]):
	price: float


class Coaching(MinMax[int]):
	price: float


class TrainingPlanRaw(BaseModel):
	name: str
	sessions: int
	price: float
	competition_validity: bool


class Validation(BaseModel):
	weight: Weight = Weight(min=0.0, max=0.0)
	competitions: Competitions = Competitions(min=0, max=1, price=22.0)
	coaching: Coaching = Coaching(min=0, max=5, price=9.50)


class Config(BaseModel):
	validation: Validation = Validation()
	weight_categories: dict[str, float] = {}
	training_plan: list[TrainingPlanRaw] = []

	@classmethod
	def new(cls, path: str = "config.toml", _retried: bool = False) -> Config:
		fpath: Path = Path(path)
		try:
			with fpath.open("rb") as file:
				config = tomllib.load(file)
		except FileNotFoundError:
			if _retried:
				raise
			_ = fpath.write_text(DEFAULT_CONFIG, "utf-8")
			return cls.new(path, _retried=True)
		
		config = Config.model_validate(config)
		if not config.weight_categories:
			raise ValueError(f"No [weight_categories] found in {fpath.resolve()}")

		return config


def enumerate_weight_categories(CONFIG: Config):
	return Enum("WeightCategory", CONFIG.weight_categories)


def enumerate_training_plans(CONFIG: Config):
	plan = {
		i.name: PlanCost(i.sessions, i.price, i.competition_validity)
		for i in CONFIG.training_plan
	}

	return Enum("TrainingPlan", plan)


CONFIG = Config.new()
WeightCategory = enumerate_weight_categories(CONFIG)
TrainingPlan = enumerate_training_plans(CONFIG)

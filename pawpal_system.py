"""Core logic layer for PawPal+.

This module holds the backend domain objects and scheduling service used by the
Streamlit app.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
	title: str
	description: str = ""
	duration_minutes: int = 0
	priority: str = "medium"
	category: str = "general"
	completed: bool = False

	def mark_complete(self) -> None:
		raise NotImplementedError

	def update_priority(self, priority: str) -> None:
		raise NotImplementedError


@dataclass
class Pet:
	name: str
	species: str
	age: int = 0
	care_notes: str = ""
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		raise NotImplementedError

	def remove_task(self, task: Task) -> None:
		raise NotImplementedError

	def get_pending_tasks(self) -> list[Task]:
		raise NotImplementedError


@dataclass
class Owner:
	name: str
	email: str
	preferences: str = ""
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		raise NotImplementedError

	def remove_pet(self, pet: Pet) -> None:
		raise NotImplementedError

	def get_pets(self) -> list[Pet]:
		raise NotImplementedError


class Scheduler:
	def __init__(self, available_minutes: int, task_queue: list[Task] | None = None) -> None:
		self.available_minutes = available_minutes
		self.task_queue = task_queue or []

	def generate_schedule(self, pet: Pet) -> list[Task]:
		raise NotImplementedError

	def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
		raise NotImplementedError

	def filter_by_time(self, tasks: list[Task]) -> list[Task]:
		raise NotImplementedError

	def explain_plan(self, tasks: list[Task]) -> str:
		raise NotImplementedError

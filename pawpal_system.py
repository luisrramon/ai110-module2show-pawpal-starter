"""Core logic layer for PawPal+.

This module holds the backend domain objects and scheduling service used by the
Streamlit app.
"""

from __future__ import annotations

from dataclasses import dataclass, field

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass(frozen=True)
class ScheduleEntry:
	task: Task
	start_minute: int
	end_minute: int
	reason: str = ""


@dataclass
class Task:
	title: str
	description: str = ""
	duration_minutes: int = 0
	priority: str = "medium"
	category: str = "general"
	completed: bool = False

	def __post_init__(self) -> None:
		if self.duration_minutes < 0:
			raise ValueError("duration_minutes must be non-negative")
		self.priority = self.priority.lower()
		if self.priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {', '.join(VALID_PRIORITIES)}")

	def mark_complete(self) -> None:
		self.completed = True

	def update_priority(self, priority: str) -> None:
		normalized_priority = priority.lower()
		if normalized_priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {', '.join(VALID_PRIORITIES)}")
		self.priority = normalized_priority


@dataclass
class Pet:
	name: str
	species: str
	age: int = 0
	care_notes: str = ""
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		if task in self.tasks:
			raise ValueError("task already exists for this pet")
		self.tasks.append(task)

	def remove_task(self, task: Task) -> None:
		try:
			self.tasks.remove(task)
		except ValueError as exc:
			raise ValueError("task not found for this pet") from exc

	def get_pending_tasks(self) -> list[Task]:
		return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
	name: str
	email: str
	preferences: str = ""
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		if pet in self.pets:
			raise ValueError("pet already exists for this owner")
		self.pets.append(pet)

	def remove_pet(self, pet: Pet) -> None:
		try:
			self.pets.remove(pet)
		except ValueError as exc:
			raise ValueError("pet not found for this owner") from exc

	def get_pets(self) -> list[Pet]:
		return list(self.pets)


class Scheduler:
	def __init__(self, available_minutes: int, task_queue: list[Task] | None = None) -> None:
		if available_minutes < 0:
			raise ValueError("available_minutes must be non-negative")
		self.available_minutes = available_minutes
		self.task_queue = task_queue or []

	def generate_schedule(self, pet: Pet) -> list[Task]:
		tasks = self.sort_by_priority(pet.get_pending_tasks())
		return self.filter_by_time(tasks)

	def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
		priority_rank = {priority: index for index, priority in enumerate(VALID_PRIORITIES)}
		return sorted(
			tasks,
			key=lambda task: (priority_rank[task.priority], task.duration_minutes, task.title.lower()),
		)

	def filter_by_time(self, tasks: list[Task]) -> list[Task]:
		selected_tasks: list[Task] = []
		remaining_minutes = self.available_minutes
		for task in tasks:
			if task.duration_minutes <= remaining_minutes:
				selected_tasks.append(task)
				remaining_minutes -= task.duration_minutes
		return selected_tasks

	def explain_plan(self, tasks: list[Task]) -> str:
		if not tasks:
			return "No tasks fit within the available time."

		lines = ["Planned tasks:"]
		elapsed_minutes = 0
		for task in tasks:
			start_minute = elapsed_minutes
			elapsed_minutes += task.duration_minutes
			lines.append(
				f"- {task.title}: priority {task.priority}, {task.duration_minutes} min, starts at +{start_minute} min"
			)
		return "\n".join(lines)

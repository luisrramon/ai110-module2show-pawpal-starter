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
	frequency: str = "daily"
	duration_minutes: int = 0
	priority: str = "medium"
	category: str = "general"
	completed: bool = False

	def __post_init__(self) -> None:
		"""Normalize task fields and validate priority and duration."""
		self.title = self.title.strip()
		self.description = self.description.strip()
		self.frequency = self.frequency.strip().lower() or "daily"
		self.category = self.category.strip().lower() or "general"
		if self.duration_minutes < 0:
			raise ValueError("duration_minutes must be non-negative")
		self.priority = self.priority.lower()
		if self.priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {', '.join(VALID_PRIORITIES)}")

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.completed = True

	def update_priority(self, priority: str) -> None:
		"""Update the task priority after validating the value."""
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

	def __post_init__(self) -> None:
		"""Normalize pet fields and validate age."""
		self.name = self.name.strip()
		self.species = self.species.strip().lower()
		self.care_notes = self.care_notes.strip()
		if self.age < 0:
			raise ValueError("age must be non-negative")

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet."""
		if task in self.tasks:
			raise ValueError("task already exists for this pet")
		self.tasks.append(task)

	def remove_task(self, task: Task) -> None:
		"""Remove a task from this pet."""
		try:
			self.tasks.remove(task)
		except ValueError as exc:
			raise ValueError("task not found for this pet") from exc

	def get_pending_tasks(self) -> list[Task]:
		"""Return tasks that are not completed."""
		return [task for task in self.tasks if not task.completed]

	def get_completed_tasks(self) -> list[Task]:
		"""Return tasks that are completed."""
		return [task for task in self.tasks if task.completed]


@dataclass
class Owner:
	name: str
	email: str
	preferences: str = ""
	pets: list[Pet] = field(default_factory=list)

	def __post_init__(self) -> None:
		"""Normalize owner fields and validate required values."""
		self.name = self.name.strip()
		self.email = self.email.strip()
		self.preferences = self.preferences.strip()
		if not self.name:
			raise ValueError("name must not be empty")
		if not self.email:
			raise ValueError("email must not be empty")

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner."""
		if pet in self.pets:
			raise ValueError("pet already exists for this owner")
		self.pets.append(pet)

	def remove_pet(self, pet: Pet) -> None:
		"""Remove a pet from this owner."""
		try:
			self.pets.remove(pet)
		except ValueError as exc:
			raise ValueError("pet not found for this owner") from exc

	def get_pets(self) -> list[Pet]:
		"""Return a copy of the owner's pet list."""
		return list(self.pets)

	def get_all_tasks(self, include_completed: bool = False) -> list[Task]:
		"""Collect tasks from every pet owned by this owner."""
		tasks: list[Task] = []
		for pet in self.pets:
			pet_tasks = pet.tasks if include_completed else pet.get_pending_tasks()
			tasks.extend(pet_tasks)
		return tasks

	def get_all_pending_tasks(self) -> list[Task]:
		"""Return all pending tasks across all pets."""
		return self.get_all_tasks(include_completed=False)


class Scheduler:
	def __init__(self, available_minutes: int, task_queue: list[Task] | None = None) -> None:
		"""Create a scheduler with a time budget and optional task queue."""
		if available_minutes < 0:
			raise ValueError("available_minutes must be non-negative")
		self.available_minutes = available_minutes
		self.task_queue = task_queue or []

	def load_tasks_from_owner(self, owner: Owner, include_completed: bool = False) -> list[Task]:
		"""Load tasks from an owner into the scheduler queue."""
		self.task_queue = owner.get_all_tasks(include_completed=include_completed)
		return list(self.task_queue)

	def generate_schedule(self, source: Owner | Pet) -> list[ScheduleEntry]:
		"""Build a schedule for an owner or a single pet."""
		if isinstance(source, Owner):
			tasks = source.get_all_pending_tasks()
		else:
			tasks = source.get_pending_tasks()

		sorted_tasks = self.sort_by_priority(tasks)
		selected_tasks = self.filter_by_time(sorted_tasks)
		return self._build_schedule_entries(selected_tasks)

	def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by priority, duration, and title."""
		priority_rank = {priority: index for index, priority in enumerate(VALID_PRIORITIES)}
		return sorted(
			tasks,
			key=lambda task: (priority_rank[task.priority], task.duration_minutes, task.title.lower()),
		)

	def filter_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Select tasks that fit within the available minutes."""
		selected_tasks: list[Task] = []
		remaining_minutes = self.available_minutes
		for task in tasks:
			if task.duration_minutes <= remaining_minutes:
				selected_tasks.append(task)
				remaining_minutes -= task.duration_minutes
		return selected_tasks

	def _build_schedule_entries(self, tasks: list[Task]) -> list[ScheduleEntry]:
		"""Convert tasks into scheduled time blocks."""
		entries: list[ScheduleEntry] = []
		elapsed_minutes = 0
		for task in tasks:
			start_minute = elapsed_minutes
			end_minute = start_minute + task.duration_minutes
			entries.append(
				ScheduleEntry(
					task=task,
					start_minute=start_minute,
					end_minute=end_minute,
					reason=f"priority {task.priority} within available time",
				)
			)
			elapsed_minutes = end_minute
		return entries

	def explain_plan(self, schedule: list[ScheduleEntry]) -> str:
		"""Return a readable summary of the generated schedule."""
		if not schedule:
			return "No tasks fit within the available time."

		lines = ["Planned tasks:"]
		for entry in schedule:
			task = entry.task
			lines.append(
				f"- {task.title}: priority {task.priority}, {task.duration_minutes} min, starts at +{entry.start_minute} min"
			)
		return "\n".join(lines)

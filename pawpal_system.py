"""Core logic layer for PawPal+.

This module holds the backend domain objects and scheduling service used by the
Streamlit app.
"""

from __future__ import annotations

from datetime import date, timedelta
from dataclasses import dataclass, field
from collections import defaultdict

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
	time: str = "00:00"
	due_date: date | None = None
	priority: str = "medium"
	category: str = "general"
	pet_name: str = ""
	completed: bool = False

	def __post_init__(self) -> None:
		"""Normalize task fields and validate priority, duration, time, and due date."""
		self.title = self.title.strip()
		self.description = self.description.strip()
		self.frequency = self.frequency.strip().lower() or "daily"
		self.category = self.category.strip().lower() or "general"
		self.pet_name = self.pet_name.strip()
		if self.duration_minutes < 0:
			raise ValueError("duration_minutes must be non-negative")
		self.time = self._normalize_time(self.time)
		self.due_date = self._normalize_due_date(self.due_date)
		self.priority = self.priority.lower()
		if self.priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {', '.join(VALID_PRIORITIES)}")

	@staticmethod
	def _normalize_time(time_value: str) -> str:
		"""Validate a task time in HH:MM format and return a normalized value."""
		normalized_time = time_value.strip()
		if not normalized_time:
			return "00:00"

		parts = normalized_time.split(":")
		if len(parts) != 2:
			raise ValueError("time must use HH:MM format")

		hour_text, minute_text = parts
		if not (hour_text.isdigit() and minute_text.isdigit()):
			raise ValueError("time must use HH:MM format")

		hour = int(hour_text)
		minute = int(minute_text)
		if hour < 0 or hour > 23 or minute < 0 or minute > 59:
			raise ValueError("time must use HH:MM format")
		return f"{hour:02d}:{minute:02d}"

	@staticmethod
	def _normalize_due_date(due_date_value: date | None) -> date | None:
		"""Keep due dates as date objects and leave them unset when omitted."""
		if due_date_value is None or isinstance(due_date_value, date):
			return due_date_value
		raise TypeError("due_date must be a datetime.date value or None")

	def create_next_occurrence(self, completion_date: date | None = None) -> Task | None:
		"""Create the next daily or weekly instance after completion."""
		normalized_frequency = self.frequency.lower()
		if normalized_frequency not in {"daily", "weekly"}:
			return None

		completion_day = completion_date or self.due_date or date.today()
		delta = timedelta(days=1) if normalized_frequency == "daily" else timedelta(days=7)
		return Task(
			title=self.title,
			description=self.description,
			frequency=self.frequency,
			duration_minutes=self.duration_minutes,
			time=self.time,
			due_date=completion_day + delta,
			priority=self.priority,
			category=self.category,
			pet_name=self.pet_name,
		)

	def mark_complete(self, completion_date: date | None = None) -> Task | None:
		"""Mark this task as completed and return the next recurring instance when needed."""
		self.completed = True
		return self.create_next_occurrence(completion_date=completion_date)

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
		task.pet_name = self.name
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

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by their HH:MM time value."""
		return sorted(
			tasks,
			key=lambda task: tuple(int(part) for part in task.time.split(":")),
		)

	def detect_task_conflicts(self, tasks: list[Task]) -> list[str]:
		"""Return warning messages for tasks that share the same scheduled time."""
		tasks_by_time: dict[str, list[Task]] = defaultdict(list)
		for task in tasks:
			tasks_by_time[task.time].append(task)

		warnings: list[str] = []
		for time_value, same_time_tasks in sorted(tasks_by_time.items()):
			if len(same_time_tasks) < 2:
				continue

			labels = [
				f"{task.title} for {task.pet_name}" if task.pet_name else task.title
				for task in same_time_tasks
			]
			warnings.append(
				f"Warning: {len(same_time_tasks)} tasks are scheduled at {time_value}: {', '.join(labels)}"
			)

		return warnings

	def filter_tasks(
		self,
		tasks: list[Task],
		*,
		completed: bool | None = None,
		pet_name: str | None = None,
	) -> list[Task]:
		"""Filter tasks by completion status, pet name, or both."""
		filtered_tasks = tasks
		if completed is not None:
			filtered_tasks = [task for task in filtered_tasks if task.completed is completed]
		if pet_name is not None:
			normalized_pet_name = pet_name.strip().lower()
			filtered_tasks = [
				task for task in filtered_tasks if task.pet_name.lower() == normalized_pet_name
			]
		return filtered_tasks

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

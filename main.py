"""Temporary testing ground to verify PawPal+ logic in the terminal."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
	owner = Owner(name="Jordan Lee", email="jordan@example.com", preferences="Morning routines preferred")

	dog = Pet(name="Mochi", species="dog", age=4, care_notes="Needs a short walk before breakfast")
	cat = Pet(name="Pixel", species="cat", age=2, care_notes="Likes a calm play session")

	dog.add_task(Task(title="Morning walk", description="Neighborhood walk", time="08:30", duration_minutes=20, priority="high", category="exercise"))
	dog.add_task(Task(title="Breakfast", description="Serve measured food", time="07:15", duration_minutes=10, priority="high", category="feeding"))
	cat.add_task(Task(title="Playtime", description="Interactive toy session", time="09:00", duration_minutes=15, priority="medium", category="enrichment"))
	cat.add_task(Task(title="Grooming", description="Brush fur", time="06:45", duration_minutes=5, priority="low", category="care"))
	cat.tasks[-1].mark_complete()

	owner.add_pet(dog)
	owner.add_pet(cat)
	return owner


def print_today_schedule() -> None:
	owner = build_demo_owner()
	scheduler = Scheduler(available_minutes=60)
	schedule = scheduler.generate_schedule(owner)
	all_tasks = owner.get_all_tasks(include_completed=True)
	conflict_task_one = Task(
		title="Water bowl refill",
		description="Refresh water for Mochi",
		time="07:15",
		duration_minutes=5,
		priority="medium",
		category="care",
	)
	conflict_task_two = Task(
		title="Medication reminder",
		description="Daily supplement",
		time="07:15",
		duration_minutes=5,
		priority="high",
		category="health",
	)
	owner.pets[0].add_task(conflict_task_one)
	owner.pets[1].add_task(conflict_task_two)
	all_tasks = owner.get_all_tasks(include_completed=True)
	medication_task = Task(
		title="Medication",
		description="Daily heart medicine",
		frequency="daily",
		time="20:00",
		due_date=date(2026, 6, 30),
		duration_minutes=5,
		priority="high",
		category="health",
	)
	next_medication_task = medication_task.mark_complete(completion_date=date(2026, 6, 30))

	print("Today's Schedule")
	print("=================")
	print(f"Owner: {owner.name}")
	print()
	print("Tasks sorted by time")
	print("--------------------")
	for task in scheduler.sort_by_time(all_tasks):
		status = "done" if task.completed else "pending"
		print(f"{task.time} | {task.pet_name} | {task.title} ({status})")

	print()
	print("Conflict warnings")
	print("-----------------")
	warnings = scheduler.detect_task_conflicts(all_tasks)
	if warnings:
		for warning in warnings:
			print(warning)
	else:
		print("No task conflicts detected.")

	print()
	print("Pending tasks for Mochi")
	print("-----------------------")
	for task in scheduler.filter_tasks(all_tasks, completed=False, pet_name="Mochi"):
		print(f"{task.time} | {task.title}")

	print()
	print("Completed tasks")
	print("---------------")
	for task in scheduler.filter_tasks(all_tasks, completed=True):
		print(f"{task.time} | {task.pet_name} | {task.title}")

	print()
	print("Recurring task demo")
	print("-------------------")
	print(
		f"Completed: {medication_task.title} due {medication_task.due_date} -> next due {next_medication_task.due_date if next_medication_task else 'n/a'}"
	)

	print()

	if not schedule:
		print("No tasks fit within the available time.")
		return

	for entry in schedule:
		task = entry.task
		print(
			f"+{entry.start_minute:02d} min to +{entry.end_minute:02d} min | {task.title} "
			f"({task.duration_minutes} min, priority: {task.priority})"
		)

	print()
	print(scheduler.explain_plan(schedule))


if __name__ == "__main__":
	print_today_schedule()


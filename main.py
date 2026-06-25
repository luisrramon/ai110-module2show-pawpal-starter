"""Temporary testing ground to verify PawPal+ logic in the terminal."""

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
	owner = Owner(name="Jordan Lee", email="jordan@example.com", preferences="Morning routines preferred")

	dog = Pet(name="Mochi", species="dog", age=4, care_notes="Needs a short walk before breakfast")
	cat = Pet(name="Pixel", species="cat", age=2, care_notes="Likes a calm play session")

	dog.add_task(Task(title="Morning walk", description="Neighborhood walk", duration_minutes=20, priority="high", category="exercise"))
	dog.add_task(Task(title="Breakfast", description="Serve measured food", duration_minutes=10, priority="high", category="feeding"))
	cat.add_task(Task(title="Playtime", description="Interactive toy session", duration_minutes=15, priority="medium", category="enrichment"))

	owner.add_pet(dog)
	owner.add_pet(cat)
	return owner


def print_today_schedule() -> None:
	owner = build_demo_owner()
	scheduler = Scheduler(available_minutes=60)
	schedule = scheduler.generate_schedule(owner)

	print("Today's Schedule")
	print("=================")
	print(f"Owner: {owner.name}")
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


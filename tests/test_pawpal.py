from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
	task = Task(title="Morning walk", duration_minutes=20)

	assert task.completed is False

	task.mark_complete()

	assert task.completed is True


def test_daily_task_creates_next_day_occurrence() -> None:
	task = Task(title="Feed cat", frequency="daily", due_date=date(2026, 6, 29), duration_minutes=10)

	next_task = task.mark_complete(completion_date=date(2026, 6, 29))

	assert task.completed is True
	assert next_task is not None
	assert next_task.frequency == "daily"
	assert next_task.due_date == date(2026, 6, 30)
	assert next_task.completed is False


def test_weekly_task_creates_next_week_occurrence() -> None:
	task = Task(title="Brush fur", frequency="weekly", due_date=date(2026, 6, 29), duration_minutes=5)

	next_task = task.mark_complete(completion_date=date(2026, 6, 29))

	assert task.completed is True
	assert next_task is not None
	assert next_task.frequency == "weekly"
	assert next_task.due_date == date(2026, 7, 6)
	assert next_task.completed is False


def test_adding_task_increases_pet_task_count() -> None:
	pet = Pet(name="Mochi", species="dog")
	task = Task(title="Breakfast", duration_minutes=10)

	assert len(pet.tasks) == 0

	pet.add_task(task)

	assert len(pet.tasks) == 1
	assert pet.tasks[0] is task
	assert task.pet_name == "Mochi"


def test_sort_by_time_orders_tasks_chronologically() -> None:
	scheduler = Scheduler(available_minutes=60)
	tasks = [
		Task(title="Walk", time="14:00", duration_minutes=20),
		Task(title="Breakfast", time="08:15", duration_minutes=10),
		Task(title="Playtime", time="09:30", duration_minutes=15),
	]

	sorted_tasks = scheduler.sort_by_time(tasks)

	assert [task.title for task in sorted_tasks] == ["Breakfast", "Playtime", "Walk"]


def test_filter_tasks_by_completion_and_pet_name() -> None:
	scheduler = Scheduler(available_minutes=60)
	mochi = Pet(name="Mochi", species="dog")
	pixel = Pet(name="Pixel", species="cat")

	walk = Task(title="Morning walk", time="08:00", duration_minutes=20)
	walk.mark_complete()
	breakfast = Task(title="Breakfast", time="07:15", duration_minutes=10)
	playtime = Task(title="Playtime", time="09:00", duration_minutes=15)

	mochi.add_task(walk)
	mochi.add_task(breakfast)
	pixel.add_task(playtime)

	all_tasks = mochi.tasks + pixel.tasks

	completed_tasks = scheduler.filter_tasks(all_tasks, completed=True)
	mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
	mochi_pending_tasks = scheduler.filter_tasks(all_tasks, completed=False, pet_name="Mochi")

	assert [task.title for task in completed_tasks] == ["Morning walk"]
	assert [task.title for task in mochi_tasks] == ["Morning walk", "Breakfast"]
	assert [task.title for task in mochi_pending_tasks] == ["Breakfast"]


def test_detect_task_conflicts_returns_warning_for_shared_time() -> None:
	scheduler = Scheduler(available_minutes=60)
	mochi = Pet(name="Mochi", species="dog")
	pixel = Pet(name="Pixel", species="cat")

	first_task = Task(title="Breakfast", time="07:15", duration_minutes=10)
	second_task = Task(title="Water bowl refill", time="07:15", duration_minutes=5)
	third_task = Task(title="Playtime", time="09:00", duration_minutes=15)

	mochi.add_task(first_task)
	pixel.add_task(second_task)
	pixel.add_task(third_task)

	warnings = scheduler.detect_task_conflicts(mochi.tasks + pixel.tasks)

	assert len(warnings) == 1
	assert "07:15" in warnings[0]
	assert "Breakfast for Mochi" in warnings[0]
	assert "Water bowl refill for Pixel" in warnings[0]


def test_generate_schedule_returns_empty_list_for_owner_with_no_pets() -> None:
	owner = Owner(name="Jordan Lee", email="jordan@example.com")
	scheduler = Scheduler(available_minutes=60)

	schedule = scheduler.generate_schedule(owner)

	assert schedule == []


def test_generate_schedule_returns_empty_list_when_time_budget_is_zero() -> None:
	pet = Pet(name="Mochi", species="dog")
	pet.add_task(Task(title="Breakfast", duration_minutes=10, priority="high"))
	scheduler = Scheduler(available_minutes=0)

	schedule = scheduler.generate_schedule(pet)

	assert schedule == []


def test_generate_schedule_excludes_completed_tasks() -> None:
	pet = Pet(name="Mochi", species="dog")
	completed_task = Task(title="Morning walk", duration_minutes=20, priority="high")
	pending_task = Task(title="Breakfast", duration_minutes=10, priority="high")
	completed_task.mark_complete()
	pet.add_task(completed_task)
	pet.add_task(pending_task)
	scheduler = Scheduler(available_minutes=60)

	schedule = scheduler.generate_schedule(pet)

	assert [entry.task.title for entry in schedule] == ["Breakfast"]
	assert schedule[0].task.completed is False


def test_unsupported_recurring_task_returns_no_next_occurrence() -> None:
	task = Task(title="Special reminder", frequency="monthly", duration_minutes=5)

	next_task = task.mark_complete(completion_date=date(2026, 7, 6))

	assert task.completed is True
	assert next_task is None

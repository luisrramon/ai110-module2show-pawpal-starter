import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, email=owner_email)

st.session_state.owner.name = owner_name
st.session_state.owner.email = owner_email

owner = st.session_state.owner

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

st.markdown("### Add a Pet")
pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=4)
pet_notes = st.text_input("Care notes", value="")

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, age=int(pet_age), care_notes=pet_notes)
    owner.add_pet(new_pet)
    st.session_state.selected_pet_index = len(owner.pets) - 1
    st.success(f"Added {new_pet.name} to {owner.name}'s pets.")

if "selected_pet_index" not in st.session_state:
    st.session_state.selected_pet_index = 0

if owner.pets:
    selected_pet_index = st.selectbox(
        "Choose a pet for the task",
        range(len(owner.pets)),
        format_func=lambda index: f"{owner.pets[index].name} ({owner.pets[index].species})",
        index=min(st.session_state.selected_pet_index, len(owner.pets) - 1),
    )
    st.session_state.selected_pet_index = selected_pet_index
    selected_pet = owner.pets[selected_pet_index]
else:
    selected_pet = None

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age, "tasks": len(pet.tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Scheduling a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_description = st.text_input("Task description", value="")
task_category = st.text_input("Task category", value="general")
task_frequency = st.text_input("Task frequency", value="daily")

if st.button("Add task"):
    if selected_pet is None:
        st.error("Add a pet first, then assign the task to that pet.")
    else:
        new_task = Task(
            title=task_title,
            description=task_description,
            frequency=task_frequency,
            duration_minutes=int(duration),
            priority=priority,
            category=task_category,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added {new_task.title} to {selected_pet.name}.")

if owner.pets:
    st.write("Current tasks:")
    current_tasks = []
    for pet in owner.pets:
        for task in pet.tasks:
            current_tasks.append(
                {
                    "pet": pet.name,
                    "task": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "completed": task.completed,
                }
            )
    st.table(current_tasks)

st.divider()

st.subheader("Build Schedule")
st.caption("This button now calls your scheduling logic.")

available_minutes = st.number_input("Available minutes", min_value=0, max_value=480, value=60)
scheduler = Scheduler(available_minutes=int(available_minutes))

all_tasks = owner.get_all_tasks(include_completed=True)

if all_tasks:
    st.markdown("### Sorted tasks")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    st.table(
        [
            {
                "time": task.time,
                "pet": task.pet_name or "Unknown",
                "task": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "completed": task.completed,
            }
            for task in sorted_tasks
        ]
    )

    st.markdown("### Task filters")
    pending_tasks = scheduler.filter_tasks(all_tasks, completed=False)
    completed_tasks = scheduler.filter_tasks(all_tasks, completed=True)

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        st.write("Pending tasks")
        st.table(
            [
                {
                    "pet": task.pet_name or "Unknown",
                    "time": task.time,
                    "task": task.title,
                    "priority": task.priority,
                }
                for task in pending_tasks
            ]
            or [{"pet": "-", "time": "-", "task": "No pending tasks", "priority": "-"}]
        )
    with filter_col2:
        st.write("Completed tasks")
        st.table(
            [
                {
                    "pet": task.pet_name or "Unknown",
                    "time": task.time,
                    "task": task.title,
                    "priority": task.priority,
                }
                for task in completed_tasks
            ]
            or [{"pet": "-", "time": "-", "task": "No completed tasks", "priority": "-"}]
        )

    conflict_warnings = scheduler.detect_task_conflicts(all_tasks)
    if conflict_warnings:
        st.warning("Schedule conflict detected. Review the tasks below and adjust one of the overlapping times.")
        for warning in conflict_warnings:
            st.warning(warning)
    else:
        st.success("No task conflicts detected.")

if not all_tasks:
    st.info("Add pets and tasks above to see sorted, filtered, and conflict-aware scheduling views.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        schedule = scheduler.generate_schedule(owner)
        st.success("Today's schedule")
        for entry in schedule:
            pet_name_for_task = next(
                (pet.name for pet in owner.pets if entry.task in pet.tasks),
                "Unknown pet",
            )
            st.write(
                f"+{entry.start_minute:02d} to +{entry.end_minute:02d} min | "
                f"{entry.task.title} for {pet_name_for_task} "
                f"({entry.task.duration_minutes} min, priority: {entry.task.priority})"
            )
        st.markdown(scheduler.explain_plan(schedule))

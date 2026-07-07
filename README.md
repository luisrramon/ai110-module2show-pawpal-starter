# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
(.venv) luisramon@Mac ai110-module2show-pawpal-starter % python main.py           
Today's Schedule
=================
Owner: Jordan Lee

+00 min to +15 min | Playtime (15 min, priority: medium)
+15 min to +25 min | Breakfast (10 min, priority: high)
+25 min to +45 min | Morning walk (20 min, priority: high)

Planned tasks:
- Playtime: priority medium, 15 min, starts at +0 min
- Breakfast: priority high, 10 min, starts at +15 min
- Morning walk: priority high, 20 min, starts at +25 min
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

These tests cover the most important PawPal+ behaviors: task completion, daily and weekly recurrence, pet task assignment, chronological sorting, filtering by completion and pet name, conflict detection for duplicate times, and schedule generation edge cases such as empty pets, zero time budgets, and excluded completed tasks.

Successful test run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/luisramon/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 11 items                                                              

tests/test_pawpal.py ...........                                         [100%]

============================== 11 passed in 0.03s ==============================
```

Confidence Level: ★★★★★

Based on the current test results, the system is reliable for the behaviors covered by the suite. The main remaining risk is untested invalid-input handling, such as malformed times or negative values.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Sorts tasks by normalized `HH:MM` time values. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status, pet name, or both. |
| Conflict detection | `Scheduler.detect_task_conflicts()` | Returns warning messages when multiple tasks share the same time. |
| Recurring task logic | `Task.mark_complete()` and `Task.create_next_occurrence()` | Creates the next daily or weekly instance after completion using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

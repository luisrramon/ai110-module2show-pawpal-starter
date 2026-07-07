# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design centered on three core user actions: adding a pet to the system, scheduling
a walk or care task, and viewing today's tasks in a clear daily list.

- What classes did you include, and what responsibilities did you assign to each?

    - Four main classes: Owner, Pet, Task, and Scheduler
        - Owner class stores the pet owner's information and preferences and keeps track of their pets
        - Pet class stores each pet's basic details and the care tasks associated with that pet
        - Task class represents an individual care activity, such as a walk or feeding, and stores details like title, duration, priority, and completion status
        - Scheduler class is responsible for organizing tasks based on available time and priority, then generating a daily plan for the user


**b. Design changes**

- Did your design change during implementation?
Yes

- If yes, describe at least one change and why you made it.
    - I added validation for task priority and duration so the schedulerworks with consistent, predictable data.
    - I changed the scheduler to sort tasks by priority and filter them by available time so the plan is actually generated from the pet's pending tasks.
    - I added basic add/remove behavior for pets and tasks so the data model can manage relationships instead of leaving them as placeholders
    - I introduced a simple schedule entry model to make it easier to expand the plan output later with timing and explanation details.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- My scheduler considers task time, priority, duration, completion status, and pet name.
- I treated priority and time as the most important constraints because the plan should handle urgent tasks first and also detect conflicts.
- I used duration as a secondary constraint so tasks fit within the available time.
- Owner preferences matter more as a design detail than as a hard rule in the current version.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- One tradeoff is that the scheduler uses simple rules instead of a more advanced optimization algorithm.
- This is reasonable because PawPal+ is a small planning tool, and the simpler approach is easier to understand, test, and explain.
- It also keeps the schedule predictable for the user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used AI to compare the initial UML draft against the final Python implementation, identify missing behaviors, draft pytest cases, and tighten the Streamlit UI so the scheduler features were visible to a user.
- The most helpful prompts were specific and outcome-based, such as asking for edge cases to test, asking how the final UML should change after implementation, and asking how the README or UI should describe the actual behavior of the scheduler.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- I did not accept a generic scheduling suggestion that would have used a more complex optimization approach.
- I kept the scheduler rule-based because the project needed something easy to understand, easy to test, and aligned with the assignment scope.
- I verified the final behavior by running the pytest suite and checking the CLI output from `main.py` to confirm that sorting, recurrence, and conflict detection matched the code.

**c. AI strategy**

- The most effective AI coding assistant features were rapid codebase-aware editing, test drafting, and help translating implementation changes back into documentation like the UML and README.
- One AI suggestion I rejected was to overcomplicate the scheduling logic with a heavier algorithm; I simplified it to keep the system clean and explainable.
- Using separate chat sessions for different phases helped me stay organized because each phase had a different goal: design first, implementation next, testing after that, and documentation last.
- Working this way made me act as the lead architect: AI could move fast on details, but I still had to decide what belonged in the system, verify correctness, and keep the final design consistent across code, tests, UI, and documentation.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- I tested task completion, daily and weekly recurrence, adding tasks to pets, sorting tasks by time, filtering by completion and pet name, conflict detection for duplicate times, and schedule edge cases such as empty pets, zero available minutes, and completed-task exclusion.
- These tests mattered because they covered the scheduler's core behavior and the edge cases most likely to break a user-facing planning tool.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- I am fairly confident in the current scheduler because the core test suite passes and the outputs are consistent with the implemented logic.
- If I had more time, I would add invalid-input tests for malformed times, negative durations, invalid priorities, empty owner fields, and duplicate pet or task handling.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I am most satisfied with how the model, scheduler, tests, and documentation now line up with each other.
- The project feels coherent end-to-end: the UML matches the code, the tests match the behavior, and the Streamlit UI exposes the scheduler features clearly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- I would improve the task input flow in the UI, add stronger validation feedback, and make the scheduling explanation more detailed for the end user.
- I would also consider richer owner preference handling if the project needed more personalization.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- The biggest lesson was that AI is most useful when I use it as a fast collaborator, not as the authority.
- When I clearly defined the architecture and kept checking the code against the design, AI helped me move faster without losing control of the system.

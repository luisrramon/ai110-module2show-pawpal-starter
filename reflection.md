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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

There should be a class/implementation to add pets to the system. For each pet in the system, there should be a a function to see what tasks each pet needs and what the owners specifically want for their pet. Additionally, there should be a function to keep track of how long each pet needs to stay and when they need to leave. To add on to this idea, there should also be a class that removes pets out of the system when pets leave.

- What classes did you include, and what responsibilities did you assign to each?

There should be a Pet class to keep track of the pets, a Owner class to match the owners to the pets and make sure each pet checks out in time, a Task class to see what tasks need to be done for each pet, and maybe a Scheduler class in order to generate a plan and order tasks by priority. Furthermore, I think having a DailyPlan class to show the user all the information they need would be good. Finally, I think having a top-level class to manage the Owner class would be good, it could help with things like removing or adding Owners.

PawPalSystem → Owner → Pet → Task

Scheduler uses (Owner + Pet) → produces DailyPlan → contains ScheduledTask → wraps Task

**b. Design changes**

- Did your design change during implementation?

Yes, during implementation, I noticed some discrepancies with the relationships of the class with made things less Pythonic. Additionally, I wanted to add a priority system in my UML but the inital draft had strings like "low", "medium", and "high" which required manual mapping to numbers.

- If yes, describe at least one change and why you made it.
    
I made the Priority into enums which makes it easier to sort by using .value. I also added @dataclass on some of the core classes in my system which makes things more Pythonic.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

1. Time budget (_fits_in_budget) — a task is only scheduled if used_minutes + task.duration_minutes <= owner.available_minutes. Tasks that don't fit are moved to skipped_tasks.

2. Priority order (_sort_tasks) — tasks are sorted HIGH → MEDIUM → LOW before the budget check runs, so higher-priority tasks always get first access to the available time.

- How did you decide which constraints mattered most?

Time budget and priority were chosen because they're the only constraints that make a schedule actually usable — if you exceed the time budget the plan is impossible, and without priority there's no principled way to decide what to skip. Everything else, like preferred time or due dates, makes the schedule better but doesn't break it if missed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler commits to tasks greedily in priority order — once a high-priority task is added, that time is gone even if a combination of lower-priority tasks would make better use of the remaining budget.

- Why is that tradeoff reasonable for this scenario?

A greedy scheduler is reasonable here because pet care tasks aren't a math optimization problem — an owner with 60 minutes who walks their dog first isn't making a mistake, they're making a practical choice. The schedules are short (a handful of tasks per pet), so the edge cases where greedy fails rarely come up, and when they do, the owner can just reorder priorities manually. The simplicity is worth more than the occasional missed minute.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

    I used AI to help me brainstorm the ideas and design for this application. It really helped me to visualize how the system works and helped me have a better grasp of the system.

- What kinds of prompts or questions were most helpful?

    Simple questions where the AI can give clear concise answers are always the best.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

The AI sometimes add things that I think is unnecessary. When adding the methods for my classes, it would add redundant things that shouldn't be there.

- How did you evaluate or verify what the AI suggested?

I looked through it to see if it looked correct and I made sure to run tests and think of edge cases that make break what the AI suggested.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?

 Confidence Level: ⭐ ⭐ ⭐ ⭐

- What edge cases would you test next if you had more time?

I would probably add more confict detection edge cases.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I really liked handling the AI and learning the potential it has.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would probably change the UML design a bit, maybe make it more simple or complex depending on how I feel.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


Honestly, working with AI made me realize how much the design decisions still fall on you. The AI can write the code fast, but it doesn't know that a pet owner needs a plain-English fix suggestion instead of raw time windows — you have to know that and tell it. The biggest thing I took away is that the clearer your mental model of the system, the more useful the AI becomes. When I had the UML figured out and knew exactly what I wanted, the AI nailed it. When I was vague, I got generic output I had to fix anyway. You're not replaced as the architect — if anything, you have to be a better one, because the AI will confidently build the wrong thing if you let it.


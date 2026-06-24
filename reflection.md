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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

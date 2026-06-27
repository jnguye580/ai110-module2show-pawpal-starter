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

=== Today's Schedule ===

Daily plan for Mochi (dog):
  08:00 — Morning walk (30 min) [priority: high]
  08:30 — Feeding (10 min) [priority: high]
  08:40 — Enrichment puzzle (20 min) [priority: medium]
  Total: 60 / 90 min used

Daily plan for Biscuit (cat):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Grooming (15 min) [priority: medium]
  08:25 — Playtime (20 min) [priority: low]
  Total: 45 / 90 min used

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite, The suite covers the full lifecycle of the PawPalSystem:
python -m pytest

# Run with coverage:
pytest tests/ --cov=pawpal_system --cov-report=term-missing
```

Sample test output:

```
======================================================= test session starts =======================================================
platform darwin -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jereminguyen/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0, cov-7.1.0
collected 38 items                                                                                                                

tests/test_pawpal.py ......................................                                                                 [100%]

======================================================= 38 passed in 0.02s ========================================================
```
# Confidence Level: ⭐ ⭐ ⭐ ⭐ 

## ✨ Features

- **Sort by priority** — `Scheduler._sort_tasks()` ranks tasks HIGH → MEDIUM → LOW so the most important care always claims the time budget first.
- **Sort by preferred time** — `Scheduler.sort_by_time()` orders tasks by their `preferred_time` (HH:MM) ascending. Tasks with no time preference are pushed last using a `"99:99"` sentinel value.
- **Filter by completion status** — `Pet.filter_tasks(completed=)` returns pending, completed, or all tasks for a single pet. `Owner.get_tasks()` does the same across every pet an owner has.
- **Priority-first schedule generation** — `Scheduler.generate_plan()` greedily fits tasks into the owner's available minutes in priority order. Tasks that don't fit are stored in `DailyPlan.skipped_tasks` and shown as warnings in the UI.
- **Conflict warnings** — `Scheduler.find_conflicts(plan)` detects overlapping time slots within one pet's plan. `Scheduler.find_cross_pet_conflicts(plans)` catches overlaps across different pets. Each conflict is surfaced in the UI as a separate error card with the task names, time windows, and a suggested fix.
- **Daily and weekly recurrence** — marking a recurring task complete via `Pet.mark_task_complete()` automatically appends the next occurrence with the `due_date` advanced by 1 day (`"daily"`) or 7 days (`"weekly"`).

## 📐 Algorithm Reference

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority | `Scheduler._sort_tasks()` | HIGH → MEDIUM → LOW; used internally by `generate_plan()` |
| Sort by time | `Scheduler.sort_by_time()` | Ascending HH:MM; no-preference tasks go last via `"99:99"` |
| Filter by status | `Pet.filter_tasks(completed=)` | Single-pet; pass `None` to return all |
| Filter across pets | `Owner.get_tasks(pet_name=, completed=)` | Returns `(pet_name, task)` tuples |
| Budget enforcement | `Scheduler._fits_in_budget()` | Skips tasks exceeding `owner.available_minutes`; stored in `DailyPlan.skipped_tasks` |
| Single-pet conflict detection | `Scheduler.find_conflicts(plan)` | O(n²) pair comparison within one plan |
| Cross-pet conflict detection | `Scheduler.find_cross_pet_conflicts(plans)` | Same overlap logic across different pets' plans |
| Conflict warning strings | `Scheduler.warn_conflicts(plans)` | Generator; yields one formatted string per conflict |
| Recurring task generation | `Task.next_occurrence()`, `Pet.mark_task_complete()` | Supports `"daily"` (+1 day) and `"weekly"` (+7 days) |

## 📸 Demo Walkthrough

### UI features

The Streamlit app (`app.py`) is divided into four steps, each building on the last:

1. **Owner** — enter a name, how many minutes are available today, and a preferred start time.
2. **Pet** — enter the pet's name, species, breed, and age. Multiple pets can be added under the same owner.
3. **Tasks** — add care tasks with a title, duration, and priority (high / medium / low). Use the **Sort by Priority / Sort by Time** toggle to reorder the task table live using `Scheduler._sort_tasks()` or `Scheduler.sort_by_time()`.
4. **Build Schedule** — click "Generate schedule" to see the time-slotted daily plan, any tasks skipped because they exceeded the time budget, and any conflict warnings with task names, time windows, and a plain-English fix suggestion.

### Example workflow

1. Set owner Jordan — 90 minutes available, starting at 08:00.
2. Add pet Mochi (dog). Add tasks: Morning walk (30 min, high), Feeding (10 min, high), Enrichment puzzle (20 min, medium).
3. Toggle "Sort by Priority" — the table shows high-priority tasks first.
4. Click "Generate schedule" — Mochi's plan is built. All three tasks fit within 90 minutes. A green "No scheduling conflicts" banner confirms there are no overlaps.
5. Add a second pet Rex with a 30-minute Morning run starting at 08:00, then generate again — a conflict warning appears because Rex's run overlaps Mochi's walk.

### Sample CLI output (`python main.py`)

```
=== Today's Schedule ===

Daily plan for Mochi (dog):
  08:00 — Morning walk (30 min) [priority: high]
  08:30 — Feeding (10 min) [priority: high]
  08:40 — Morning walk (30 min) [priority: high]
  09:10 — Feeding (10 min) [priority: high]
  Skipped (time): Enrichment puzzle
  Total: 80 / 90 min used

Daily plan for Biscuit (cat):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Feeding (10 min) [priority: high]
  08:20 — Bath (20 min) [priority: medium]
  08:40 — Bath (20 min) [priority: medium]
  09:00 — Playtime (20 min) [priority: low]
  Total: 80 / 90 min used

=== Conflict Detection Demo ===

Daily plan for Rex (dog):
  08:00 — Morning run (30 min) [priority: high]
  Total: 30 / 60 min used

Daily plan for Luna (cat):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Grooming (20 min) [priority: medium]
  Total: 30 / 60 min used

WARNING: 'Morning run' (Rex, 08:00–08:30) conflicts with 'Feeding' (Luna, 08:00–08:10)
WARNING: 'Morning run' (Rex, 08:00–08:30) conflicts with 'Grooming' (Luna, 08:10–08:30)
```

---

## 🧠 What I Learned About Being the Lead Architect

Honestly, working with AI made me realize how much the design decisions still fall on you. The AI can write the code fast, but it doesn't know that a pet owner needs a plain-English fix suggestion instead of raw time windows — you have to know that and tell it. The biggest thing I took away is that the clearer your mental model of the system, the more useful the AI becomes. When I had the UML figured out and knew exactly what I wanted, the AI nailed it. When I was vague, I got generic output I had to fix anyway. You're not replaced as the architect — if anything, you have to be a better one, because the AI will confidently build the wrong thing if you let it.

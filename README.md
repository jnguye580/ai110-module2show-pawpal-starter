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
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting by priority | `Scheduler._sort_tasks()` | Sorts HIGH → MEDIUM → LOW before scheduling; highest-priority tasks claim the budget first |
| Task sorting by time | `Scheduler.sort_by_time()` | Sorts by `preferred_time` (HH:MM) ascending; tasks with no time set go last via `"99:99"` sentinel |
| Filtering by status | `Pet.filter_tasks(completed=)` | Returns pending, completed, or all tasks for a single pet |
| Filtering by pet / status | `Owner.get_tasks(pet_name=, completed=)` | Aggregates across all pets; returns `(pet_name, task)` tuples |
| Budget enforcement | `Scheduler._fits_in_budget()` | Skips any task that would exceed `owner.available_minutes`; skipped tasks stored in `DailyPlan.skipped_tasks` |
| Conflict detection | `Scheduler.warn_conflicts()` | Generator that yields a warning string for every overlapping time slot across multiple pets' plans |
| Recurring tasks | `Task.next_occurrence()`, `Pet.mark_task_complete()` | Supports `"daily"` (+1 day) and `"weekly"` (+7 days); completing a recurring task automatically appends the next occurrence with an updated `due_date` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

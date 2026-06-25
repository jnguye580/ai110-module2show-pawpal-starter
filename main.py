from datetime import datetime
from pawpal_system import Owner, Pet, Task, Priority, PawPalSystem, Scheduler

system = PawPalSystem()

owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00")

# Simulate "today" so due_date output is predictable
TODAY = datetime(2026, 6, 25)

# Tasks added out of order — preferred_time intentionally scrambled
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)
mochi.add_task(Task(title="Enrichment puzzle", duration_minutes=20, priority=Priority.MEDIUM, preferred_time="14:00"))
mochi.add_task(Task(title="Morning walk",      duration_minutes=30, priority=Priority.HIGH,   preferred_time="08:00",
                    is_recurring=True, recurrence_frequency="daily"))
mochi.add_task(Task(title="Feeding",           duration_minutes=10, priority=Priority.HIGH,   preferred_time="07:30",
                    is_recurring=True, recurrence_frequency="daily"))

biscuit = Pet(name="Biscuit", species="cat", breed="Tabby", age_years=5)
biscuit.add_task(Task(title="Playtime", duration_minutes=20, priority=Priority.LOW,    preferred_time="15:00"))
biscuit.add_task(Task(title="Feeding",  duration_minutes=10, priority=Priority.HIGH,   preferred_time="07:00",
                      is_recurring=True, recurrence_frequency="daily"))
biscuit.add_task(Task(title="Bath",     duration_minutes=20, priority=Priority.MEDIUM, preferred_time="10:00",
                      is_recurring=True, recurrence_frequency="weekly"))

owner.add_pet(mochi)
owner.add_pet(biscuit)
system.add_owner(owner)

scheduler_mochi   = system.get_scheduler(owner.name, "Mochi")
scheduler_biscuit = system.get_scheduler(owner.name, "Biscuit")

# --- Recurring task completion → next occurrence ---
print("=== Recurring Task Completion ===\n")
print(f"Today: {TODAY.strftime('%Y-%m-%d')}\n")

for pet, titles in [(mochi, ["Morning walk", "Feeding"]), (biscuit, ["Feeding", "Bath"])]:
    for title in titles:
        next_task = pet.mark_task_complete(title, today=TODAY)
        completed = pet.get_task(title)
        print(f"[{pet.name}] Completed '{title}'")
        print(f"         due_date on completed task : {completed.due_date}")
        print(f"         Next occurrence due_date   : {next_task.due_date.strftime('%Y-%m-%d')} "
              f"(+{next_task._RECURRENCE_DAYS[next_task.recurrence_frequency]} day(s))")
        print()

# --- Sort by preferred_time ---
print("=== Sort by preferred_time ===\n")
for pet_name, scheduler in [("Mochi", scheduler_mochi), ("Biscuit", scheduler_biscuit)]:
    pet_obj = owner.get_pet(pet_name)
    sorted_tasks = scheduler.sort_by_time(pet_obj.tasks)
    print(f"{pet_name}:")
    for t in sorted_tasks:
        time_label = t.preferred_time if t.preferred_time else "(no time)"
        due = f"  due {t.due_date.strftime('%Y-%m-%d')}" if t.due_date else ""
        print(f"  {time_label}  {t.title} [{t.priority.name.lower()}]{due}")
    print()

# --- Filter by completion status ---
print("=== Filter by completion status ===\n")
pending = owner.get_tasks(completed=False)
print("Pending tasks (all pets):")
for pet_name, task in pending:
    due = f"  due {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
    print(f"  [{pet_name}] {task.title}{due}")

print()
done = owner.get_tasks(completed=True)
print("Completed tasks (all pets):")
for pet_name, task in done:
    print(f"  [{pet_name}] {task.title}")

# --- Generated schedule ---
print("\n=== Today's Schedule ===\n")
for pet in owner.pets:
    scheduler = system.get_scheduler(owner.name, pet.name)
    plan = scheduler.generate_plan()
    print(plan.explain())
    print()

# --- Conflict detection demo ---
# Both pets start at 08:00, so their tasks will overlap
print("=== Conflict Detection Demo ===\n")
conflict_owner = Owner(name="Alex", available_minutes=60, preferred_start_time="08:00")

rex = Pet(name="Rex", species="dog", breed="Labrador", age_years=2)
rex.add_task(Task(title="Morning run", duration_minutes=30, priority=Priority.HIGH))

luna = Pet(name="Luna", species="cat", breed="Siamese", age_years=4)
luna.add_task(Task(title="Feeding",  duration_minutes=10, priority=Priority.HIGH))
luna.add_task(Task(title="Grooming", duration_minutes=20, priority=Priority.MEDIUM))

conflict_owner.add_pet(rex)
conflict_owner.add_pet(luna)
system.add_owner(conflict_owner)

plans = [system.get_scheduler("Alex", p.name).generate_plan() for p in conflict_owner.pets]
for plan in plans:
    print(plan.explain())
    print()

warnings = list(Scheduler.warn_conflicts(plans))
if warnings:
    for w in warnings:
        print(w)
else:
    print("No conflicts detected.")

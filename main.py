from pawpal_system import Owner, Pet, Task, Priority, PawPalSystem

system = PawPalSystem()

owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00")

# Tasks added out of order — preferred_time is intentionally scrambled
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)
mochi.add_task(Task(title="Enrichment puzzle", duration_minutes=20, priority=Priority.MEDIUM, preferred_time="14:00"))
mochi.add_task(Task(title="Morning walk",      duration_minutes=30, priority=Priority.HIGH,   preferred_time="08:00"))
mochi.add_task(Task(title="Feeding",           duration_minutes=10, priority=Priority.HIGH,   preferred_time="07:30"))

biscuit = Pet(name="Biscuit", species="cat", breed="Tabby", age_years=5)
biscuit.add_task(Task(title="Playtime", duration_minutes=20, priority=Priority.LOW,    preferred_time="15:00"))
biscuit.add_task(Task(title="Feeding",  duration_minutes=10, priority=Priority.HIGH,   preferred_time="07:00"))
biscuit.add_task(Task(title="Grooming", duration_minutes=15, priority=Priority.MEDIUM, preferred_time=""))  # no time preference

owner.add_pet(mochi)
owner.add_pet(biscuit)
system.add_owner(owner)

# Mark one task complete to demonstrate filtering
mochi.get_task("Feeding").mark_complete()

scheduler_mochi   = system.get_scheduler(owner.name, "Mochi")
scheduler_biscuit = system.get_scheduler(owner.name, "Biscuit")

# --- Sort by time ---
print("=== Sort by preferred_time ===\n")
for pet, scheduler in [("Mochi", scheduler_mochi), ("Biscuit", scheduler_biscuit)]:
    tasks = system.get_owner(owner.name).get_pet(pet).tasks
    sorted_tasks = scheduler.sort_by_time(tasks)
    print(f"{pet}:")
    for t in sorted_tasks:
        time_label = t.preferred_time if t.preferred_time else "(no time)"
        print(f"  {time_label}  {t.title} [{t.priority.name.lower()}]")
    print()

# --- Filter by completion status ---
print("=== Filter by completion status ===\n")

pending = owner.get_tasks(completed=False)
print("Pending tasks (all pets):")
for pet_name, task in pending:
    print(f"  [{pet_name}] {task.title}")

print()
done = owner.get_tasks(completed=True)
print("Completed tasks (all pets):")
for pet_name, task in done:
    print(f"  [{pet_name}] {task.title}")

# --- Filter by pet name ---
print()
print("=== Filter by pet name (Biscuit only, all statuses) ===\n")
for pet_name, task in owner.get_tasks(pet_name="Biscuit"):
    status = "done" if task.completed else "pending"
    print(f"  {task.title} [{task.priority.name.lower()}] — {status}")

# --- Generated schedule ---
print("\n=== Today's Schedule ===\n")
for pet in owner.pets:
    scheduler = system.get_scheduler(owner.name, pet.name)
    plan = scheduler.generate_plan()
    print(plan.explain())
    print()

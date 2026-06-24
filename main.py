from pawpal_system import Owner, Pet, Task, Priority, PawPalSystem

system = PawPalSystem()

owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00")

mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority=Priority.HIGH))
mochi.add_task(Task(title="Feeding", duration_minutes=10, priority=Priority.HIGH))
mochi.add_task(Task(title="Enrichment puzzle", duration_minutes=20, priority=Priority.MEDIUM))

biscuit = Pet(name="Biscuit", species="cat", breed="Tabby", age_years=5)
biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority=Priority.HIGH))
biscuit.add_task(Task(title="Grooming", duration_minutes=15, priority=Priority.MEDIUM))
biscuit.add_task(Task(title="Playtime", duration_minutes=20, priority=Priority.LOW))

owner.add_pet(mochi)
owner.add_pet(biscuit)
system.add_owner(owner)

print("=== Today's Schedule ===\n")
for pet in owner.pets:
    scheduler = system.get_scheduler(owner.name, pet.name)
    plan = scheduler.generate_plan()
    print(plan.explain())
    print()

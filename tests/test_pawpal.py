import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Priority, Scheduler, PawPalSystem


def make_task(title="Morning walk", duration=30, priority=Priority.HIGH,
              preferred_time="", is_recurring=False, recurrence_frequency=""):
    return Task(
        title=title,
        duration_minutes=duration,
        priority=priority,
        preferred_time=preferred_time,
        is_recurring=is_recurring,
        recurrence_frequency=recurrence_frequency,
    )


def make_pet():
    return Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)


def make_owner(minutes=90):
    return Owner(name="Jordan", available_minutes=minutes, preferred_start_time="08:00")


# --- Task completion ---

def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_mark_complete_is_idempotent():
    task = make_task()
    task.mark_complete()
    task.mark_complete()
    assert task.completed is True


# --- Task addition ---

def test_add_task_increases_count():
    pet = make_pet()
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1


def test_add_multiple_tasks_increases_count():
    pet = make_pet()
    pet.add_task(make_task("Walk", 30, Priority.HIGH))
    pet.add_task(make_task("Feeding", 10, Priority.MEDIUM))
    assert len(pet.tasks) == 2


def test_add_duplicate_task_raises():
    pet = make_pet()
    pet.add_task(make_task())
    with pytest.raises(ValueError):
        pet.add_task(make_task())


# --- Edge cases ---

def test_task_invalid_priority_raises():
    with pytest.raises(ValueError):
        Task(title="Walk", duration_minutes=30, priority="high")


def test_task_invalid_priority_bool_raises():
    with pytest.raises(ValueError):
        Task(title="Walk", duration_minutes=30, priority=True)


def test_remove_nonexistent_task_raises():
    pet = make_pet()
    with pytest.raises(ValueError):
        pet.remove_task("Nonexistent")


def test_pet_tasks_empty_by_default():
    pet = make_pet()
    assert pet.tasks == []


# --- Recurring tasks / next_occurrence ---

def test_daily_task_advances_due_date_by_one_day():
    task = make_task(is_recurring=True, recurrence_frequency="daily")
    today = datetime(2026, 6, 25)
    next_task = task.next_occurrence(today)
    assert next_task.due_date == datetime(2026, 6, 26)


def test_weekly_task_advances_due_date_by_seven_days():
    task = make_task(is_recurring=True, recurrence_frequency="weekly")
    today = datetime(2026, 6, 25)
    next_task = task.next_occurrence(today)
    assert next_task.due_date == datetime(2026, 7, 2)


def test_next_occurrence_returns_incomplete_task():
    task = make_task(is_recurring=True, recurrence_frequency="daily")
    task.mark_complete()
    next_task = task.next_occurrence(datetime(2026, 6, 25))
    assert next_task.completed is False


def test_next_occurrence_on_non_recurring_raises():
    task = make_task(is_recurring=False)
    with pytest.raises(ValueError):
        task.next_occurrence(datetime(2026, 6, 25))


def test_invalid_recurrence_frequency_raises():
    with pytest.raises(ValueError):
        make_task(is_recurring=True, recurrence_frequency="monthly")


# --- Pet.mark_task_complete ---

def test_recurring_task_appends_new_instance():
    pet = make_pet()
    pet.add_task(make_task(is_recurring=True, recurrence_frequency="daily"))
    assert len(pet.tasks) == 1
    pet.mark_task_complete("Morning walk", today=datetime(2026, 6, 25))
    assert len(pet.tasks) == 2


def test_non_recurring_task_does_not_grow_list():
    pet = make_pet()
    pet.add_task(make_task())
    pet.mark_task_complete("Morning walk")
    assert len(pet.tasks) == 1


def test_mark_task_complete_returns_none_for_non_recurring():
    pet = make_pet()
    pet.add_task(make_task())
    result = pet.mark_task_complete("Morning walk")
    assert result is None


def test_mark_task_complete_returns_new_task_for_recurring():
    pet = make_pet()
    pet.add_task(make_task(is_recurring=True, recurrence_frequency="daily"))
    result = pet.mark_task_complete("Morning walk", today=datetime(2026, 6, 25))
    assert result is not None
    assert result.completed is False
    assert result.due_date == datetime(2026, 6, 26)


def test_mark_nonexistent_task_complete_raises():
    pet = make_pet()
    with pytest.raises(ValueError):
        pet.mark_task_complete("Nonexistent")


# --- Filtering ---

def test_filter_tasks_pending_excludes_completed():
    pet = make_pet()
    pet.add_task(make_task("Walk"))
    pet.add_task(make_task("Feeding", 10, Priority.MEDIUM))
    pet.tasks[0].mark_complete()
    pending = pet.filter_tasks(completed=False)
    assert len(pending) == 1
    assert pending[0].title == "Feeding"


def test_filter_tasks_completed_returns_only_done():
    pet = make_pet()
    pet.add_task(make_task("Walk"))
    pet.add_task(make_task("Feeding", 10, Priority.MEDIUM))
    pet.tasks[0].mark_complete()
    done = pet.filter_tasks(completed=True)
    assert len(done) == 1
    assert done[0].title == "Walk"


def test_filter_tasks_none_returns_all():
    pet = make_pet()
    pet.add_task(make_task("Walk"))
    pet.add_task(make_task("Feeding", 10, Priority.MEDIUM))
    pet.tasks[0].mark_complete()
    assert len(pet.filter_tasks()) == 2


# --- Scheduler: sort_by_time ---

def test_sort_by_time_orders_ascending():
    owner = make_owner()
    pet = make_pet()
    pet.add_task(make_task("Afternoon puzzle", 20, Priority.MEDIUM, preferred_time="14:00"))
    pet.add_task(make_task("Morning walk",     30, Priority.HIGH,   preferred_time="08:00"))
    pet.add_task(make_task("Early feeding",    10, Priority.HIGH,   preferred_time="07:00"))
    scheduler = Scheduler(owner, pet)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    assert [t.preferred_time for t in sorted_tasks] == ["07:00", "08:00", "14:00"]


def test_sort_by_time_no_preferred_time_goes_last():
    owner = make_owner()
    pet = make_pet()
    pet.add_task(make_task("No-time task", 20, Priority.MEDIUM, preferred_time=""))
    pet.add_task(make_task("Morning walk", 30, Priority.HIGH,   preferred_time="08:00"))
    scheduler = Scheduler(owner, pet)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    assert sorted_tasks[0].title == "Morning walk"
    assert sorted_tasks[-1].title == "No-time task"


# --- Scheduler: generate_plan ---

def test_generate_plan_skips_tasks_over_budget():
    owner = make_owner(minutes=30)
    pet = make_pet()
    pet.add_task(make_task("Walk",    30, Priority.HIGH))
    pet.add_task(make_task("Feeding", 10, Priority.HIGH))
    plan = Scheduler(owner, pet).generate_plan()
    assert len(plan.scheduled_tasks) == 1
    assert len(plan.skipped_tasks) == 1
    assert plan.skipped_tasks[0].title == "Feeding"


def test_generate_plan_respects_priority_order():
    owner = make_owner(minutes=30)
    pet = make_pet()
    pet.add_task(make_task("Low task",  30, Priority.LOW))
    pet.add_task(make_task("High task", 30, Priority.HIGH))
    plan = Scheduler(owner, pet).generate_plan()
    assert plan.scheduled_tasks[0].task.title == "High task"
    assert plan.skipped_tasks[0].title == "Low task"


# --- Conflict detection ---

def test_warn_conflicts_detects_overlap():
    owner = make_owner()
    pet_a = Pet(name="Rex",  species="dog", breed="Lab",     age_years=2)
    pet_b = Pet(name="Luna", species="cat", breed="Siamese", age_years=4)
    pet_a.add_task(make_task("Morning run", 30, Priority.HIGH))
    pet_b.add_task(make_task("Feeding",     10, Priority.HIGH))
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)
    system = PawPalSystem()
    system.add_owner(owner)
    plans = [system.get_scheduler(owner.name, p.name).generate_plan() for p in owner.pets]
    warnings = list(Scheduler.warn_conflicts(plans))
    assert len(warnings) == 1
    assert "WARNING" in warnings[0]


def test_warn_conflicts_no_overlap_yields_nothing():
    owner_a = make_owner()
    owner_b = Owner(name="Sam", available_minutes=90, preferred_start_time="12:00")
    pet_a = Pet(name="Rex",  species="dog", breed="Lab",     age_years=2)
    pet_b = Pet(name="Luna", species="cat", breed="Siamese", age_years=4)
    pet_a.add_task(make_task("Morning run", 30, Priority.HIGH))
    pet_b.add_task(make_task("Feeding",     10, Priority.HIGH))
    owner_a.add_pet(pet_a)
    owner_b.add_pet(pet_b)
    system = PawPalSystem()
    system.add_owner(owner_a)
    system.add_owner(owner_b)
    plan_a = system.get_scheduler(owner_a.name, "Rex").generate_plan()
    plan_b = system.get_scheduler(owner_b.name, "Luna").generate_plan()
    warnings = list(Scheduler.warn_conflicts([plan_a, plan_b]))
    assert warnings == []

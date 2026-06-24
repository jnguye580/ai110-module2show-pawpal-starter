import pytest
from pawpal_system import Pet, Task, Priority


def make_task(title="Morning walk", duration=30, priority=Priority.HIGH):
    return Task(title=title, duration_minutes=duration, priority=priority)


def make_pet():
    return Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)


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

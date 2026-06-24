from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class PawPalSystem:
    def __init__(self):
        self.owners: list[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def remove_owner(self, owner_name: str) -> None:
        self.owners = [o for o in self.owners if o.name != owner_name]

    def get_owner(self, owner_name: str) -> Optional[Owner]:
        return next((o for o in self.owners if o.name == owner_name), None)

    def get_scheduler(self, owner_name: str, pet_name: str) -> "Scheduler":
        owner = self.get_owner(owner_name)
        if owner is None:
            raise ValueError(f"Owner '{owner_name}' not found.")
        pet = next((p for p in owner.pets if p.name == pet_name), None)
        if pet is None:
            raise ValueError(f"Pet '{pet_name}' not found for owner '{owner_name}'.")
        return Scheduler(owner, pet)


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferred_start_time: str  # "HH:MM"
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if any(p.name == pet.name for p in self.pets):
            raise ValueError(f"Pet '{pet.name}' already exists for owner '{self.name}'.")
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        if not any(p.name == pet_name for p in self.pets):
            raise ValueError(f"Pet '{pet_name}' not found for owner '{self.name}'.")
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        return next((p for p in self.pets if p.name == pet_name), None)


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if any(t.title == task.title for t in self.tasks):
            raise ValueError(f"Task '{task.title}' already exists for pet '{self.name}'.")
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        if not any(t.title == task_name for t in self.tasks):
            raise ValueError(f"Task '{task_name}' not found for pet '{self.name}'.")
        self.tasks = [t for t in self.tasks if t.title != task_name]

    def get_task(self, task_name: str) -> Optional[Task]:
        return next((t for t in self.tasks if t.title == task_name), None)

    def high_priority_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.priority == Priority.HIGH]


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    is_recurring: bool = False
    recurrence_frequency: str = ""
    notes: str = ""

    def __post_init__(self):
        if not isinstance(self.priority, Priority):
            raise ValueError(f"priority must be a Priority enum, got {self.priority!r}")

    def is_high_priority(self) -> bool:
        return self.priority == Priority.HIGH


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> "DailyPlan":
        plan = DailyPlan(pet=self.pet, owner=self.owner)
        used = 0
        for task in self._sort_tasks(self.pet.tasks):
            if self._fits_in_budget(task, used):
                plan.add_entry(task)
                used += task.duration_minutes
            else:
                plan.skipped_tasks.append(task)
        return plan

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    def _fits_in_budget(self, task: Task, used: int) -> bool:
        return used + task.duration_minutes <= self.owner.available_minutes


class DailyPlan:
    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.owner = owner
        self.start_time: datetime = datetime.strptime(owner.preferred_start_time, "%H:%M")
        self.scheduled_tasks: list[ScheduledTask] = []
        self.skipped_tasks: list[Task] = []

    def add_entry(self, task: Task) -> None:
        start = self.start_time + timedelta(minutes=self.total_minutes())
        end = start + timedelta(minutes=task.duration_minutes)
        self.scheduled_tasks.append(ScheduledTask(task=task, start_time=start, end_time=end))

    def total_minutes(self) -> int:
        return sum(t.task.duration_minutes for t in self.scheduled_tasks)

    def explain(self) -> str:
        lines = [f"Daily plan for {self.pet.name} ({self.pet.species}):"]
        for entry in self.scheduled_tasks:
            lines.append(
                f"  {entry.start_time:%H:%M} — {entry.task.title} "
                f"({entry.task.duration_minutes} min) [priority: {entry.task.priority.name.lower()}]"
            )
        if self.skipped_tasks:
            skipped = ", ".join(t.title for t in self.skipped_tasks)
            lines.append(f"  Skipped (time): {skipped}")
        lines.append(f"  Total: {self.total_minutes()} / {self.owner.available_minutes} min used")
        return "\n".join(lines)


@dataclass
class ScheduledTask:
    task: Task
    start_time: datetime
    end_time: datetime

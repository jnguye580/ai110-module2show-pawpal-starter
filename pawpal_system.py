class PawPalSystem:
    def __init__(self):
        self.owners: list = []

    def add_owner(self, owner: "Owner") -> None:
        pass

    def remove_owner(self, owner_name: str) -> None:
        pass

    def get_owner(self, owner_name: str) -> "Owner":
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str):
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.pets: list = []

    def add_pet(self, pet: "Pet") -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass


class Pet:
    def __init__(self, name: str, species: str, breed: str, age_years: int):
        self.name = name
        self.species = species
        self.breed = breed
        self.age_years = age_years
        self.tasks: list = []

    def add_task(self, task: "Task") -> None:
        pass

    def remove_task(self, task_name: str) -> None:
        pass


class Task:
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        priority: str,
        is_recurring: bool = False,
        recurrence_frequency: str = "",
        notes: str = "",
    ):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_recurring = is_recurring
        self.recurrence_frequency = recurrence_frequency
        self.notes = notes

    def is_high_priority(self) -> bool:
        pass


class Scheduler:
    def __init__(self, owner: "Owner", pet: "Pet"):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> "DailyPlan":
        pass

    def _sort_tasks(self, tasks: list) -> list:
        pass

    def _fits_in_budget(self, task: "Task", used: int) -> bool:
        pass


class DailyPlan:
    def __init__(self, pet: "Pet", start_time: str):
        self.pet = pet
        self.start_time = start_time
        self.scheduled_tasks: list = []
        self.skipped_tasks: list = []

    def add_entry(self, task: "Task", start_offset: int) -> None:
        pass

    def total_minutes(self) -> int:
        pass

    def explain(self) -> str:
        pass


class ScheduledTask:
    def __init__(self, task: "Task", start_time: str, end_time: str):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

import streamlit as st
from pawpal_system import PawPalSystem, Owner, Pet, Task, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan your pet's day — add tasks, sort by priority or time, and catch scheduling conflicts before they happen.")

# --- Session state initialization ---
if "system" not in st.session_state:
    st.session_state.system = PawPalSystem()
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

system: PawPalSystem = st.session_state.system

# --- Owner setup ---
st.subheader("1. Owner")
col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Available minutes", min_value=1, max_value=480, value=60)
with col3:
    preferred_start = st.text_input("Start time (HH:MM)", value="08:00")

if st.button("Set owner", use_container_width=True):
    existing = system.get_owner(owner_name)
    if existing is not None:
        st.session_state.owner = existing
        st.info(f"Loaded existing owner **{owner_name}**.")
    else:
        new_owner = Owner(
            name=owner_name,
            available_minutes=int(available_minutes),
            preferred_start_time=preferred_start,
        )
        system.add_owner(new_owner)
        st.session_state.owner = new_owner
        st.success(f"Owner **{owner_name}** created.")

if st.session_state.owner:
    o = st.session_state.owner
    st.success(f"Active owner: **{o.name}** — {o.available_minutes} min available, starting at {o.preferred_start_time}")

st.divider()

# --- Pet setup ---
st.subheader("2. Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Mixed")
with col4:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Set pet", use_container_width=True):
    if st.session_state.owner is None:
        st.error("Set an owner first.")
    else:
        owner: Owner = st.session_state.owner
        existing_pet = owner.get_pet(pet_name)
        if existing_pet is not None:
            st.session_state.pet = existing_pet
            st.info(f"Loaded existing pet **{pet_name}**.")
        else:
            new_pet = Pet(name=pet_name, species=species, breed=breed, age_years=int(age))
            owner.add_pet(new_pet)
            st.session_state.pet = new_pet
            st.success(f"Pet **{pet_name}** added.")

if st.session_state.pet:
    p = st.session_state.pet
    st.success(f"Active pet: **{p.name}** — {p.species}, {p.breed}, {p.age_years} yrs old")

st.divider()

# --- Task setup ---
st.subheader("3. Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task", use_container_width=True):
    if st.session_state.pet is None:
        st.error("Set a pet first.")
    else:
        pet: Pet = st.session_state.pet
        if pet.get_task(task_title) is not None:
            st.warning(f"**{task_title}** already exists for {pet.name}. Choose a different title.")
        else:
            priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority_map[priority_str],
            )
            pet.add_task(new_task)
            st.session_state.tasks = [
                {"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority.name.lower()}
                for t in pet.tasks
            ]
            st.success(f"Task **{task_title}** added ({duration} min, {priority_str} priority).")

PRIORITY_BADGE = {"high": "🔴 high", "medium": "🟡 medium", "low": "🟢 low"}

if st.session_state.tasks:
    sort_mode = st.radio("Sort tasks by", ["Priority", "Time"], horizontal=True)

    if st.session_state.owner and st.session_state.pet:
        scheduler = system.get_scheduler(st.session_state.owner.name, st.session_state.pet.name)
        raw_tasks = st.session_state.pet.tasks
        sorted_tasks = (
            scheduler._sort_tasks(raw_tasks)
            if sort_mode == "Priority"
            else scheduler.sort_by_time(raw_tasks)
        )
        display = [
            {
                "Title": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": PRIORITY_BADGE.get(t.priority.name.lower(), t.priority.name.lower()),
                "Preferred time": t.preferred_time or "—",
            }
            for t in sorted_tasks
        ]
    else:
        display = [
            {
                "Title": row["title"],
                "Duration (min)": row["duration_minutes"],
                "Priority": PRIORITY_BADGE.get(row["priority"], row["priority"]),
                "Preferred time": "—",
            }
            for row in st.session_state.tasks
        ]

    st.table(display)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule generation ---
st.subheader("4. Build Schedule")

if st.button("Generate schedule", use_container_width=True):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.error("Set an owner and a pet before generating a schedule.")
    else:
        scheduler = system.get_scheduler(st.session_state.owner.name, st.session_state.pet.name)
        plan = scheduler.generate_plan()

        # Scheduled tasks as a clean table
        if plan.scheduled_tasks:
            st.success(f"Schedule built — {plan.total_minutes()} of {st.session_state.owner.available_minutes} minutes used.")
            schedule_rows = [
                {
                    "Time": f"{entry.start_time:%H:%M} – {entry.end_time:%H:%M}",
                    "Task": entry.task.title,
                    "Duration (min)": entry.task.duration_minutes,
                    "Priority": PRIORITY_BADGE.get(entry.task.priority.name.lower(), entry.task.priority.name.lower()),
                }
                for entry in plan.scheduled_tasks
            ]
            st.table(schedule_rows)
        else:
            st.warning("No tasks could be scheduled. Check that tasks fit within the available time budget.")

        # Skipped tasks
        if plan.skipped_tasks:
            skipped_names = ", ".join(f"**{t.title}**" for t in plan.skipped_tasks)
            st.warning(f"Skipped (exceeded time budget): {skipped_names}")

        # Conflict warnings — one callout per conflict so each is actionable
        conflicts = scheduler.find_conflicts(plan)
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} scheduling conflict{'s' if len(conflicts) > 1 else ''} detected — review the tasks below and shorten or reschedule one from each pair.")
            for a, b in conflicts:
                st.error(
                    f"**Conflict:** {a.task.title} ({a.start_time:%H:%M}–{a.end_time:%H:%M}) "
                    f"overlaps with {b.task.title} ({b.start_time:%H:%M}–{b.end_time:%H:%M})\n\n"
                    f"Tip: reduce the duration of **{a.task.title}** or move **{b.task.title}** to a different time."
                )
        else:
            st.success("No scheduling conflicts — your plan looks great!")

import streamlit as st
from pawpal_system import PawPalSystem, Owner, Pet, Task, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

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
st.subheader("Owner")
col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Available minutes", min_value=1, max_value=480, value=60)
with col3:
    preferred_start = st.text_input("Start time (HH:MM)", value="08:00")

if st.button("Set owner"):
    existing = system.get_owner(owner_name)
    if existing is not None:
        st.session_state.owner = existing
        st.info(f"Loaded existing owner '{owner_name}' from the system.")
    else:
        new_owner = Owner(
            name=owner_name,
            available_minutes=int(available_minutes),
            preferred_start_time=preferred_start,
        )
        system.add_owner(new_owner)
        st.session_state.owner = new_owner
        st.success(f"Created new owner '{owner_name}'.")

if st.session_state.owner:
    o = st.session_state.owner
    st.caption(f"Active owner: **{o.name}** — {o.available_minutes} min available, starts at {o.preferred_start_time}")

st.divider()

# --- Pet setup ---
st.subheader("Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Mixed")
with col4:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Set pet"):
    if st.session_state.owner is None:
        st.error("Set an owner first.")
    else:
        owner: Owner = st.session_state.owner
        existing_pet = owner.get_pet(pet_name)
        if existing_pet is not None:
            st.session_state.pet = existing_pet
            st.info(f"Loaded existing pet '{pet_name}' from the owner.")
        else:
            new_pet = Pet(name=pet_name, species=species, breed=breed, age_years=int(age))
            owner.add_pet(new_pet)
            st.session_state.pet = new_pet
            st.success(f"Created new pet '{pet_name}'.")

if st.session_state.pet:
    p = st.session_state.pet
    st.caption(f"Active pet: **{p.name}** ({p.species}, {p.breed}, {p.age_years} yrs)")

st.divider()

# --- Task setup ---
st.subheader("Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.pet is None:
        st.error("Set a pet first.")
    else:
        pet: Pet = st.session_state.pet
        if pet.get_task(task_title) is not None:
            st.warning(f"Task '{task_title}' already exists for {pet.name}.")
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
            st.success(f"Added task '{task_title}'.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule generation ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.error("Set an owner and a pet before generating a schedule.")
    else:
        scheduler = system.get_scheduler(st.session_state.owner.name, st.session_state.pet.name)
        plan = scheduler.generate_plan()
        st.text(plan.explain())

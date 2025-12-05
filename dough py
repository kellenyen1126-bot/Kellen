import streamlit as st
import random

st.title("Mini Blox Fruits Game")

# Step 1: Choose a fruit
fruits = ["T-Rex Fruit", "Tiger Fruit", "Dragon Fruit"]
if "fruit" not in st.session_state:
    st.session_state.fruit = None
if "health" not in st.session_state:
    st.session_state.health = 100

st.subheader("Pick a fruit:")
col1, col2, col3 = st.columns(3)
if col1.button("T-Rex Fruit"):
    st.session_state.fruit = "T-Rex Fruit"
if col2.button("Tiger Fruit"):
    st.session_state.fruit = "Tiger Fruit"
if col3.button("Dragon Fruit"):
    st.session_state.fruit = "Dragon Fruit"

if st.session_state.fruit:
    st.success(f"You picked {st.session_state.fruit}!")

# Step 2: Use skill
st.subheader("Use your skill:")
if st.session_state.fruit:
    if st.button("Attack"):
        damage = random.randint(10, 30)
        st.session_state.health -= damage
        st.write(f"You used {st.session_state.fruit}'s skill and took {damage} damage!")
        st.write(f"Your health: {st.session_state.health}")
        if st.session_state.health <= 0:
            st.error("You have been defeated! Restart the game.")
else:
    st.info("Pick a fruit first!")

# Step 3: Reset game
if st.button("Reset Game"):
    st.session_state.fruit = None
    st.session_state.health = 100
    st.experimental_rerun()

import streamlit as st
import math
import time

# -----------------------------
# Initialize game state
# -----------------------------
if "ball_x" not in st.session_state:
    st.session_state.ball_x = 4
    st.session_state.ball_y = 7
    st.session_state.hole_x = 4
    st.session_state.hole_y = 1
    st.session_state.angle = 90   # degrees
    st.session_state.power = 1
    st.session_state.strokes = 0
    st.session_state.moving = False

st.title("⛳ Streamlit Mini Golf")

# -----------------------------
# Controls
# -----------------------------
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⬅️ Angle"):
        st.session_state.angle = max(0, st.session_state.angle - 10)

with c2:
    if st.button("➡️ Angle"):
        st.session_state.angle = min(180, st.session_state.angle + 10)

with c3:
    if st.button("💥 Hit"):
        st.session_state.moving = True
        st.session_state.strokes += 1

st.slider("Power", 1, 5, key="power")
st.write(f"🎯 Angle: {st.session_state.angle}°")
st.write(f"⛳ Strokes: {st.session_state.strokes}")

# -----------------------------
# Move ball
# -----------------------------
if st.session_state.moving:
    rad = math.radians(st.session_state.angle)
    dx = round(math.cos(rad))
    dy = -round(math.sin(rad))

    for _ in range(st.session_state.power):
        st.session_state.ball_x += dx
        st.session_state.ball_y += dy

        st.session_state.ball_x = max(0, min(8, st.session_state.ball_x))
        st.session_state.ball_y = max(0, min(8, st.session_state.ball_y))

        time.sleep(0.15)
        st.experimental_rerun()

    st.session_state.moving = False

# -----------------------------
# Draw field (9x9)
# -----------------------------
field = [["⬜" for _ in range(9)] for _ in range(9)]

field[st.session_state.hole_y][st.session_state.hole_x] = "🕳️"
field[st.session_state.ball_y][st.session_state.ball_x] = "⚪"

for row in field:
    st.write("".join(row))

# -----------------------------
# Win condition
# -----------------------------
if (
    st.session_state.ball_x == st.session_state.hole_x
    and st.session_state.ball_y == st.session_state.hole_y
):
    st.success(f"🏆 Hole completed in {st.session_state.strokes} strokes!")
    if st.button("🔄 New Hole"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()

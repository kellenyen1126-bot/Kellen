import streamlit as st
import random
import time

# --------------------
# 初始化 session state
# --------------------
if "player_x" not in st.session_state:
    st.session_state.player_x = 4
    st.session_state.enemy_x = random.randint(0, 8)
    st.session_state.enemy_y = 0
    st.session_state.score = 0
    st.session_state.game_over = False

# --------------------
# 標題
# --------------------
st.title("🎮 Streamlit Dodge Game")

# --------------------
# 控制按鈕
# --------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️"):
        st.session_state.player_x = max(0, st.session_state.player_x - 1)

with col3:
    if st.button("➡️"):
        st.session_state.player_x = min(8, st.session_state.player_x + 1)

# --------------------
# 遊戲邏輯
# --------------------
if not st.session_state.game_over:
    st.session_state.enemy_y += 1

    if st.session_state.enemy_y > 8:
        st.session_state.enemy_y = 0
        st.session_state.enemy_x = random.randint(0, 8)
        st.session_state.score += 1

    # 碰撞判定
    if (
        st.session_state.enemy_y == 8
        and st.session_state.enemy_x == st.session_state.player_x
    ):
        st.session_state.game_over = True

# --------------------
# 畫遊戲畫面（9x9）
# --------------------
grid = [["⬜" for _ in range(9)] for _ in range(9)]

# 玩家
grid[8][st.session_state.player_x] = "🟦"

# 敵人
if not st.session_state.game_over:
    grid[st.session_state.enemy_y][st.session_state.enemy_x] = "🟥"

for row in grid:
    st.write("".join(row))

# --------------------
# 分數
# --------------------
st.subheader(f"Score: {st.session_state.score}")

# --------------------
# Game Over
# --------------------
if st.session_state.game_over:
    st.error("💥 GAME OVER")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# 自動刷新（動畫）
time.sleep(0.4)
st.experimental_rerun()


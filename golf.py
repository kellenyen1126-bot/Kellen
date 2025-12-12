import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import math
import time

st.set_page_config(page_title="City Golf Game")

# 地圖大小
MAP_WIDTH = 600
MAP_HEIGHT = 400

BALL_RADIUS = 10

# 初始化球位置
if "ball_pos" not in st.session_state:
    st.session_state.ball_pos = [50, 350]  # x, y

# 洞的位置
hole_pos = [550, 50]

# 建築障礙 [x1, y1, x2, y2]
obstacles = [
    [200, 300, 250, 350],
    [350, 150, 400, 300],
    [100, 50, 150, 100]
]

# 力量和方向
if "drag_start" not in st.session_state:
    st.session_state.drag_start = None

# Canvas: 用來畫輔助線
canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=2,
    stroke_color="red",
    background_color="lightgreen",
    width=MAP_WIDTH,
    height=MAP_HEIGHT,
    drawing_mode="line",
    key="canvas",
    initial_drawing=None
)

# 取得滑鼠拖曳事件
if canvas_result.json_data is not None:
    objs = canvas_result.json_data["objects"]
    if len(objs) > 0:
        line = objs[-1]
        x0, y0 = line["left"], line["top"]
        x1, y1 = x0 + line["width"], y0 + line["height"]

        # 計算方向向量和距離
        dx = x1 - x0
        dy = y1 - y0
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx /= distance
            dy /= distance

            # 球沿方向滾動
            steps = int(distance / 5)
            bx, by = st.session_state.ball_pos
            for _ in range(steps):
                nx, ny = bx + dx*5, by + dy*5
                # 邊界檢查
                if nx < BALL_RADIUS or nx > MAP_WIDTH-BALL_RADIUS:
                    break
                if ny < BALL_RADIUS or ny > MAP_HEIGHT-BALL_RADIUS:
                    break
                # 障礙物檢查
                hit_obstacle = False
                for obs in obstacles:
                    if obs[0] <= nx <= obs[2] and obs[1] <= ny <= obs[3]:
                        hit_obstacle = True
                        break
                if hit_obstacle:
                    break
                bx, by = nx, ny
                # 畫動畫
                st.session_state.ball_pos = [bx, by]
                draw_html = f"""
                <div style="position:relative;width:{MAP_WIDTH}px;height:{MAP_HEIGHT}px;background-color:lightgreen;">
                    <div style="
                        position:absolute;width:{BALL_RADIUS*2}px;height:{BALL_RADIUS*2}px;
                        border-radius:50%;background-color:white;
                        left:{bx-BALL_RADIUS}px;top:{by-BALL_RADIUS}px;"></div>
                    <div style="
                        position:absolute;width:{BALL_RADIUS*2}px;height:{BALL_RADIUS*2}px;
                        border-radius:50%;background-color:yellow;
                        left:{hole_pos[0]-BALL_RADIUS}px;top:{hole_pos[1]-BALL_RADIUS}px;"></div>
                    {"".join([f'<div style="position:absolute;background-color:grey;left:{obs[0]}px;top:{obs[1]}px;width:{obs[2]-obs[0]}px;height:{obs[3]-obs[1]}px;"></div>' for obs in obstacles])}
                </div>
                """
                st.markdown(draw_html, unsafe_allow_html=True)
                time.sleep(0.01)

# 畫靜態球、洞、建築
bx, by = st.session_state.ball_pos
st.markdown(
    f"""
    <div style="position:relative;width:{MAP_WIDTH}px;height:{MAP_HEIGHT}px;background-color:lightgreen;">
        <div style="
            position:absolute;width:{BALL_RADIUS*2}px;height:{BALL_RADIUS*2}px;
            border-radius:50%;background-color:white;
            left:{bx-BALL_RADIUS}px;top:{by-BALL_RADIUS}px;"></div>
        <div style="
            position:absolute;width:{BALL_RADIUS*2}px;height:{BALL_RADIUS*2}px;
            border-radius:50%;background-color:yellow;
            left:{hole_pos[0]-BALL_RADIUS}px;top:{hole_pos[1]-BALL_RADIUS}px;"></div>
        {"".join([f'<div style="position:absolute;background-color:grey;left:{obs[0]}px;top:{obs[1]}px;width:{obs[2]-obs[0]}px;height:{obs[3]-obs[1]}px;"></div>' for obs in obstacles])}
    </div>
    """,
    unsafe_allow_html=True
)

# 判定是否進洞
if math.hypot(bx-hole_pos[0], by-hole_pos[1]) < BALL_RADIUS*2:
    st.success("🎉 球進洞了！你贏了！")

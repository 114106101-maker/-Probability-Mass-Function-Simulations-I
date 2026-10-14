import time
import textwrap
import numpy as np
import pandas as pd
import streamlit as st
from math import comb

# ============================================================
# 1. 頁面配置
# ============================================================
st.set_page_config(
    page_title="📊 機率模擬實驗 | Probability Simulations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CSS：保留原本的簡潔卡片風格
# ============================================================
custom_css = textwrap.dedent("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #ffffff !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", sans-serif !important;
    color: #1c1c1e !important;
}
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px;
}
.card {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.06);
}
.ios-kpi-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 14px 10px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.06);
}
.ios-kpi-title {
    font-size: 12px;
    font-weight: 500;
    color: #8e8e93;
    margin-bottom: 4px;
    line-height: 1.3;
}
.ios-kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #1c1c1e;
}
div[data-testid="stSidebar"] {
    background-color: #f8f9fa !important;
    border-right: 1px solid rgba(0, 0, 0, 0.06);
}
div.stButton > button {
    border-radius: 16px !important;
    background-color: #ffffff !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    padding: 0.6rem 0.25rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.2s ease !important;
}
div.stButton > button, div.stButton > button p, div.stButton > button span {
    color: #1c1c1e !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
div.stButton > button:hover {
    background-color: #f2f2f7 !important;
    transform: translateY(-5px) scale(1.05) !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #007aff 0%, #0056b3 100%) !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3) !important;
}
div.stButton > button[kind="primary"],
div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {
    color: #ffffff !important;
}
</style>
""")
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================
# 3. KPI 卡片
# ============================================================
def render_kpi_html(title_cn, title_en, val, color="#1c1c1e"):
    return textwrap.dedent(f"""
    <div class="ios-kpi-card">
        <div class="ios-kpi-title">{title_cn}<br><span style="font-size:10px;">{title_en}</span></div>
        <div class="ios-kpi-value" style="color: {color};">{val}</div>
    </div>
    """)

# ============================================================
# 4. 理論值
# ============================================================
def theoretical_sim1_p_x3():
    # X ~ Hypergeometric(N=40, K=8, n=10)
    return comb(8, 3) * comb(32, 7) / comb(40, 10)


def theoretical_sim2_p_y_gt_3():
    # Y ~ Geometric(p=0.8)
    # Y > 3 表示前三次都失敗
    return (1 - 0.8) ** 3

# ============================================================
# 5. 模擬函式
# ============================================================
@st.cache_data
def run_simulation_1(total_n, seed):
    rng = np.random.default_rng(seed)

    # 1 = 缺陷，0 = 正常
    data = np.array([1] * 8 + [0] * 32)

    # 每次不放回抽取 10 個
    x_values = np.empty(total_n, dtype=int)
    for i in range(total_n):
        sample = rng.choice(data, size=10, replace=False)
        x_values[i] = np.sum(sample)

    cumulative_mean = np.cumsum(x_values) / np.arange(1, total_n + 1)
    cumulative_p_x3 = np.cumsum(x_values == 3) / np.arange(1, total_n + 1)

    return x_values, cumulative_mean, cumulative_p_x3


@st.cache_data
def run_simulation_2(total_n, seed):
    rng = np.random.default_rng(seed)

    # Y = 第一次成功所需的傳輸次數，p(success)=0.8
    y_values = rng.geometric(p=0.8, size=total_n)

    cumulative_mean = np.cumsum(y_values) / np.arange(1, total_n + 1)
    cumulative_p_y_gt_3 = np.cumsum(y_values > 3) / np.arange(1, total_n + 1)

    return y_values, cumulative_mean, cumulative_p_y_gt_3

# ============================================================
# 6. Streamlit 原生圖表
#    不依賴 Plotly，避免 Streamlit Cloud 缺少 plotly 套件
# ============================================================
def make_histogram_df(values, max_x=None):
    if max_x is None:
        max_x = int(np.max(values))

    min_x = 0 if np.min(values) == 0 else 1
    x_values = np.arange(min_x, max_x + 1)
    counts = np.array([np.sum(values == x) for x in x_values])
    relative_frequency = counts / len(values)

    return pd.DataFrame({
        "相對次數": relative_frequency
    }, index=x_values)

# ============================================================
# 7. Session State
# ============================================================
if "simulation_type" not in st.session_state:
    st.session_state.simulation_type = "模擬一：軟體缺陷抽樣檢查"
if "anim_status" not in st.session_state:
    st.session_state.anim_status = "idle"
if "current_step_idx" not in st.session_state:
    st.session_state.current_step_idx = 0
if "total_n" not in st.session_state:
    st.session_state.total_n = 10000

# ============================================================
# 8. Sidebar 控制面板
# ============================================================
with st.sidebar:
    st.header("⚙️ 控制面板 (Control Panel)")

    def sync_simulation_change():
        st.session_state.anim_status = "idle"
        st.session_state.current_step_idx = 0

    st.markdown("**選擇模擬 (Select Simulation)**")
    simulation_type = st.radio(
        "Simulation",
        ["模擬一：軟體缺陷抽樣檢查", "模擬二：網路封包遺失與重傳"],
        index=0 if st.session_state.simulation_type.startswith("模擬一") else 1,
        key="simulation_radio",
        on_change=sync_simulation_change,
        label_visibility="collapsed"
    )
    st.session_state.simulation_type = simulation_type

    st.markdown("**模擬總次數 (N) / Total Simulations**")
    total_n = st.number_input(
        "輸入模擬次數",
        min_value=100,
        max_value=10000,
        value=st.session_state.total_n,
        step=100,
        key="total_n_input",
        label_visibility="collapsed"
    )
    st.session_state.total_n = total_n

    fps = st.slider("動畫速率 (FPS) / Speed", 2, 25, 8)
    seed = st.number_input("隨機種子 (Seed) / Random Seed", 0, 9999, 42)

    st.divider()
    col_b1, col_b2, col_b3 = st.columns(3)
    start_click = col_b1.button("🚀 開始 Start", type="primary", use_container_width=True)
    pause_label = "▶️ 繼續 Resume" if st.session_state.anim_status == "paused" else "⏸️ 暫停 Pause"
    pause_click = col_b2.button(pause_label, use_container_width=True)
    quick_click = col_b3.button("⚡ 結算 Finish", use_container_width=True)

    if start_click:
        st.session_state.anim_status = "running"
        st.session_state.current_step_idx = 0
        st.rerun()

    if pause_click:
        if st.session_state.anim_status == "running":
            st.session_state.anim_status = "paused"
        elif st.session_state.anim_status == "paused":
            st.session_state.anim_status = "running"
        st.rerun()

    if quick_click:
        st.session_state.anim_status = "finished"
        st.session_state.current_step_idx = 0
        st.rerun()

# ============================================================
# 9. 依照選擇執行模擬
# ============================================================
if simulation_type.startswith("模擬一"):
    values, cumulative_mean, cumulative_probability = run_simulation_1(total_n, seed)
    theory_probability = theoretical_sim1_p_x3()
    theory_mean = 2.0
    event_label = "P(X = 3)"
    mean_label = "E(X)"
    title = "💻 模擬一：軟體缺陷抽樣檢查"
else:
    values, cumulative_mean, cumulative_probability = run_simulation_2(total_n, seed)
    theory_probability = theoretical_sim2_p_y_gt_3()
    theory_mean = 1 / 0.8
    event_label = "P(Y > 3)"
    mean_label = "E(Y)"
    title = "📡 模擬二：網路封包遺失與重傳"

# ============================================================
# 10. 頁面說明
# ============================================================
if simulation_type.startswith("模擬一"):
    description = f"""
    <div class="card">
        <div style="font-size:22px;font-weight:800;margin-bottom:8px;">{title}</div>
        <div style="font-size:14px;line-height:1.7;color:#3a3a3c;">
        📌 <b>實驗設定：</b>共有 40 個待檢查程式，其中 8 個有缺陷、32 個正常。<br>
        每次<b>不放回</b>隨機抽取 10 個程式，令 <b>X</b> 為抽到的缺陷程式數。<br>
        重複模擬 <b>{total_n:,}</b> 次，觀察 X 的相對次數。<br>
        🎯 理論平均：<b>E(X) = 10 × 8 / 40 = 2</b><br>
        🎯 理論 {event_label}：<b>{theory_probability:.6f}</b>
        </div>
    </div>
    """
else:
    description = f"""
    <div class="card">
        <div style="font-size:22px;font-weight:800;margin-bottom:8px;">{title}</div>
        <div style="font-size:14px;line-height:1.7;color:#3a3a3c;">
        📌 <b>實驗設定：</b>每次封包傳輸成功的機率為 <b>0.8</b>，各次傳輸互相獨立。<br>
        持續重傳直到第一次成功，令 <b>Y</b> 為所需傳輸次數。<br>
        重複模擬 <b>{total_n:,}</b> 次，觀察 Y 的相對次數。<br>
        🎯 理論平均：<b>E(Y) = 1 / 0.8 = 1.25</b><br>
        🎯 理論 {event_label}：<b>{theory_probability:.6f}</b>
        </div>
    </div>
    """

st.markdown(description, unsafe_allow_html=True)

# ============================================================
# 11. 動畫資料
# ============================================================
num_frames = min(total_n, 60)
frame_indices = np.unique(np.linspace(1, total_n, num=num_frames, dtype=int))

st.subheader("📈 數據儀表板 (Data Dashboard)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
spot_kpi1 = kpi1.empty()
spot_kpi2 = kpi2.empty()
spot_kpi3 = kpi3.empty()
spot_kpi4 = kpi4.empty()

chart_spot = st.empty()
conv_spot = st.empty()

# ============================================================
# 12. 渲染目前畫面
# ============================================================
def render_frame_ui(frame_n):
    current_values = values[:frame_n]
    current_probability = cumulative_probability[frame_n - 1]
    current_mean = cumulative_mean[frame_n - 1]

    if simulation_type.startswith("模擬一"):
        current_event_count = int(np.sum(current_values == 3))
        event_text = f"{current_probability:.4f}"
        kpi2_text = f"{current_event_count}"
        chart_title = "X 的相對次數直方圖"
        x_title = "X = 抽到的缺陷程式數"
        max_x = 8
        conv_title = "P(X=3) 收斂軌跡"
        conv_y_title = "模擬 P(X=3)"
    else:
        current_event_count = int(np.sum(current_values > 3))
        event_text = f"{current_probability:.4f}"
        kpi2_text = f"{current_event_count}"
        chart_title = "Y 的相對次數直方圖"
        x_title = "Y = 第一次成功所需傳輸次數"
        max_x = min(max(8, int(np.percentile(values, 99))), 15)
        conv_title = "P(Y>3) 收斂軌跡"
        conv_y_title = "模擬 P(Y>3)"

    spot_kpi1.markdown(render_kpi_html("模擬次數", "Simulations", f"{frame_n:,}"), unsafe_allow_html=True)
    spot_kpi2.markdown(render_kpi_html(f"{event_label} 發生次數", "Event Count", kpi2_text), unsafe_allow_html=True)
    spot_kpi3.markdown(render_kpi_html(f"模擬 {event_label}", "Simulation", event_text, "#007AFF"), unsafe_allow_html=True)
    spot_kpi4.markdown(render_kpi_html(f"理論 {event_label}", "Theory", f"{theory_probability:.4f}", "#FF3B30"), unsafe_allow_html=True)

    chart_spot.markdown(f"### {chart_title}")
    chart_spot.bar_chart(
        make_histogram_df(current_values, max_x=max_x),
        use_container_width=True
    )

    df_conv = pd.DataFrame({
        "模擬值": cumulative_probability[:frame_n],
        "理論值": [theory_probability] * frame_n
    }, index=np.arange(1, frame_n + 1))
    conv_spot.markdown(f"### {conv_title}")
    conv_spot.line_chart(
        df_conv,
        use_container_width=True
    )

    st.caption(f"目前平均值 {mean_label} = {current_mean:.4f} ｜ 理論平均 = {theory_mean:.4f}")

# ============================================================
# 13. Start / Pause / Finish
# ============================================================
if st.session_state.anim_status == "idle":
    render_frame_ui(1)
    st.info("👈 請點擊左側 **「🚀 開始 / Start」** 播放動畫，或 **「⚡ 結算 / Finish」** 直接觀看完整結果。")

elif st.session_state.anim_status == "finished":
    render_frame_ui(total_n)
    final_probability = cumulative_probability[-1]
    final_mean = cumulative_mean[-1]
    st.success(
        f"🎉 模擬完成！{event_label} 模擬值 = {final_probability:.6f}，"
        f"理論值 = {theory_probability:.6f}，"
        f"誤差 = {abs(final_probability - theory_probability):.6f}；"
        f"平均值 = {final_mean:.6f}，理論平均 = {theory_mean:.6f}。"
    )

elif st.session_state.anim_status == "paused":
    current_n = frame_indices[st.session_state.current_step_idx]
    render_frame_ui(current_n)
    st.warning(f"⏸️ 動畫已暫停於第 {current_n:,} 次模擬，點擊左側 **「▶️ 繼續 / Resume」** 可繼續播放。")

elif st.session_state.anim_status == "running":
    progress_bar = st.progress(0)
    start_idx = st.session_state.current_step_idx

    for idx in range(start_idx, len(frame_indices)):
        st.session_state.current_step_idx = idx
        current_n = frame_indices[idx]
        progress_bar.progress(int((idx + 1) / len(frame_indices) * 100))
        render_frame_ui(current_n)
        time.sleep(1 / fps)

    progress_bar.empty()
    st.session_state.anim_status = "finished"
    st.rerun()

# ============================================================
# 14. 最終統計表
# ============================================================
if st.session_state.anim_status in ["paused", "finished"]:
    st.subheader("📊 指定模擬次數統計結果 (Summary Table)")
    targets = [n for n in [100, 500, 1000, 2500, 5000, 10000] if n <= total_n]

    rows = []
    for n in targets:
        rows.append({
            "模擬次數 / Simulations": n,
            f"模擬 {event_label}": f"{cumulative_probability[n-1]:.6f}",
            f"模擬 {mean_label}": f"{cumulative_mean[n-1]:.6f}",
            f"理論 {event_label}": f"{theory_probability:.6f}",
            f"理論 {mean_label}": f"{theory_mean:.6f}"
        })

    table_df = pd.DataFrame(rows)
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    # 題目要求的最後答案
    st.subheader("📝 題目要求結果")
    final_probability = cumulative_probability[-1]
    final_mean = cumulative_mean[-1]

    result_col1, result_col2 = st.columns(2)
    with result_col1:
        st.markdown(f"**理論 {event_label}：** `{theory_probability:.6f}`")
        st.markdown(f"**模擬 {event_label}：** `{final_probability:.6f}`")
    with result_col2:
        st.markdown(f"**理論 {mean_label}：** `{theory_mean:.6f}`")
        st.markdown(f"**模擬 {mean_label}：** `{final_mean:.6f}`")

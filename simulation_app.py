import time
import textwrap
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import altair as alt
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
.inspect-card { background:#f8f9fa; border-radius:18px; padding:16px; margin:8px 0 18px 0; border:1px solid rgba(0,0,0,.06); }
.inspect-title { font-size:16px; font-weight:750; margin-bottom:10px; }
.inspect-grid { display:grid; grid-template-columns:repeat(5,minmax(70px,1fr)); gap:8px; }
.inspect-item { background:#fff; border-radius:14px; padding:10px 6px; text-align:center; border:1px solid rgba(0,0,0,.06); box-shadow:0 2px 8px rgba(0,0,0,.03); }
.inspect-item .num { font-size:11px; color:#8e8e93; }
.inspect-item .state { font-size:24px; margin:2px 0; }
.inspect-item .label { font-size:11px; font-weight:650; }
.inspect-success { color:#34c759; } .inspect-fail { color:#ff3b30; } .inspect-defect { color:#ff9500; } .inspect-normal { color:#007aff; }
.packet-scene { background:#fff; border:1px solid rgba(0,0,0,.07); border-radius:14px; padding:14px; margin:12px 0; }
.packet-lane { display:grid; grid-template-columns:76px minmax(100px,1fr) 76px; align-items:center; gap:10px; margin:10px 0; }
.packet-node { text-align:center; font-size:12px; font-weight:700; color:#4b5563; }
.packet-node .node-icon { font-size:25px; display:block; }
.packet-track { height:34px; position:relative; border-top:2px dashed #cbd5e1; margin-top:12px; }
.packet-track:before { content:""; position:absolute; right:-1px; top:-7px; border-left:10px solid #94a3b8; border-top:6px solid transparent; border-bottom:6px solid transparent; }
.packet-dot { position:absolute; left:0; top:-17px; width:34px; height:30px; border-radius:8px; background:#dbeafe; border:1px solid #60a5fa; display:flex; align-items:center; justify-content:center; font-size:17px; box-shadow:0 2px 5px rgba(0,0,0,.08); animation:packetMove 1.8s ease-in-out infinite; }
.packet-dot.failed { --travel: calc((100% - 34px) * .62); animation-name:packetFail; }
.packet-dot.success { --travel: calc(100% - 34px); animation-name:packetMove; }
@keyframes packetMove { 0% { left:0; } 75%,100% { left:var(--travel, calc(100% - 34px)); } }
@keyframes packetFail { 0% { left:0; opacity:1; } 60% { left:var(--travel); opacity:1; } 75%,100% { left:var(--travel); opacity:.15; } }
.packet-status { font-size:12px; font-weight:700; margin-top:2px; }
@media (max-width:700px) { .inspect-grid { grid-template-columns:repeat(5,minmax(50px,1fr)); gap:5px; } .inspect-item { padding:7px 3px; } .packet-lane { grid-template-columns:58px minmax(70px,1fr) 58px; gap:6px; } .packet-node { font-size:10px; } }
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

    # 逐次保存實際抽到的 10 個程式，方便模擬結束後查閱每一次的明細
    population = np.array([1] * 8 + [0] * 32, dtype=np.int8)
    samples = np.empty((total_n, 10), dtype=np.int8)
    for i in range(total_n):
        samples[i] = rng.choice(population, size=10, replace=False)

    x_values = samples.sum(axis=1)
    cumulative_mean = np.cumsum(x_values) / np.arange(1, total_n + 1)
    cumulative_p_x3 = np.cumsum(x_values == 3) / np.arange(1, total_n + 1)

    return x_values, cumulative_mean, cumulative_p_x3, samples


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
def make_histogram_df(values, max_x=None, simulation_type=None):
    """建立模擬相對次數與理論機率的對照資料。"""
    if max_x is None:
        max_x = int(np.max(values))

    min_x = 0 if simulation_type and simulation_type.startswith("模擬一") else 1
    x_values = np.arange(min_x, max_x + 1)
    counts = np.array([np.sum(values == x) for x in x_values])
    relative_frequency = counts / len(values)

    if simulation_type and simulation_type.startswith("模擬一"):
        # X ~ Hypergeometric(N=40, K=8, n=10)
        theoretical_probability = np.array([
            comb(8, int(x)) * comb(32, 10 - int(x)) / comb(40, 10)
            if 0 <= x <= 8 and 0 <= 10 - x <= 32 else 0.0
            for x in x_values
        ])
    else:
        # Y ~ Geometric(p=0.8), P(Y=y)=0.8*(0.2)^(y-1)
        theoretical_probability = 0.8 * np.power(0.2, x_values - 1)

    return pd.DataFrame({
        "模擬相對次數": relative_frequency,
        "理論機率": theoretical_probability,
    }, index=x_values)

# ============================================================
# 7. 檢查動畫資料
# ============================================================
@st.cache_data
def build_inspection_records_1(total_n, seed, num_records=60):
    """建立模擬一的逐次抽樣檢查動畫紀錄。"""
    rng = np.random.default_rng(seed)
    data = np.array([1] * 8 + [0] * 32)
    indices = np.unique(np.linspace(1, total_n, num=min(total_n, num_records), dtype=int))
    target_set = set(indices.tolist())
    records = {}
    for i in indices:
        sample = rng.choice(data, size=10, replace=False)
        records[int(i)] = sample.tolist()
    return records


@st.cache_data
def build_inspection_records_2(total_n, seed, num_records=60):
    """建立模擬二的逐次重傳動畫紀錄。"""
    rng = np.random.default_rng(seed)
    indices = np.unique(np.linspace(1, total_n, num=min(total_n, num_records), dtype=int))
    target_set = set(indices.tolist())
    records = {}
    for i in indices:
        records[int(i)] = int(rng.geometric(p=0.8))
    return records


def render_inspection_ui(frame_n):
    """顯示目前動畫畫面的實際檢查過程。"""
    checkpoint_pos = np.searchsorted(frame_indices, frame_n, side="right") - 1
    checkpoint_pos = max(0, checkpoint_pos)
    checkpoint = int(frame_indices[checkpoint_pos])

    if simulation_type.startswith("模擬一"):
        # 動畫顯示實際模擬資料，與圖表及結束後的明細一致
        sample = sample_matrix[checkpoint - 1].tolist()
        items = []
        for j, state in enumerate(sample, 1):
            if state == 1:
                icon, cls, label = "⚠️", "inspect-defect", "有缺陷"
            else:
                icon, cls, label = "✓", "inspect-normal", "正常"
            items.append(
                f'<div class="inspect-item"><div class="num">程式 {j}</div>'
                f'<div class="state {cls}">{icon}</div><div class="label {cls}">{label}</div></div>'
            )

        defect_count = int(sum(sample))
        inspection_spot.markdown(
            f'<div class="inspect-card">'
            f'<div class="inspect-title">🔎 第 {checkpoint:,} 次抽樣檢查：逐一檢查 10 個程式</div>'
            f'<div style="font-size:13px;color:#6e6e73;margin-bottom:10px;">'
            f'本次抽到 <b>{defect_count}</b> 個缺陷程式、<b>{10-defect_count}</b> 個正常程式。</div>'
            f'<div class="inspect-grid">{"".join(items)}</div></div>',
            unsafe_allow_html=True
        )
    else:
        attempts = int(values[checkpoint - 1])
        items = []
        lanes = []
        for j in range(1, attempts + 1):
            success = j == attempts
            icon = "✓" if success else "✕"
            cls = "inspect-success" if success else "inspect-fail"
            label = "封包抵達，傳輸成功" if success else "封包遺失，準備重傳"
            packet_cls = "success" if success else "failed"
            items.append(
                f'<div class="inspect-item"><div class="num">第 {j} 次</div>'
                f'<div class="state {cls}">{icon}</div><div class="label {cls}">{"成功" if success else "失敗"}</div></div>'
            )
            lanes.append(
                f'<div class="packet-lane">'
                f'<div class="packet-node"><span class="node-icon">💻</span>傳送端</div>'
                f'<div><div class="packet-track"><div class="packet-dot {packet_cls}" '
                f'style="animation-delay:{(j-1)*0.18:.2f}s; --travel:calc(100% - 34px);">📦</div></div>'
                f'<div class="packet-status {cls}">第 {j} 次：{label}</div></div>'
                f'<div class="packet-node"><span class="node-icon">🖥️</span>接收端</div>'
                f'</div>'
            )

        inspection_spot.markdown(
            f'<div class="inspect-card">'
            f'<div class="inspect-title">📡 第 {checkpoint:,} 次封包傳遞動畫</div>'
            f'<div style="font-size:13px;color:#6e6e73;margin-bottom:10px;">'
            f'每個 📦 代表一次封包傳送；紅色失敗封包會中途消失，直到綠色封包成功抵達。'
            f'本次共傳送 <b>{attempts}</b> 次。</div>'
            f'<div class="packet-scene">{"".join(lanes)}</div>'
            f'<div class="inspect-grid">{"".join(items)}</div></div>',
            unsafe_allow_html=True
        )

# ============================================================
# 8. Session State
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

    fps = st.slider("動畫速率 (FPS) / Speed", 2, 15, 6)
    sound_enabled = st.checkbox("🔊 開啟動畫提示音", value=True, help="每次動畫更新時播放短提示音；若瀏覽器阻擋自動播放，請先點擊頁面中的啟用音效按鈕。")
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
    values, cumulative_mean, cumulative_probability, sample_matrix = run_simulation_1(total_n, seed)
    theory_probability = theoretical_sim1_p_x3()
    theory_mean = 2.0
    event_label = "P(X = 3)"
    mean_label = "E(X)"
    title = "💻 模擬一：軟體缺陷抽樣檢查"
else:
    values, cumulative_mean, cumulative_probability = run_simulation_2(total_n, seed)
    sample_matrix = None
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
num_frames = min(total_n, 24)
frame_indices = np.unique(np.linspace(1, total_n, num=num_frames, dtype=int))

st.subheader("📈 數據儀表板 (Data Dashboard)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
spot_kpi1 = kpi1.empty()
spot_kpi2 = kpi2.empty()
spot_kpi3 = kpi3.empty()
spot_kpi4 = kpi4.empty()

# 抽樣動畫固定放在圖表上方
inspection_spot = st.empty()
chart_spot = st.empty()
conv_spot = st.empty()
mean_spot = st.empty()

# ============================================================
# 12. 渲染目前畫面
# ============================================================
def render_frame_ui(frame_n, play_sound=False):
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

    render_inspection_ui(frame_n)

    spot_kpi1.markdown(render_kpi_html("模擬次數", "Simulations", f"{frame_n:,}"), unsafe_allow_html=True)
    spot_kpi2.markdown(render_kpi_html(f"{event_label} 發生次數", "Event Count", kpi2_text), unsafe_allow_html=True)
    spot_kpi3.markdown(render_kpi_html(f"模擬 {event_label}", "Simulation", event_text, "#007AFF"), unsafe_allow_html=True)
    spot_kpi4.markdown(render_kpi_html(f"理論 {event_label}", "Theory", f"{theory_probability:.4f}", "#FF3B30"), unsafe_allow_html=True)

    # 使用固定容器包住標題與圖表，避免同一個 st.empty() 互相覆蓋位置
    with chart_spot.container():
        st.markdown(f"### {chart_title}")
        histogram_df = make_histogram_df(
            current_values,
            max_x=max_x,
            simulation_type=simulation_type,
        ).rename_axis("結果").reset_index()
        histogram_long = histogram_df.melt(
            id_vars="結果",
            value_vars=["模擬相對次數", "理論機率"],
            var_name="機率類型",
            value_name="機率",
        )
        # 用 xOffset 將兩組長條並排顯示，避免模擬值與理論值重疊
        histogram_chart = (
            alt.Chart(histogram_long)
            .mark_bar()
            .encode(
                x=alt.X("結果:O", title=x_title, axis=alt.Axis(labelAngle=0)),
                xOffset=alt.XOffset("機率類型:N"),
                y=alt.Y("機率:Q", title="機率", scale=alt.Scale(domainMin=0)),
                color=alt.Color("機率類型:N", title="圖例"),
                tooltip=[
                    alt.Tooltip("結果:O", title="結果"),
                    alt.Tooltip("機率類型:N", title="類型"),
                    alt.Tooltip("機率:Q", title="機率", format=".4f"),
                ],
            )
            .properties(height=320)
        )
        st.altair_chart(histogram_chart, use_container_width=True)
        st.caption("每個結果的模擬相對次數與理論機率以並排長條呈現；模擬次數增加時，兩者通常會逐漸接近。")

    # 收斂圖最多取 400 個點，避免每一幀都傳送數千筆資料
    conv_n = min(frame_n, 400)
    conv_idx = np.linspace(0, frame_n - 1, conv_n, dtype=int)
    df_conv = pd.DataFrame({
        "模擬值": cumulative_probability[conv_idx],
        "理論值": np.full(conv_n, theory_probability)
    }, index=conv_idx + 1)
    with conv_spot.container():
        st.markdown(f"### {conv_title}")
        st.line_chart(
            df_conv,
            use_container_width=True
        )

    # 平均值也更新固定位置，避免動畫每一幀都新增一行文字、推擠下方圖表
    mean_spot.caption(
        f"目前平均值 {mean_label} = {current_mean:.4f} ｜ 理論平均 = {theory_mean:.4f}"
    )

    # 瀏覽器端柔和三音提示：只在動畫播放時觸發，並稍微延後以貼近畫面更新。
    if sound_enabled:
        components.html(
            f"""<div style="font-family: sans-serif; font-size: 12px; color: #666;">
            <button id="enableSound" style="padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#fff;cursor:pointer;">
              🔊 啟用／測試音效
            </button>
            <span id="soundStatus" style="margin-left:8px;">首次使用請點擊按鈕測試音效</span>
            <script>
              (() => {{
                const button = document.getElementById('enableSound');
                const status = document.getElementById('soundStatus');
                let ctx;
                function playChime() {{
                  if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
                  const start = ctx.currentTime + 0.015;
                  // 縮短成清楚、柔和的雙音提示，避免音效延續到下一幀。
                  [659.25, 783.99].forEach((freq, i) => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    const t = start + i * 0.035;
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, t);
                    gain.gain.setValueAtTime(0.0001, t);
                    gain.gain.exponentialRampToValueAtTime(0.045, t + 0.008);
                    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.045);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(t);
                    osc.stop(t + 0.05);
                  }});
                }}
                button.addEventListener('click', async () => {{
                  try {{
                    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
                    if (ctx.state !== 'running') await ctx.resume();
                    playChime();
                    status.textContent = '音效已啟用；若動畫仍無聲，請確認瀏覽器分頁未靜音。';
                  }} catch (e) {{ status.textContent = '無法播放，請檢查瀏覽器音量與音效權限'; }}
                }});
                if ({str(bool(play_sound)).lower()}) {{
                  // 不再額外延遲 120ms；在此動畫幀的 iframe 首次繪製時立刻排程音效。
                  requestAnimationFrame(async () => {{
                    try {{
                      if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
                      if (ctx.state !== 'running') await ctx.resume();
                      if (ctx.state === 'running') playChime();
                    }} catch (e) {{ /* 瀏覽器可能要求先由使用者點擊啟用 */ }}
                  }});
                }}
              }})();
            </script>
            </div>""",
            height=42,
        )

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
        render_frame_ui(current_n, play_sound=True)
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

    # 模擬結束後可逐次查閱完整抽樣結果
    st.divider()
    st.subheader("🔍 每一次抽樣結果查詢 (Trial-by-trial Details)")
    st.caption("可選擇任一次模擬查看詳細結果；下方表格也列出全部模擬的摘要。")

    detail_col, _ = st.columns([1, 2])
    with detail_col:
        selected_trial = st.number_input(
            "要查看第幾次模擬？", min_value=1, max_value=int(total_n),
            value=1, step=1, key="selected_trial_detail"
        )

    trial_idx = int(selected_trial) - 1
    if simulation_type.startswith("模擬一"):
        selected_sample = sample_matrix[trial_idx]
        detail_df = pd.DataFrame({
            "抽樣位置": np.arange(1, 11),
            "程式編號": [f"程式 {i}" for i in range(1, 11)],
            "抽樣結果": ["有缺陷" if state == 1 else "正常" for state in selected_sample],
        })
        defect_count = int(selected_sample.sum())
        st.markdown(
            f"**第 {int(selected_trial):,} 次結果：** 抽到 {defect_count} 個有缺陷程式、"
            f"{10 - defect_count} 個正常程式；本次 X = {defect_count}。"
        )
        st.dataframe(detail_df, use_container_width=True, hide_index=True)
    else:
        attempts = int(values[trial_idx])
        detail_df = pd.DataFrame({
            "傳輸次數": np.arange(1, attempts + 1),
            "結果": ["成功" if j == attempts else "失敗" for j in range(1, attempts + 1)],
        })
        st.markdown(f"**第 {int(selected_trial):,} 次結果：** 共傳輸 {attempts} 次才首次成功；本次 Y = {attempts}。")
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

    # 全部模擬摘要：每一列對應一次模擬，可用 Streamlit 表格搜尋與排序
    all_trials_df = pd.DataFrame({
        "模擬次數": np.arange(1, int(total_n) + 1),
        "結果值": values,
        f"{event_label} 是否發生": (values == 3) if simulation_type.startswith("模擬一") else (values > 3),
        "累積平均值": cumulative_mean,
        f"累積 {event_label}": cumulative_probability,
    })
    st.markdown("**全部模擬摘要（每列一筆，可搜尋、排序及下載）**")
    st.dataframe(all_trials_df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ 下載全部模擬結果 CSV",
        data=all_trials_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="simulation_trial_results.csv",
        mime="text/csv",
        use_container_width=False,
    )

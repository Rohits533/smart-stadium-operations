import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. CONFIGURATION & VIBE-CSS
# ==========================================
st.set_page_config(page_title="StadiumPulse Ops Centre", page_icon="🏟️", layout="wide")

st.markdown("""
<style>
/* Entrance Animation */
@keyframes fadeInSlide {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInSlide 0.6s ease-out forwards; }

.stApp {
    background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 41, 59) 90.1%);
    color: #f1f5f9;
    font-family: 'Helvetica Neue', sans-serif;
}
.block-container { padding-top: 1.5rem; padding-bottom: 8rem !important; }
[data-testid="stSidebar"] { background-color: rgb(15, 23, 42) !important; border-right: 1px solid rgba(255,255,255,0.1); }
.main-header { color: white; font-weight: 800; font-size: 2.5rem; margin-bottom: 0.25rem; }
.main-subheader { font-weight: 500; color: rgba(255,255,255,0.6); font-size: 1rem; margin-bottom: 2rem; }
.section-header { font-weight: 700; font-size: 1.4rem; margin-top: 1.5rem; margin-bottom: 1rem; color: #f1f5f9; }
.glass-card { background: rgba(255, 255, 255, 0.03); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 1.5rem; backdrop-filter: blur(8px); margin-bottom: 1.5rem; }
.neon-text { color: #22d3ee; text-shadow: 0 0 10px rgba(34, 211, 238, 0.6); font-weight: 800; font-size: 1.8rem; }
.pink-neon { color: #f472b6; text-shadow: 0 0 10px rgba(244, 114, 182, 0.6); font-weight: 800; font-size: 1.8rem; }
.playback-bar {
    position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(12px); border-top: 1px solid rgba(255,255,255,0.1);
    padding: 0.75rem 2rem; display: flex; justify-content: space-between; align-items: center;
    z-index: 999; font-size: 0.9rem; color: rgba(255,255,255,0.6);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. BACKEND & STATE
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")
if "model" not in st.session_state and api_key:
    genai.configure(api_key=api_key)
    st.session_state.model = genai.GenerativeModel("gemini-2.5-flash")

if "current_view" not in st.session_state: st.session_state.current_view = "Dashboard"

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### StadiumPulse Ops")
    nav_options = ["Dashboard", "Stadium Map", "Telemetry Feed", "Crowd Flow", "Operations Manual", "Team Channels", "Incident Reports"]
    selection = st.radio("Navigation", nav_options, index=nav_options.index(st.session_state.current_view))
    if selection != st.session_state.current_view:
        st.session_state.current_view = selection
        st.rerun()

# ==========================================
# 3. MAIN CONTENT (Wrapped in Animation)
# ==========================================
st.markdown("<div class='animate-in'>", unsafe_allow_html=True)

if st.session_state.current_view == "Dashboard":
    st.markdown("<div class='main-header'>StadiumPulse Control Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Real-time logistics and crowd intelligence.</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: st.html('<div class="glass-card"><div class="neon-text">92%</div>GATE A CONGESTION</div>')
    with m2: st.html('<div class="glass-card"><div class="pink-neon">14 MIN</div>CONCESSION #4</div>')
    with m3: st.html('<div class="glass-card"><div style="color:#22c55e; font-size:1.8rem; font-weight:800;">ACTIVE</div>AI ROUTING</div>')

elif st.session_state.current_view == "Stadium Map":
    st.markdown("<div class='main-header'>Stadium Tactical Heatmap</div>", unsafe_allow_html=True)
    st.html('<div class="glass-card">Live Map View Rendered Here</div>')

elif st.session_state.current_view == "Telemetry Feed":
    st.markdown("<div class='main-header'>Live Telemetry Feed</div>", unsafe_allow_html=True)
    st.code("[19:34:10] CAM-04: Density 3.4/sqm\n[19:34:12] SYSTEM: OPTIMAL")

elif st.session_state.current_view == "Crowd Flow":
    st.markdown("<div class='main-header'>Crowd Flow Optimizer</div>", unsafe_allow_html=True)

elif st.session_state.current_view == "Operations Manual":
    st.markdown("<div class='main-header'>Operations Manual</div>", unsafe_allow_html=True)

elif st.session_state.current_view == "Team Channels":
    st.markdown("<div class='main-header'>Team Channels</div>", unsafe_allow_html=True)

elif st.session_state.current_view == "Incident Reports":
    st.markdown("<div class='main-header'>Incident Archives</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Close animate-in div

# ==========================================
# 4. FIXED FOOTER
# ==========================================
st.html("""
    <div class='playback-bar'>
        <span>User: StadiumOps-4</span>
        <span>EVENT PROGRESS: 1h 32m (LIVE)</span>
        <span style='color: #22d3ee; font-weight:600;'>SYSTEM OPTIMIZED</span>
    </div>
""")

Got it! Right now, the app is only changing its views based on the `nav_main` selection from the Operations Centre radio buttons, meaning the **Resources** menu choices don't actually swap out the page content when clicked.

To fix this, we can unify the navigation logic in the sidebar so that clicking *any* item under either menu switches the view perfectly, and then implement the full layouts and text content for **Operations Manual**, **Team Channels**, and **Incident Reports**.

Here is the fully upgraded `app.py` with all resource sections functional and beautifully styled to match your dark glassmorphic layout:

```python
import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. CONFIGURATION & VIBE-CSS INJECTION
# ==========================================
st.set_page_config(page_title="StadiumPulse Ops Centre", page_icon="🏟️", layout="wide")

# Sleek glassmorphic dark theme
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 41, 59) 90.1%);
    color: #f1f5f9;
    font-family: 'Helvetica Neue', sans-serif;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 8rem !important;
}
[data-testid="stSidebar"] {
    background-color: rgb(15, 23, 42) !important;
    border-right: 1px solid rgba(255,255,255,0.1);
    z-index: 100 !important;
}
[data-testid="stSidebar"] * {
    pointer-events: auto !important;
}
.sidebar-title {
    color: #f1f5f9;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.sidebar-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.main-header {
    color: white;
    font-weight: 800;
    font-size: 2.5rem;
    margin-bottom: 0.25rem;
}
.main-subheader {
    font-weight: 500;
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    margin-bottom: 2rem;
}
.section-header {
    font-weight: 700;
    font-size: 1.4rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: #f1f5f9;
}
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1.5rem;
    backdrop-filter: blur(8px);
    margin-bottom: 1.5rem;
}
.neon-text {
    color: #22d3ee;
    text-shadow: 0 0 10px rgba(34, 211, 238, 0.6);
    font-weight: 800;
    font-size: 1.8rem;
}
.pink-neon {
    color: #f472b6;
    text-shadow: 0 0 10px rgba(244, 114, 182, 0.6);
    font-weight: 800;
    font-size: 1.8rem;
}
.playback-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.1);
    padding: 0.75rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 90 !important;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.6);
}
.user-profile { display: flex; align-items: center; gap: 10px; }
.user-avatar { width: 28px; height: 28px; border-radius: 50%; background-color: #f472b6; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. BACKEND API KEY CHECK
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")

def init_gemini(key):
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=(
                "You are 'StadiumPulse AI'—an elite Smart Stadium Operations AI built for FIFA World Cup 2026."
            )
        )
    except Exception:
        return None

if "model" not in st.session_state and api_key:
    st.session_state.model = init_gemini(api_key)


# ==========================================
# 2. SIDEBAR NAVIGATION CONTROLLER
# ==========================================
# Using a single session state variable ensures the menus don't fight each other
if "current_view" not in st.session_state:
    st.session_state.current_view = "Dashboard"

with st.sidebar:
    st.markdown("<div class='sidebar-title'>StadiumPulse Ops</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-label'>Operations Centre</div>", unsafe_allow_html=True)
    # Find matching index or default to None if the active view belongs to the other list
    ops_options = ["Dashboard", "Stadium Map", "Telemetry Feed", "Crowd Flow"]
    try:
        ops_idx = ops_options.index(st.session_state.current_view)
    except ValueError:
        ops_idx = 0 # Default placeholder if current view is a resource item

    nav_main = st.radio(
        "Ops Navigation", 
        ops_options, 
        index=ops_idx,
        key="nav_main_selection", 
        label_visibility="collapsed"
    )
    
    st.markdown("<div class='sidebar-label'>Resources</div>", unsafe_allow_html=True)
    res_options = ["Operations Manual", "Team Channels", "Incident Reports"]
    try:
        res_idx = res_options.index(st.session_state.current_view)
    except ValueError:
        res_idx = 0

    nav_res = st.radio(
        "Resources Navigation", 
        res_options, 
        index=res_idx,
        key="nav_resources_selection", 
        label_visibility="collapsed"
    )

    # Sync mechanisms to detect which radio button clicked last
    if st.is_experimental_rerun:
        pass # Avoid break cycles
        
# Determine what page should actually render based on interactions
ctx_changes = st.session_state.get("last_nav_main", "Dashboard") != nav_main
res_changes = st.session_state.get("last_nav_resources", "Operations Manual") != nav_res

if ctx_changes:
    st.session_state.current_view = nav_main
    st.session_state.last_nav_main = nav_main
elif res_changes:
    st.session_state.current_view = nav_res
    st.session_state.last_nav_resources = nav_res

active_page = st.session_state.current_view


# ==========================================
# 3. MAIN CONTENT MANAGEMENT
# ==========================================

# --- DASHBOARD VIEW ---
if active_page == "Dashboard":
    st.markdown("<div class='main-header'>StadiumPulse Control Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Real-time logistics, crowd intelligence, and automated operational routing.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Active Telemetry</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)

    with m1:
        st.html("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">GATE A CONGESTION</div>
                <div class="neon-text">92% <span style="font-size:0.95rem; color:#ef4444; font-weight:600; margin-left: 8px;">🔴 CRITICAL SURGE</span></div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Directing fans to overflow Gates B and C.</div>
            </div>
        """)

    with m2:
        st.html("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">CONCESSION STAND #4</div>
                <div class="pink-neon">14 MIN <span style="font-size:0.95rem; color:#f59e0b; font-weight:600; margin-left: 8px;">🟡 SLOW</span></div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Queue length currently at 18 active visitors.</div>
            </div>
        """)

    with m3:
        st.html("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">AI OPERATION ROUTING</div>
                <div style="font-weight: 800; font-size: 1.8rem; color: #22c55e;">ACTIVE</div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Dynamic digital signboards synced.</div>
            </div>
        """)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='section-header'>Live System Telemetry Logs</div>", unsafe_allow_html=True)
        st.code(
            "[19:32:01] INFO: Crowd surge detected near Gate A after transit drop-off.\n"
            "[19:32:15] WARN: Concession Stand #4 queue exceeds 15 people.\n"
            "[19:32:30] READY: Awaiting AI crowd-routing recommendations...",
            language="bash"
        )
    with col2:
        st.markdown("<div class='section-header'>Operations Chat Co-Pilot</div>", unsafe_allow_html=True)
        if not api_key:
            st.html("""
                <div class="glass-card" style="background:rgba(239, 68, 68, 0.08); border:1px solid rgba(239, 68, 68, 0.25);">
                    <div style="font-weight: 700; color: #f87171; font-size: 1.1rem;">⚠️ API KEY NOT FOUND IN SECRETS</div>
                    <div style="font-size:0.85rem; margin-top:6px; color:rgba(248, 113, 113, 0.8);">
                        Please set your Gemini API key in your Streamlit Cloud Workspace Secrets.
                    </div>
                </div>
            """)
            st.stop()

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Awaiting commands."}]
            
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if prompt := st.chat_input("Ask AI Co-Pilot..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    model = st.session_state.get("model")
                    reply = model.generate_content(prompt).text if model else "Operational error: Could not initialize Gemini connection."
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- STADIUM MAP VIEW ---
elif active_page == "Stadium Map":
    st.markdown("<div class='main-header'>Stadium Tactical Heatmap</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Real-time spatial density and spectator flow metrics.</div>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.5, 1])
    
    with col_map:
        st.markdown("<div class='section-header'>Live Perimeter Map</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card" style="text-align: center; padding: 2rem;">
                <svg width="100%" height="300" viewBox="0 0 600 300" style="background: transparent;">
                    <rect x="50" y="20" width="500" height="260" rx="130" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="8" />
                    <rect x="150" y="70" width="300" height="160" rx="80" fill="rgba(34, 211, 238, 0.05)" stroke="rgba(34, 211, 238, 0.3)" stroke-width="4" />
                    
                    <path d="M 50 150 A 130 130 0 0 1 150 20 L 200 70 A 80 80 0 0 0 150 150 Z" fill="rgba(239, 68, 68, 0.45)" stroke="#ef4444" stroke-width="3" />
                    <text x="80" y="80" fill="white" font-weight="bold" font-size="14">ZONE A (92%)</text>
                    
                    <path d="M 450 20 A 130 130 0 0 1 550 150 L 450 150 A 80 80 0 0 0 400 70 Z" fill="rgba(34, 211, 238, 0.15)" stroke="#22d3ee" stroke-width="2" />
                    <text x="460" y="80" fill="rgba(255,255,255,0.7)" font-size="12">ZONE B (20%)</text>

                    <path d="M 550 150 A 130 130 0 0 1 450 280 L 400 230 A 80 80 0 0 0 450 150 Z" fill="rgba(34, 211, 238, 0.15)" stroke="#22d3ee" stroke-width="2" />
                    <text x="460" y="230" fill="rgba(255,255,255,0.7)" font-size="12">ZONE C (18%)</text>
                    
                    <text x="300" y="155" fill="white" font-weight="bold" font-size="18" text-anchor="middle" letter-spacing="3">PLAYING FIELD</text>
                </svg>
                <div style="margin-top: 15px; color: #ef4444; font-weight: bold; font-size: 0.9rem; text-shadow: 0 0 6px rgba(239, 68, 68, 0.3);">
                    ⚠️ ALERT: ZONE A PERIMETER SURGE DETECTED
                </div>
            </div>
        """)

        st.markdown("<div class='section-header'>Tactical Close-up: Gate A Bottleneck Analysis</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card" style="text-align: center; padding: 1.5rem;">
                <svg width="100%" height="180" viewBox="0 0 500 180" style="background: rgba(0,0,0,0.2); border-radius: 8px;">
                    <line x1="0" y1="30" x2="500" y2="30" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
                    <line x1="0" y1="90" x2="500" y2="90" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
                    <line x1="0" y1="150" x2="500" y2="150" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
                    <line x1="20" y1="40" x2="350" y2="40" stroke="rgba(255,255,255,0.2)" stroke-width="3" />
                    <line x1="20" y1="140" x2="350" y2="140" stroke="rgba(255,255,255,0.2)" stroke-width="3" />
                    <line x1="350" y1="40" x2="350" y2="140" stroke="#f472b6" stroke-width="4" stroke-dasharray="8 8" />
                    <text x="360" y="35" fill="#f472b6" font-size="10" font-weight="bold">ACTIVE TURNSTILES</text>
                    <ellipse cx="250" cy="90" rx="90" ry="35" fill="rgba(239, 68, 68, 0.35)" stroke="#ef4444" stroke-width="2" />
                    <text x="250" y="94" fill="white" font-weight="bold" font-size="11" text-anchor="middle">CRITICAL SURGE DENSITY</text>
                    <path d="M 44 90 L 110 90 M 100 85 L 110 90 L 100 95" fill="none" stroke="#ef4444" stroke-width="3" />
                    <text x="45" y="78" fill="rgba(255,255,255,0.6)" font-size="10">Spectator Flow Inward</text>
                    <rect x="380" y="100" width="100" height="40" rx="4" fill="rgba(34, 197, 94, 0.1)" stroke="#22c55e" stroke-width="1" />
                    <text x="430" y="124" fill="#22c55e" font-weight="bold" font-size="10" text-anchor="middle">BYPASS LANE</text>
                    <text x="25" y="25" fill="#22d3ee" font-weight="bold" font-size="11">GATE A PLAZA FEED</text>
                </svg>
                <div style="display: flex; justify-content: space-between; margin-top: 12px; font-size: 0.85rem; color: rgba(255,255,255,0.6);">
                    <span>🔴 Flow Obstruction: <strong>92% (High Risk)</strong></span>
                    <span>🟢 Backup Routing Capacity: <strong>800/min</strong></span>
                </div>
            </div>
        """)
        
    with col_details:
        st.markdown("<div class='section-header'>Gate Statistics</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card">
                <table style="width: 100%; border-collapse: collapse; color: white;">
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left; font-size: 0.85rem; color: rgba(255,255,255,0.5);">
                        <th style="padding: 8px 0;">GATE</th>
                        <th style="padding: 8px 0;">STATUS</th>
                        <th style="padding: 8px 0;">FLOW RATE</th>
                        <th style="padding: 8px 0;">WAIT TIME</th>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 12px 0; font-weight: bold; color: #ef4444;">Gate A</td>
                        <td style="color: #ef4444;">SURGE</td>
                        <td>412/min</td>
                        <td><strong>26 min</strong></td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 12px 0; font-weight: bold; color: #22d3ee;">Gate B</td>
                        <td style="color: #22d3ee;">CLEAR</td>
                        <td>88/min</td>
                        <td><strong>3 min</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0; font-weight: bold; color: #22d3ee;">Gate C</td>
                        <td style="color: #22d3ee;">CLEAR</td>
                        <td>62/min</td>
                        <td><strong>2 min</strong></td>
                    </tr>
                </table>
            </div>
        """)

# --- TELEMETRY FEED VIEW ---
elif active_page == "Telemetry Feed":
    st.markdown("<div class='main-header'>Real-Time Telemetry Feed</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Granular data streams gathered from stadium sensors, cameras, and transport networks.</div>", unsafe_allow_html=True)
    
    col_sys, col_cam = st.columns([1, 1])
    with col_sys:
        st.markdown("<div class='section-header'>Hardware Sensor Matrix</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px;">
                    <span style="color: rgba(255,255,255,0.5);">SENSOR TYPE</span>
                    <span style="color: rgba(255,255,255,0.5);">STATUS</span>
                    <span style="color: rgba(255,255,255,0.5);">FEED VALUE</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span>🎫 NFC Turnstiles (Gate A)</span>
                    <span style="color: #4ade80;">ONLINE</span>
                    <strong style="color: #22d3ee;">142 scans/min</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span>🎟️ NFC Turnstiles (Gate B)</span>
                    <span style="color: #4ade80;">ONLINE</span>
                    <strong style="color: #22d3ee;">34 scans/min</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span>🚌 Metro Transit Shuttle</span>
                    <span style="color: #f59e0b;">DELAYED</span>
                    <strong style="color: #f472b6;">+8 Min Arrival</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>🍔 POS Registries (Stall 4)</span>
                    <span style="color: #ef4444;">OVERLOAD</span>
                    <strong style="color: #ef4444;">18 active orders</strong>
                </div>
            </div>
        """)
    with col_cam:
        st.markdown("<div class='section-header'>AI Computer Vision Feed</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card">
                <div style="background-color: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; border: 1px solid rgba(255,255,255,0.05); font-family: monospace; font-size: 0.85rem;">
                    <div style="color: #22d3ee; margin-bottom: 8px;">🎥 [CAM-04-NORTH] ANALYSING SPECTATOR VELOCITY...</div>
                    <span style="color: rgba(255,255,255,0.4);">[19:34:10]</span> Density: 3.4 persons/sqm <br>
                    <span style="color: rgba(255,255,255,0.4);">[19:34:11]</span> Direction: North-to-South (91%) <br>
                    <span style="color: rgba(255,255,255,0.4);">[19:34:12]</span> Flow classification: <span style="color: #ef4444; font-weight: bold;">Bottlenecking risk high</span> <br>
                    <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                    <div style="color: #f472b6; margin-bottom: 8px;">🎥 [CAM-09-EAST] ANALYSING CONCOURSE...</div>
                    <span style="color: rgba(255,255,255,0.4);">[19:34:08]</span> Density: 0.8 persons/sqm <br>
                    <span style="color: rgba(255,255,255,0.4);">[19:34:12]</span> Flow classification: <span style="color: #4ade80;">Optimal</span>
                </div>
            </div>
        """)

# --- CROWD FLOW VIEW ---
elif active_page == "Crowd Flow":
    st.markdown("<div class='main-header'>Crowd Flow Optimizer</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Automated corridor routing models and crowd mitigation protocols.</div>", unsafe_allow_html=True)
    
    col_routes, col_alerts = st.columns([1.2, 1])
    
    with col_routes:
        st.markdown("<div class='section-header'>Dynamic Routing Corridors</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card">
                <div style="font-weight: 700; font-size: 1.1rem; color: white; margin-bottom: 12px;">Active Evacuation & Directional Routings</div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                        <span>🚇 Sector North Express Way</span>
                        <span style="color: #ef4444; font-weight: bold;">88% Load</span>
                    </div>
                    <div style="height: 8px; background-color: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                        <div style="width: 88%; height: 100%; background-color: #ef4444; box-shadow: 0 0 8px #ef4444;"></div>
                    </div>
                </div>

                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                        <span>🏟️ East Concourse Walkway</span>
                        <span style="color: #22d3ee; font-weight: bold;">24% Load</span>
                    </div>
                    <div style="height: 8px; background-color: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                        <div style="width: 24%; height: 100%; background-color: #22d3ee; box-shadow: 0 0 8px #22d3ee;"></div>
                    </div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                        <span>🎟️ West Gate B Overflow Corridor</span>
                        <span style="color: #4ade80; font-weight: bold;">12% Load</span>
                    </div>
                    <div style="height: 8px; background-color: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                        <div style="width: 12%; height: 100%; background-color: #4ade80; box-shadow: 0 0 8px #4ade80;"></div>
                    </div>
                </div>
            </div>
        """)
        
    with col_alerts:
        st.markdown("<div class='section-header'>Flow Intervention Triggers</div>", unsafe_allow_html=True)
        st.html("""
            <div class="glass-card" style="border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.02);">
                <div style="font-weight: 700; color: #ef4444; margin-bottom: 6px; font-size: 1.1rem;">⚠️ LEVEL 2 INTERVENTION REQUIRED</div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7); line-height: 1.5;">
                    Spectator queue build-up at <strong>Gate A</strong> exceeds stadium perimeter buffer limit. 
                    Recommended protocol: Trigger LED signage re-routes and dispatch 2 field safety supervisors to corridor intersection 2-A.
                </div>
            </div>
        """)

# ==========================================
# NEW RESOURCE LAYOUTS & INTERACTION CONTENTS
# ==========================================

# --- OPERATIONS MANUAL ---
elif active_page == "Operations Manual":
    st.markdown("<div class='main-header'>Stadium Operations Manual</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Standard regulatory frameworks and automated response logic trees.</div>", unsafe_allow_html=True)
    
    man_col1, man_col2 = st.columns([1, 1])
    with man_col1:
        st.html("""
            <div class="glass-card">
                <h3 style="color: #22d3ee; margin-bottom: 12px;">Protocol 04: Crowd Congestion Relief</h3>
                <p style="font-size: 0.9rem; color: rgba(255,255,255,0.8); line-height: 1.6;">
                    When total physical entry chokepoint capacity at any tier-1 turnstile cluster equals or exceeds <strong>85% max theoretical volume</strong>:
                </p>
                <ol style="font-size: 0.85rem; color: rgba(255,255,255,0.7); padding-left: 20px; line-height: 1.6;">
                    <li>Activate alternative dynamic digital array banners outside perimeter zones.</li>
                    <li>Synchronize automated push notifications to incoming ticket holders within a 1km radius geo-fence.</li>
                    <li>Instruct transit dispatch services to stagger arrivals by up to 180 seconds to buffer surge volume.</li>
                </ol>
            </div>
        """)
    with man_col2:
        st.html("""
            <div class="glass-card">
                <h3 style="color: #f472b6; margin-bottom: 12px;">Emergency Exit Strategies</h3>
                <p style="font-size: 0.9rem; color: rgba(255,255,255,0.8); line-height: 1.5;">
                    Perimeter release mechanics are pre-loaded into the primary server stack. In the event of secondary intervention overrides, structural slide-gates are programmatically commanded to drop away to clear corridors completely.
                </p>
            </div>
        """)

# --- TEAM CHANNELS ---
elif active_page == "Team Channels":
    st.markdown("<div class='main-header'>Comms & Team Channels</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Live operations frequency channels and cross-departmental logs.</div>", unsafe_allow_html=True)
    
    chan_col1, chan_col2 = st.columns([1.2, 1])
    with chan_col1:
        st.html("""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
                    <span style="font-weight: bold; color: #22d3ee;">📡 FREQUENCY CHAN-02 (GROUND OPERATIONS)</span>
                    <span style="color: #4ade80; font-size: 0.8rem;">● SECURE AUDIO STREAM</span>
                </div>
                <div style="font-size: 0.9rem; line-height: 1.6;">
                    <p><strong>[19:28:44] Supervisor Delta:</strong> Perimeter barriers at Gate A are holding up, but spacing between lines is closing fast. We need the signboard reroute active now.</p>
                    <p><strong>[19:29:10] Transport Lead:</strong> Shuttle arrivals from North lot held back for next two cycles. Directing remaining drop-offs to South Terminal B loop.</p>
                    <p style="color: rgba(255,255,255,0.4);"><em>[19:30:00] System Broadcast: Automated alert routed to central deck.</em></p>
                </div>
            </div>
        """)
    with chan_col2:
        st.html("""
            <div class="glass-card">
                <h4 style="color: white; margin-bottom: 10px;">Inter-Dept Directory</h4>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                    🔹 <strong>Logistics Command:</strong> Ext. 402 (Active)<br>
                    🔹 <strong>Transit Coordination:</strong> Ext. 819 (Active)<br>
                    🔹 <strong>Medical Services Hub:</strong> Ext. 112 (Standby)
                </div>
            </div>
        """)

# --- INCIDENT REPORTS ---
elif active_page == "Incident Reports":
    st.markdown("<div class='main-header'>Incident Logs & Archives</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Active operational anomalies registered during current match-day deployment.</div>", unsafe_allow_html=True)
    
    st.html("""
        <div class="glass-card">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; color: white;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: rgba(255,255,255,0.4); font-size: 0.8rem;">
                    <th style="padding: 10px 5px;">INCIDENT ID</th>
                    <th style="padding: 10px 5px;">TIMESTAMP</th>
                    <th style="padding: 10px 5px;">LOCATION</th>
                    <th style="padding: 10px 5px;">SEVERITY</th>
                    <th style="padding: 10px 5px;">STATUS</th>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 12px 5px; font-family: monospace;">#INC-2026-8812</td>
                    <td>19:32:01</td>
                    <td>Gate A Turnstiles</td>
                    <td><span style="color: #ef4444; font-weight: bold;">CRITICAL</span></td>
                    <td><span style="background: rgba(239,68,68,0.2); padding: 2px 6px; border-radius: 4px; color: #ef4444; font-size:0.8rem;">MITIGATING</span></td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 12px 5px; font-family: monospace;">#INC-2026-8809</td>
                    <td>19:15:22</td>
                    <td>Concession Stand #4</td>
                    <td><span style="color: #f59e0b; font-weight: bold;">WARNING</span></td>
                    <td><span style="background: rgba(245,158,11,0.2); padding: 2px 6px; border-radius: 4px; color: #f59e0b; font-size:0.8rem;">MONITORING</span></td>
                </tr>
                <tr>
                    <td style="padding: 12px 5px; font-family: monospace;">#INC-2026-8794</td>
                    <td>18:44:10</td>
                    <td>North Parking Deck</td>
                    <td><span style="color: #4ade80; font-weight: bold;">MINOR</span></td>
                    <td><span style="background: rgba(74,222,128,0.2); padding: 2px 6px; border-radius: 4px; color: #4ade80; font-size:0.8rem;">RESOLVED</span></td>
                </tr>
            </table>
        </div>
    """)

# ==========================================
# 4. FIXED FOOTER PLAYBACK BAR
# ==========================================
st.html("""
    <div class='playback-bar'>
        <div class='user-profile'>
            <div class='user-avatar'>S</div>
            <span style="color: white; font-weight: 600;">User: StadiumOps-4</span>
        </div>
        <div>EVENT PROGRESS: 1h 32m (LIVE)</div>
        <div style='color: #22d3ee; font-weight:600; text-shadow: 0 0 5px rgba(34, 211, 238, 0.4);'>SYSTEM OPTIMIZED</div>
    </div>
""")

```

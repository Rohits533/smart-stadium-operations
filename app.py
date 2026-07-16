import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. CONFIGURATION & VIBE-CSS INJECTION
# ==========================================
st.set_page_config(page_title="StadiumPulse Ops Centre", page_icon="🏟️", layout="wide")

# Sleek glassmorphic dark theme with completely isolated sidebar pointer rules
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 41, 59) 90.1%);
        color: #f1f5f9;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Override Streamlit container padding and ensure bottom content doesn't get cut off by footer */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 8rem !important;
    }

    /* CRITICAL INTERACTION FIX FOR SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: rgb(15, 23, 42) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
        z-index: 100 !important;
    }

    /* Force all child elements in the sidebar to accept clicks */
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

    /* Main Dashboard Layout Components */
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

    /* Section Headers */
    .section-header {
        font-weight: 700;
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #f1f5f9;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(34, 211, 238, 0.15);
    }
    
    /* Neon Text Accents */
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

    /* Code Box Styling */
    div[data-testid="stCodeBlock"] {
        border-radius: 12px;
        background-color: rgb(15, 23, 42);
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    /* Fixed Footer Bar - keeps z-index low so it doesn't overlap sidebar clicks */
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
# 1. SECURE BACKEND API KEY CHECK
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")

def init_gemini(key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=(
                "You are 'StadiumPulse AI'—an elite Smart Stadium Operations AI built for FIFA World Cup 2026. "
                "Telemetry context: Gate A is 92% congested. Gate B/C are at 20%. Concession Stand #4 is backlogged. "
                "Give highly operational, bulleted, action-oriented responses. Draft signage text or announcements when asked."
            )
        )
        return model
    except Exception as e:
        return None

if "model" not in st.session_state and api_key:
    st.session_state.model = init_gemini(api_key)


# ==========================================
# 2. SIDEBAR (NAVIGATION)
# ==========================================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>StadiumPulse Ops</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-label'>Operations Centre</div>", unsafe_allow_html=True)
    nav_main = st.radio(
        "Ops Navigation", 
        ["Dashboard", "Stadium Map", "Telemetry Feed", "Crowd Flow"], 
        index=0, 
        key="nav_main_selection", 
        label_visibility="collapsed"
    )
    
    st.markdown("<div class='sidebar-label'>Resources</div>", unsafe_allow_html=True)
    nav_resources = st.radio(
        "Resources Navigation", 
        ["Operations Manual", "Team Channels", "Incident Reports"], 
        index=0, 
        key="nav_resources_selection", 
        label_visibility="collapsed"
    )


# ==========================================
# 3. MAIN DASHBOARD CONTENT (Dynamic rendering based on Nav)
# ==========================================

# --- DASHBOARD VIEW ---
if nav_main == "Dashboard":
    st.markdown("<div class='main-header'>StadiumPulse Control Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Real-time logistics, crowd intelligence, and automated operational routing.</div>", unsafe_allow_html=True)

    # Grid Layout: Critical Telemetry Cards
    st.markdown("<div class='section-header'>Active Telemetry</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">GATE A CONGESTION</div>
                <div class="neon-text">92% <span style="font-size:0.95rem; color:#ef4444; text-shadow:none; font-weight:600; margin-left: 8px;">🔴 CRITICAL SURGE</span></div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Directing fans to overflow Gates B and C.</div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">CONCESSION STAND #4</div>
                <div class="pink-neon">14 MIN <span style="font-size:0.95rem; color:#f59e0b; text-shadow:none; font-weight:600; margin-left: 8px;">🟡 SLOW</span></div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Queue length currently at 18 active visitors.</div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
            <div class="glass-card">
                <div style="color: rgba(255,255,255,0.4); font-weight: 600; margin-bottom: 8px; font-size: 0.8rem; letter-spacing: 0.05em;">AI OPERATION ROUTING</div>
                <div style="font-weight: 800; font-size: 1.8rem; color: #22c55e; text-shadow: 0 0 10px rgba(34, 197, 94, 0.4);">ACTIVE</div>
                <div style="font-size:0.85rem; margin-top:8px; color:rgba(255,255,255,0.5);">Dynamic digital signboards synced.</div>
            </div>
        """, unsafe_allow_html=True)


    # Dynamic Bottom Section: Terminal logs and AI Assistant
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
        
        # Missing secrets handling
        if not api_key:
            st.markdown("""
                <div class="glass-card" style="background:rgba(239, 68, 68, 0.08); border:1px solid rgba(239, 68, 68, 0.25);">
                    <div style="font-weight: 700; color: #f87171; font-size: 1.1rem;">⚠️ API KEY NOT FOUND IN SECRETS</div>
                    <div style="font-size:0.85rem; margin-top:6px; color:rgba(248, 113, 113, 0.8);">
                        Please set your Gemini API key in your Streamlit Cloud Workspace Secrets as: <br>
                        <code style="background-color: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; color: white;">GEMINI_API_KEY = "your-api-key"</code>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.stop()

        # Chat UI container setup
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "Awaiting commands. I have processed the live telemetry feed. Ready to design emergency routing signs or redirect logistical units."
            }]
            
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat Input handler
        if prompt := st.chat_input("Ask AI Co-Pilot (e.g., 'Draft a rerouting billboard announcement for Gate A')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("AI is routing..."):
                    model = st.session_state.get("model")
                    if model:
                        try:
                            response = model.generate_content(prompt)
                            reply = response.text
                        except Exception as e:
                            reply = f"Error calling Gemini API: {str(e)}"
                    else:
                        reply = "Operational error: Could not initialize Gemini connection."
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- STADIUM MAP VIEW ---
elif nav_main == "Stadium Map":
    st.markdown("<div class='main-header'>Stadium Tactical Heatmap</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Real-time spatial density and spectator flow metrics.</div>", unsafe_allow_html=True)
    
    col_map, col_details = st.columns([1.5, 1])
    
    with col_map:
        st.markdown("<div class='section-header'>Live Perimeter Map</div>", unsafe_allow_html=True)
        st.markdown("""
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
                <div style="margin-top: 15px; color: #ef4444; font-weight: bold; font-size: 0.9rem;">
                    ⚠️ ALERT: ZONE A PERIMETER SURGE DETECTED
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_details:
        st.markdown("<div class='section-header'>Gate Statistics</div>", unsafe_allow_html=True)
        st.markdown("""
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
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #22d3ee;">
                <div style="font-weight: 700; color: #22d3ee; margin-bottom: 5px;">AI CO-PILOT ACTIONS</div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7); line-height: 1.4;">
                    1. Re-routing North Lot shuttle drop-offs to Gate B corridor.<br>
                    2. Updating Gate A digital signage to: 'USE ALTERNATIVE GATES B & C'.
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- TELEMETRY FEED VIEW ---
elif nav_main == "Telemetry Feed":
    st.markdown("<div class='main-header'>Real-Time Telemetry Feed</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Granular data streams gathered from stadium sensors, cameras, and transport networks.</div>", unsafe_allow_html=True)
    
    col_sys, col_cam = st.columns([1, 1])
    
    with col_sys:
        st.markdown("<div class='section-header'>Hardware Sensor Matrix</div>", unsafe_allow_html=True)
        st.markdown("""
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
        """, unsafe_allow_html=True)
        
    with col_cam:
        st.markdown("<div class='section-header'>AI Computer Vision Feed</div>", unsafe_allow_html=True)
        st.markdown("""
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
        """, unsafe_allow_html=True)

# --- CROWD FLOW VIEW ---
elif nav_main == "Crowd Flow":
    st.markdown("<div class='main-header'>Crowd Flow Optimizer</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Automated corridor routing models and crowd mitigation protocols.</div>", unsafe_allow_html=True)
    
    col_routes, col_alerts = st.columns([1.2, 1])
    
    with col_routes:
        st.markdown("<div class='section-header'>Dynamic Routing Corridors</div>", unsafe_allow_html=True)
        st.markdown("""
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
        """, unsafe_allow_html=True)
        
    with col_alerts:
        st.markdown("<div class='section-header'>Flow Intervention Triggers</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.02);">
                <div style="font-weight: 700; color: #ef4444; margin-bottom: 6px; font-size: 1.1rem;">⚠️ LEVEL 2 INTERVENTION REQUIRED</div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7); line-height: 1.5;">
                    Spectator queue build-up at <strong>Gate A</strong> exceeds stadium perimeter buffer limit. 
                    Recommended protocol: Trigger LED signage re-routes and dispatch 2 field safety supervisors to corridor intersection 2-A.
                </div>
            </div>
            
            <div class="glass-card" style="border-left: 4px solid #22d3ee;">
                <div style="font-weight: 700; color: #22d3ee; margin-bottom: 6px; font-size: 1rem;">DIGITAL SIGNBOARD SYNC STATUS</div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7); line-height: 1.4;">
                    Digital message sign boards at the central terminal are synced with alternative routes redirecting spectators to East Walkways.
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- FALLBACK / DEFAULT RESOURCE VIEWS ---
else:
    st.markdown(f"<div class='main-header'>{nav_main} View</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-subheader'>Monitoring resource feed for {nav_main}</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; margin-bottom: 10px;">Operational Status: Live</h3>
            <p style="color: rgba(255,255,255,0.7);">System metrics and asset distribution are fully aligned with the central command. No alerts raised.</p>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. FIXED FOOTER PLAYBACK BAR
# ==========================================
st.markdown("""
    <div class='playback-bar'>
        <div class='user-profile'>
            <div class='user-avatar'>S</div>
            <span style="color: white; font-weight: 600;">User: StadiumOps-4</span>
        </div>
        <div>EVENT PROGRESS: 1h 32m (LIVE)</div>
        <div style='color: #22d3ee; font-weight:600; text-shadow: 0 0 5px rgba(34, 211, 238, 0.4);'>SYSTEM OPTIMIZED</div>
    </div>
""", unsafe_allow_html=True)

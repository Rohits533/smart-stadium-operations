import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. CONFIGURATION & VIBE-CSS INJECTION
# ==========================================
st.set_page_config(page_title="StadiumPulse Ops Centre", page_icon="🏟️", layout="wide")

# Sleek glassmorphic dark theme inspired by premium music dashboards
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 41, 59) 90.1%);
        color: #f1f5f9;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Override Streamlit container padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #f1f5f9;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .sidebar-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: rgba(255,255,255,0.5);
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
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
    
    /* Fixed Footer Bar */
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
        z-index: 1000;
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
# Quietly reads the key from Streamlit Secrets
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

# Initialize Gemini model seamlessly in the background
if "model" not in st.session_state and api_key:
    st.session_state.model = init_gemini(api_key)


# ==========================================
# 2. SIDEBAR (NAVIGATION)
# ==========================================
with st.sidebar:
    st.markdown("<h2>STADIUMPULSE OPS</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-label'>Operations Centre</div>", unsafe_allow_html=True)
    st.radio("Navigation", ["Dashboard", "Stadium Map", "Telemetry Feed", "Crowd Flow"], index=0, key="nav_main", label_visibility="collapsed")
    
    st.markdown("<div class='sidebar-label'>Resources</div>", unsafe_allow_html=True)
    st.radio("Resources", ["Operations Manual", "Team Channels", "Incident Reports"], index=0, key="nav_resources", label_visibility="collapsed")


# ==========================================
# 3. MAIN DASHBOARD CONTENT
# ==========================================
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
    
    # Missing secrets handling (Strictly formatted to notify admins, no inputs on home screen)
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

import streamlit as st
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="StadiumPulse AI", page_icon="🏟️", layout="wide")

# Dark sleek dashboard theme injection
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        color: #22d3ee !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏟️ STADIUMPULSE AI — Smart Stadium Operations")
st.write("Leveraging Gemini AI for real-time tournament operations, crowd logistics, and fan routing.")
st.write("---")

# Main Page Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Operations Control Panel")
    
    # Simulated telemetry metrics representing stadium sensors
    m1, m2, m3 = st.columns(3)
    m1.metric("Gate A Congestion", "92%", "Critical Surge", delta_color="inverse")
    m2.metric("Food Stall #4 Queue", "14 min Wait", "Slowing Down", delta_color="off")
    m3.metric("Active Live Support Chats", "1,240 Fans", "Normal Load")
    
    st.write("### 🚨 Live Event Telemetry Stream")
    st.code(
        "[19:32:01] INFO: Crowd surge detected near Gate A after transit drop-off.\n"
        "[19:32:15] WARN: Concession Stand #4 queue exceeds 15 people.\n"
        "[19:32:30] READY: Awaiting AI crowd-routing recommendations...",
        language="bash"
    )

with col2:
    st.subheader("GenAI Assistant Co-Pilot")
    
    # Input for Gemini API Key to secure the backend
    api_key = st.text_input("Enter your Gemini API Key", type="password", help="Get a free key from Google AI Studio")
    
    # Initialize session state for chatbot
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Hi! I am your Stadium Co-Pilot. Telemetry shows Gate A is congested (92%). Would you like me to generate alternative routing prompts for the digital signs?"
        }]
        
    # Render previous messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    # Chat Input
    if prompt := st.chat_input("Ask AI (e.g., 'Draft a rerouting message for Gate A')"):
        if not api_key:
            st.error("Please provide your Gemini API key above to consult the AI.")
        else:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.spinner("AI is thinking..."):
                try:
                    # Configured model
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        system_instruction=(
                            "You are 'StadiumPulse AI'—an elite Smart Stadium Operations AI built for FIFA World Cup 2026. "
                            "Telemetry context: Gate A is 92% congested. Gate B/C are at 20%. Concession Stand #4 is backlogged. "
                            "Give highly operational, bulleted, action-oriented responses. Draft signage text or announcements when asked."
                        )
                    )
                    response = model.generate_content(prompt)
                    reply = response.text
                except Exception as e:
                    reply = f"Error calling Gemini API: {str(e)}"
                
                # Append assistant reply
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)

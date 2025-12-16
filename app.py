import streamlit as st
import os
from src.engine import NarrativeEngine

# Page Config
st.set_page_config(
    page_title="CRNE: Ethical Intelligence",
    page_icon="⚖️",
    layout="centered"
)

# Premium CSS for "Contemplative, Restrained Tone"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&display=swap');
    
    .stApp {
        background-color: #fcfbf9; /* Light parchment */
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Merriweather', serif;
        color: #2c2c2c;
        font-weight: 300;
    }
    
    h1 {
        text-align: center;
        border-bottom: 1px solid #e0dcd3;
        padding-bottom: 20px;
        margin-bottom: 40px;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
    }

    /* Stage Cards */
    .stage-container {
        border-left: 2px solid #e0dcd3;
        padding-left: 30px;
        margin-left: 10px;
        padding-bottom: 40px;
        position: relative;
    }
    
    .stage-marker {
        position: absolute;
        left: -11px;
        top: 0;
        width: 20px;
        height: 20px;
        background-color: #fcfbf9;
        border: 2px solid #8c8c8c;
        border-radius: 50%;
        z-index: 10;
    }
    
    .stage-label {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 0.75rem;
        color: #8c8c8c;
        text-transform: uppercase;
        letter-spacing: 0.15rem;
        margin-bottom: 12px;
    }
    
    .narrative-content {
        font-family: 'Merriweather', serif;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #1a1a1a;
        background-color: white;
        padding: 25px;
        border: 1px solid #f0f0f0;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    /* Buttons */
    .stButton button {
        background-color: #ffffff;
        color: #444;
        border: 1px solid #ccc;
        font-family: 'Helvetica Neue', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
        transition: all 0.3s;
        width: 100%;
        border-radius: 0;
    }
    .stButton button:hover {
        background-color: #f4f4f4;
        border-color: #999;
        color: #000;
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# Helper for displaying stages
def render_stage(stage_num, content):
    stage_names = {
        1: "Situation Emergence",
        2: "Ethical Pause",
        3: "Possible Action Space",
        4: "Actual Action",
        5: "Counterfactual Simulation",
        6: "Dharma Resolution"
    }
    name = stage_names.get(stage_num, f"Stage {stage_num}")
    
    st.markdown(f"""
    <div class="stage-container">
        <div class="stage-marker"></div>
        <div class="stage-label">Stage {stage_num} • {name}</div>
        <div class="narrative-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

st.title("Counterfactual Ramayana")

# Sidebar for Context
with st.sidebar:
    st.markdown("### Core Principles")
    st.info(
        """
        **1. Ethical System**: Not mythology, but a system of decisions.
        \n**2. Restraint**: Silence is a decision, not an absence.
        \n**3. Order**: Actions preserve *Dharma* vs. *Adharma*.
        """
    )
    st.markdown("---")
    if st.button("Reset Narrative Loop"):
        if "engine" in st.session_state and st.session_state.engine:
            st.session_state.engine.reset()
            st.rerun()

# Initialize Engine
if "engine" not in st.session_state:
    try:
        st.session_state.engine = NarrativeEngine()
        st.session_state.error = None
    except ValueError as e:
        st.session_state.engine = None
        st.session_state.error = str(e)

# Main Interface
if st.session_state.error:
    st.error(f"System Error: {st.session_state.error}")
else:
    engine = st.session_state.engine
    state = engine.get_current_state()
    
    # Display History
    # NOTE: In a 'real' app we might want to collapse previous situations, 
    # but for now we focus on the current flow.
    
    # Render current situation stages
    for stage_num in range(1, state["stage"] + 1):
        if stage_num in state["content"]:
            render_stage(stage_num, state["content"][stage_num])

    # Controls
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if state["stage"] == 0:
            if st.button("Begin New Situation"):
                with st.spinner("Consulting the text..."):
                    engine.advance()
                st.rerun()
        elif state["stage"] < 6:
            if st.button("Advance Narrative"):
                with st.spinner("Analyzing ethical space..."):
                    engine.advance()
                st.rerun()
        else:
            st.markdown("""
                <div style='text-align: center; color: #666; font-style: italic; margin-bottom: 20px;'>
                    Situation Resolved.
                </div>
            """, unsafe_allow_html=True)
            if st.button("Next Situation"):
                with st.spinner("Moving to next context..."):
                    engine.advance()
                st.rerun()

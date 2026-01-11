"""
AI Research Assistant - Professional Research Agent
Deep Analysis with Comprehensive Reports
"""
import streamlit as st
import sys
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


def format_report(content):
    """Format report with proper reference styling and highlights"""
    # Fix references on same line - add line breaks before [number]
    content = re.sub(r'\s*\[(\d+)\]', r'\n[\1]', content)

    # Make sure References section has proper formatting
    if "## References" in content or "## Sources" in content:
        parts = re.split(r'(## References|## Sources)', content)
        if len(parts) >= 2:
            main_content = parts[0]
            ref_header = parts[1]
            ref_content = parts[2] if len(parts) > 2 else ""
            # Clean up reference content
            ref_content = re.sub(r'\[(\d+)\]', r'\n**[\1]**', ref_content)
            content = main_content + ref_header + ref_content

    return content

from src.config import validate_config
from src.state import create_initial_state

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Highlight important keywords */
    .report-content h3 {
        color: #2563eb;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 5px;
    }
    .report-content strong {
        color: #059669;
    }
    /* Reference styling */
    .report-content a {
        color: #7c3aed;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for persisting results
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""
if 'searches_made' not in st.session_state:
    st.session_state.searches_made = []
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'research_done' not in st.session_state:
    st.session_state.research_done = False

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Research Settings")

    try:
        validate_config()
        st.success("✅ API Keys Configured")
    except ValueError as e:
        st.error(f"Error: {e}")
        st.stop()

    st.markdown("---")

    research_depth = st.select_slider(
        "Research Depth",
        options=["Quick", "Standard", "Deep", "Comprehensive"],
        value="Standard"
    )

    depth_map = {"Quick": 3, "Standard": 5, "Deep": 7, "Comprehensive": 10}
    max_iter = depth_map[research_depth]

    st.caption(f"Will perform up to {max_iter} research iterations")

    st.markdown("---")
    st.markdown("""
    ### About
    This AI Research Agent performs deep web research on any topic and generates comprehensive, well-cited reports.

    **Features:**
    - Multi-source research
    - Synthesized analysis
    - Proper citations
    - Downloadable reports
    """)

    st.markdown("---")
    st.caption("Built by **Saikrishna**")

# Main content
st.title("🔬 AI Research Assistant")
st.markdown("*Deep research and comprehensive analysis powered by Claude + LangGraph + Tavily*")

st.markdown("---")

# Input section
st.markdown("### 📝 Enter Your Research Topic")
query = st.text_area(
    "What would you like to research?",
    placeholder="Enter a detailed research topic or question...\n\nExample: What are the latest advances in Chain of Thought reasoning for LLMs in 2024-2025?",
    height=100,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    start = st.button("🚀 Start Research", type="primary", use_container_width=True)
with col2:
    if st.session_state.research_done:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.report_content = ""
            st.session_state.searches_made = []
            st.session_state.query = ""
            st.session_state.research_done = False
            st.rerun()

if start and query:
    st.markdown("---")

    # Create columns for layout
    col_progress, col_status = st.columns([3, 1])

    with col_status:
        st.markdown("### 📊 Status")
        progress = st.progress(0)
        status_box = st.empty()
        iteration_box = st.empty()

    with col_progress:
        st.markdown("### 🔍 Research Activity")
        activity_container = st.container()

    try:
        from src.workflow import research_agent

        initial_state = create_initial_state(query)
        searches_made = []
        iteration = 0
        final_state = None

        status_box.info("🔄 Researching...")

        for state in research_agent.stream(initial_state):
            iteration += 1
            progress.progress(min(iteration / (max_iter * 2), 0.95))
            iteration_box.caption(f"Iteration {iteration}")

            with activity_container:
                if "agent" in state:
                    messages = state["agent"].get("messages", [])
                    if messages:
                        msg = messages[-1]

                        # Show search queries being made
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tc in msg.tool_calls:
                                q = tc.get('args', {}).get('query', '')
                                if q and q not in searches_made:
                                    searches_made.append(q)
                                    st.info(f"🔍 **Searching:** {q}")

                elif "tools" in state:
                    st.caption("📥 Processing search results...")

                final_state = state

            if iteration >= max_iter * 2:
                break

        progress.progress(1.0)
        status_box.success("✅ Research Complete!")

        # Extract final report
        report_content = ""
        if final_state:
            fs = final_state.get("agent", final_state.get("tools", final_state))

            if fs.get("final_report"):
                report_content = fs["final_report"]
            else:
                msgs = fs.get("messages", [])
                if msgs:
                    # Get the last AI message (not tool message)
                    for m in reversed(msgs):
                        if hasattr(m, 'content') and not hasattr(m, 'tool_call_id'):
                            content = m.content
                            if isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict) and item.get('type') == 'text':
                                        report_content = item.get('text', '')
                                        break
                            elif isinstance(content, str) and len(content) > 100:
                                report_content = content
                            if report_content and len(report_content) > 200:
                                break

        if report_content and len(report_content) > 200:
            # Save to session state (will display below)
            st.session_state.report_content = report_content
            st.session_state.searches_made = searches_made
            st.session_state.query = query
            st.session_state.research_done = True
        else:
            st.warning("The research agent did not generate a complete report. Please try again with a different query or increase research depth.")

            if searches_made:
                st.markdown("### Searches Made:")
                for s in searches_made:
                    st.markdown(f"- {s}")

    except Exception as e:
        st.error(f"❌ Research failed: {e}")
        st.exception(e)

elif start:
    st.warning("⚠️ Please enter a research topic")

# Display saved results (persists after download click)
if st.session_state.research_done and st.session_state.report_content:
    st.markdown("---")
    st.markdown("## 📄 Research Report")
    # Format and display the report
    formatted_report = format_report(st.session_state.report_content)
    st.markdown(formatted_report)

    # Download section
    st.markdown("---")
    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])

    download_content = f"""# Research Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Topic: {st.session_state.query}

---

{st.session_state.report_content}

---

## Research Queries Made:
{chr(10).join(f"- {s}" for s in st.session_state.searches_made)}

---
Generated by AI Research Assistant (Claude + LangGraph + Tavily)
"""

    with col_dl1:
        st.download_button(
            label="📥 Download Report (.md)",
            data=download_content,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Show searches in expander
    if st.session_state.searches_made:
        with st.expander("🔍 Research Queries Used", expanded=False):
            for i, s in enumerate(st.session_state.searches_made, 1):
                st.markdown(f"**{i}.** {s}")

import streamlit as st

from components.footer import render_footer
from components.navbar import render_header
from components.sidebar import render_sidebar
from components.splash import show_splash
from components.styles import apply_styles
from pathlib import Path

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "logo-blue.png"

st.set_page_config(
    page_title="Xeno OS Simulator",
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

# Check if dashboard button was clicked from header
if st.session_state.get("reset_navigation"):
    st.session_state["selected_algorithm"] = None
    st.session_state["selected_function"] = None
    st.session_state["reset_navigation"] = False

current_page, selected_function, selected_algorithm = render_sidebar()

show_splash()

# Render Header (Hero Banner with internal buttons)
render_header()

if current_page == "Algorithm" and selected_algorithm:
    algorithm_number, algorithm_name = selected_algorithm.split(".", 1)

    st.subheader(
        f"Module {algorithm_number.strip()}: {algorithm_name.strip()}"
    )
    st.write(f"**Category:** {selected_function}")

    clean_algo_name = algorithm_name.strip().lower()

    if "process state transition" in clean_algo_name:
        try:
            from ui.process_management.state_transition_ui import (
                render_state_transition_ui,
            )

            render_state_transition_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/process_management/state_transition_ui.py'."
            )

    elif "process creation" in clean_algo_name:
        try:
            from ui.process_management.process_creation_ui import (
                render_process_creation_ui,
            )

            render_process_creation_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/process_management/process_creation_ui.py'."
            )

    elif "fork" in clean_algo_name or "wait" in clean_algo_name:
        try:
            from ui.process_management.fork_wait_ui import (
                render_fork_wait_ui,
            )

            render_fork_wait_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/process_management/fork_wait_ui.py'."
            )

    elif "message passing" in clean_algo_name or "ipc" in clean_algo_name:
        try:
            from ui.ipc.message_passing_ui import render_message_passing_ui

            render_message_passing_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/ipc/message_passing_ui.py'."
            )
    elif "shared memory" in clean_algo_name:
        try:
            from ui.ipc.shared_memory_ui import render_shared_memory_ui

            render_shared_memory_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/ipc/shared_memory_ui.py'."
            )
    elif "pipe" in clean_algo_name:
        try:
            from ui.ipc.pipe_ui import render_pipe_ui

            render_pipe_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/ipc/pipe_ui.py'."
            )
    elif "thread lifecycle" in clean_algo_name:
        try:
            from ui.threads.thread_lifecycle_ui import (
                render_thread_lifecycle_ui,
            )

            render_thread_lifecycle_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/threads/thread_lifecycle_ui.py'."
            )
    elif (
        "thread synchronization" in clean_algo_name
        or "synchronization" in clean_algo_name
    ):
        try:
            from ui.threads.thread_sync_ui import render_thread_sync_ui

            render_thread_sync_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/threads/thread_sync_ui.py'."
            )
    elif "round robin" in clean_algo_name or "robin" in clean_algo_name:
        try:
            from ui.cpu_scheduling.preemptive.round_robin_ui import (
                render_round_robin_ui,
            )

            render_round_robin_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/preemptive/round_robin_ui.py'."
            )
    elif "srtf" in clean_algo_name or "remaining time" in clean_algo_name:
        try:
            from ui.cpu_scheduling.preemptive.srtf_ui import render_srtf_ui

            render_srtf_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/preemptive/srtf_ui.py'."
            )
    elif "priority" in clean_algo_name and not "non-preemptive" in clean_algo_name:
        try:
            from ui.cpu_scheduling.preemptive.priority_ui import (
                render_priority_ui,
            )

            render_priority_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/preemptive/priority_ui.py'."
            )
    elif "fcfs" in clean_algo_name or "first come" in clean_algo_name:
        try:
            from ui.cpu_scheduling.non_preemptive.fcfs_ui import render_fcfs_ui

            render_fcfs_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/non_preemptive/fcfs_ui.py'."
            )
            
    elif (
        "prediction" in clean_algo_name
        or "next burst" in clean_algo_name
        or "sjf" in clean_algo_name
    ):
        try:
            from ui.cpu_scheduling.non_preemptive.sjf_prediction_ui import (
                render_sjf_prediction_ui,
            )

            render_sjf_prediction_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/non_preemptive/sjf_prediction_ui.py'."
            )

    elif "priority" in clean_algo_name and (
        "non" in clean_algo_name or "non-preemptive" in clean_algo_name
    ):
        try:
            from ui.cpu_scheduling.non_preemptive.priority_non_preemptive_ui import (
                render_priority_non_preemptive_ui,
            )

            render_priority_non_preemptive_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/non_preemptive/priority_non_preemptive_ui.py'."
            )
    elif "multilevel feedback" in clean_algo_name or "mlfq" in clean_algo_name:
        try:
            from ui.cpu_scheduling.preemptive.mlfq_ui import render_mlfq_ui

            render_mlfq_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/preemptive/mlfq_ui.py'."
            )

    elif "multilevel queues" in clean_algo_name or "mlq" in clean_algo_name:
        try:
            from ui.cpu_scheduling.non_preemptive.multilevel_queue_ui import (
                render_multilevel_queue_ui,
            )

            render_multilevel_queue_ui()
        except ImportError:
            st.error(
                "UI component file nahi mili! Kindly check 'ui/cpu_scheduling/non_preemptive/multilevel_queue_ui.py'."
            )
    else:
        st.warning(
            "Not Implemented Yet — input forms and calculations "
            "will be added in a future update."
        )

else:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        .stat-card {
            background: #f8fafc;
            border-radius: 10px;
            padding: 12px 20px;
            margin-top: 5px;
            margin-bottom: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            border: 1px solid #e2e8f0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border-color: #cbd5e1;
        }
        .stat-label { font-size: 13px; color: #64748b; margin-bottom: 4px; font-weight: 500; }
        .stat-value { font-size: 24px; color: #0f172a; margin: 0; line-height: 1.1; }
        .bold-text { font-weight: 800; color: #1e293b; }
        .thin-text { font-weight: 300; color: #475569; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Welcome to Xeno OS")
    st.write(
        "Select a category from the sidebar and choose an algorithm "
        "to explore its simulation module."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-label">Simulation modules</div>
                <div class="stat-value">
                    <span class="bold-text">10</span> <span class="thin-text">Categories</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-label">Supported algorithms</div>
                <div class="stat-value">
                    <span class="bold-text">38+</span> <span class="thin-text">Models</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

render_footer()
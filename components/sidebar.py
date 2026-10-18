from pathlib import Path
from io import BytesIO
import base64

import streamlit as st
from PIL import Image


LOGO_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "logo.png"
)


def get_logo_base64():
    """Return the original logo as a transparent PNG."""
    if not LOGO_PATH.exists():
        return None

    logo = Image.open(LOGO_PATH).convert("RGBA")

    output = BytesIO()
    logo.save(output, format="PNG")

    return base64.b64encode(
        output.getvalue()
    ).decode("utf-8")


FUNCTIONS = {
    "01 · Process Management": [
        "1. Process State Transition",
        "2. Process Creation Simulation",
        "3. fork() / wait() Concept Simulation",
    ],

    "02 · Inter-Process Communication (IPC)": [
        "1. Message Passing",
        "2. Shared Memory Simulation",
        "3. Pipe Communication Simulation",
    ],

    "03 · Threads": [
        "1. Thread Lifecycle Simulation",
        "2. Thread Synchronization Simulation",
    ],

    "04 · CPU Scheduling": {
        "Preemptive": [
            "1. Round Robin (RR)",
            "2. Shortest Remaining Time First (SRTF)",
            "3. Preemptive Priority Scheduling",
            "4. Multilevel Feedback Queue",
        ],
        "Non-Preemptive": [
            "1. First Come, First Served (FCFS)",
            "2. SJF + Prediction of next burst of SJF",
            "3. Non-Preemptive Priority Scheduling",
            "4. Multilevel Queues",
        ],
    },

    "05 · Process Synchronization": [
        "1. Critical Section Simulation",
        "2. Peterson's Algorithm",
        "3. Semaphore Simulation",
        "4. Producer-Consumer / Bounded Buffer",
        "5. Dining Philosophers",
    ],

    "06 · Deadlocks": [
        "1. Banker's Algorithm",
        "2. Safe Sequence Detection",
    ],

    "07 · Memory Management": [
        "1. First Fit",
        "2. Best Fit",
        "3. Worst Fit",
    ],

    "08 · Virtual Memory / Page Replacement": [
        "1. FIFO Page Replacement",
        "2. LRU Page Replacement",
        "3. Optimal Page Replacement",
    ],

    "09 · File Allocation": [
        "1. Contiguous Allocation",
        "2. Linked Allocation",
        "3. Indexed Allocation",
    ],

    "10 · Disk Scheduling": [
        "1. FCFS Disk Scheduling",
        "2. SSTF (Shortest Seek Time First)",
        "3. SCAN",
        "4. C-SCAN",
        "5. LOOK",
        "6. C-LOOK",
    ],
}


def render_sidebar():
    defaults = {
        "open_category": None,
        "open_subcategory": None,
        "selected_function": None,
        "selected_algorithm": None,
        "current_page": "App",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    with st.sidebar:
        logo_base64 = get_logo_base64()

        # Brand section
        if logo_base64:
            st.markdown(
                f"""
                <div class="sidebar-brand">
                    <div class="brand-logo">
                        <img
                            src="data:image/png;base64,{logo_base64}"
                            alt="XENO OS Logo"
                        />
                    </div>
                    <div class="brand-copy">
                        <div class="brand-title">XENO OS</div>
                        <div class="brand-caption">
                            Operating System Simulator
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("### XENO OS")
            st.caption("Operating System Simulator")

        st.markdown(
            '<div class="nav-label">Simulation Modules</div>',
            unsafe_allow_html=True,
        )

        # Main category navigation
        for index, (category, items) in enumerate(
            FUNCTIONS.items()
        ):
            is_open = (
                st.session_state.open_category == category
            )

            if st.button(
                f"{'▾' if is_open else '▸'}  {category}",
                key=f"function_{index}",
                type="primary" if is_open else "secondary",
                use_container_width=True,
            ):
                st.session_state.open_category = (
                    None if is_open else category
                )
                st.session_state.open_subcategory = None
                st.rerun()

            if not is_open:
                continue

            # CPU Scheduling subcategories
            if isinstance(items, dict):
                for sub_index, (
                    subcategory,
                    algorithms,
                ) in enumerate(items.items()):

                    subcategory_key = (
                        f"{category}_{subcategory}"
                    )

                    is_sub_open = (
                        st.session_state.open_subcategory
                        == subcategory_key
                    )

                    if st.button(
                        f"{'▾' if is_sub_open else '▸'}  {subcategory}",
                        key=f"subcategory_{index}_{sub_index}",
                        type=(
                            "primary"
                            if is_sub_open
                            else "secondary"
                        ),
                        use_container_width=True,
                    ):
                        st.session_state.open_subcategory = (
                            None
                            if is_sub_open
                            else subcategory_key
                        )
                        st.rerun()

                    if is_sub_open:
                        for algorithm_index, algorithm in enumerate(
                            algorithms
                        ):
                            is_selected = (
                                st.session_state.selected_algorithm
                                == algorithm
                            )

                            if st.button(
                                algorithm,
                                key=(
                                    f"algorithm_{index}_"
                                    f"{sub_index}_{algorithm_index}"
                                ),
                                type=(
                                    "primary"
                                    if is_selected
                                    else "secondary"
                                ),
                                use_container_width=True,
                            ):
                                st.session_state.selected_function = category
                                st.session_state.selected_algorithm = algorithm
                                st.session_state.current_page = "Algorithm"
                                st.rerun()

            # Regular categories
            else:
                for algorithm_index, algorithm in enumerate(
                    items
                ):
                    is_selected = (
                        st.session_state.selected_algorithm
                        == algorithm
                    )

                    if st.button(
                        algorithm,
                        key=f"algorithm_{index}_{algorithm_index}",
                        type=(
                            "primary"
                            if is_selected
                            else "secondary"
                        ),
                        use_container_width=True,
                    ):
                        st.session_state.selected_function = category
                        st.session_state.selected_algorithm = algorithm
                        st.session_state.current_page = "Algorithm"
                        st.rerun()

    return (
        st.session_state.current_page,
        st.session_state.selected_function,
        st.session_state.selected_algorithm,
    )
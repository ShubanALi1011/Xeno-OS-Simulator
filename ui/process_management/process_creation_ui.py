import streamlit as st
from core.process_management.process_creation import ProcessCreationSimulator


def render_process_tree(node, level=0):
    indent_px = level * 20
    prefix = "" if level == 0 else "└─ "
    badge_bg = "#142D50" if level == 0 else "#E8F1FC"
    badge_color = "#FFFFFF" if level == 0 else "#2868B2"

    st.markdown(
        f"""
        <div style="margin-bottom: 6px; font-family: 'Inter', sans-serif; font-size: 13px; margin-left: {indent_px}px;">
            <span style="color: #94a3b8;">{prefix}</span>
            <strong style="color: #0f172a;">{node.name}</strong>
            <span style="font-size: 10px; color: {badge_color}; background: {badge_bg}; padding: 2px 8px; border-radius: 6px; margin-left: 6px; font-weight: 600;">
                PID: {node.pid} | {node.memory_allocated}MB | {node.priority}
            </span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    for child in node.children:
        render_process_tree(child, level + 1)


def render_process_creation_ui():
    # --- Custom Sleek OS Styling ---
    st.markdown(
        """
        <style>
        .os-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        }
        .log-item-fork {
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #2868B2;
        }
        .log-item-exit {
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #fff5f5;
            border: 1px solid #fed7d7;
            border-left: 3px solid #e53e3e;
        }
        
        /* Universal Form Submit & Standard Buttons Override to Xeno OS Blue */
        div.stFormSubmitButton > button,
        div.stButton > button {
            background: #2868B2 !important;
            background-color: #2868B2 !important;
            border: 1px solid #2868B2 !important;
            color: #FFFFFF !important;
        }
        div.stFormSubmitButton > button:hover,
        div.stButton > button:hover {
            background: #205895 !important;
            background-color: #205895 !important;
            border: 1px solid #205895 !important;
            color: #FFFFFF !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Session State Initialization
    if "process_creation_sim" not in st.session_state:
        st.session_state.process_creation_sim = ProcessCreationSimulator()

    sim = st.session_state.process_creation_sim

    # --- Top Control Form & Hierarchy Tree ---
    col_form, col_tree = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Spawn Child Process (sys_fork)</h5>",
            unsafe_allow_html=True,
        )

        with st.form("fork_process_form", clear_on_submit=True):
            available_parents = {
                f"{p.name} (PID: {p.pid})": p.pid
                for p in sim.processes.values()
            }
            parent_label = st.selectbox(
                "Parent Process", list(available_parents.keys())
            )
            child_name = st.text_input(
                "Child Process Name", value="chrome_worker"
            )

            c_mem, c_prio = st.columns(2)
            with c_mem:
                memory_mb = st.number_input(
                    "Memory (MB)", min_value=16, max_value=1024, value=64, step=16
                )
            with c_prio:
                priority = st.selectbox(
                    "Priority", ["Low", "Normal", "High", "Realtime"], index=1
                )

            submit_fork = st.form_submit_button(
                "Execute sys_fork()", use_container_width=True
            )

            if submit_fork:
                parent_pid = available_parents[parent_label]
                if child_name.strip():
                    success, msg = sim.fork_process(
                        parent_pid,
                        child_name.strip(),
                        memory_mb,
                        priority,
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter a valid process name.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Terminate Process (sys_exit)</h5>",
            unsafe_allow_html=True,
        )

        term_parents = {
            f"{p.name} (PID: {p.pid})": p.pid
            for p in sim.processes.values()
            if p.pid != 1
        }
        if term_parents:
            c_term, c_btn = st.columns([0.75, 0.25])
            with c_term:
                term_label = st.selectbox(
                    "Select Process to Terminate",
                    list(term_parents.keys()),
                    label_visibility="collapsed",
                )
            with c_btn:
                if st.button("Kill", use_container_width=True):
                    target_pid = term_parents[term_label]
                    success, msg = sim.terminate_process(target_pid)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.caption(
                "No terminable child processes active (Init process protected)."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Process Tree", use_container_width=True):
            sim.reset()
            st.rerun()

    with col_tree:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Process Hierarchy Tree</h5>",
            unsafe_allow_html=True,
        )

        # Native scrollable container for clean HTML rendering inside box
        tree_container = st.container(height=310)
        with tree_container:
            render_process_tree(sim.root)

    # --- Bottom: Process Table & System Call Log ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;'>Kernel Process Table (PCB Records)</h5>",
        unsafe_allow_html=True,
    )

    proc_df = sim.get_process_list()
    st.dataframe(proc_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;'>System Call Execution Log</h5>",
        unsafe_allow_html=True,
    )

    log_box = st.container(height=200)
    with log_box:
        for log in reversed(sim.history):
            log_class = (
                "log-item-exit" if log["action"] == "EXIT" else "log-item-fork"
            )
            st.markdown(
                f"""
                <div class="{log_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="font-size: 11px; color: #1e293b;">{log['action']}</strong>
                        <span style="font-size: 10px; color: #64748b;">{log['time']}</span>
                    </div>
                    <div style="font-size: 12px; color: #475569; margin-top: 2px;">{log['description']}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
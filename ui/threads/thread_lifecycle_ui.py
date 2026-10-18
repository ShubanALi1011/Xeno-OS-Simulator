import pandas as pd
import streamlit as st
from core.threads.thread_lifecycle_sim import ThreadLifecycleSimulator


def render_thread_lifecycle_ui():
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
        .log-item {
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #2868B2;
        }
        div.stButton > button {
            background: #2868B2 !important;
            background-color: #2868B2 !important;
            border: 1px solid #2868B2 !important;
            color: #FFFFFF !important;
        }
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

    if "thread_sim" not in st.session_state:
        st.session_state.thread_sim = ThreadLifecycleSimulator()

    sim = st.session_state.thread_sim

    col_form, col_act = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Spawn New Thread (pthread_create)</h5>",
            unsafe_allow_html=True,
        )

        with st.form("create_thread_form", clear_on_submit=True):
            t_name = st.text_input("Thread Name", value="worker_thread_2")
            t_priority = st.selectbox(
                "Priority", ["Low", "Normal", "High", "Realtime"], index=1
            )
            sub_create = st.form_submit_button(
                "Create Thread", use_container_width=True
            )
            if sub_create:
                if t_name.strip():
                    success, msg = sim.create_thread(
                        t_name.strip(), t_priority
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter a valid thread name.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Manage Thread State</h5>",
            unsafe_allow_html=True,
        )

        with st.form("state_thread_form", clear_on_submit=True):
            target_tid = st.selectbox(
                "Select Thread TID", list(sim.threads.keys())
            )
            target_state = st.selectbox(
                "New State", ["READY", "RUNNING", "BLOCKED", "TERMINATED"]
            )
            sub_state = st.form_submit_button(
                "Update State", use_container_width=True
            )
            if sub_state:
                success, msg = sim.change_state(int(target_tid), target_state)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with col_act:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Thread Termination</h5>",
            unsafe_allow_html=True,
        )

        with st.form("term_thread_form", clear_on_submit=True):
            term_tid = st.selectbox(
                "Select Thread to Terminate",
                [t for t in sim.threads.keys() if t != 101],
            )
            sub_term = st.form_submit_button(
                "Terminate Thread", use_container_width=True
            )
            if sub_term:
                success, msg = sim.terminate_thread(int(term_tid))
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Simulation", use_container_width=True):
            sim.reset()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Active Thread Control Block (TCB) Table</h5>",
        unsafe_allow_html=True,
    )

    df = pd.DataFrame(list(sim.threads.values()))
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Thread Audit Logs</h5>",
        unsafe_allow_html=True,
    )

    log_box = st.container(height=200)
    with log_box:
        for log in sim.history:
            st.markdown(
                f"""
                <div class="log-item">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="font-size: 11px; color: #2868B2;">[{log['sender']}]</strong>
                        <span style="font-size: 10px; color: #64748b;">{log['time']}</span>
                    </div>
                    <div style="font-size: 12px; color: #475569; margin-top: 2px;">{log['message']}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
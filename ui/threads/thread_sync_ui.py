import streamlit as st
from core.threads.thread_sync_sim import ThreadSyncSimulator


def render_thread_sync_ui():
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

    if "sync_sim" not in st.session_state:
        st.session_state.sync_sim = ThreadSyncSimulator()

    sim = st.session_state.sync_sim

    col_ctrl, col_status = st.columns([1.1, 0.9], gap="large")

    with col_ctrl:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Mutex & Critical Section Controls</h5>",
            unsafe_allow_html=True,
        )

        with st.form("sync_form", clear_on_submit=True):
            thread_name = st.selectbox(
                "Select Thread Context",
                [
                    "worker_thread_1",
                    "worker_thread_2",
                    "background_sync_thread",
                ],
            )
            action = st.selectbox(
                "Synchronization Action",
                [
                    "Acquire Mutex Lock",
                    "Increment Critical Counter",
                    "Release Mutex Lock",
                ],
            )
            sub_action = st.form_submit_button(
                "Execute Operation", use_container_width=True
            )

            if sub_action:
                if action == "Acquire Mutex Lock":
                    success, msg = sim.acquire_mutex(thread_name)
                elif action == "Increment Critical Counter":
                    success, msg = sim.increment_counter(thread_name)
                else:
                    success, msg = sim.release_mutex(thread_name)

                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Synchronization State", use_container_width=True):
            sim.reset()
            st.rerun()

    with col_status:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Mutex & Counter State</h5>",
            unsafe_allow_html=True,
        )

        lock_badge = (
            f"<span style='color: #b91c1c; font-weight: 700;'>LOCKED (Owner: {sim.active_lock_owner})</span>"
            if sim.mutex_locked
            else "<span style='color: #15803d; font-weight: 700;'>UNLOCKED (Available)</span>"
        )

        st.markdown(
            f"""
            <div class="os-card">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">MUTEX SYNCHRONIZATION PRIMITIVE</div>
                <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                    Mutex State: {lock_badge}<br>
                    Shared Counter Value: <b>{sim.shared_counter}</b>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Synchronization Audit Logs</h5>",
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
import streamlit as st
from core.ipc.shared_memory_sim import SharedMemorySimulator


def render_shared_memory_ui():
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
        .mem-block {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 16px;
            font-family: monospace;
            font-size: 13px;
            color: #0f172a;
            margin-bottom: 12px;
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

    if "shm_sim" not in st.session_state:
        st.session_state.shm_sim = SharedMemorySimulator()

    sim = st.session_state.shm_sim

    col_ctrl, col_view = st.columns([1.1, 0.9], gap="large")

    with col_ctrl:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Shared Memory Controls</h5>",
            unsafe_allow_html=True,
        )

        with st.form("shm_write_form", clear_on_submit=True):
            writer_pid = st.selectbox(
                "Active Process (Writer)", sim.attached_processes
            )
            new_content = st.text_input(
                "New Data Payload", value="Updated_Telemetry_Data_99"
            )
            sub_write = st.form_submit_button(
                "Write to Shared Memory", use_container_width=True
            )
            if sub_write:
                success, msg = sim.write_memory(writer_pid, new_content.strip())
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        c_att, c_det = st.columns(2)
        with c_att:
            att_pid = st.number_input(
                "Attach PID", min_value=100, max_value=999, value=103, step=1
            )
            if st.button("Attach Process", use_container_width=True):
                success, msg = sim.attach_process(int(att_pid))
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with c_det:
            det_pid = st.selectbox("Detach PID", sim.attached_processes)
            if st.button("Detach Process", use_container_width=True):
                success, msg = sim.detach_process(int(det_pid))
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        c_lock, c_reset = st.columns(2)
        with c_lock:
            lock_label = (
                "Unlock Segment"
                if sim.is_locked
                else "Lock Segment (Mutex)"
            )
            if st.button(lock_label, use_container_width=True):
                sim.toggle_lock()
                st.rerun()
        with c_reset:
            if st.button("Reset Segment", use_container_width=True):
                sim.reset()
                st.rerun()

    with col_view:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Segment State & Content</h5>",
            unsafe_allow_html=True,
        )

        lock_badge = (
            "<span style='color: #b91c1c; font-weight: 700;'>LOCKED (Mutex Protected)</span>"
            if sim.is_locked
            else "<span style='color: #15803d; font-weight: 700;'>UNLOCKED</span>"
        )

        st.markdown(
            f"""
            <div class="os-card">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">SHM IDENTIFIER: {sim.shm_id}</div>
                <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                    Segment Size: <b>{sim.size_kb} KB</b><br>
                    Synchronization Status: {lock_badge}<br>
                    Attached Processes (PIDs): <b>{sim.attached_processes}</b>
                </div>
                <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 12px 0;">
                <div style="font-size: 12px; font-weight: 600; color: #1e293b; margin-bottom: 4px;">CURRENT SHARED DATA CONTENT:</div>
                <div class="mem-block">{sim.shared_data}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Shared Memory Audit Logs</h5>",
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
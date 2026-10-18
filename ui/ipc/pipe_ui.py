import streamlit as st
from core.ipc.pipe_sim import PipeSimulator


def render_pipe_ui():
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
        .pipe-slot {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-left: 3px solid #2868B2;
            font-family: monospace;
            font-size: 13px;
        }
        .log-item {
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #0f172a;
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

    if "pipe_sim" not in st.session_state:
        st.session_state.pipe_sim = PipeSimulator()

    sim = st.session_state.pipe_sim

    col_form, col_box = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Pipe Communication Controls</h5>",
            unsafe_allow_html=True,
        )

        with st.form("pipe_write_form", clear_on_submit=True):
            writer_pid = st.number_input(
                "Writer Process PID",
                min_value=100,
                max_value=999,
                value=101,
                step=1,
            )
            data_chunk = st.text_input(
                "Data Chunk to Write", value="STREAM_BYTE_PACKET_01"
            )
            sub_write = st.form_submit_button(
                "Write to Pipe (fd[1])", use_container_width=True
            )
            if sub_write:
                if data_chunk.strip():
                    success, msg = sim.write_to_pipe(
                        writer_pid, data_chunk.strip()
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter valid data chunk.")

        st.markdown("<br>", unsafe_allow_html=True)
        c_read, c_reset = st.columns(2)
        with c_read:
            reader_pid = st.number_input(
                "Reader PID", min_value=100, max_value=999, value=102, step=1
            )
            if st.button("Read from Pipe (fd[0])", use_container_width=True):
                success, msg = sim.read_from_pipe(reader_pid)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with c_reset:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Reset Pipe", use_container_width=True):
                sim.reset()
                st.rerun()

    with col_box:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Unidirectional Pipe Buffer</h5>",
            unsafe_allow_html=True,
        )

        pipe_container = st.container(height=260)
        with pipe_container:
            if not sim.buffer:
                st.caption(
                    "Pipe buffer is currently empty (No data stream in transit)."
                )
            else:
                for idx, chunk in enumerate(sim.buffer):
                    st.markdown(
                        f"""
                        <div class="pipe-slot">
                            <span style="color: #64748b; font-size: 11px;">SLOT [{idx}] ➔</span> <b>{chunk}</b>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Kernel Pipe Audit Logs</h5>",
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
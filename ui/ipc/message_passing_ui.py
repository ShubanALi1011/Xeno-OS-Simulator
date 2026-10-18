import streamlit as st
from core.ipc.message_passing_sim import MessagePassingSimulator


def render_message_passing_ui():
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
        .mail-slot {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-left: 3px solid #2868B2;
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

    if "msg_sim" not in st.session_state:
        st.session_state.msg_sim = MessagePassingSimulator()

    sim = st.session_state.msg_sim

    col_form, col_box = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>IPC Message Passing Controls</h5>",
            unsafe_allow_html=True,
        )

        with st.form("send_msg_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                sender_pid = st.number_input(
                    "Sender PID", min_value=100, max_value=999, value=101, step=1
                )
            with c2:
                receiver_pid = st.number_input(
                    "Receiver PID",
                    min_value=100,
                    max_value=999,
                    value=102,
                    step=1,
                )

            msg_text = st.text_input(
                "Message Payload", value="Hello from process context!"
            )
            submit_send = st.form_submit_button(
                "Send Message (enqueue)", use_container_width=True
            )

            if submit_send:
                if msg_text.strip():
                    success, msg = sim.send_message(
                        sender_pid, receiver_pid, msg_text.strip()
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter a message payload.")

        st.markdown("<br>", unsafe_allow_html=True)
        c_recv, c_reset = st.columns(2)
        with c_recv:
            if st.button(
                "Receive Message (dequeue)", use_container_width=True
            ):
                success, msg = sim.receive_message(receiver_pid)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with c_reset:
            if st.button("Reset Mailbox", use_container_width=True):
                sim.reset()
                st.rerun()

    with col_box:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Mailbox Buffer Queue</h5>",
            unsafe_allow_html=True,
        )

        mailbox_container = st.container(height=260)
        with mailbox_container:
            if not sim.mailbox:
                st.caption(
                    "Mailbox buffer is currently empty (No pending messages)."
                )
            else:
                for item in sim.mailbox:
                    st.markdown(
                        f"""
                        <div class="mail-slot">
                            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b;">
                                <span><b>{item['sender']} ➔ {item['receiver']}</b></span>
                                <span>{item['time']}</span>
                            </div>
                            <div style="font-size: 12px; color: #0f172a; margin-top: 4px;">Payload: <b>{item['text']}</b></div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Kernel IPC Audit Logs</h5>",
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
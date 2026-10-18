import streamlit as st
from core.process_management.fork_wait_sim import ForkWaitSimulator


def render_fork_wait_ui():
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

    if "fork_wait_sim" not in st.session_state:
        st.session_state.fork_wait_sim = ForkWaitSimulator()

    sim = st.session_state.fork_wait_sim

    col_ctrl, col_status = st.columns([1.1, 0.9], gap="large")

    with col_ctrl:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Fork & Wait System Call Controls</h5>",
            unsafe_allow_html=True,
        )

        st.info(
            "Simulates UNIX `fork()` process duplication and `wait()` synchronization semantics."
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "Execute sys_fork()",
                disabled=(sim.execution_step > 0),
                use_container_width=True,
            ):
                success, msg = sim.execute_fork()
                if success:
                    st.success(msg)
                    st.rerun()

        with c2:
            if st.button(
                "Execute sys_wait()",
                disabled=(sim.execution_step != 1),
                use_container_width=True,
            ):
                success, msg = sim.execute_wait()
                if success:
                    st.success(msg)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 8px;'>Isolate Memory Modifier (Copy-on-Write)</h5>",
            unsafe_allow_html=True,
        )

        with st.form("modify_var_form", clear_on_submit=True):
            actor_choice = st.selectbox(
                "Select Process Context", ["PARENT", "CHILD"]
            )
            new_val = st.number_input(
                "New Value for Variable X", value=42, step=1
            )
            sub_mod = st.form_submit_button(
                "Modify Variable X", use_container_width=True
            )
            if sub_mod:
                success, msg = sim.modify_variable(actor_choice, int(new_val))
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Simulation", use_container_width=True):
            sim.reset()
            st.rerun()

    with col_status:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Process Context & State</h5>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="os-card">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">PARENT PROCESS</div>
                <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                    PID: <b>{sim.parent_pid}</b><br>
                    Status: <span style="color: #15803d; font-weight: 600;">{sim.parent_status}</span><br>
                    Variable X Value: <b>{sim.shared_variable_x}</b>
                </div>
            </div>
            <div class="os-card">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">CHILD PROCESS</div>
                <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                    PID: <b>{sim.child_pid if sim.child_pid else 'N/A (Not Forked)'}</b><br>
                    Status: <span style="color: #b45309; font-weight: 600;">{sim.child_status}</span><br>
                    Variable X Value: <b>{sim.shared_variable_x}</b>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Execution Audit Logs</h5>",
        unsafe_allow_html=True,
    )

    log_box = st.container(height=220)
    with log_box:
        for log in sim.logs:
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
import streamlit as st
from core.process_management.state_transition import ProcessSimulator


def render_state_transition_ui():
    # --- Custom Minimalist Styling for State Transition ---
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
        .state-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-new { background: #e0f2fe; color: #0369a1; }
        .badge-ready { background: #fef3c7; color: #b45309; }
        .badge-running { background: #dcfce7; color: #15803d; }
        .badge-waiting { background: #f3e8ff; color: #6b21a8; }
        .badge-terminated { background: #fee2e2; color: #b91c1c; }
        
        .log-item {
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 8px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #2868B2;
        }

        /* Override Streamlit Primary Button to Xeno OS Blue */
        div.stButton > button[kind="primary"],
        div.stButton > button[data-testid="stBaseButton-primary"] {
            background-color: #2868B2 !important;
            border-color: #2868B2 !important;
            color: #FFFFFF !important;
        }
        div.stButton > button[kind="primary"]:hover,
        div.stButton > button[data-testid="stBaseButton-primary"]:hover {
            background-color: #205895 !important;
            border-color: #205895 !important;
            color: #FFFFFF !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Session state initialization
    if "process_sim" not in st.session_state:
        st.session_state.process_sim = ProcessSimulator()

    sim = st.session_state.process_sim
    current = sim.current_state

    # Map current state to CSS badge class
    badge_class = f"badge-{current.lower()}"

    # --- Layout: Two Balanced Columns ---
    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown(
            f"""
            <div class="os-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div>
                        <span style="font-size: 12px; color: #64748b; font-weight: 500;">ACTIVE PROCESS</span><br>
                        <strong style="font-size: 18px; color: #0f172a;">{sim.process_name}</strong> <span style="font-size: 13px; color: #64748b;">({sim.process_id})</span>
                    </div>
                    <div>
                        <span class="state-badge {badge_class}">{current}</span>
                    </div>
                </div>
                <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 12px 0;">
                <div style="font-size: 13px; color: #475569;">
                    <b>Lifecycle Stage:</b> Process is currently residing in the <u>{current}</u> queue buffer.
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h5 style='font-size: 15px; font-weight: 600; color: #1e293b; margin-top: 15px;'>Kernel Execution Controls</h5>",
            unsafe_allow_html=True,
        )

        # Action Buttons matching exact clean OS states
        if current == "New":
            if st.button(
                "Admit Process (New ➔ Ready)",
                type="primary",
                use_container_width=True,
            ):
                sim.transition("Admit")
                st.rerun()

        elif current == "Ready":
            if st.button(
                "Dispatch to CPU (Ready ➔ Running)",
                type="primary",
                use_container_width=True,
            ):
                sim.transition("Dispatch")
                st.rerun()

        elif current == "Running":
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("Interrupt", use_container_width=True):
                    sim.transition("Interrupt")
                    st.rerun()
            with b2:
                if st.button("I/O Request", use_container_width=True):
                    sim.transition("I/O Request")
                    st.rerun()
            with b3:
                if st.button("Terminate", use_container_width=True):
                    sim.transition("Exit")
                    st.rerun()

        elif current == "Waiting":
            if st.button(
                "Complete I/O (Waiting ➔ Ready)",
                type="primary",
                use_container_width=True,
            ):
                sim.transition("I/O Complete")
                st.rerun()

        elif current == "Terminated":
            st.info(
                "Execution complete. Process lifecycle terminated successfully."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Simulator State", use_container_width=True):
            sim.reset()
            st.rerun()

    with col2:
        st.markdown(
            "<h5 style='font-size: 15px; font-weight: 600; color: #1e293b; margin-bottom: 12px;'>Transition Audit Trail</h5>",
            unsafe_allow_html=True,
        )

        # Scrollable clean audit container simulation
        log_container = st.container(height=340)
        with log_container:
            for i, log in enumerate(reversed(sim.history)):
                step_num = len(sim.history) - i
                st.markdown(
                    f"""
                    <div class="log-item">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-size: 11px; font-weight: 600; color: #2868B2;">STEP 0{step_num}</span>
                            <span style="font-size: 11px; font-weight: 700; color: #0f172a;">{log['state'].upper()}</span>
                        </div>
                        <div style="font-size: 12px; color: #475569; line-height: 1.4;">{log['description']}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
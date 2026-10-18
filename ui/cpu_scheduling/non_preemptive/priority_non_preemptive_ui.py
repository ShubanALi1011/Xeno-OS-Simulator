import pandas as pd
import streamlit as st
from core.cpu_scheduling.non_preemptive.priority_non_preemptive_sim import PriorityNonPreemptiveSimulator


def render_priority_non_preemptive_ui():
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

    if "priority_np_sim" not in st.session_state:
        st.session_state.priority_np_sim = PriorityNonPreemptiveSimulator()

    sim = st.session_state.priority_np_sim

    col_ctrl, col_stats = st.columns([1.1, 0.9], gap="large")

    with col_ctrl:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Priority Controls (Non-Preemptive)</h5>",
            unsafe_allow_html=True,
        )

        with st.form("priority_np_form", clear_on_submit=False):
            num_processes = st.number_input(
                "Number of Processes", min_value=1, max_value=10, value=len(sim.processes), step=1
            )
            sub_run = st.form_submit_button(
                "Run Priority Simulation", use_container_width=True
            )

            if sub_run:
                success, msg = sim.run_simulation(int(num_processes))
                if success:
                    st.success(msg)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Simulation Queue", use_container_width=True):
            sim.reset(num_processes=4)
            st.rerun()

    with col_stats:
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Queue Overview</h5>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="os-card">
                <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">NON-PREEMPTIVE PRIORITY CONFIG</div>
                <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                    Total Processes in Ready Queue: <b>{len(sim.processes)}</b><br>
                    Algorithm Type: <b>Priority Scheduling (Non-Preemptive, Lower number = Higher priority)</b>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # --- Gantt Chart Visualization ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Execution Timeline (Gantt Chart)</h5>",
        unsafe_allow_html=True,
    )

    if sim.gantt_chart:
        cols = st.columns(len(sim.gantt_chart))
        for idx, item in enumerate(sim.gantt_chart):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #2868B2; color: white; padding: 10px 4px; border-radius: 8px; text-align: center; font-size: 11px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        {item['name']}<br>
                        <span style="font-size: 9px; font-weight: 400; opacity: 0.9;">{item['start']} ➔ {item['end']}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Click 'Run Priority Simulation' to generate Gantt chart timeline.")

    # --- Metrics Table ---
    if sim.metrics:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Process Performance Metrics</h5>",
            unsafe_allow_html=True,
        )
        df = pd.DataFrame(sim.metrics)[
            [
                "name",
                "arrival",
                "burst",
                "priority",
                "completion",
                "turnaround",
                "waiting",
            ]
        ]
        df.columns = [
            "Process",
            "Arrival Time",
            "Burst Time",
            "Priority",
            "Completion Time",
            "Turnaround Time",
            "Waiting Time",
        ]
        st.dataframe(df, use_container_width=True, hide_index=True)

        avg_wt = df["Waiting Time"].mean()
        avg_tat = df["Turnaround Time"].mean()
        st.caption(
            f"📊 **Averages** — Waiting Time: **{avg_wt:.2f}** units | Turnaround Time: **{avg_tat:.2f}** units"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 10px; text-transform: uppercase;'>Scheduler Audit Logs</h5>",
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
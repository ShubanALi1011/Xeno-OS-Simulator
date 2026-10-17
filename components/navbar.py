import streamlit as st


def render_header():
    # Single unified horizontal block row with auto-adjusting column bounds
    col_text, col_btns = st.columns([7.2, 2.8], gap="medium")

    with col_text:
        st.markdown(
            """
            <div class="hero-left-content">
                <h1 class="hero-title">XENO OS <span class="simulator-word">Simulator</span></h1>
                <p class="hero-subtitle">Explore operating system concepts through interactive simulations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_btns:
        st.markdown('<div class="hero-buttons-wrapper">', unsafe_allow_html=True)
        if st.button("Restart OS", key="hero_restart_btn", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        if st.button("Dashboard", key="hero_dashboard_btn", use_container_width=True):
            st.session_state["reset_navigation"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
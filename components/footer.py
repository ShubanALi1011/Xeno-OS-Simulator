
import streamlit as st


def render_footer():
    st.markdown("---")

    st.markdown(
        """
        <div class="footer">
            © 2026 XENO OS Simulator · All rights reserved
        </div>
        """,
        unsafe_allow_html=True,
    )

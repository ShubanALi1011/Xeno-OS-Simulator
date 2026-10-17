import base64
import time
from pathlib import Path

import streamlit as st


DURATION = 5

BG_CENTER = "#031C4C"
BG_EDGE = "#000000"
ACCENT = "#5AA2FF"
LIGHT = "#CFE3FF"

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"


HTML = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700;800&display=swap');

.splash {
    position: fixed;
    inset: 0;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', sans-serif;
    color: #F2F6FF;
    background: radial-gradient(
        ellipse at 50% 40%,
        BG_CENTER 0%,
        BG_EDGE 100%
    );
    animation: fade .6s ease calc(DURs - .6s) forwards;
}

.content {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: reveal 1s ease both;
}

.logo {
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo img {
    width: 82px;
    height: 82px;
    object-fit: contain;
    filter: drop-shadow(0 0 18px ACCENT66);
}

.ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 1px solid ACCENT22;
    border-top-color: ACCENT;
    animation: spin 2.4s linear infinite;
}

h1 {
    margin: 0;
    font-size: 40px;
    font-weight: 800;
    letter-spacing: -1px;
}

h1 span {
    color: LIGHT;
    font-weight: 300;
}

.tag {
    margin-top: 14px;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: none;
    color: LIGHT;
    opacity: .7;
}

.bar {
    width: 160px;
    height: 2px;
    margin-top: 38px;
    background: #ffffff1a;
    overflow: hidden;
}

.bar i {
    display: block;
    height: 100%;
    width: 0;
    background: ACCENT;
    box-shadow: 0 0 10px ACCENT;
    animation: load DURs ease-out forwards;
}

.loading {
    margin-top: 14px;
    font-size: 11px;
    letter-spacing: 2px;
    color: LIGHT;
    opacity: .7;
}

@keyframes reveal {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

@keyframes load {
    to {
        width: 100%;
    }
}

@keyframes fade {
    to {
        opacity: 0;
        visibility: hidden;
    }
}
</style>

<div class="splash">
    <div class="content">
        <div class="logo">
            <div class="ring"></div>
            LOGO_TAG
        </div>

        <h1>Xeno OS <span>Simulator</span></h1>

        <div class="tag">
            A new space to compute
        </div>

        <div class="bar">
            <i></i>
        </div>

        <div class="loading">
            Loading...
        </div>
    </div>
</div>
"""


def build_html():
    logo_tag = ""

    if LOGO.exists():
        data = base64.b64encode(LOGO.read_bytes()).decode()
        logo_tag = f'<img src="data:image/png;base64,{data}">'

    html = HTML

    for key, value in {
        "BG_CENTER": BG_CENTER,
        "BG_EDGE": BG_EDGE,
        "ACCENT": ACCENT,
        "LIGHT": LIGHT,
        "DUR": DURATION,
        "LOGO_TAG": logo_tag,
    }.items():
        html = html.replace(key, str(value))

    return html


def show_splash():
    if st.session_state.get("splash_done"):
        return

    box = st.empty()
    box.html(build_html())

    time.sleep(DURATION)

    box.empty()
    st.session_state.splash_done = True
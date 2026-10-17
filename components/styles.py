import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Material+Symbols+Rounded&display=swap'
        );

        /* ========================================
           XENO OS - MODERN DESIGN SYSTEM
        ======================================== */

        :root {
            --navy: #142D50;
            --navy-deep: #102440;
            --blue: #2868B2;
            --blue-hover: #205895;
            --blue-soft: #E8F1FC;
            --blue-border: #C8DBF2;

            --page: #F3F6FA;
            --sidebar: #F8FAFD;
            --white: #FFFFFF;

            --text: #202F43;
            --text-secondary: #62738A;
            --muted: #8593A6;

            --border: #DCE4EE;
            --border-light: #E9EEF5;
        }

        /* ========================================
           GLOBAL TYPOGRAPHY
        ======================================== */

        html,
        body,
        .stApp,
        .stApp *,
        button,
        input,
        textarea,
        select {
            font-family: 'Inter', sans-serif !important;
        }

        /* Preserve Material Symbols */

        [data-testid="stIconMaterial"],
        .material-symbols-rounded {
            font-family: 'Material Symbols Rounded' !important;
            font-weight: normal !important;
            font-style: normal !important;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            font-feature-settings: 'liga';
        }

        /* App background */

        .stApp {
            background: var(--page);
            color: var(--text);
        }

        #MainMenu,
        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1rem !important;
            padding-bottom: 1.5rem;
        }


        /* ========================================
           PERFECT SIDEBAR TOP ALIGNMENT & GAPS
        ======================================== */
        
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
            display: flex !important;
            height: 40px !important;
            min-height: 40px !important;
            margin: 0 !important;
            padding: 0 8px !important;
        }

        section[data-testid="stSidebar"] div.block-container {
            padding-top: 1rem !important;
        }

        section[data-testid="stSidebar"]
        div[data-testid="stVerticalBlock"] {
            gap: 0.25rem !important;
        }

        section[data-testid="stSidebar"] {
            background: var(--sidebar) !important;
            border-right: 1px solid #DCE4EE;
            box-shadow: 3px 0 16px rgba(25, 48, 78, .025);
        }

        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarExpandButton"] button {
            color: #315F98 !important;
        }

        /* ========================================
           BRAND AREA
        ======================================== */

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0px 3px 15px !important;
            margin-top: 0px !important;
            margin-bottom: 8px;
            border-bottom: 1px solid #E1E8F1;
        }

        .brand-logo {
            width: 46px;
            height: 46px;
            min-width: 46px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 6px;
            box-sizing: border-box;
            overflow: hidden;
            border-radius: 13px;

            background: linear-gradient(
                145deg,
                #183C6B,
                #2868B2
            );

            border: 1px solid #2B639E;
            box-shadow: 0 4px 10px rgba(30, 75, 125, .16);
        }

        .brand-logo img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: contain;
            background: transparent;
        }

        .brand-copy {
            flex: 1;
            min-width: 0;
        }

        .brand-title {
            color: #172F50;
            font-size: 19px;
            font-weight: 800;
            line-height: 1.3;
            letter-spacing: -.65px;
        }

        .brand-caption {
            color: #718198;
            font-size: 9px;
            font-weight: 500;
            line-height: 1.6;
            margin-top: 4px;
            letter-spacing: .45px;
        }

        .nav-label {
            color: #172F50;
            font-size: 15px;
            font-weight: 800;
            margin: 7px 0 12px;
            padding-left: 3px;
        }

        /* ========================================
           SIDEBAR BUTTON STRUCTURE
        ======================================== */

        section[data-testid="stSidebar"] .stButton {
            width: 100%;
        }

        section[data-testid="stSidebar"] .stButton > button {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start !important;

            width: 100%;
            min-height: 43px;
            padding: 10px 12px;
            border-radius: 10px;

            background: #FFFFFF !important;
            background-image: none !important;
            color: #35465C !important;

            border: 1px solid #E1E7EF !important;
            box-shadow: 0 1px 3px rgba(25, 48, 78, .035) !important;

            transition: background .18s ease, border-color .18s ease, color .18s ease;
        }

        section[data-testid="stSidebar"]
        .stButton > button > div {
            display: flex;
            align-items: center;
            justify-content: flex-start !important;
            width: 100%;
            text-align: left !important;
        }

        section[data-testid="stSidebar"]
        .stButton > button p {
            width: 100%;
            margin: 0;
            text-align: left !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 12px;
            font-weight: 600 !important;
            line-height: 1.55;
        }

        /* Category Buttons */

        section[data-testid="stSidebar"]
        [class*="st-key-function_"] button {
            background: #FFFFFF !important;
            color: #35465C !important;
            border: 1px solid #E1E7EF !important;
        }

        section[data-testid="stSidebar"]
        [class*="st-key-function_"] button:hover {
            background: #EDF4FC !important;
            color: #24558F !important;
            border-color: #CADCF0 !important;
        }

        section[data-testid="stSidebar"]
        [class*="st-key-function_"] button[kind="primary"],
        section[data-testid="stSidebar"]
        [class*="st-key-function_"] button[data-testid="stBaseButton-primary"] {
            background: #244F86 !important;
            color: #FFFFFF !important;
            border: 1px solid #244F86 !important;
            font-weight: 600 !important;
        }

        /* Algorithm Submenu */

        section[data-testid="stSidebar"]
        [class*="st-key-algorithm_"] {
            margin-left: 11px;
            padding-left: 11px;
            border-left: 2px solid #CEDCEE;
        }

        section[data-testid="stSidebar"]
        [class*="st-key-algorithm_"] button {
            min-height: 36px;
            padding: 7px 10px;
            border-radius: 8px;
            background: #F0F3F8 !important;
            color: #53657B !important;
            border: 1px solid #E2E8F0 !important;
            font-size: 11px;
            font-weight: 500 !important;
        }

        section[data-testid="stSidebar"]
        [class*="st-key-algorithm_"] button:hover {
            background: #E4EDF9 !important;
            color: #244F86 !important;
            border-color: #C8DAF0 !important;
        }

        section[data-testid="stSidebar"]
        [class*="st-key-algorithm_"] button[kind="primary"],
        section[data-testid="stSidebar"]
        [class*="st-key-algorithm_"] button[data-testid="stBaseButton-primary"] {
            background: #DCE9F9 !important;
            color: #173F72 !important;
            border: 1px solid #BCD2ED !important;
            box-shadow: inset 3px 0 0 #3478C9 !important;
            font-weight: 700 !important;
        }

        /* ========================================
           UNIFIED HERO BANNER ROW STYLING
        ======================================== */

        div[data-testid="stHorizontalBlock"]:has(.hero-left-content) {
            position: relative;
            overflow: hidden;
            isolation: isolate;

            background: linear-gradient(
                115deg,
                #122947 0%,
                #193F70 55%,
                #2868B2 100%
            ) !important;

            border: 1px solid rgba(255, 255, 255, .16) !important;
            border-radius: 19px !important;
            padding: 28px 34px !important;
            margin-top: 5px !important;
            margin-bottom: 23px !important;
            color: #FFFFFF !important;

            box-shadow: 0 8px 24px rgba(20, 45, 80, .12) !important;
            align-items: center !important;
            min-height: 130px !important;
        }

        /* Right side glowing light layers */
        div[data-testid="stHorizontalBlock"]:has(.hero-left-content)::before {
            content: "";
            position: absolute;
            width: 280px;
            height: 280px;
            right: -40px;
            top: -100px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
            z-index: 0;
            pointer-events: none;
        }

        div[data-testid="stHorizontalBlock"]:has(.hero-left-content)::after {
            content: "";
            position: absolute;
            width: 200px;
            height: 200px;
            right: 80px;
            bottom: -90px;
            border-radius: 50%;
            background: rgba(160, 198, 241, 0.12);
            z-index: 0;
            pointer-events: none;
        }

        /* Left Content - Strict Inner Containment */
        .hero-left-content {
            position: relative;
            display: flex;
            flex-direction: column;
            gap: 6px;
            z-index: 2;
            justify-content: center;
            width: 100%;
        }

        .hero-title {
            color: #FFFFFF !important;
            font-size: 45px !important;
            font-weight: 700 !important;
            letter-spacing: -.8px !important;
            line-height: 1.15 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .hero-title .simulator-word {
            font-weight: 300 !important;
            letter-spacing: -.5px !important;
        }

        .hero-subtitle {
            color: #DCE8F7 !important;
            font-size: 12px !important;
            font-weight: 400 !important;
            line-height: 1.4 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Buttons container inside right column */
        .hero-buttons-wrapper {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 6px;
            align-items: flex-end;
            justify-content: center;
            height: 100%;
        }

        div[class*="st-key-hero_"] button {
            background: rgba(255, 255, 255, 0.14) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            backdrop-filter: blur(6px) !important;
            border-radius: 6px !important;
            font-size: 11px !important;
            font-weight: 500 !important;
            padding: 4px 10px !important;
            min-height: 28px !important;
            max-width: 115px !important;
            cursor: pointer !important;
            transition: all 0.18s ease !important;
        }

        div[class*="st-key-hero_"] button:hover {
            background: #FFFFFF !important;
            color: #122947 !important;
            border-color: #FFFFFF !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
        }

        /* ========================================
           CONTENT CARDS & FOOTER
        ======================================== */

        .module-card {
            background: #FFFFFF;
            border: 1px solid #DFE7F0;
            border-radius: 15px;
            padding: 24px;
            margin-bottom: 18px;
            box-shadow: 0 3px 12px rgba(28, 48, 77, .04);
        }

        .footer {
            text-align: center;
            color: #8493A6;
            font-size: 11px;
            font-weight: 400;
            padding: 13px 0 5px;
        }

        /* ========================================
           RESPONSIVE
        ======================================== */

        @media (max-width: 640px) {
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }

            section[data-testid="stSidebar"] .block-container {
                padding: 1rem .7rem;
            }

            .sidebar-brand {
                padding-bottom: 16px;
            }

            .brand-title {
                font-size: 18px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
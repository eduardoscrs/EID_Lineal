import streamlit as st


def configurar_pagina() -> None:
    """Configura la pagina y aplica estilos visuales simples."""
    st.set_page_config(
        page_title="Buscador Semantico Vectorial",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(20, 184, 166, 0.14), transparent 28rem),
                radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.12), transparent 26rem),
                #071826;
            color: #e6f6f4;
        }
        .main .block-container {
            padding-top: 1.7rem;
            padding-bottom: 2rem;
            max-width: 1220px;
        }
        h1, h2, h3 {
            letter-spacing: 0;
            color: #f0fdfa;
        }
        p, li, label, span {
            color: inherit;
        }
        [data-testid="stSidebar"] {
            background: #06131f;
            border-right: 1px solid #123247;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #d8fbf2;
        }
        .stTextInput input,
        .stTextArea textarea {
            background: #0b2233;
            color: #e6f6f4;
            border: 1px solid #1c4a63;
            border-radius: 8px;
        }
        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #14b8a6;
            box-shadow: 0 0 0 1px #14b8a6;
        }
        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
            color: #04111b;
            border: 1px solid #2dd4bf;
            border-radius: 8px;
            font-weight: 800;
        }
        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%);
            color: #03131d;
            border-color: #99f6e4;
        }
        button[data-baseweb="tab"] {
            color: #b8d9d5;
            background: #0a1d2c;
            border-radius: 8px 8px 0 0;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #071826;
            background: #5eead4;
        }
        .app-hero {
            background:
                radial-gradient(circle at top right, rgba(45, 212, 191, 0.24), transparent 32%),
                linear-gradient(135deg, #0b2233 0%, #102f46 54%, #0f3d3a 100%);
            border: 1px solid #1e5f74;
            border-radius: 8px;
            padding: 1.35rem 1.45rem;
            margin-bottom: 1rem;
            box-shadow: 0 16px 42px rgba(0, 0, 0, 0.28);
        }
        .app-hero h1 {
            margin: 0 0 0.35rem 0;
            color: #f0fdfa;
            font-size: 2.15rem;
        }
        .app-hero p {
            margin: 0;
            color: #b8d9d5;
            font-size: 1.02rem;
        }
        .hero-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.9rem;
        }
        .hero-badge {
            background: #082638;
            border: 1px solid #1f9e8c;
            border-radius: 999px;
            color: #a7f3d0;
            font-size: 0.86rem;
            font-weight: 650;
            padding: 0.35rem 0.65rem;
        }
        .info-box {
            background: #0b2233;
            border: 1px solid #1c4a63;
            border-left: 5px solid #14b8a6;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            color: #d8fbf2;
            margin: 0.5rem 0 1rem 0;
        }
        .small-note {
            color: #a9c9c5;
            font-size: 0.92rem;
        }
        .flow-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 0.7rem;
        }
        .flow-step {
            background: linear-gradient(180deg, #0d2638 0%, #0a1d2c 100%);
            border: 1px solid #1b4f69;
            border-radius: 8px;
            padding: 0.85rem;
            min-height: 116px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
        }
        .flow-number {
            width: 1.8rem;
            height: 1.8rem;
            background: #14b8a6;
            color: #03131d;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 750;
            margin-bottom: 0.5rem;
        }
        .flow-title {
            color: #f0fdfa;
            font-weight: 750;
            margin-bottom: 0.25rem;
        }
        .flow-text {
            color: #b8d9d5;
            font-size: 0.9rem;
            line-height: 1.35;
        }
        .doc-card {
            background: linear-gradient(180deg, #0d2638 0%, #0a1d2c 100%);
            border: 1px solid #1b4f69;
            border-radius: 8px;
            padding: 0.95rem;
            min-height: 180px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
            margin-bottom: 0.75rem;
        }
        .doc-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            margin-bottom: 0.55rem;
        }
        .doc-name {
            color: #e6fffb;
            font-weight: 800;
            font-size: 1.02rem;
        }
        .doc-topic {
            background: #063b3a;
            color: #99f6e4;
            border: 1px solid #14b8a6;
            border-radius: 999px;
            padding: 0.25rem 0.55rem;
            font-size: 0.78rem;
            font-weight: 700;
            white-space: nowrap;
        }
        .doc-text {
            color: #cfe8e4;
            line-height: 1.42;
            margin-bottom: 0.65rem;
        }
        .doc-meta {
            color: #91b7b2;
            font-size: 0.82rem;
        }
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin: 0.45rem 0 1rem 0;
        }
        .pill {
            background: #0b2233;
            border: 1px solid #1c4a63;
            border-radius: 999px;
            color: #a7f3d0;
            padding: 0.25rem 0.55rem;
            font-size: 0.82rem;
            font-weight: 650;
        }
        .top-result-card {
            background:
                radial-gradient(circle at top right, rgba(94, 234, 212, 0.18), transparent 34%),
                linear-gradient(135deg, #0e2b3f 0%, #063b3a 100%);
            border: 1px solid #20c6b4;
            border-radius: 8px;
            padding: 1rem 1.1rem;
            margin: 0.75rem 0 1rem 0;
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.26);
        }
        .top-result-kicker {
            color: #5eead4;
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04rem;
            margin-bottom: 0.25rem;
        }
        .top-result-title {
            color: #f0fdfa;
            font-size: 1.25rem;
            font-weight: 850;
            margin-bottom: 0.35rem;
        }
        .top-result-text {
            color: #cfe8e4;
            line-height: 1.45;
            margin-bottom: 0.65rem;
        }
        .rank-card {
            background: #0a1d2c;
            border: 1px solid #1b4f69;
            border-radius: 8px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.6rem;
            box-shadow: 0 9px 22px rgba(0, 0, 0, 0.22);
        }
        .rank-line {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: center;
            margin-bottom: 0.45rem;
        }
        .rank-title {
            color: #e6fffb;
            font-weight: 800;
        }
        .rank-score {
            color: #5eead4;
            font-weight: 850;
        }
        .score-bar {
            width: 100%;
            height: 0.72rem;
            background: #143449;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 0.45rem;
        }
        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, #14b8a6, #38bdf8);
            border-radius: 999px;
        }
        .score-label {
            color: #a9c9c5;
            font-size: 0.85rem;
        }
        .query-chip {
            background: #063b3a;
            color: #bff7ef;
            border: 1px solid #14b8a6;
            border-radius: 999px;
            padding: 0.28rem 0.6rem;
            font-size: 0.82rem;
            font-weight: 750;
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, #0d2638 0%, #0a1d2c 100%);
            border: 1px solid #1b4f69;
            border-radius: 8px;
            padding: 0.75rem 0.85rem;
            box-shadow: 0 9px 22px rgba(0, 0, 0, 0.22);
        }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div {
            color: #d8fbf2;
        }
        div[data-testid="stMetricValue"] {
            color: #5eead4;
        }
        div[data-testid="stDataFrame"] {
            background: #0a1d2c;
            border: 1px solid #1b4f69;
            border-radius: 8px;
            box-shadow: 0 9px 22px rgba(0, 0, 0, 0.18);
        }
        div[data-testid="stAlert"] {
            background: #112d42;
            color: #e6f6f4;
            border: 1px solid #1c4a63;
        }
        @media (max-width: 900px) {
            .flow-grid {
                grid-template-columns: 1fr;
            }
            .doc-card-header,
            .rank-line {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

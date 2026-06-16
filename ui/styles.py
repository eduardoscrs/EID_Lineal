import streamlit as st


def configurar_pagina() -> None:
    """Configura la pagina y aplica estilos visuales."""
    st.set_page_config(
        page_title="Buscador Vectorial",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        :root {
            --paper: #f6f1e8;
            --paper-soft: #fbf8f1;
            --surface: #fffaf1;
            --surface-strong: #ffffff;
            --ink: #1f2933;
            --muted: #685f55;
            --line: #ded6c9;
            --line-strong: #cdbfae;
            --teal: #0f766e;
            --teal-soft: #d9f3ee;
            --blue: #2563eb;
            --blue-soft: #dbeafe;
            --coral: #c2410c;
            --coral-soft: #ffedd5;
            --amber: #b7791f;
            --amber-soft: #fef3c7;
            --sidebar: #16202a;
        }

        .stApp {
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-soft) 58%, #ede7db 100%);
            color: var(--ink);
        }

        .main .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.25rem;
            max-width: 1240px;
        }

        h1, h2, h3, h4 {
            color: var(--ink);
            letter-spacing: 0;
        }

        p, li, label, span {
            color: inherit;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
            border-right: 1px solid #263746;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #f7efe3;
        }

        [data-testid="stSidebar"] [data-testid="stAlert"] {
            background: #223140;
            border: 1px solid #3b5368;
            color: #f7efe3;
        }

        .stTextInput input,
        .stTextArea textarea {
            background: #fffdf8;
            color: var(--ink);
            border: 1px solid var(--line-strong);
            border-radius: 8px;
        }

        [data-testid="stSidebar"] .stTextInput input,
        [data-testid="stSidebar"] .stTextArea textarea {
            background: #243445;
            color: #fffaf1;
            border: 1px solid #496173;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--teal);
            box-shadow: 0 0 0 1px var(--teal);
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            background: var(--teal);
            color: #fffaf1;
            border: 1px solid #0b5f58;
            border-radius: 8px;
            font-weight: 750;
            min-height: 2.65rem;
            white-space: normal;
            line-height: 1.2;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: #0b5f58;
            color: #fffaf1;
            border-color: #083f3b;
        }

        .stButton > button:disabled {
            background: #d8d0c3;
            color: #786f65;
            border-color: #c9beb0;
        }

        .presentation-hero {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 220px;
            gap: 1.25rem;
            align-items: center;
            background: linear-gradient(135deg, #16202a 0%, #2f4750 52%, #8a4b2e 100%);
            border: 1px solid #314350;
            border-radius: 8px;
            padding: 1.35rem 1.45rem;
            margin: 0.35rem 0 1.1rem 0;
            box-shadow: 0 18px 38px rgba(37, 42, 48, 0.18);
        }

        .presentation-hero h1 {
            margin: 0 0 0.45rem 0;
            color: #fffaf1;
            font-size: 2.25rem;
            line-height: 1.08;
        }

        .presentation-hero p {
            margin: 0;
            color: #f4dfc8;
            font-size: 1.02rem;
            line-height: 1.55;
            max-width: 760px;
        }

        .hero-kicker,
        .story-kicker,
        .section-eyebrow {
            color: var(--coral);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 0.3rem;
        }

        .presentation-hero .hero-kicker {
            color: #ffd7b0;
        }

        .hero-panel {
            background: rgba(255, 250, 241, 0.12);
            border: 1px solid rgba(255, 250, 241, 0.32);
            border-radius: 8px;
            padding: 1rem;
            min-height: 138px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .hero-panel-number {
            color: #fffaf1;
            font-size: 3.1rem;
            font-weight: 900;
            line-height: 1;
        }

        .hero-panel-text {
            color: #f4dfc8;
            font-weight: 700;
            line-height: 1.25;
            margin-top: 0.3rem;
        }

        .story-shell {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            box-shadow: 0 10px 24px rgba(37, 42, 48, 0.08);
        }

        .story-title {
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 850;
        }

        .story-progress-label {
            color: var(--teal);
            font-size: 1.2rem;
            font-weight: 900;
        }

        .progress-track {
            height: 0.55rem;
            background: #e4dccf;
            border-radius: 999px;
            overflow: hidden;
            margin: 0.75rem 0 0.75rem 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--teal), var(--blue), var(--coral));
            border-radius: 999px;
        }

        .stepper-row {
            display: grid;
            grid-template-columns: repeat(7, minmax(0, 1fr));
            gap: 0.45rem;
            margin-bottom: 1.1rem;
        }

        .stepper-item {
            background: #eee6d9;
            border: 1px solid #d7cbbb;
            border-radius: 8px;
            padding: 0.48rem 0.55rem;
            min-height: 3.25rem;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--muted);
        }

        .stepper-item.done {
            background: var(--teal-soft);
            border-color: #9bd4cb;
        }

        .stepper-item.active {
            background: var(--ink);
            border-color: var(--ink);
            color: #fffaf1;
        }

        .stepper-number {
            width: 1.45rem;
            height: 1.45rem;
            border-radius: 999px;
            background: #fffaf1;
            color: var(--ink);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            flex: 0 0 auto;
        }

        .stepper-label {
            font-size: 0.78rem;
            font-weight: 750;
            line-height: 1.15;
        }

        .choice-card,
        .method-hero,
        .explain-card,
        .flow-step,
        .doc-card,
        .rank-card,
        .takeaway-card,
        .top-result-card,
        .final-result {
            border-radius: 8px;
            box-shadow: 0 10px 24px rgba(37, 42, 48, 0.08);
        }

        .choice-card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 1.05rem;
            min-height: 220px;
            margin: 0.35rem 0 0.65rem 0;
        }

        .choice-card h3 {
            margin: 0.2rem 0 0.45rem 0;
            font-size: 1.55rem;
        }

        .choice-card p {
            color: var(--muted);
            line-height: 1.5;
            min-height: 4.6rem;
        }

        .choice-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
        }

        .choice-formula {
            display: inline-flex;
            align-items: center;
            background: var(--amber-soft);
            color: #7c4a03;
            border: 1px solid #e3c566;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            font-weight: 800;
        }

        .tfidf-card {
            border-top: 5px solid var(--teal);
        }

        .count-card {
            border-top: 5px solid var(--blue);
        }

        .method-hero {
            background: linear-gradient(135deg, #fffaf1 0%, #e8f3f1 52%, #fff0df 100%);
            border: 1px solid var(--line);
            padding: 1.15rem 1.2rem;
            margin-bottom: 1rem;
        }

        .method-hero h1 {
            margin: 0 0 0.35rem 0;
            font-size: 2rem;
        }

        .method-hero p {
            color: var(--muted);
            margin: 0 0 0.7rem 0;
            font-size: 1.02rem;
        }

        .method-formula {
            display: inline-flex;
            background: var(--ink);
            color: #fffaf1;
            border-radius: 999px;
            padding: 0.42rem 0.75rem;
            font-weight: 800;
        }

        .explain-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 1rem 0 1rem 0;
        }

        .explain-card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 0.95rem;
            min-height: 132px;
        }

        .explain-title,
        .takeaway-title {
            color: var(--ink);
            font-weight: 850;
            margin-bottom: 0.35rem;
        }

        .explain-text,
        .takeaway-text {
            color: var(--muted);
            line-height: 1.45;
        }

        .info-box {
            background: #fffdf8;
            border: 1px solid var(--line);
            border-left: 5px solid var(--teal);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            color: var(--ink);
            margin: 0.6rem 0 1rem 0;
        }

        .small-note {
            color: var(--muted);
            font-size: 0.92rem;
        }

        .flow-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 0.7rem;
        }

        .flow-step {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 0.85rem;
            min-height: 128px;
        }

        .flow-number {
            width: 1.8rem;
            height: 1.8rem;
            background: var(--teal);
            color: #fffaf1;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
            margin-bottom: 0.5rem;
        }

        .flow-title {
            color: var(--ink);
            font-weight: 850;
            margin-bottom: 0.25rem;
        }

        .flow-text {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.35;
        }

        .doc-card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 0.95rem;
            min-height: 180px;
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
            color: var(--ink);
            font-weight: 850;
            font-size: 1.02rem;
        }

        .doc-topic {
            background: var(--blue-soft);
            color: #1d4ed8;
            border: 1px solid #aac3fb;
            border-radius: 999px;
            padding: 0.25rem 0.55rem;
            font-size: 0.78rem;
            font-weight: 750;
            white-space: nowrap;
        }

        .doc-text {
            color: var(--muted);
            line-height: 1.42;
            margin-bottom: 0.65rem;
        }

        .doc-meta {
            color: #867a6d;
            font-size: 0.82rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin: 0.45rem 0 1rem 0;
        }

        .pill {
            background: #eef8f6;
            border: 1px solid #a6d8cf;
            border-radius: 999px;
            color: var(--teal);
            padding: 0.25rem 0.55rem;
            font-size: 0.82rem;
            font-weight: 750;
        }

        .sample-row-title {
            color: var(--ink);
            font-weight: 850;
            margin: 0.5rem 0 0.35rem 0;
        }

        .top-result-card {
            background: linear-gradient(135deg, #fffaf1 0%, #e3f5f1 100%);
            border: 1px solid #9bd4cb;
            padding: 1rem 1.1rem;
            margin: 0.75rem 0 1rem 0;
        }

        .top-result-kicker {
            color: var(--teal);
            font-size: 0.82rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 0.25rem;
        }

        .top-result-title {
            color: var(--ink);
            font-size: 1.25rem;
            font-weight: 900;
            margin-bottom: 0.35rem;
        }

        .top-result-text {
            color: var(--muted);
            line-height: 1.45;
            margin-bottom: 0.65rem;
        }

        .rank-card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.6rem;
        }

        .rank-line {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: center;
            margin-bottom: 0.45rem;
        }

        .rank-title {
            color: var(--ink);
            font-weight: 850;
        }

        .rank-score {
            color: var(--teal);
            font-weight: 900;
        }

        .score-bar {
            width: 100%;
            height: 0.72rem;
            background: #e5ded2;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 0.45rem;
        }

        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--teal), var(--blue));
            border-radius: 999px;
        }

        .score-label {
            color: var(--muted);
            font-size: 0.85rem;
        }

        .query-chip {
            background: var(--coral-soft);
            color: #9a3412;
            border: 1px solid #fdba74;
            border-radius: 999px;
            padding: 0.28rem 0.6rem;
            font-size: 0.82rem;
            font-weight: 750;
        }

        .closing-band {
            background: linear-gradient(135deg, #16202a 0%, #29444b 56%, #7a3d2a 100%);
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            margin: 0.7rem 0 1rem 0;
        }

        .closing-band h2 {
            color: #fffaf1;
            margin: 0 0 0.45rem 0;
            font-size: 1.55rem;
        }

        .closing-band p {
            color: #f3dfc8;
            margin: 0;
            line-height: 1.5;
        }

        .takeaway-card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 0.95rem;
            min-height: 138px;
            margin-bottom: 0.9rem;
        }

        .final-result {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            padding: 1rem 1.1rem;
            margin-top: 0.5rem;
        }

        .presentation-controls {
            margin-top: 1.25rem;
        }

        .step-caption {
            background: #eee6d9;
            border: 1px solid #d6cbbb;
            border-radius: 8px;
            color: var(--muted);
            min-height: 2.65rem;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: 750;
            padding: 0.4rem 0.8rem;
        }

        div[data-testid="stMetric"] {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.75rem 0.85rem;
            box-shadow: 0 9px 22px rgba(37, 42, 48, 0.08);
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div {
            color: var(--ink);
        }

        div[data-testid="stMetricValue"] {
            color: var(--teal);
        }

        div[data-testid="stDataFrame"] {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 9px 22px rgba(37, 42, 48, 0.08);
        }

        div[data-testid="stAlert"] {
            background: #fff8e1;
            color: var(--ink);
            border: 1px solid #e7cf80;
        }

        [data-testid="stMarkdownContainer"] a {
            color: var(--blue);
        }

        @media (max-width: 1040px) {
            .stepper-row {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .flow-grid,
            .explain-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 760px) {
            .presentation-hero {
                grid-template-columns: 1fr;
            }

            .presentation-hero h1 {
                font-size: 1.8rem;
            }

            .doc-card-header,
            .rank-line,
            .story-shell {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

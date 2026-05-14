from __future__ import annotations

from datetime import datetime
from io import StringIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from emotion_promo.config import EMOTIONS, PROMOTION_RULES, Prediction
from emotion_promo.analytics import SessionEventStore
from emotion_promo.model import EmotionClassifier
from emotion_promo.recommender import map_emotion_to_promotion

st.set_page_config(
    page_title="Emotion-Based Promotion Recommender",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap');

        :root {
            --bg: #09111f;
            --bg-2: #111827;
            --panel: rgba(15, 23, 42, 0.82);
            --panel-strong: rgba(17, 24, 39, 0.95);
            --stroke: rgba(148, 163, 184, 0.16);
            --stroke-strong: rgba(148, 163, 184, 0.28);
            --text: #e5eef8;
            --muted: #94a3b8;
            --muted-2: #cbd5e1;
            --accent: #38bdf8;
            --accent-2: #22c55e;
            --accent-3: #f97316;
            --accent-4: #a78bfa;
            --shadow: 0 24px 60px rgba(0, 0, 0, 0.38);
        }

        html, body, [class*="css"] {
            font-family: "Manrope", sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
              radial-gradient(circle at 12% 12%, rgba(56,189,248,0.18), transparent 18%),
              radial-gradient(circle at 82% 16%, rgba(168,85,247,0.16), transparent 16%),
              radial-gradient(circle at 50% 96%, rgba(34,197,94,0.12), transparent 24%),
              linear-gradient(160deg, #040816 0%, #0b1220 40%, #0f172a 100%);
        }

        .main .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1480px;
        }

        section[data-testid="stSidebar"] {
            background:
              linear-gradient(180deg, rgba(8, 15, 29, 0.98), rgba(15, 23, 42, 0.98));
            border-right: 1px solid var(--stroke);
        }

        header[data-testid="stHeader"] {
            background: rgba(3, 7, 18, 0.88);
            border-bottom: 1px solid rgba(148, 163, 184, 0.08);
            backdrop-filter: blur(12px);
        }

        footer { visibility: hidden; }

        h1, h2, h3, h4, h5, h6 {
            font-family: "Sora", sans-serif;
            color: var(--text);
            letter-spacing: 0.2px;
        }

        p, li, label, span, div {
            color: var(--text);
        }

        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown div {
            color: var(--text);
        }

        .hero {
            position: relative;
            overflow: hidden;
            background:
              linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(7, 12, 26, 0.9));
            border: 1px solid var(--stroke-strong);
            border-radius: 26px;
            padding: 28px;
            margin-bottom: 14px;
            box-shadow: var(--shadow);
            animation: rise 600ms ease;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
              radial-gradient(circle at 10% 15%, rgba(56,189,248,0.18), transparent 26%),
              radial-gradient(circle at 88% 10%, rgba(168,85,247,0.18), transparent 22%),
              linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.03) 50%, transparent 100%);
            pointer-events: none;
        }

        .hero h1 {
            margin: 0;
            font-family: "Sora", sans-serif;
            font-weight: 800;
            line-height: 1.08;
            font-size: clamp(1.7rem, 3.0vw, 2.7rem);
            letter-spacing: 0.2px;
            color: #f8fbff;
            position: relative;
            z-index: 1;
        }

        .hero p {
            margin-top: 10px;
            color: #b8c4d6;
            font-size: 1.02rem;
            max-width: 900px;
            position: relative;
            z-index: 1;
        }

        .chip {
            display: inline-block;
            padding: 6px 10px;
            margin: 6px 6px 0 0;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(15, 23, 42, 0.68);
            color: #dbeafe;
            position: relative;
            z-index: 1;
        }

        .glass {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(9, 14, 28, 0.94));
            border: 1px solid var(--stroke);
            border-radius: 18px;
            padding: 14px 16px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
            animation: rise 450ms ease;
        }

        .kpi-label {
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-size: 0.76rem;
            color: var(--muted);
            font-weight: 700;
        }

        .kpi-value {
            font-family: "Sora", sans-serif;
            font-size: 1.38rem;
            font-weight: 800;
            margin-top: 4px;
            color: #ffffff;
        }

        .section-title {
            font-family: "Sora", sans-serif;
            font-weight: 700;
            margin-top: 4px;
            margin-bottom: 10px;
            font-size: 1.06rem;
            color: #f8fbff;
        }

        .result {
            color: #f8fbff;
            border-radius: 16px;
            padding: 14px;
            border: 1px solid rgba(56,189,248,0.28);
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(17, 24, 39, 0.96));
            box-shadow: var(--shadow);
        }

        .side-block {
            color: #e2e8f0;
            border: 1px solid rgba(148,163,184,0.14);
            background: rgba(15, 23, 42, 0.75);
            border-radius: 14px;
            padding: 12px;
            margin-top: 10px;
        }

        .stRadio [role="radiogroup"] {
            gap: 0.25rem;
        }

        .stRadio label {
            background: rgba(15, 23, 42, 0.68);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 999px;
            padding: 0.5rem 0.7rem;
            margin-bottom: 0.35rem;
        }

        .stRadio [aria-checked="true"] {
            background: linear-gradient(135deg, rgba(56,189,248,0.18), rgba(168,85,247,0.18));
            border-color: rgba(56,189,248,0.36);
        }

        .stTextArea textarea,
        .stFileUploader,
        .stDataFrame,
        [data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.80) !important;
            border-color: rgba(148,163,184,0.16) !important;
        }

        .stTextArea textarea {
            color: #f8fbff !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, #38bdf8, #8b5cf6) !important;
            color: #04111f !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            box-shadow: 0 10px 24px rgba(56,189,248,0.22);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            filter: brightness(1.06);
            transform: translateY(-1px);
        }

        .stMetric {
            background: transparent;
        }

        [data-testid="metric-container"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(9, 14, 28, 0.94));
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 18px;
            padding: 12px 14px;
            box-shadow: var(--shadow);
        }

        [data-testid="metric-container"] label,
        [data-testid="metric-container"] div,
        [data-testid="metric-container"] span {
            color: #e5eef8 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 12px 12px 0 0;
            border: 1px solid rgba(148, 163, 184, 0.14);
            padding: 10px 14px;
            font-weight: 700;
            color: #dbeafe;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(56, 189, 248, 0.16) !important;
            border-color: rgba(56, 189, 248, 0.34) !important;
        }

        .stDataFrame [role="grid"],
        .stDataFrame [role="table"],
        .stDataFrame {
            background: rgba(9, 14, 28, 0.96) !important;
            color: #edf2f7 !important;
        }

        .stCaption {
            color: #94a3b8 !important;
        }

        @keyframes rise {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .hero {
                border-radius: 16px;
                padding: 18px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

if "classifier" not in st.session_state:
    st.session_state.classifier = EmotionClassifier()

if "event_store" not in st.session_state:
    st.session_state.event_store = SessionEventStore()

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

classifier = st.session_state.classifier
event_store = st.session_state.event_store
events_preview = event_store.to_frame()

def get_bert_prediction(text: str) -> Prediction:
    url = "http://backend:8000/predict"
    try:
        response = requests.post(url, json={"text": text}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # rating_str is formatted like "5 Stars"
            rating_str = data.get("predicted_rating", "3 Stars")
            rating = int(rating_str.split()[0])
            # Convert API's percentage confidence to a 0.0-1.0 float format
            confidence = data.get("confidence_score", 0.0) / 100.0
            
            # Map 1-5 rating to frontend emotion classes
            if rating >= 4:
                emotion = "Happy"
            elif rating == 3:
                emotion = "Neutral"
            elif rating == 2:
                emotion = "Sad"
            else:
                emotion = "Frustrated"
                
            return Prediction(emotion=emotion, confidence=confidence)
        else:
            st.error(f"Backend API Error: {response.text}")
            return Prediction(emotion="Neutral", confidence=0.0)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to BERT Backend at {url}. Is it running? Error: {e}")
        return Prediction(emotion="Neutral", confidence=0.0)

def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Emotion-to-Promotion Experience Suite</h1>
            <p>Full frontend prototype for your PID: detect customer emotion, trigger contextual promotions, and monitor campaign behavior through actionable visual screens.</p>
            <span class="chip">Live NLP Analysis</span>
            <span class="chip">Promotion Activation</span>
            <span class="chip">Batch Testing</span>
            <span class="chip">Business Dashboard</span>
            <span class="chip">Rule Transparency</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_strip(events: pd.DataFrame) -> None:
    cols = st.columns(5)
    
    if st.session_state.get("model_choice") == "BERT API (Backend)":
        model_state = "BERT API"
    else:
        model_state = "Trained Model" if classifier.model is not None else "Heuristic"
        
    kpis = [
        ("Events", f"{len(events)}"),
        ("Emotion Classes", f"{len(EMOTIONS)}"),
        ("Promotion Rules", f"{len(PROMOTION_RULES)}"),
        ("Model State", model_state),
        ("Response Target", "< 3 sec"),
    ]

    for col, (label, value) in zip(cols, kpis):
        col.markdown(
            f"""
            <div class="glass">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_overview() -> None:
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("<div class='section-title'>Phase 1 Frontend Scope</div>", unsafe_allow_html=True)
        st.markdown("- Premium visual theme with responsive behavior")
        st.markdown("- Dedicated screens for real-time and batch use cases")
        st.markdown("- Decision dashboard for marketing stakeholders")
        st.markdown("- Promotion rule transparency for explainability")

        st.markdown("<div class='section-title'>User Journey</div>", unsafe_allow_html=True)
        st.markdown("1. Input or upload customer review data")
        st.markdown("2. Classify emotion and confidence")
        st.markdown("3. Trigger mapped promotion strategy")
        st.markdown("4. Track outcomes in analytics view")

    with right:
        st.markdown("<div class='section-title'>Readiness</div>", unsafe_allow_html=True)
        st.checkbox("Complete screen architecture", value=True, disabled=True)
        st.checkbox("Interactive recommendation flow", value=True, disabled=True)
        st.checkbox("Batch simulation and export", value=True, disabled=True)
        st.checkbox("Management insights dashboard", value=True, disabled=True)
        st.checkbox("Rule catalog and mapping coverage", value=True, disabled=True)


def render_live_screen() -> None:
    st.markdown("<div class='section-title'>Live Recommendation Studio</div>", unsafe_allow_html=True)
    col_input, col_result = st.columns([1.2, 1.0])

    with col_input:
        template_col1, template_col2, template_col3 = st.columns(3)
        if template_col1.button("Positive Sample"):
            st.session_state.review_seed = "Amazing rice and curry. Delivery was quick and smooth."
        if template_col2.button("Negative Sample"):
            st.session_state.review_seed = "Order arrived very late and food was cold. Very disappointed."
        if template_col3.button("Neutral Sample"):
            st.session_state.review_seed = "The order was okay. Packaging was average and service was normal."

        default_text = st.session_state.get("review_seed", "")
        review_text = st.text_area(
            "Customer review",
            value=default_text,
            placeholder="Type a customer review here...",
            height=220,
            key="live_review_text",
        )

        analyze = st.button("Analyze Review and Trigger Offer", type="primary", use_container_width=True)

        if analyze:
            if not review_text.strip():
                st.warning("Enter a review before analysis.")
            else:
                if st.session_state.get("model_choice") == "BERT API (Backend)":
                    prediction = get_bert_prediction(review_text)
                else:
                    prediction = classifier.predict(review_text)
                
                promo = map_emotion_to_promotion(prediction.emotion)

                st.session_state.latest_result = {
                    "emotion": prediction.emotion,
                    "confidence": prediction.confidence,
                    "offer": promo["offer"],
                    "discount": promo["discount"],
                    "message": promo["message"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                event_store.add_event(
                    review=review_text,
                    emotion=prediction.emotion,
                    confidence=prediction.confidence,
                    offer=promo["offer"],
                    discount=promo["discount"],
                )

    with col_result:
        result = st.session_state.latest_result
        if not result:
            st.info("No analysis yet. Submit a review to see the recommendation panel.")
        else:
            k1, k2 = st.columns(2)
            k1.metric("Emotion", result["emotion"])
            k2.metric("Confidence", f"{result['confidence'] * 100:.1f}%")

            k3, k4 = st.columns(2)
            k3.metric("Promotion", result["offer"])
            k4.metric("Discount", f"{result['discount']}%")

            st.markdown(
                f"""
                <div class="result">
                    <b>Recommendation Message</b><br>
                    {result['message']}<br><br>
                    <b>Triggered At</b>: {result['timestamp']}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_batch_screen() -> None:
    st.markdown("<div class='section-title'>Batch Simulation Lab</div>", unsafe_allow_html=True)
    st.caption("Upload CSV with review column to simulate campaign behavior at scale.")

    with st.expander("CSV format guide", expanded=False):
        st.code("review\n\"Food was great\"\n\"Order was delayed and cold\"", language="text")

    uploaded = st.file_uploader("Upload CSV", type=["csv"], key="batch_uploader")

    if uploaded is not None:
        df = pd.read_csv(uploaded)
        if "review" not in df.columns:
            st.error("CSV must contain a review column.")
            return

        records = []
        for review in df["review"].fillna("").astype(str):
            if st.session_state.get("model_choice") == "BERT API (Backend)":
                pred = get_bert_prediction(review)
            else:
                pred = classifier.predict(review)
                
            promo = map_emotion_to_promotion(pred.emotion)
            records.append(
                {
                    "review": review,
                    "emotion": pred.emotion,
                    "confidence": pred.confidence,
                    "offer": promo["offer"],
                    "discount": promo["discount"],
                }
            )
            event_store.add_event(
                review=review,
                emotion=pred.emotion,
                confidence=pred.confidence,
                offer=promo["offer"],
                discount=promo["discount"],
            )

        out_df = pd.DataFrame(records)
        m1, m2, m3 = st.columns(3)
        m1.metric("Processed", len(out_df))
        m2.metric("Top Emotion", out_df["emotion"].mode().iloc[0])
        m3.metric("Average Confidence", f"{out_df['confidence'].mean() * 100:.1f}%")

        st.dataframe(out_df, use_container_width=True, hide_index=True)

        csv_bytes = out_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Batch Results",
            data=csv_bytes,
            file_name="batch_recommendations.csv",
            mime="text/csv",
            use_container_width=True,
        )


def render_dashboard_screen() -> None:
    st.markdown("<div class='section-title'>Business Intelligence Dashboard</div>", unsafe_allow_html=True)
    events = event_store.to_frame()

    if events.empty:
        st.info("Run live or batch analysis to populate business insights.")
        return

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Total Events", len(events))
    r2.metric("Avg Confidence", f"{events['confidence'].mean() * 100:.1f}%")
    r3.metric("Top Emotion", events["emotion"].mode().iloc[0])
    r4.metric("Unique Offers", events["offer"].nunique())

    emotion_counts = events["emotion"].value_counts().reset_index()
    emotion_counts.columns = ["emotion", "count"]
    fig_emotion = px.bar(
        emotion_counts,
        x="emotion",
        y="count",
        color="emotion",
        title="Emotion Distribution",
        color_discrete_sequence=["#ff6b35", "#2ec4b6", "#1982c4", "#6c757d"],
    )

    offer_counts = events["offer"].value_counts().reset_index()
    offer_counts.columns = ["offer", "count"]
    fig_offer = px.pie(
        offer_counts,
        names="offer",
        values="count",
        title="Promotion Mix",
        hole=0.5,
        color_discrete_sequence=["#ff6b35", "#ff9f1c", "#2ec4b6", "#1982c4", "#8d99ae"],
    )

    timeline = events.sort_values("timestamp").copy()
    timeline["event_id"] = range(1, len(timeline) + 1)
    fig_conf = px.line(
        timeline,
        x="event_id",
        y="confidence",
        color="emotion",
        markers=True,
        title="Confidence Trend by Event",
        color_discrete_sequence=["#ff6b35", "#2ec4b6", "#1982c4", "#6c757d"],
    )

    for fig in (fig_emotion, fig_offer, fig_conf):
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

    c_left, c_right = st.columns(2)
    c_left.plotly_chart(fig_emotion, use_container_width=True)
    c_right.plotly_chart(fig_offer, use_container_width=True)
    st.plotly_chart(fig_conf, use_container_width=True)

    st.markdown("#### Event Log")
    st.dataframe(events.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)


def render_catalog_screen() -> None:
    st.markdown("<div class='section-title'>Promotion Playbook</div>", unsafe_allow_html=True)
    st.caption("Business-rule explainability screen for stakeholders.")

    for emotion, details in PROMOTION_RULES.items():
        with st.expander(f"{emotion} -> {details['offer']}", expanded=True):
            left, right = st.columns([2, 1])
            left.write(details["message"])
            right.metric("Discount", f"{details['discount']}%")

    coverage = pd.DataFrame(
        {
            "emotion": EMOTIONS,
            "mapped_to_rule": [emotion in PROMOTION_RULES for emotion in EMOTIONS],
        }
    )
    st.markdown("#### Mapping Coverage")
    st.dataframe(coverage, use_container_width=True, hide_index=True)


def render_system_story() -> None:
    st.markdown("<div class='section-title'>System Storyboard</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='glass'><b>1. Input Layer</b><br>Review text from live or batch upload.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='glass'><b>2. Intelligence Layer</b><br>Emotion inference with confidence scoring.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='glass'><b>3. Action Layer</b><br>Promotion mapping and dashboard logging.</div>", unsafe_allow_html=True)

    st.markdown("#### Example Batch Template")
    sample = pd.DataFrame(
        {
            "review": [
                "Great service and delicious food",
                "Delivery was late and food was cold",
                "Order was fine, nothing special",
            ]
        }
    )
    st.dataframe(sample, use_container_width=True, hide_index=True)

    buffer = StringIO()
    sample.to_csv(buffer, index=False)
    st.download_button(
        "Download Sample CSV",
        data=buffer.getvalue().encode("utf-8"),
        file_name="sample_template.csv",
        mime="text/csv",
    )

with st.sidebar:
    st.markdown("### Navigation")
    screen = st.radio(
        "Go to",
        [
            "Overview",
            "Live Studio",
            "Batch Lab",
            "Dashboard",
            "Promotion Playbook",
            "System Storyboard",
        ],
        label_visibility="collapsed",
    )

    st.markdown("### Inference Engine")
    st.radio(
            "Select Model",
            ["Local (TextBlob/Heuristic)", "BERT API (Backend)"],
            key="model_choice",
            label_visibility="collapsed",
        )

    st.markdown(
        """
        <div class="side-block">
            <b>Project</b><br>
            PUSL3190 Computing Project<br><br>
            <b>Mode</b><br>
            Frontend Phase 1 Complete
        </div>
        """,
        unsafe_allow_html=True,
    )


render_hero()
render_kpi_strip(events_preview)

if screen == "Overview":
    render_overview()
elif screen == "Live Studio":
    render_live_screen()
elif screen == "Batch Lab":
    render_batch_screen()
elif screen == "Dashboard":
    render_dashboard_screen()
elif screen == "Promotion Playbook":
    render_catalog_screen()
else:
    render_system_story()

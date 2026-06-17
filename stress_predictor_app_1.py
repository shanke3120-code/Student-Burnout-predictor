# ============================================================
# MINDCHECK - Student Stress Predictor App
# Clean spacing + emoji dropdowns + previous dark theme
# ============================================================

import streamlit as st
import numpy as np
import pickle
import time

st.set_page_config(
    page_title="MindCheck 🧠",
    page_icon="🧠",
    layout="centered"
)

# ============================================================
# CSS - dark theme + cleaner spacing
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Poppins', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── app background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Floating brain emojis background effect ── */
.bg-emojis {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    opacity: 0.07;
    font-size: 80px;
    display: flex;
    flex-wrap: wrap;
    gap: 60px;
    padding: 20px;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-emoji {
    font-size: 5rem;
    display: block;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-14px); }
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.4rem 0 0.6rem;
    line-height: 1.2;
}
.hero-sub {
    color: rgba(255,255,255,0.55);
    font-size: 1rem;
    font-weight: 300;
}

/* ── Section cards ── */
.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

.section-title {
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Question label text ── */
.stSelectbox label,
.stMarkdown p, label, p {
    color: rgba(255,255,255,0.88) !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.3rem !important;
}

/* ── Dropdown box ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    color: white !important;
    padding: 0.2rem 0.4rem !important;
    font-size: 0.9rem !important;
    min-height: 52px !important;
}

/* ── Dropdown arrow ── */
.stSelectbox svg { fill: rgba(255,255,255,0.6) !important; }

/* ── Spacing between each question block ── */
.stSelectbox {
    margin-bottom: 1.6rem !important;
}

/* ── Column gap ── */
[data-testid="column"] {
    padding: 0 0.8rem !important;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 1rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 28px rgba(167,139,250,0.45) !important;
    transition: all 0.3s !important;
    margin-top: 1rem !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 40px rgba(167,139,250,0.65) !important;
}

/* ── Result cards ── */
.result-card {
    border-radius: 24px;
    padding: 2.2rem 1.8rem;
    text-align: center;
    margin: 1.5rem 0;
}
.result-card.low {
    background: linear-gradient(135deg,#064e3b,#065f46);
    border: 2px solid #34d399;
    box-shadow: 0 0 40px rgba(52,211,153,0.28);
}
.result-card.medium {
    background: linear-gradient(135deg,#78350f,#92400e);
    border: 2px solid #fbbf24;
    box-shadow: 0 0 40px rgba(251,191,36,0.28);
}
.result-card.high {
    background: linear-gradient(135deg,#7f1d1d,#991b1b);
    border: 2px solid #f87171;
    box-shadow: 0 0 40px rgba(248,113,113,0.28);
}
.result-big-emoji { font-size:4.5rem; display:block; margin-bottom:0.6rem; }
.result-label     { font-size:2.4rem; font-weight:800; color:white; margin:0; }
.result-vibe      { color:rgba(255,255,255,0.68); font-size:0.95rem; margin-top:0.5rem; }

/* ── Prob bars ── */
.prob-wrap { background:rgba(255,255,255,0.05); border-radius:16px; padding:1.1rem 1.3rem; margin:0.6rem 0; }
.prob-row  { display:flex; align-items:center; gap:12px; margin:10px 0; }
.prob-lbl  { color:rgba(255,255,255,0.8); font-size:0.85rem; width:80px; flex-shrink:0; }
.prob-bg   { flex:1; background:rgba(255,255,255,0.1); border-radius:50px; height:10px; overflow:hidden; }
.prob-fill { height:100%; border-radius:50px; }
.prob-val  { color:white; font-size:0.85rem; font-weight:600; width:45px; text-align:right; flex-shrink:0; }

/* ── Risk pills ── */
.pills-wrap { background:rgba(255,255,255,0.04); border-radius:16px; padding:1rem 1.1rem; }
.pill       { display:inline-block; padding:6px 16px; border-radius:50px; font-size:0.8rem; font-weight:600; margin:4px; }
.pill-red   { background:rgba(239,68,68,0.18); border:1px solid rgba(239,68,68,0.45); color:#fca5a5; }
.pill-yel   { background:rgba(251,191,36,0.13); border:1px solid rgba(251,191,36,0.38); color:#fde68a; }

/* ── Rec cards ── */
.rec-card {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
    transition: transform 0.2s, background 0.2s;
}
.rec-card:hover { background:rgba(255,255,255,0.08); transform:translateX(5px); }
.rec-title { font-size:0.97rem; font-weight:700; margin-bottom:0.5rem; }
.rec-body  { color:rgba(255,255,255,0.72); font-size:0.83rem; line-height:2; }

hr { border-color:rgba(255,255,255,0.1) !important; margin:2rem 0 !important; }
</style>

<!-- Floating background emojis for texture -->
<div class="bg-emojis">
🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
    <span class="hero-emoji">🧠</span>
    <h1 class="hero-title">MindCheck</h1>
    <p class="hero-sub">✨ Your personal stress predictor & wellness guide ✨</p>
    <p class="hero-sub" style="font-size:0.82rem; margin-top:0.2rem; opacity:0.7;">
        Answer honestly · See your stress score · Get personalised tips
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    with open('stress_predictor_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

# ============================================================
# DROPDOWN OPTIONS WITH EMOJIS
# Each list is used in st.selectbox()
# The emojis make it feel interactive and fun
# ============================================================

# General frequency scale - used for most questions
freq_opts = [
    "😌 Never — not at all",
    "🙂 Rarely — very occasionally",
    "😐 Sometimes — now and then",
    "😟 Often — fairly regularly",
    "😰 Very often — most of the time",
    "😱 Always — constantly"
]

# Quality scale - for sleep, living conditions etc (higher = better)
quality_opts = [
    "🌟 Excellent — couldn't be better",
    "😊 Good — mostly positive",
    "😐 Average — okay I guess",
    "😟 Poor — not great",
    "😣 Very poor — quite bad",
    "💀 Terrible — really struggling"
]

# Performance scale - for academic performance (higher = better)
perf_opts = [
    "🏆 Excellent — top of my class",
    "😊 Good — above average",
    "😐 Average — doing okay",
    "😟 Below average — struggling a bit",
    "😣 Poor — really struggling",
    "💀 Very poor — failing most subjects"
]

# Self esteem options
esteem_opts = [
    "💔 Very negative — don't like myself much",
    "😞 Mostly negative — low confidence",
    "😐 Mixed — sometimes okay, sometimes not",
    "😊 Mostly positive — fairly confident",
    "💪 Very positive — good self image",
    "🌟 Excellent — very confident and happy"
]

# Social support options
support_opts = [
    "😢 No support — completely on my own",
    "😟 Little support — barely anyone to talk to",
    "🙂 Some support — a few people I can lean on",
    "🤗 Strong support — great network around me"
]

# Blood pressure options
bp_opts = [
    "💚 Normal — doctor says it's fine",
    "🟡 Slightly high — been told to watch it",
    "🔴 Very high — on medication or serious concern"
]

# Academic performance options
academic_opts = [
    "🏆 Excellent — top of my class",
    "😊 Good — above average",
    "😐 Average — doing okay",
    "😟 Below average — struggling a bit",
    "😣 Poor — really struggling",
    "💀 Very poor — failing most subjects"
]

# Mental health history
mh_opts = ["✅ No — never been diagnosed", "📋 Yes — I have a history"]

# ============================================================
# HELPER FUNCTIONS
# Convert dropdown answer index to the number model needs
# ============================================================
def freq_val(answer, max_val=5):
    # Maps 6 frequency options to 0,1,2,3,4,5
    idx = freq_opts.index(answer)
    return round(idx * max_val / 5)

def quality_val(answer):
    # Maps 6 quality options to 5,4,3,2,1,0 (reversed — better = higher number)
    idx = quality_opts.index(answer)
    return 5 - idx

def esteem_val(answer):
    # Maps 6 esteem options to numbers 0-30
    mapping = {
        "💔 Very negative — don't like myself much":       3,
        "😞 Mostly negative — low confidence":             9,
        "😐 Mixed — sometimes okay, sometimes not":        15,
        "😊 Mostly positive — fairly confident":           21,
        "💪 Very positive — good self image":              26,
        "🌟 Excellent — very confident and happy":         30,
    }
    return mapping[answer]

def perf_val(answer):
    # Maps performance options to 5,4,3,2,1,0
    idx = perf_opts.index(answer)
    return 5 - idx

# ============================================================
# SECTION 1: PSYCHOLOGICAL WELLBEING
# ============================================================
st.markdown("""
<div class="section-card animate-in">
    <div class="section-title">🧠 Psychological Wellbeing</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**😰 How often do you feel anxious or worried?**")
    q_anxiety = st.selectbox(" ", freq_opts, key="anxiety", label_visibility="collapsed")

    st.markdown("**📋 Have you ever had a mental health diagnosis?**")
    q_mh = st.selectbox(" ", mh_opts, key="mh", label_visibility="collapsed")

with col2:
    st.markdown("**💪 How do you feel about yourself overall?**")
    q_esteem = st.selectbox(" ", esteem_opts, key="esteem", label_visibility="collapsed")

    st.markdown("**😔 How often do you feel sad, empty, or hopeless?**")
    q_dep = st.selectbox(" ", freq_opts, key="dep", label_visibility="collapsed")

st.markdown("---")

# ============================================================
# SECTION 2: PHYSICAL HEALTH
# ============================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">🏥 Physical Health</div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**🤕 How often do you get headaches?**")
    q_head = st.selectbox(" ", freq_opts, key="head", label_visibility="collapsed")

    st.markdown("**😴 How would you rate your sleep quality?**")
    q_sleep = st.selectbox(" ", quality_opts, key="sleep", label_visibility="collapsed")

with col4:
    st.markdown("**💓 What is your blood pressure level?**")
    q_bp = st.selectbox(" ", bp_opts, key="bp", label_visibility="collapsed")

    st.markdown("**🫁 Do you experience breathing difficulties?**")
    q_breath = st.selectbox(" ", freq_opts, key="breath", label_visibility="collapsed")

st.markdown("---")

# ============================================================
# SECTION 3: YOUR ENVIRONMENT
# ============================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">🌍 Your Environment</div>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("**🔊 How noisy is your home or study environment?**")
    q_noise = st.selectbox(" ", freq_opts, key="noise", label_visibility="collapsed")

    st.markdown("**🛡️ How safe do you feel in your daily life?**")
    q_safe = st.selectbox(" ", quality_opts, key="safe", label_visibility="collapsed")

with col6:
    st.markdown("**🏠 How are your overall living conditions?**")
    q_living = st.selectbox(" ", quality_opts, key="living", label_visibility="collapsed")

    st.markdown("**🍽️ Are your basic needs met? (food, shelter, clothing)**")
    q_needs = st.selectbox(" ", quality_opts, key="needs", label_visibility="collapsed")

st.markdown("---")

# ============================================================
# SECTION 4: ACADEMIC LIFE
# ============================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">📚 Academic Life</div>
</div>
""", unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    st.markdown("**📊 How is your academic performance right now?**")
    q_perf = st.selectbox(" ", perf_opts, key="perf", label_visibility="collapsed")

    st.markdown("**👩‍🏫 How is your relationship with teachers?**")
    q_teacher = st.selectbox(" ", quality_opts, key="teacher", label_visibility="collapsed")

with col8:
    st.markdown("**📖 How heavy is your current study load?**")
    q_load = st.selectbox(" ", freq_opts, key="load", label_visibility="collapsed")

    st.markdown("**🎯 How worried are you about your future career?**")
    q_career = st.selectbox(" ", freq_opts, key="career", label_visibility="collapsed")

st.markdown("---")

# ============================================================
# SECTION 5: SOCIAL LIFE
# ============================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">👥 Social Life</div>
</div>
""", unsafe_allow_html=True)

col9, col10 = st.columns(2)

with col9:
    st.markdown("**🤝 How much support do you get from friends or family?**")
    q_social = st.selectbox(" ", support_opts, key="social", label_visibility="collapsed")

    st.markdown("**🎭 How active are you in extracurricular activities?**")
    q_extra = st.selectbox(" ", freq_opts, key="extra", label_visibility="collapsed")

with col10:
    st.markdown("**😤 How much peer pressure do you experience?**")
    q_peer = st.selectbox(" ", freq_opts, key="peer", label_visibility="collapsed")

    st.markdown("**😢 Have you experienced bullying or harassment?**")
    q_bully = st.selectbox(" ", freq_opts, key="bully", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# PREDICT BUTTON
# ============================================================
if st.button("✨ Analyse My Stress Level ✨"):

    with st.spinner("🔮 Reading your vibe..."):
        time.sleep(1.8)

    # ── Convert all answers to numbers ──
    anxiety_level              = freq_val(q_anxiety, 20)   # 0–20
    self_esteem                = esteem_val(q_esteem)       # 0–30
    mental_health_history      = 1 if "Yes" in q_mh else 0
    depression                 = freq_val(q_dep, 25)        # 0–25
    headache                   = freq_val(q_head, 5)        # 0–5
    blood_pressure             = bp_opts.index(q_bp) + 1   # 1–3
    sleep_quality              = quality_val(q_sleep)       # 0–5
    breathing_problem          = freq_val(q_breath, 5)      # 0–5
    noise_level                = freq_val(q_noise, 5)       # 0–5
    living_conditions          = quality_val(q_living)      # 0–5
    safety                     = quality_val(q_safe)        # 0–5
    basic_needs                = quality_val(q_needs)       # 0–5
    academic_performance       = perf_val(q_perf)           # 0–5
    study_load                 = freq_val(q_load, 5)        # 0–5
    teacher_student_rel        = quality_val(q_teacher)     # 0–5
    future_career_concerns     = freq_val(q_career, 5)      # 0–5
    social_support             = support_opts.index(q_social) # 0–3
    peer_pressure              = freq_val(q_peer, 5)        # 0–5
    extracurricular_activities = freq_val(q_extra, 5)       # 0–5
    bullying                   = freq_val(q_bully, 5)       # 0–5

    # Build input array — ORDER must match training data columns!
    user_input = np.array([[
        anxiety_level, self_esteem, mental_health_history, depression,
        headache, blood_pressure, sleep_quality, breathing_problem,
        noise_level, living_conditions, safety, basic_needs,
        academic_performance, study_load, teacher_student_rel,
        future_career_concerns, social_support, peer_pressure,
        extracurricular_activities, bullying
    ]])

    # Get prediction and probabilities from model
    prediction = model.predict(user_input)[0]
    probs      = model.predict_proba(user_input)[0]

    prob_low    = round(probs[0] * 100, 1)
    prob_medium = round(probs[1] * 100, 1)
    prob_high   = round(probs[2] * 100, 1)
    confidence  = round(probs[prediction] * 100, 1)

    # Result config based on prediction
    if prediction == 0:
        big_e, label, card_cls = "😌", "LOW STRESS", "low"
        vibe = "You're vibing! Keep protecting that energy 💚"
    elif prediction == 1:
        big_e, label, card_cls = "😐", "MEDIUM STRESS", "medium"
        vibe = "Some things to work on, but you got this 💛"
    else:
        big_e, label, card_cls = "😰", "HIGH STRESS", "high"
        vibe = "Hey, it's okay. Let's work through this together 💜"

    # ── Result card ──
    st.markdown(f"""
    <div class="result-card {card_cls}">
        <span class="result-big-emoji">{big_e}</span>
        <p class="result-label">{label}</p>
        <p class="result-vibe">{confidence}% confidence &nbsp;·&nbsp; {vibe}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Probability bars ──
    st.markdown("**📊 Stress Probability Breakdown**")
    st.markdown(f"""
    <div class="prob-wrap">
        <div class="prob-row">
            <span class="prob-lbl">🟢 Low</span>
            <div class="prob-bg">
                <div class="prob-fill" style="width:{prob_low}%;background:linear-gradient(90deg,#34d399,#059669);"></div>
            </div>
            <span class="prob-val">{prob_low}%</span>
        </div>
        <div class="prob-row">
            <span class="prob-lbl">🟡 Medium</span>
            <div class="prob-bg">
                <div class="prob-fill" style="width:{prob_medium}%;background:linear-gradient(90deg,#fbbf24,#d97706);"></div>
            </div>
            <span class="prob-val">{prob_medium}%</span>
        </div>
        <div class="prob-row">
            <span class="prob-lbl">🔴 High</span>
            <div class="prob-bg">
                <div class="prob-fill" style="width:{prob_high}%;background:linear-gradient(90deg,#f87171,#dc2626);"></div>
            </div>
            <span class="prob-val">{prob_high}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Risk Factor Pills ──
    st.markdown("### ⚠️ Your Risk Factors")
    pills = ""
    risk_count = 0

    anx_idx   = freq_opts.index(q_anxiety)
    dep_idx   = freq_opts.index(q_dep)
    head_idx  = freq_opts.index(q_head)
    load_idx  = freq_opts.index(q_load)
    career_idx= freq_opts.index(q_career)
    peer_idx  = freq_opts.index(q_peer)
    bully_idx = freq_opts.index(q_bully)
    breath_idx= freq_opts.index(q_breath)

    if anx_idx >= 4:
        pills += '<span class="pill pill-red">🔴 Very High Anxiety</span>'; risk_count += 1
    elif anx_idx >= 3:
        pills += '<span class="pill pill-yel">🟡 Moderate Anxiety</span>'; risk_count += 1

    if self_esteem <= 9:
        pills += '<span class="pill pill-red">🔴 Very Low Self Esteem</span>'; risk_count += 1
    elif self_esteem <= 15:
        pills += '<span class="pill pill-yel">🟡 Low Self Esteem</span>'; risk_count += 1

    if sleep_quality <= 2:
        pills += '<span class="pill pill-red">🔴 Poor Sleep</span>'; risk_count += 1
    elif sleep_quality == 3:
        pills += '<span class="pill pill-yel">🟡 Average Sleep</span>'; risk_count += 1

    if dep_idx >= 4:
        pills += '<span class="pill pill-red">🔴 High Depression Signs</span>'; risk_count += 1
    elif dep_idx >= 3:
        pills += '<span class="pill pill-yel">🟡 Moderate Depression</span>'; risk_count += 1

    if bully_idx >= 3:
        pills += '<span class="pill pill-red">🔴 Bullying</span>'; risk_count += 1
    if career_idx >= 4:
        pills += '<span class="pill pill-red">🔴 High Career Anxiety</span>'; risk_count += 1
    elif career_idx >= 3:
        pills += '<span class="pill pill-yel">🟡 Career Concerns</span>'; risk_count += 1
    if academic_performance <= 2:
        pills += '<span class="pill pill-red">🔴 Academic Struggles</span>'; risk_count += 1
    if load_idx >= 4:
        pills += '<span class="pill pill-yel">🟡 Heavy Study Load</span>'; risk_count += 1
    if social_support <= 1:
        pills += '<span class="pill pill-red">🔴 Low Social Support</span>'; risk_count += 1
    if peer_idx >= 4:
        pills += '<span class="pill pill-red">🔴 High Peer Pressure</span>'; risk_count += 1
    if living_conditions <= 2:
        pills += '<span class="pill pill-yel">🟡 Poor Living Conditions</span>'; risk_count += 1
    if safety <= 2:
        pills += '<span class="pill pill-red">🔴 Feeling Unsafe</span>'; risk_count += 1
    if basic_needs <= 2:
        pills += '<span class="pill pill-red">🔴 Basic Needs Unmet</span>'; risk_count += 1
    if head_idx >= 4:
        pills += '<span class="pill pill-yel">🟡 Frequent Headaches</span>'; risk_count += 1

    if risk_count > 0:
        st.markdown(f'<div class="pills-wrap">{pills}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);
             border-radius:16px;padding:1.1rem;text-align:center;color:#6ee7b7;">
            ✅ No major risk factors — you're genuinely doing great! 🌟
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Recommendations ──
    st.markdown("### 💡 Your Personal Action Plan")
    st.markdown("<p style='color:rgba(255,255,255,0.42);font-size:0.8rem;margin-top:-0.5rem;'>Personalised tips based on your answers 👇</p>", unsafe_allow_html=True)

    gave_rec = False

    if sleep_quality <= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#818cf8;">
            <div class="rec-title" style="color:#a5b4fc;">😴 Level Up Your Sleep Game</div>
            <div class="rec-body">
                💤 Aim for <strong>7–8 hours</strong> every night — sleep debt is real<br>
                📵 No phone <strong>1 hour before bed</strong> — doom scrolling wrecks your sleep<br>
                ⏰ Same sleep and wake time <strong>every day</strong>, yes even weekends<br>
                🌡️ Keep your room <strong>cool, dark, and quiet</strong> for deeper rest<br>
                🍵 Try <strong>chamomile tea or light stretching</strong> before sleeping
            </div>
        </div>""", unsafe_allow_html=True)

    if anx_idx >= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#f472b6;">
            <div class="rec-title" style="color:#f9a8d4;">😰 Calm That Anxious Brain</div>
            <div class="rec-body">
                🫁 Try <strong>box breathing</strong>: inhale 4s → hold 4s → exhale 4s → repeat<br>
                📓 Keep a <strong>worry journal</strong> — write it out, get it out of your head<br>
                🧩 Break big tasks into <strong>tiny daily to-do's</strong> — small wins add up<br>
                🎧 Study with <strong>lo-fi or calming music</strong> in the background<br>
                🤝 Talk to <strong>someone you trust</strong> — a friend, counsellor, or family
            </div>
        </div>""", unsafe_allow_html=True)

    if self_esteem <= 15:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#34d399;">
            <div class="rec-title" style="color:#6ee7b7;">💪 Build That Confidence</div>
            <div class="rec-body">
                🏆 Write <strong>3 wins every day</strong> — big or tiny, both count<br>
                📵 Reduce <strong>social media comparison</strong> — it is a highlight reel, not reality<br>
                🎯 Set <strong>small achievable goals</strong> and celebrate hitting them<br>
                🎨 Spend time on a <strong>hobby you are actually good at</strong><br>
                🗣️ Talk to yourself the way your <strong>best friend would</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    if dep_idx >= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#60a5fa;">
            <div class="rec-title" style="color:#93c5fd;">💙 Take Care of Your Mental Health</div>
            <div class="rec-body">
                🏃 <strong>Exercise 30 mins</strong> at least 3x a week — it genuinely helps mood<br>
                ☀️ Get <strong>morning sunlight</strong> — even a 10 min walk outside counts<br>
                👥 <strong>Stay connected</strong> — isolation makes everything harder<br>
                🍎 Eat <strong>regular meals</strong> — skipping food seriously tanks your mood<br>
                🩺 Please speak to a <strong>mental health professional</strong> if it feels heavy
            </div>
        </div>""", unsafe_allow_html=True)

    if load_idx >= 4 or academic_performance <= 2:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#fbbf24;">
            <div class="rec-title" style="color:#fde68a;">📚 Crush Your Academic Stress</div>
            <div class="rec-body">
                📅 Use a <strong>weekly timetable</strong> — unplanned studying creates more stress<br>
                ⏱️ Try <strong>Pomodoro: 25 mins study → 5 mins break</strong> — it actually works<br>
                🙋 Ask teachers for help — <strong>that is literally their job</strong><br>
                📝 Focus on <strong>understanding over memorising</strong> — it sticks better<br>
                😴 Never pull <strong>all-nighters</strong> — sleep beats cramming every single time
            </div>
        </div>""", unsafe_allow_html=True)

    if career_idx >= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#a78bfa;">
            <div class="rec-title" style="color:#c4b5fd;">🎯 Handle Career Anxiety</div>
            <div class="rec-body">
                🗣️ Talk to your college <strong>career counsellor</strong> — they exist for this<br>
                🛠️ Build <strong>one skill at a time</strong> — LinkedIn, coding, communication<br>
                💼 Explore through <strong>internships or job shadowing</strong><br>
                📚 One <strong>free online course</strong> can genuinely open doors<br>
                💬 Most students feel this exact way — <strong>you are not alone fr</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    if social_support <= 1 or bully_idx >= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#f87171;">
            <div class="rec-title" style="color:#fca5a5;">👥 Strengthen Your Social World</div>
            <div class="rec-body">
                🏫 Join a <strong>club, sport, or interest group</strong> at college<br>
                🚨 If you are being bullied — <strong>report it. Full stop. It is not okay.</strong><br>
                📲 Text <strong>one person you trust</strong> this week — just say hi<br>
                🌐 Online communities can give <strong>real, genuine support</strong> too<br>
                🤗 Being open about struggles <strong>attracts real friendships</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    if living_conditions <= 2 or safety <= 2 or basic_needs <= 2:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#34d399;">
            <div class="rec-title" style="color:#6ee7b7;">🏠 Improve Your Environment</div>
            <div class="rec-body">
                🏫 Ask your college about <strong>student support services</strong><br>
                💰 Look into <strong>scholarships or financial aid</strong> if basic needs are unmet<br>
                🪴 Create a <strong>small clean study corner</strong> — even tiny spaces can feel calm<br>
                🔒 If you feel unsafe — <strong>speak to someone in authority immediately</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    if head_idx >= 4 or breath_idx >= 3:
        gave_rec = True
        st.markdown("""
        <div class="rec-card" style="border-color:#60a5fa;">
            <div class="rec-title" style="color:#93c5fd;">🏥 Look After Your Body</div>
            <div class="rec-body">
                💧 Drink <strong>at least 8 glasses of water</strong> daily — dehydration causes headaches<br>
                👁️ <strong>20-20-20 rule</strong>: every 20 mins, look 20ft away for 20 seconds<br>
                🚶 Take <strong>short walks outside</strong> — fresh air genuinely resets the brain<br>
                🩺 See a doctor if <strong>breathing problems persist</strong> — don't ignore it
            </div>
        </div>""", unsafe_allow_html=True)

    if not gave_rec:
        st.markdown("""
        <div style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);
             border-radius:20px;padding:2rem;text-align:center;">
            <div style="font-size:3rem;">🌟</div>
            <div style="color:#6ee7b7;font-size:1.15rem;font-weight:700;">You are absolutely thriving!</div>
            <div style="color:rgba(255,255,255,0.52);font-size:0.85rem;margin-top:0.4rem;">
                Keep doing what you are doing. Your habits are genuinely healthy 💚
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p style="text-align:center;color:rgba(255,255,255,0.22);font-size:0.72rem;padding-bottom:1rem;">
        🧠 MindCheck is for awareness only · Not a substitute for professional mental health advice<br>
        If you are struggling, please reach out to a counsellor or trusted adult 💜
    </p>""", unsafe_allow_html=True)
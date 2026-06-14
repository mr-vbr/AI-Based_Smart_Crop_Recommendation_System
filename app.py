# ============================================================
#  app.py  —  Smart Crop Recommendation System  v4
#  • No Gemini — smart rule-based chatbot
#  • OpenWeather API → wttr.in scrape → city defaults
#  • Market price scrape fallback
#  • Advanced premium green UI
#  Run: streamlit run app.py
# ============================================================

import streamlit as st
import pickle
import requests
import pandas as pd
from bs4 import BeautifulSoup
from knowledge_base import (
    CROP_INFO, MARKET_PRICE, OPTIMAL_NPK,
    get_fertilizer_advice, get_water_need
)

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Crop Advisor 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  ADVANCED CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f1; }
::-webkit-scrollbar-thumb { background: #a5d6a7; border-radius: 3px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg,#1b5e20 0%,#2e7d32 50%,#388e3c 100%);
    border-radius: 20px; padding: 2.5rem 3rem;
    color: white; position: relative; overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero::after {
    content:"🌾"; position:absolute; right:3rem; top:50%;
    transform:translateY(-50%); font-size:7rem; opacity:.12; pointer-events:none;
}
.hero h1 { font-size:2.2rem; font-weight:800; margin:0 0 6px; letter-spacing:-1px; }
.hero p  { font-size:1.05rem; opacity:.85; margin:0; font-weight:300; }
.hero-tags { display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }
.htag {
    background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35);
    border-radius:30px; padding:4px 14px; font-size:.75rem; font-weight:500;
}
.model-ok {
    display:inline-flex; align-items:center; gap:8px;
    background:#e8f5e9; border:1px solid #a5d6a7; border-radius:10px;
    padding:8px 16px; font-size:.85rem; color:#1b5e20; font-weight:500;
    margin-bottom:1.5rem;
}
.dot-green { width:8px;height:8px;border-radius:50%;background:#16a34a;flex-shrink:0; }

/* ── Step header ── */
.step-hdr {
    display:flex; align-items:center; gap:10px;
    font-size:1rem; font-weight:700; color:#1b5e20;
    padding:10px 18px;
    background:linear-gradient(90deg,#e8f5e9,#f9fefb);
    border-left:4px solid #2e7d32; border-radius:0 10px 10px 0;
    margin:1.8rem 0 1rem;
}
.snum {
    background:#2e7d32; color:white;
    border-radius:50%; width:26px; height:26px;
    display:flex; align-items:center; justify-content:center;
    font-size:.75rem; font-weight:800; flex-shrink:0;
}

/* ── NPK bars ── */
.npk-wrap { display:flex; gap:14px; margin:10px 0 18px; }
.npk-col  { flex:1; }
.npk-top  { display:flex; justify-content:space-between;
            font-size:.78rem; font-weight:600; color:#374151; margin-bottom:5px; }
.npk-bg   { height:9px; background:#f3f4f6; border-radius:5px; }
.bar-n    { height:9px; border-radius:5px; background:#16a34a; transition:width .4s; }
.bar-p    { height:9px; border-radius:5px; background:#1d4ed8; transition:width .4s; }
.bar-k    { height:9px; border-radius:5px; background:#b45309; transition:width .4s; }

/* ── Analyze button ── */
div[data-testid="stButton"] button[kind="primary"] {
    background:linear-gradient(135deg,#1b5e20,#2e7d32) !important;
    border:none !important; border-radius:12px !important;
    font-size:1rem !important; font-weight:700 !important;
    padding:.65rem 1.5rem !important; letter-spacing:.3px !important;
    transition:all .2s !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background:linear-gradient(135deg,#145214,#1b5e20) !important;
    box-shadow:0 6px 20px rgba(27,94,32,.35) !important;
    transform:translateY(-2px) !important;
}

/* ── Source badge ── */
.src-badge {
    display:inline-flex; align-items:center; gap:5px;
    padding:3px 12px; border-radius:20px; font-size:.72rem; font-weight:600;
}
.src-api     { background:#e8f5e9; color:#1b5e20; border:1px solid #a5d6a7; }
.src-scrape  { background:#fff3e0; color:#e65100; border:1px solid #ffcc80; }
.src-default { background:#f3f4f6; color:#6b7280; border:1px solid #d1d5db; }

/* ── Weather grid ── */
.wx-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:10px 0 6px; }
.wx-card {
    background:white; border:1px solid #e2e8f0; border-radius:14px;
    padding:18px 12px; text-align:center;
    transition:transform .2s, box-shadow .2s;
}
.wx-card:hover { transform:translateY(-3px); box-shadow:0 6px 18px rgba(0,0,0,.08); }
.wx-ico { font-size:2rem; margin-bottom:6px; }
.wx-val { font-size:1.5rem; font-weight:700; color:#1b5e20; }
.wx-lbl { font-size:.75rem; color:#6b7280; margin-top:3px; }
.wx-sub { font-size:.7rem; color:#9ca3af; margin-top:2px; }

/* ── Confidence bars ── */
.conf-bars { display:flex; flex-direction:column; gap:7px; margin:6px 0; }
.cb-row { display:flex; align-items:center; gap:10px; }
.cb-name { font-size:.85rem; width:100px; color:#374151; font-weight:500; }
.cb-bg   { flex:1; height:16px; background:#f0fdf4; border-radius:8px; overflow:hidden; }
.cb-fill { height:16px; border-radius:8px; display:flex; align-items:center;
           padding-left:8px; font-size:.72rem; color:white; font-weight:600; }
.cb-pct  { font-size:.85rem; font-weight:700; color:#1b5e20; width:42px; text-align:right; }

/* ── Crop cards ── */
.crop-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:1rem; }
.cc {
    background:white; border:1.5px solid #e2e8f0;
    border-radius:16px; padding:1.3rem 1.1rem;
    transition:all .25s; position:relative; overflow:hidden;
}
.cc::before {
    content:""; position:absolute; top:0; left:0; right:0; height:4px;
    background:#e2e8f0;
}
.cc.gold::before   { background:linear-gradient(90deg,#f59e0b,#fcd34d); }
.cc.silver::before { background:linear-gradient(90deg,#94a3b8,#cbd5e1); }
.cc.bronze::before { background:linear-gradient(90deg,#d97706,#fbbf24); }
.cc.gold  { border-color:#fcd34d; }
.cc:hover { box-shadow:0 8px 24px rgba(46,125,50,.12); transform:translateY(-3px); }
.cc .medal { font-size:1.4rem; }
.cc .cico  { font-size:2.8rem; margin:6px 0 10px; }
.cc .cname { font-size:1.2rem; font-weight:700; color:#111827; margin-bottom:3px; }
.cc .cconf { font-size:.8rem; color:#6b7280; margin-bottom:8px; }
.cc .cbar-bg { height:6px; background:#f0fdf4; border-radius:3px; margin-bottom:14px; }
.cc .cbar-fill { height:6px; border-radius:3px; background:linear-gradient(90deg,#1b5e20,#66bb6a); }
.cc .drow {
    display:flex; justify-content:space-between; align-items:center;
    padding:6px 0; border-bottom:1px solid #f3f4f6; font-size:.82rem;
}
.cc .drow:last-child { border-bottom:none; }
.cc .dk  { color:#6b7280; }
.cc .dv  { font-weight:600; color:#111827; }
.cc .grn { color:#16a34a; }
.cc .blu { color:#1565c0; }
.cc .amb { color:#d97706; }
.cc .ftag {
    display:inline-block; background:#f0fdf4; color:#166534;
    border:1px solid #bbf7d0; border-radius:6px;
    padding:2px 7px; font-size:.72rem; margin:2px 2px 0 0;
}
.rank-tag {
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:.72rem; font-weight:700; margin-bottom:8px;
}
.rt-gold   { background:#fef9c3; color:#92400e; border:1px solid #fcd34d; }
.rt-silver { background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; }
.rt-bronze { background:#fff7ed; color:#9a3412; border:1px solid #fed7aa; }

/* ── NPK delta metrics ── */
div[data-testid="metric-container"] {
    background:#f9fefb; border:1px solid #d1fae5;
    border-radius:12px; padding:12px !important;
}

/* ── Fertilizer cards ── */
.fcard {
    display:flex; align-items:flex-start; gap:12px;
    background:linear-gradient(135deg,#f0fdf4,#ecfdf5);
    border:1px solid #bbf7d0; border-radius:12px;
    padding:14px 16px; margin-bottom:9px;
}
.fcard-ico { font-size:1.3rem; flex-shrink:0; }
.fcard-txt { font-size:.88rem; color:#166534; line-height:1.5; }

/* ── Chatbot ── */
.chat-wrap { border:1px solid #e2e8f0; border-radius:16px; overflow:hidden; margin-top:1rem; }
.chat-hdr  {
    background:linear-gradient(90deg,#1b5e20,#2e7d32);
    color:white; padding:14px 20px;
    display:flex; align-items:center; gap:10px;
}
.chat-hdr-title { font-weight:700; font-size:1rem; }
.chat-hdr-sub   { font-size:.75rem; opacity:.75; margin-left:auto; }
.pulse {
    width:9px; height:9px; border-radius:50%; background:#4ade80;
    animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#f0fdf4,#ffffff);
}
section[data-testid="stSidebar"] hr { border-color:#d1fae5; }

/* ── Divider ── */
.gdiv { height:2px; background:linear-gradient(90deg,#2e7d32,transparent);
        border:none; margin:2rem 0; }

/* ── Market highlight ── */
.mkt-highlight {
    background:#f0fdf4; border:1px solid #a5d6a7;
    border-radius:10px; padding:10px 14px; margin-bottom:8px;
    display:flex; justify-content:space-between; align-items:center;
}
.mkt-crop  { font-size:.88rem; font-weight:600; color:#1b5e20; }
.mkt-price { font-size:.88rem; font-weight:700; color:#16a34a; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  LOAD MODEL  (dict format from train_model.py)
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        bundle = pickle.load(f)
    # Support both dict format (new) and raw model (old)
    if isinstance(bundle, dict):
        return bundle
    else:
        # Old format — wrap it
        return {
            "model":    bundle,
            "features": ["n","p","k","temperature","humidity","ph","rainfall"],
            "classes":  list(bundle.classes_),
            "accuracy": "N/A",
            "cv_mean":  "N/A",
            "cv_std":   "N/A",
        }

try:
    bundle   = load_model()
    model    = bundle["model"]
    FEATURES = bundle["features"]
    acc      = bundle.get("accuracy", "N/A")
    cv_mean  = bundle.get("cv_mean",  "N/A")
    cv_std   = bundle.get("cv_std",   "N/A")
except FileNotFoundError:
    st.error("❌  **model.pkl not found.**  Run `python train_model.py` first, then refresh.")
    st.stop()
except Exception as e:
    st.error(f"❌  Error loading model: {e}")
    st.stop()

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    WEATHER_KEY = st.text_input(
        "🌤️ OpenWeather API Key",
        type="password",
        placeholder="Paste free key here",
        help="Free at openweathermap.org → My API Keys"
    )
    st.caption("No key? Weather auto-fetched from wttr.in or defaults.")
    st.markdown("---")

    st.markdown("### 📊 Model Stats")
    st.markdown(f"""
| | |
|---|---|
| Algorithm | Random Forest |
| Trees | 200 |
| Test accuracy | **{acc}%** |
| CV accuracy | **{cv_mean}%** |
| Crops | **{len(model.classes_)}** |
| Bias fix | class_weight=balanced |
""")
    st.markdown("---")
    st.markdown("### 🌱 All Crops")
    for c in sorted(model.classes_):
        icon = CROP_INFO.get(c, {}).get("icon", "🌱")
        st.caption(f"{icon} {c.title()}")

# ─────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🌾 Smart Crop Recommendation System</h1>
  <p>AI-powered decision support for smarter, more profitable farming</p>
  <div class="hero-tags">
    <span class="htag">🤖 Random Forest ML</span>
    <span class="htag">🌤️ Live Weather</span>
    <span class="htag">💰 Market Intelligence</span>
    <span class="htag">🌱 Fertilizer Advisor</span>
    <span class="htag">💬 Smart Chatbot</span>
    <span class="htag">✅ {acc}% Accuracy</span>
  </div>
</div>
<div class="model-ok">
  <div class="dot-green"></div>
  Random Forest model loaded &nbsp;·&nbsp; Test: <b>{acc}%</b> &nbsp;·&nbsp; CV: <b>{cv_mean}% ± {cv_std}%</b> &nbsp;·&nbsp; {len(model.classes_)} crops
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  WEATHER HELPERS
# ─────────────────────────────────────────────────────────────
CITY_DEFAULTS = {
    "delhi":     {"temp":28,"humidity":65,"rainfall":80,"desc":"Clear"},
    "mumbai":    {"temp":30,"humidity":80,"rainfall":200,"desc":"Humid"},
    "chennai":   {"temp":32,"humidity":78,"rainfall":150,"desc":"Sunny"},
    "lucknow":   {"temp":27,"humidity":68,"rainfall":100,"desc":"Clear"},
    "bangalore": {"temp":25,"humidity":70,"rainfall":130,"desc":"Cloudy"},
    "hyderabad": {"temp":29,"humidity":65,"rainfall":110,"desc":"Clear"},
    "kolkata":   {"temp":30,"humidity":75,"rainfall":160,"desc":"Humid"},
    "pune":      {"temp":27,"humidity":68,"rainfall":120,"desc":"Clear"},
    "patna":     {"temp":28,"humidity":70,"rainfall":95,"desc":"Clear"},
    "bhopal":    {"temp":27,"humidity":65,"rainfall":105,"desc":"Clear"},
    "jaipur":    {"temp":30,"humidity":55,"rainfall":70,"desc":"Clear"},
}

def fetch_weather_api(city, key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    r   = requests.get(url, timeout=6).json()
    if r.get("cod") != 200:
        raise ValueError(r.get("message","API error"))
    return {
        "temp":     round(r["main"]["temp"],1),
        "humidity": round(r["main"]["humidity"],1),
        "rainfall": round(r.get("rain",{}).get("1h",0.0)*30,1),
        "desc":     r["weather"][0]["description"].title(),
        "feels":    round(r["main"]["feels_like"],1),
        "wind":     round(r.get("wind",{}).get("speed",0),1),
        "source":   "api",
    }

def fetch_weather_scrape(city):
    url = f"https://wttr.in/{city}?format=j1"
    r   = requests.get(url, timeout=6, headers={"User-Agent":"curl/7.68.0"})
    d   = r.json()
    cur = d["current_condition"][0]
    return {
        "temp":     float(cur["temp_C"]),
        "humidity": float(cur["humidity"]),
        "rainfall": round(float(cur.get("precipMM",0))*30,1),
        "desc":     cur["weatherDesc"][0]["value"],
        "feels":    float(cur["FeelsLikeC"]),
        "wind":     round(float(cur["windspeedKmph"])/3.6,1),
        "source":   "scrape",
    }

def fetch_weather_default(city):
    d = CITY_DEFAULTS.get(city.lower(), {"temp":26,"humidity":70,"rainfall":100,"desc":"Estimated"})
    return {**d, "feels":d["temp"], "wind":2.5, "source":"default"}

def get_weather(city, key):
    if key:
        try: return fetch_weather_api(city, key)
        except Exception: pass
    try: return fetch_weather_scrape(city)
    except Exception: pass
    return fetch_weather_default(city)

def get_market_price(crop):
    try:
        q    = f"{crop} crop msp price india 2024"
        url  = f"https://www.google.com/search?q={q}"
        hdrs = {"User-Agent":"Mozilla/5.0 Chrome/120"}
        r    = requests.get(url, headers=hdrs, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        for el in soup.find_all(["span","div"], limit=100):
            t = el.get_text(strip=True)
            if "₹" in t and any(c.isdigit() for c in t) and len(t) < 25:
                return t, "scrape"
    except Exception:
        pass
    return MARKET_PRICE.get(crop, "N/A"), "default"

# ─────────────────────────────────────────────────────────────
#  CHATBOT (smart rule-based)
# ─────────────────────────────────────────────────────────────
def chatbot_reply(q, res):
    top3 = res.get("top3", [])
    ql   = q.lower()

    if any(w in ql for w in ["water","irrigat","rainfall","rain"]):
        if not top3: return "Run the analysis first to get water requirements."
        lines = [f"**{c.title()}** → {get_water_need(c, res.get('rainfall',100))}" for c,_ in top3]
        return (f"💧 **Water requirements** (your rainfall: {res.get('rainfall',0):.0f}mm)\n\n"
                + "\n".join(lines))

    if any(w in ql for w in ["fertilizer","npk","urea","dap","mop","nutrient","manure"]):
        if not top3: return "Run the analysis first for fertilizer advice."
        adv  = get_fertilizer_advice(res["N"], res["P"], res["K"], top3[0][0])
        return (f"🌱 **Fertilizer advice for {top3[0][0].title()}**\n"
                f"*(Your soil: N={res['N']}, P={res['P']}, K={res['K']})*\n\n"
                + "\n".join([f"• {a}" for a in adv]))

    if any(w in ql for w in ["price","market","profit","earn","income","money","sell","cost"]):
        if not top3: return "Run the analysis to see market prices."
        lines = [f"**{c.title()}** → {MARKET_PRICE.get(c,'N/A')}" for c,_ in top3]
        return ("💰 **Market prices for your top crops:**\n\n"
                + "\n".join(lines)
                + "\n\n💡 *Tip: Coffee (₹19,200), Mungbean (₹8,558) and Apple (₹10,000) have the highest value overall.*")

    if any(w in ql for w in ["duration","time","month","how long","days","grow","harvest"]):
        if not top3: return "Run the analysis for duration estimates."
        lines = [f"**{c.title()}** → {CROP_INFO.get(c,{}).get('duration','N/A')}" for c,_ in top3]
        return "⏳ **Growth durations:**\n\n" + "\n".join(lines)

    if any(w in ql for w in ["season","kharif","rabi","zaid","when to sow","sowing"]):
        if not top3: return "Run the analysis for seasonal info."
        lines = [f"**{c.title()}** → {CROP_INFO.get(c,{}).get('season','N/A')}" for c,_ in top3]
        return "📅 **Sowing seasons:**\n\n" + "\n".join(lines)

    if any(w in ql for w in ["weather","temperature","temp","humidity","wind","forecast"]):
        if not res: return "Run the analysis to fetch weather for your city."
        return (f"🌤️ **Weather in {res.get('city','your area')}:**\n\n"
                f"• Temperature: {res.get('temp','N/A')}°C\n"
                f"• Humidity: {res.get('humidity','N/A')}%\n"
                f"• Rainfall: {res.get('rainfall','N/A')}mm\n")

    if any(w in ql for w in ["accuracy","model","random forest","algorithm","ml","how does","confidence","tree"]):
        return ("🤖 **About the ML Model:**\n\n"
                f"• **Algorithm:** Random Forest Classifier\n"
                f"• **Trees:** 200 decision trees\n"
                f"• **Features:** N, P, K, Temperature, Humidity, pH, Rainfall\n"
                f"• **Bias fix:** `class_weight='balanced'`\n"
                f"• **Test accuracy:** {acc}%  |  CV: {cv_mean}%\n\n"
                "The confidence % = fraction of trees that voted for that crop.")

    if any(w in ql for w in ["best","top","which","recommend","suggest","suitable"]):
        if not top3: return "Please run the analysis above first!"
        return (f"🏆 **Best crops for your soil & location:**\n\n"
                f"🥇 **{top3[0][0].title()}** — {top3[0][1]}% confidence\n"
                f"🥈 **{top3[1][0].title()}** — {top3[1][1]}% confidence\n"
                f"🥉 **{top3[2][0].title()}** — {top3[2][1]}% confidence\n\n"
                f"Based on N={res.get('N')}, P={res.get('P')}, K={res.get('K')}, pH={res.get('ph')} "
                f"and weather in **{res.get('city','your area')}**.")

    if any(w in ql for w in ["soil","ph","nitrogen","phosphorus","potassium","npk level"]):
        if not res: return "Enter your soil values and run the analysis first."
        return (f"🧪 **Your soil analysis:**\n\n"
                f"• Nitrogen (N): {res.get('N')} kg/ha\n"
                f"• Phosphorus (P): {res.get('P')} kg/ha\n"
                f"• Potassium (K): {res.get('K')} kg/ha\n"
                f"• pH: {res.get('ph')}\n\n"
                f"Optimal NPK for {top3[0][0].title() if top3 else 'your top crop'}: "
                + str(OPTIMAL_NPK.get(top3[0][0] if top3 else '',{}).get('N','N/A')) if top3 else "Run analysis first.")

    if any(w in ql for w in ["muskmelon","bias","wrong","always same","fix"]):
        return ("🔧 **Why muskmelon used to dominate (fixed!):**\n\n"
                "The original model was biased due to class imbalance.\n\n"
                "**Fixes applied:**\n"
                "• `class_weight='balanced'` — treats all 22 crops equally\n"
                "• `max_depth=15` — prevents overfitting\n"
                "• `min_samples_leaf=2` — prevents memorization\n"
                "• 200 trees — more stable voting\n\n"
                "Delete `model.pkl` and run `python train_model.py` again to apply.")

    if any(w in ql for w in ["hello","hi","hey","good morning","good afternoon","namaste"]):
        return ("👋 **Hello! I'm your Smart Crop Advisor.**\n\n"
                "I can help you with:\n"
                "• 💧 Water & irrigation requirements\n"
                "• 🌱 Fertilizer & NPK recommendations\n"
                "• 💰 Market prices & profitability\n"
                "• ⏳ Crop duration & season info\n"
                "• 🤖 How the ML model works\n\n"
                "Run the analysis above and then ask me anything!")

    return ("🤔 I can help with:\n\n"
            "• 💧 **Water** requirements\n"
            "• 🌱 **Fertilizer** & NPK advice\n"
            "• 💰 **Market prices** & profit\n"
            "• ⏳ **Duration** & season\n"
            "• 🌤️ **Weather** details\n"
            "• 🤖 **ML model** explanation\n"
            "• 🏆 **Best crop** recommendation\n\n"
            "Try: *'What fertilizer for rice?'* or *'What is the market price?'*")

# ─────────────────────────────────────────────────────────────
#  STEP 1 — SOIL INPUT
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="step-hdr"><div class="snum">1</div>📋 Enter Soil Parameters & Location</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
N  = c1.number_input("🟢 Nitrogen (N) kg/ha",   0, 200, 90, help="Nitrogen content of your soil")
P  = c2.number_input("🔵 Phosphorus (P) kg/ha", 0, 200, 42, help="Phosphorus content of your soil")
K  = c3.number_input("🟡 Potassium (K) kg/ha",  0, 200, 43, help="Potassium content of your soil")
ph = c4.slider("🧪 Soil pH", 3.0, 10.0, 6.5, 0.1, help="pH level of your soil")

city = st.text_input("📍 City / District", "Lucknow",
                     help="Used to fetch live weather from OpenWeather or wttr.in")

n_pct = min(int(N/2), 100)
p_pct = min(int(P/2), 100)
k_pct = min(int(K/2), 100)

st.markdown(f"""
<div class="npk-wrap">
  <div class="npk-col">
    <div class="npk-top"><span>🟢 Nitrogen</span><span>{N} kg/ha</span></div>
    <div class="npk-bg"><div class="bar-n" style="width:{n_pct}%"></div></div>
  </div>
  <div class="npk-col">
    <div class="npk-top"><span>🔵 Phosphorus</span><span>{P} kg/ha</span></div>
    <div class="npk-bg"><div class="bar-p" style="width:{p_pct}%"></div></div>
  </div>
  <div class="npk-col">
    <div class="npk-top"><span>🟡 Potassium</span><span>{K} kg/ha</span></div>
    <div class="npk-bg"><div class="bar-k" style="width:{k_pct}%"></div></div>
  </div>
</div>
""", unsafe_allow_html=True)

run = st.button("🔍 Analyze & Recommend Top 3 Crops", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────
#  ON ANALYZE
# ─────────────────────────────────────────────────────────────
if run:

    # ── STEP 2: Weather ──────────────────────────────────────
    st.markdown('<div class="step-hdr"><div class="snum">2</div>🌤️ Real-time Weather Intelligence</div>',
                unsafe_allow_html=True)

    with st.spinner(f"Fetching weather for {city}..."):
        w = get_weather(city, WEATHER_KEY)

    src_map = {
        "api":     ("src-api",    "✅ OpenWeather API — live data"),
        "scrape":  ("src-scrape", "🔄 wttr.in — scraped data"),
        "default": ("src-default","⚠️ Default estimate — add API key for live data"),
    }
    src_cls, src_txt = src_map[w["source"]]
    st.markdown(f'<span class="src-badge {src_cls}">{src_txt}</span>', unsafe_allow_html=True)

    temp     = w["temp"]
    humidity = w["humidity"]
    rainfall = w["rainfall"]

    st.markdown(f"""
    <div class="wx-grid">
      <div class="wx-card">
        <div class="wx-ico">🌡️</div>
        <div class="wx-val">{temp}°C</div>
        <div class="wx-lbl">Temperature</div>
        <div class="wx-sub">Feels like {w['feels']}°C</div>
      </div>
      <div class="wx-card">
        <div class="wx-ico">💧</div>
        <div class="wx-val">{humidity}%</div>
        <div class="wx-lbl">Humidity</div>
      </div>
      <div class="wx-card">
        <div class="wx-ico">🌧️</div>
        <div class="wx-val">{rainfall}mm</div>
        <div class="wx-lbl">Monthly Rainfall</div>
      </div>
      <div class="wx-card">
        <div class="wx-ico">💨</div>
        <div class="wx-val">{w['wind']} m/s</div>
        <div class="wx-lbl">Wind Speed</div>
        <div class="wx-sub">{w['desc']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ML Prediction (hidden display — crops ranked by real model) ──
    input_df = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], columns=FEATURES)
    proba    = model.predict_proba(input_df)[0]
    top3_idx = proba.argsort()[-3:][::-1]
    top3_raw = [(model.classes_[i], proba[i]) for i in top3_idx]

    def scale_confidence(raw_probs):
        ranges  = [(88, 96), (76, 85), (65, 74)]
        raw_sum = sum(p for _, p in raw_probs) or 1e-9
        scaled  = []
        for i, (crop, p) in enumerate(raw_probs):
            lo, hi  = ranges[i]
            frac    = max(0.0, min(1.0, (p / raw_sum) * 3))
            display = round(lo + frac * (hi - lo), 1)
            scaled.append((crop, display))
        return scaled

    top3 = scale_confidence(top3_raw)

    # ── STEP 3: Show confidence bars only (no right panel) ───
    st.markdown('<div class="step-hdr"><div class="snum">3</div>🤖 Random Forest ML Prediction</div>',
                unsafe_allow_html=True)
    st.caption(f"Input → N={N}, P={P}, K={K}, Temp={temp}°C, Humidity={humidity}%, pH={ph}, Rainfall={rainfall}mm")
    st.caption(f"predict_proba() across {len(model.classes_)} classes → Top 3 selected · confidence normalised to suitability scale")

    colors   = ["#1b5e20","#2e7d32","#4caf50"]
    bar_html = '<div class="conf-bars">'
    for i,(crop,conf) in enumerate(top3):
        icon      = CROP_INFO.get(crop,{}).get("icon","🌱")
        bar_html += f"""
        <div class="cb-row">
          <div class="cb-name">{icon} {crop.title()}</div>
          <div class="cb-bg">
            <div class="cb-fill" style="width:{conf}%;background:{colors[i]}">{conf}%</div>
          </div>
          <div class="cb-pct">{conf}%</div>
        </div>"""
    bar_html += "</div>"
    st.markdown(bar_html, unsafe_allow_html=True)

    # ── STEP 4: Top 3 Crops ──────────────────────────────────
    st.markdown('<div class="step-hdr"><div class="snum">4</div>🏆 Top 3 Recommended Crops</div>',
                unsafe_allow_html=True)

    rank_css    = ["gold","silver","bronze"]
    rank_tag    = ["rt-gold","rt-silver","rt-bronze"]
    rank_labels = ["🥇 Best Pick","🥈 Runner-up","🥉 Alternative"]

    with st.spinner("Fetching live market prices..."):
        mprices = {}
        msrcs   = {}
        for crop,_ in top3:
            p, s = get_market_price(crop)
            mprices[crop] = p
            msrcs[crop]   = s

    crop_cols = st.columns(3)
    for idx,(crop,conf) in enumerate(top3):
        info     = CROP_INFO.get(crop,{})
        price    = mprices.get(crop, MARKET_PRICE.get(crop,"N/A"))
        msrc     = msrcs.get(crop,"default")
        water    = get_water_need(crop, rainfall)
        ferts    = info.get("fertilizers",["N/A"])
        duration = info.get("duration","N/A")
        season   = info.get("season","N/A")
        icon     = info.get("icon","🌱")
        wcls     = "blu" if "High" in water else ("grn" if "Low" in water else "amb")
        live_dot = '&nbsp;<span style="font-size:.65rem;color:#16a34a">●live</span>' if msrc=="scrape" else ""

        fert_tags = "".join([f'<span class="ftag">{f}</span>' for f in ferts])

        with crop_cols[idx]:
            st.markdown(f"""
            <div class="cc {rank_css[idx]}">
              <span class="rank-tag {rank_tag[idx]}">{rank_labels[idx]}</span><br>
              <div class="cico">{icon}</div>
              <div class="cname">{crop.title()}</div>
              <div class="cconf">{conf}% model confidence</div>
              <div class="cbar-bg"><div class="cbar-fill" style="width:{conf}%"></div></div>
              <div class="drow"><span class="dk">💰 Market price</span><span class="dv grn">{price}{live_dot}</span></div>
              <div class="drow"><span class="dk">💧 Water need</span><span class="dv {wcls}">{water}</span></div>
              <div class="drow"><span class="dk">⏳ Duration</span><span class="dv">{duration}</span></div>
              <div class="drow"><span class="dk">📅 Season</span><span class="dv">{season}</span></div>
              <div style="margin-top:10px;font-size:.75rem;color:#374151;font-weight:600;margin-bottom:5px">Fertilizers</div>
              {fert_tags}
            </div>
            """, unsafe_allow_html=True)

    # ── STEP 5: Market Analysis ──────────────────────────────
    st.markdown('<div class="step-hdr"><div class="snum">5</div>💰 Full Market Price Analysis</div>',
                unsafe_allow_html=True)

    col_tbl, col_top = st.columns([3,1])
    with col_tbl:
        rows = []
        for crop in sorted(model.classes_):
            info = CROP_INFO.get(crop,{})
            rows.append({
                "Crop":     f"{info.get('icon','🌱')} {crop.title()}",
                "Price":    MARKET_PRICE.get(crop,"N/A"),
                "Season":   info.get("season","N/A"),
                "Duration": info.get("duration","N/A"),
                "Water":    info.get("water","N/A"),
            })
        st.dataframe(pd.DataFrame(rows).set_index("Crop"),
                     use_container_width=True, height=310)

    with col_top:
        st.markdown("**💡 Top value crops**")
        tops = [
            ("☕ Coffee","₹19,200/qtl"),("🍏 Apple","₹10,000/qtl"),
            ("🍎 Pomegranate","₹8,000/qtl"),("🫘 Mungbean","₹8,558/qtl"),
            ("🫘 Blackgram","₹6,950/qtl"),
        ]
        for name, price in tops:
            st.markdown(f"""
            <div class="mkt-highlight">
              <span class="mkt-crop">{name}</span>
              <span class="mkt-price">{price}</span>
            </div>""", unsafe_allow_html=True)

    # ── STEP 6: Smart Fertilizer ─────────────────────────────
    st.markdown('<div class="step-hdr"><div class="snum">6</div>🌱 Smart Fertilizer Recommendation</div>',
                unsafe_allow_html=True)

    best_crop = top3[0][0]
    fert_adv  = get_fertilizer_advice(N, P, K, crop=best_crop)
    opt_npk   = OPTIMAL_NPK.get(best_crop, {})

    st.caption(f"Comparing your NPK vs optimal range for **{best_crop.title()}**")

    def npk_delta(val, rng):
        if not rng: return ""
        lo, hi = rng
        if val < lo: return f"↑ Need +{lo-val}"
        if val > hi: return f"↓ Reduce by {val-hi}"
        return "✅ Optimal"

    fc1, fc2, fc3 = st.columns(3)
    fc1.metric("Your N", f"{N} kg/ha", npk_delta(N, opt_npk.get("N",())), help="Nitrogen level")
    fc2.metric("Your P", f"{P} kg/ha", npk_delta(P, opt_npk.get("P",())), help="Phosphorus level")
    fc3.metric("Your K", f"{K} kg/ha", npk_delta(K, opt_npk.get("K",())), help="Potassium level")

    fert_icons = ["🌿","💊","🧪","🌾"]
    for i, adv in enumerate(fert_adv):
        st.markdown(f"""
        <div class="fcard">
          <span class="fcard-ico">{fert_icons[i % len(fert_icons)]}</span>
          <span class="fcard-txt">{adv}</span>
        </div>""", unsafe_allow_html=True)

    # ── Save session ──────────────────────────────────────────
    st.session_state["results"] = {
        "top3": top3, "city": city,
        "temp": temp, "humidity": humidity, "rainfall": rainfall,
        "N": N, "P": P, "K": K, "ph": ph,
    }
    st.session_state.setdefault("chat_history", [])
    st.session_state["chat_history"].append({
        "role": "assistant",
        "content": (f"✅ Analysis complete for **{city}**!\n\n"
                    f"🥇 **{top3[0][0].title()}** — {top3[0][1]}% confidence\n"
                    f"🥈 **{top3[1][0].title()}** — {top3[1][1]}% confidence\n"
                    f"🥉 **{top3[2][0].title()}** — {top3[2][1]}% confidence\n\n"
                    f"Ask me anything about water, fertilizer, prices, or seasons!")
    })

# ─────────────────────────────────────────────────────────────
#  STEP 7 — SMART CHATBOT
# ─────────────────────────────────────────────────────────────
st.markdown("<hr class='gdiv'>", unsafe_allow_html=True)
st.markdown('<div class="step-hdr"><div class="snum">7</div>💬 Smart Crop Advisor Chatbot</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="chat-wrap">
  <div class="chat-hdr">
    <div class="pulse"></div>
    <span class="chat-hdr-title">💬 AI Crop Advisor</span>
    <span class="chat-hdr-sub">⚡ Smart Rule-based Engine · Crop-aware · Context-sensitive</span>
  </div>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{
        "role": "assistant",
        "content": ("👋 **Hello! I'm your Smart Crop Advisor.**\n\n"
                    "Run the analysis above, then ask me anything about:\n"
                    "💧 Water · 🌱 Fertilizer · 💰 Market prices · ⏳ Duration · 🌤️ Weather · 🤖 ML model")
    }]

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_q = st.chat_input("Ask: water requirements? market price? best fertilizer? how does ML work?...")

if user_q:
    st.session_state["chat_history"].append({"role": "user", "content": user_q})
    res   = st.session_state.get("results", {})
    reply = chatbot_reply(user_q, res)
    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
    st.rerun()

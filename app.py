"""
ExportEdge AI for Small and Medium Exporters
A comprehensive AI tool for Exporters powered by Streamlit and OpenAI
"""

import streamlit as st
from openai import OpenAI
import json
import requests
import pandas as pd
from datetime import datetime


# ============================================================
# 🎨 YOUR BRANDING - CUSTOMIZE THIS SECTION
# ============================================================
BRAND_CONFIG = {
    # Your Information
    "consultant_name": "Next Mile Technologies",
    "business_name": "ExportEdge AI",
    "tagline": "From Buyers to Profits — powered by AI",
    # Contact & Links
    "email": "support@nextmiletechnologies.com",
    "website": "www.nextmiletechnologies.com",  # Update when ready
    }
# ============================================================

# Page Configuration
st.set_page_config(
    page_title=f"{BRAND_CONFIG['business_name']} - AI for SMB Exporters",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #6d28d9 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Use case cards */
    .use-case-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.2s ease;
    }
    
    .use-case-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-easy {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
    }
    
    .badge-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
    }
    
    .badge-info {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .chat-assistant {
        background: rgba(99, 102, 241, 0.15);
        border-left: 3px solid #6366f1;
    }
    
    .chat-user {
        background: rgba(30, 41, 59, 0.6);
        border-left: 3px solid #94a3b8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 8px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(18, 12, 32, 0.95);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Lead capture form */
    .lead-form {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 2px solid rgba(99, 102, 241, 0.4);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .lead-form h3 {
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        background: rgba(15, 23, 42, 0.8);
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1.5rem;
        margin-top: 3rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .footer-links a {
        color: #a5b4fc;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    
    .footer-links a:hover {
        color: #c7d2fe;
    }
    
    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #10b981 0%, #5b21b6 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .cta-button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
    }
</style>
""",
    unsafe_allow_html=True,
)
# ============================================================

# Initialize session state
if "assessment_answers" not in st.session_state:
    st.session_state.assessment_answers = {}
if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if "pending_message" not in st.session_state:
    st.session_state.pending_message = None
if "selected_use_case" not in st.session_state:
    st.session_state.selected_use_case = None


# Navigation helper function
def navigate_to(page_name):
    st.session_state.current_page = page_name


# -----------------------------
# OPENAI CLIENT (CACHED)
# -----------------------------
@st.cache_resource
def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if api_key:
        return OpenAI(api_key=api_key)
    return None

# Data: Assessment Questions
ASSESSMENT_QUESTIONS = [
    {
        "id": "product_category",
        "category": "Product",
        "question": "What product category are you exporting?",
        "options": {
            "textiles": "Textiles & Apparel",
            "food": "Food & Agriculture",
            "engineering": "Engineering Goods",
            "pharma": "Pharmaceuticals",
            "other": "Other",
        },
    },
    {
        "id": "export_stage",
        "category": "Export Experience",
        "question": "What is your current export stage?",
        "options": {
            1: "Not exporting yet",
            2: "0–2 years",
            3: "2–5 years",
            4: "5+ years",
        },
    },
    {
        "id": "capacity",
        "category": "Supply Capability",
        "question": "What is your production capacity?",
        "options": {
            1: "Small",
            2: "Medium",
            3: "Large",
            4: "Very Large",
        },
    },
    {
        "id": "price_position",
        "category": "Pricing Strategy",
        "question": "How do you position your pricing?",
        "options": {
            1: "Low cost",
            2: "Competitive",
            3: "Mid-range",
            4: "Premium",
        },
    },
    {
        "id": "certifications",
        "category": "Compliance",
        "question": "What certifications do you have?",
        "options": {
            1: "None",
            2: "Basic (ISO)",
            3: "International (CE, FDA)",
            4: "Advanced / Multiple",
        },
    },
    {
        "id": "current_markets",
        "category": "Market Presence",
        "question": "Where are you currently exporting?",
        "options": {
            1: "Not exporting",
            2: "Middle East",
            3: "Europe/USA",
            4: "Multiple regions",
        },
    },
    {
        "id": "challenge",
        "category": "Pain Point",
        "question": "What is your biggest export challenge?",
        "options": {
            "buyers": "Finding buyers",
            "pricing": "Pricing",
            "logistics": "Logistics",
            "compliance": "Compliance",
            "scaling": "Scaling",
        },
    },
    {
        "id": "market_preference",
        "category": "Strategy",
        "question": "Which markets are you targeting?",
        "options": {
            1: "High margin (EU/US)",
            2: "High volume (Middle East/Africa)",
            3: "Emerging markets",
            4: "Not sure",
        },
    },
]

# -----------------------------
# CONTENT TEMPLATES
# -----------------------------
CONTENT_TEMPLATES = [
    {"id": "email", "name": "Export Outreach Sequence", "icon": "✉️"},
    {"id": "social", "name": "LinkedIn Outreach", "icon": "💼"},
    {"id": "product", "name": "B2B Product Pitch", "icon": "📦"},
    {"id": "ad", "name": "Quick Sales Messages", "icon": "📢"},
]

def get_assessment_results():
    answers = st.session_state.assessment_answers

    numeric_scores = []
    for key in ["export_stage", "capacity", "price_position", "certifications", "current_markets"]:
        if key in answers and isinstance(answers[key], int):
            numeric_scores.append(answers[key])

    avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 1

    # -----------------------------
    # EXPORTER LEVEL
    # -----------------------------
    if avg_score < 2:
        level = {
            "name": "Beginner Exporter",
            "color": "🟠",
            "desc": "You are at an early stage and should focus on easy-entry markets."
        }
        recommended_markets = ["UAE", "Saudi Arabia", "Africa"]
    elif avg_score < 3:
        level = {
            "name": "Emerging Exporter",
            "color": "🟡",
            "desc": "You can scale into mid-complexity markets."
        }
        recommended_markets = ["UAE", "UK", "Southeast Asia"]
    else:
        level = {
            "name": "Advanced Exporter",
            "color": "🟢",
            "desc": "You are ready for high-value global markets."
        }
        recommended_markets = ["USA", "Germany", "UK"]

    # -----------------------------
    # PAIN POINT
    # -----------------------------
    challenge = answers.get("challenge", "buyers")

    challenge_map = {
        "buyers": "Buyer Discovery",
        "pricing": "Pricing Optimization",
        "logistics": "Logistics Planning",
        "compliance": "Certification & Compliance",
        "scaling": "Market Expansion Strategy",
    }

    priority = challenge_map.get(challenge, "Buyer Discovery")

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    return {
        "avg_score": avg_score,
        "level": level,
        "recommended_markets": recommended_markets,
        "priority": priority,
        "product_category": answers.get("product_category"),
    }


def call_openai(messages, system_prompt=None):
    """Call OpenAI API with messages"""
    client = get_openai_client()
    if not client:
        return "⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY to your Streamlit secrets."

    try:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        response = client.chat.completions.create(
            model="gpt-4o", messages=full_messages, max_tokens=1500, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling OpenAI: {str(e)}"

 # -----------------------------
# SIDEBAR STYLING (IMPORTANT)
# -----------------------------
st.sidebar.markdown("""
<style>
.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 4px;
}
.sidebar-subtitle {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 15px;
}
.sidebar-section {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.footer-box {
    font-size: 12px;
    color: #d1d5db;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# BRAND HEADER
# -----------------------------
st.sidebar.markdown(
    f"<div class='sidebar-title'>💯 {BRAND_CONFIG['business_name']}</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div class='sidebar-subtitle'>AI Copilot for Export Growth</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# -----------------------------
# NAVIGATION SECTION
# -----------------------------
st.sidebar.markdown(
    "<div class='sidebar-section'>Navigation</div>",
    unsafe_allow_html=True
)

page_options = [
    "🏠 Home",
    "🌍 Export Opportunity Finder",
    "🛰️ Outreach Generator",
    "✅ Readiness Assessment",
    "💲 Profitability Calculator",
]

selected_page = st.sidebar.radio(
    "",
    page_options,
    label_visibility="collapsed"
)

# Sync with your app
current_page = selected_page

st.sidebar.markdown("---")

# -----------------------------
# QUICK VALUE PROPOSITION
# -----------------------------
st.sidebar.markdown(
    "<div class='sidebar-section'>What You Can Do</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("""
- 🌍 Find best export markets  
- 🛰️ Reach global buyers  
- ✅ Assess export readiness  
- 💲 Maximize profitability  
""")

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<div class='sidebar-section'>Contact Us</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    f"""
<div class='footer-box'>
<strong>{BRAND_CONFIG['consultant_name']}</strong><br><br>
📧 {BRAND_CONFIG['email']}<br>
🌐 {BRAND_CONFIG['website']}
</div>
""",
    unsafe_allow_html=True
)

# Get current index
current_index = (
    page_options.index(st.session_state.current_page)
    if st.session_state.current_page in page_options
    else 0
)



# -----------------------------
# HOME PAGE
# -----------------------------
if current_page == "🏠 Home":

    # -----------------------------
    # CUSTOM STYLING (KEY UPGRADE)
    # -----------------------------
    st.markdown("""
    <style>
    .hero-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .hero-tagline {
        font-size: 20px;
        color: #d1d5db;
        margin-bottom: 20px;
    }
    .info-box {
        background: rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 30px;
        font-size: 15px;
    }
    .section-title {
        font-size: 26px;
        font-weight: 600;
        margin: 30px 0 20px 0;
    }
    .card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 14px;
        min-height: 220px;
    }
    .card-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .card ul {
        padding-left: 18px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # HERO SECTION
    # -----------------------------
    st.markdown(f"<div class='hero-title'>💯 {BRAND_CONFIG['business_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-tagline'>{BRAND_CONFIG['tagline']}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        🚀 <strong>AI-Driven Decision Making</strong><br>
        End-to-end export growth copilot helping you identify markets, win buyers, and maximize profitability.
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # HOW IT WORKS
    # -----------------------------
    st.markdown("<div class='section-title'>How It Works</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🌍 Export Opportunity Finder</div>
            <ul>
                <li>Identify high-potential global markets</li>
                <li>Analyze demand and growth trends</li>
                <li>Understand competitive landscape</li>
                <li>Get market entry strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">✅ Readiness Assessment</div>
            <ul>
                <li>Evaluate export maturity level</li>
                <li>Identify capability gaps early</li>
                <li>Recommend best-fit global markets</li>
                <li>Generate actionable export roadmap</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🛰️ Outreach Generator</div>
            <ul>
                <li>Generate personalized buyer outreach</li>
                <li>Create email follow-up sequences</li>
                <li>Adapt messaging by market</li>
                <li>Improve response conversion rates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">💲 Profitability Calculator</div>
            <ul>
                <li>Estimate export profit margins</li>
                <li>Analyze cost structure drivers</li>
                <li>Simulate currency impact scenarios</li>
                <li>Optimize pricing decisions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # CTA SECTION
    # -----------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Get Started — Take Assessment", use_container_width=True):
            st.session_state.assessment_complete = False
            navigate_to("✅ Readiness Assessment")
            st.rerun()


# OPPORTUNITY FOUNDER PAGE
elif current_page == "🌍 Export Opportunity Finder":
    st.markdown("# 🌍 Export Opportunity Finder")
    
    # -----------------------------
    # PRODUCT + HS CODE MAPPING
    # -----------------------------
    product_hs_mapping = {
        "Home Textiles (6302)": {"product": "Home Textiles", "hs_code": "6302"},
        "Rice (1006)": {"product": "Rice", "hs_code": "1006"},
        "T-Shirts (6109)": {"product": "T-Shirts", "hs_code": "6109"},
        "Auto Components (8708)": {"product": "Auto Components", "hs_code": "8708"},
        "Pharmaceuticals (3004)": {"product": "Pharmaceuticals", "hs_code": "3004"},
    }

    # -----------------------------
    # INPUT: PRODUCT
    # -----------------------------
    st.subheader("📦 Product Selection")

    selected_product = st.selectbox(
        "Select Product Category",
        list(product_hs_mapping.keys())
    )

    product = product_hs_mapping[selected_product]["product"]
    hs_code = product_hs_mapping[selected_product]["hs_code"]

    st.info(f"📦 Analyzing **{product}** (HS Code: {hs_code})")

    # -----------------------------
    # INPUT: EXPORTER PROFILE
    # -----------------------------
    st.subheader("🏭 Exporter Profile")

    col1, col2 = st.columns(2)

    with col1:
        export_stage = st.selectbox(
            "Export Stage",
            ["New Exporter", "Growing", "Established"]
        )

        price_position = st.selectbox(
            "Price Positioning",
            ["Low Cost", "Mid-Range", "Premium"]
        )

        capacity = st.selectbox(
            "Production Capacity",
            ["Small", "Medium", "Large"]
        )

    with col2:
        certifications = st.selectbox(
            "Certifications",
            ["None", "Basic", "Advanced"]
        )

        market_preference = st.selectbox(
            "Market Preference",
            ["High Margin (EU/US)", "High Volume (Middle East/Africa)", "No Preference"]
        )

    # -----------------------------
    # MOCK TRADE DATA
    # -----------------------------
    trade_data = pd.DataFrame({
        "Market": ["USA", "Germany", "UAE", "Saudi Arabia", "UK"],
        "Import_Value_Bn": [6.5, 2.8, 1.2, 1.0, 2.2],
        "Growth_%": [8, 5, 14, 12, 6],
        "Top_Competitor": ["China", "Turkey", "China", "China", "Pakistan"],
        "Avg_Price_per_kg": [6.2, 6.8, 5.0, 4.8, 6.0]
    })
    buyer_data = {
    "USA": ["Walmart", "Target", "Amazon"],
    "Germany": ["Metro AG", "Otto Group", "Lidl"],
    "UAE": ["Carrefour UAE", "LuLu Group", "Noon"],
    "Saudi Arabia": ["Panda Retail", "Othaim Markets", "Danube"],
    "UK": ["Tesco", "Sainsbury's", "Marks & Spencer"]
    }

    def get_price_level(price):
        if price > 6:
            return "Premium"
        elif price > 5:
            return "Mid-Range"
        else:
            return "Low Cost"
    # -----------------------------
    # OPPORTUNITY SCORE (CONTEXT-AWARE)
    # -----------------------------
    def calculate_score(row):
        base_score = (
            row["Import_Value_Bn"] * 0.4 +
            row["Growth_%"] * 0.3
        )

        competition = 10 if row["Top_Competitor"] != "China" else 6

        fit_score = 0

        if price_position == "Premium" and row["Avg_Price_per_kg"] > 6:
            fit_score += 5

        if market_preference == "High Volume (Middle East/Africa)" and row["Market"] in ["UAE", "Saudi Arabia"]:
            fit_score += 5

        if certifications == "Advanced" and row["Market"] in ["USA", "Germany", "UK"]:
            fit_score += 5

        return base_score + (competition * 0.2) + fit_score


    trade_data["Opportunity Score"] = trade_data.apply(calculate_score, axis=1)
    trade_data = trade_data.sort_values(by="Opportunity Score", ascending=False)


    # -----------------------------
    # RUN ANALYSIS
    # -----------------------------
    if st.button("🔍 Find Export Opportunities"):

        # -----------------------------
        # FINAL OUTPUT TABLE
        # -----------------------------
        output_df = trade_data.copy()

        # Add new columns
        output_df["Competitor Country"] = output_df["Top_Competitor"]
        output_df["Estimated Price Level"] = output_df["Avg_Price_per_kg"].apply(get_price_level)
        output_df["Top Buyers / Importers"] = output_df["Market"].map(
            lambda x: ", ".join(buyer_data.get(x, ["N/A"]))
        )

        # Select final columns
        output_df = output_df[[
            "Market",
            "Competitor Country",
            "Estimated Price Level",
            "Top Buyers / Importers",
            "Opportunity Score"
        ]]

        st.subheader("📊 Export Opportunity Intelligence Table")

        st.dataframe(output_df, use_container_width=True)

        # -----------------------------
        # TOP 3 MARKETS
        # -----------------------------
        st.subheader("🏆 Top 3 Opportunities")

        top3 = output_df.head(3)

        for _, row in top3.iterrows():
            st.success(
                f"{row['Market']} | {row['Estimated Price Level']} Market | Score: {row['Opportunity Score']:.2f}"
            )

    # -----------------------------
     # LLM PROMPT
    # -----------------------------
    prompt = f"""
    You are a senior export strategy consultant.

    Analyze export opportunities based on BOTH market data and exporter profile.

    ### Product:
    {product}
    HS Code: {hs_code}

    ### Exporter Profile:
    - Stage: {export_stage}
    - Price Position: {price_position}
    - Capacity: {capacity}
    - Certifications: {certifications}
    - Market Preference: {market_preference}

    ### Market Data:
    {trade_data.to_string(index=False)}

    Provide:

    ### 1. Best-Fit Markets
    Top 3 markets tailored to this exporter

    ### 2. Why These Markets Fit
    Explain alignment

    ### 3. Markets to Avoid
    Where exporter may struggle

    ### 4. Pricing Strategy
    How to position pricing

    ### 5. Action Plan
    Clear next steps

    Be practical and decision-focused.
    """

    # -----------------------------
    # CALL LLM (CORRECT FORMAT)
    # -----------------------------
    with st.spinner("Generating AI insights..."):
        insights = call_openai(
                messages=[{"role": "user", "content": prompt}],
                system_prompt="You are an expert in global trade and export strategy."
            )

        st.subheader("🧠 AI Export Strategy Insights")
        st.markdown(insights)

# AI TOOLS PAGE
elif current_page == "🛰️ Outreach Generator":
    st.markdown("# 🛰️ AI Outreach Generator")

    tool_tab = st.tabs(["✨ Buyer Outreach"])

    # -----------------------------
    # CONTENT GENERATOR TAB
    # -----------------------------
    with tool_tab[0]:
        st.markdown("### 🌍 Generate buyer outreach + follow-up sequences instantly")
        #st.markdown("*Generate buyer outreach + follow-up sequences instantly*")
 
        template = st.selectbox(
            "Select Outreach Type",
            options=[t["id"] for t in CONTENT_TEMPLATES],
            format_func=lambda x: next(
                t["icon"] + " " + t["name"] for t in CONTENT_TEMPLATES if t["id"] == x
            ),
        )

        # -----------------------------
        # EXPORTER INPUTS
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            business_name = st.text_input(
                "Exporter Company Name", placeholder="e.g., ABC Textiles India"
            )
            product = st.text_input(
                "Export Product", placeholder="e.g., Cotton bedsheets"
            )

        with col2:
            audience = st.text_input(
                "Target Buyer / Importer",
                placeholder="e.g., German home textile importer",
            )
            tone = st.selectbox(
                "Tone",
                [
                    "Professional",
                    "Friendly & Casual",
                    "Luxurious & Premium",
                    "Playful & Fun",
                    "Authoritative & Expert",
                ],
            )

        additional_info = st.text_area(
            "Additional Details (USP, certifications, pricing, etc.)",
            placeholder="e.g., OEKO-TEX certified, competitive pricing, large capacity...",
        )

        # -----------------------------
        # BUYER CONTEXT (NEW)
        # -----------------------------
        st.markdown("### 🌍 Buyer Context")

        col3, col4 = st.columns(2)

        with col3:
            buyer_type = st.selectbox(
                "Buyer Type",
                ["Importer", "Distributor", "Retailer", "Wholesaler", "Not Sure"],
            )

            country = st.selectbox(
                "Target Market",
                ["USA", "Germany", "UAE", "UK", "Saudi Arabia", "Other"],
            )

        with col4:
            buyer_size = st.selectbox(
                "Buyer Size",
                ["Small", "Mid-sized", "Large Enterprise"],
            )

            relationship_stage = st.selectbox(
                "Relationship Stage",
                ["Cold Outreach", "Warm Lead", "Existing Buyer"],
            )

        # -----------------------------
        # GENERATE BUTTON
        # -----------------------------
        if st.button("🚀 Generate Outreach", use_container_width=True):
            if not get_openai_client():
                st.error("OpenAI API key not configured")
            else:
                template_prompts = {

                    "email": f"""
You are an expert export sales strategist.

Generate a complete outreach sequence for an exporter.

### Exporter:
{business_name or 'an exporter'}

### Product:
{product or 'a product'}

### USP:
{additional_info or 'high quality and reliable supply'}

### Buyer:
- Type: {buyer_type}
- Target: {audience or 'an importer'}
- Market: {country}
- Size: {buyer_size}
- Stage: {relationship_stage}

### Instructions:

1. Write a HIGH-CONVERSION cold email (120–150 words)
2. Write 2 follow-up emails
3. Provide 3 subject lines
4. Write:
   - LinkedIn message
   - WhatsApp message

### Market Adaptation:
- Germany → formal, precise
- USA → direct
- UAE → relationship-driven

Keep everything concise and practical.
""",

                    "social": f"""
Generate LinkedIn outreach sequence.

Exporter: {business_name}
Product: {product}
Buyer: {audience}
Market: {country}

Output:
- Initial message
- Follow-up message
- Connection request
""",

                    "product": f"""
Create a B2B export pitch.

Exporter: {business_name}
Product: {product}
Buyer: {audience}
Market: {country}

Include:
- Intro pitch
- Differentiators
- Why switch supplier
""",

                    "ad": f"""
Generate quick export sales messages.

Exporter: {business_name}
Product: {product}
Buyer: {audience}
Market: {country}

Output:
- Email intro
- WhatsApp pitch
- LinkedIn pitch
"""
                }

                with st.spinner("Generating outreach..."):
                    response = call_openai(
                        [{"role": "user", "content": template_prompts[template]}]
                    )
                    st.session_state.generated_content = response

        # -----------------------------
        # OUTPUT
        # -----------------------------
        if st.session_state.generated_content:
            st.markdown("### 📬 Outreach & Follow-up Sequence")
            st.markdown(st.session_state.generated_content)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "📥 Download",
                    st.session_state.generated_content,
                    file_name=f"{template}_outreach.txt",
                    mime="text/plain",
                )

            with col2:
                if st.button("🔄 Generate Again"):
                    st.session_state.generated_content = ""
                    st.rerun()

# ASSESSMENT PAGE
elif current_page == "✅ Readiness Assessment":
    st.markdown("# ✅ Export Readiness Assessment")

    if not st.session_state.assessment_complete:
        st.markdown("### Answer 8 quick questions to assess your export readiness and get market recommendations")

        answered_count = len(st.session_state.assessment_answers)
        total_questions = len(ASSESSMENT_QUESTIONS)
        progress = answered_count / total_questions

        # Progress bar
        st.progress(progress)

        if answered_count == total_questions:
            st.success(
                f"✅ All {total_questions} questions answered! Click below to see your export readiness report."
            )
        else:
            st.info(
                f"📝 {answered_count} of {total_questions} questions answered. Complete all to unlock insights."
            )

        st.markdown("---")

        # Callback
        def update_answer(question_id, key):
            value = st.session_state.get(key)
            if value is not None:
                st.session_state.assessment_answers[question_id] = value

        # Questions Loop
        for q in ASSESSMENT_QUESTIONS:
            is_answered = q["id"] in st.session_state.assessment_answers
            status = "✅" if is_answered else "⬜"

            st.markdown(f"### {status} {q['category']}")

            current_value = st.session_state.assessment_answers.get(q["id"])
            current_index = (
                list(q["options"].keys()).index(current_value)
                if current_value in q["options"]
                else None
            )

            st.radio(
                q["question"],
                options=list(q["options"].keys()),
                format_func=lambda x, opts=q["options"]: opts[x],
                key=f"q_{q['id']}",
                index=current_index,
                on_change=update_answer,
                args=(q["id"], f"q_{q['id']}"),
            )
            st.markdown("---")

        # CTA
        st.markdown("### 📊 Get Your Export Readiness Report")

        if answered_count == total_questions:
            if st.button("🚀 See My Export Strategy", use_container_width=True, type="primary"):
                st.session_state.assessment_complete = True
                st.rerun()
        else:
            remaining = total_questions - answered_count
            st.warning(f"⚠️ Please answer {remaining} more question(s).")

    else:
        # -----------------------------
        # RESULTS
        # -----------------------------
        results = get_assessment_results()

        st.markdown(
            f"## {results['level']['color']} Your Exporter Profile: **{results['level']['name']}**"
        )
        st.markdown(f"*{results['level']['desc']}*")

        # Score
        st.progress(results["avg_score"] / 4)
        st.markdown(f"**Readiness Score: {results['avg_score']:.1f} / 4.0**")

        st.markdown("---")

        # -----------------------------
        # MARKETS
        # -----------------------------
        st.markdown("### 🌍 Recommended Export Markets")

        for market in results["recommended_markets"]:
            st.markdown(f"- ✅ {market}")

        st.markdown("---")

        # -----------------------------
        # PRIORITY AREA
        # -----------------------------
        st.markdown("### ⚠️ Your Key Focus Area")
        st.info(results["priority"])

        st.markdown("---")

        # -----------------------------
        # AI RECOMMENDATIONS
        # -----------------------------
        st.markdown("### 🧠 AI Export Strategy Recommendations")

        prompt = f"""
You are an expert export strategy consultant.

Based on the exporter profile:

- Product Category: {results['product_category']}
- Exporter Level: {results['level']['name']}
- Score: {results['avg_score']:.2f}
- Recommended Markets: {results['recommended_markets']}
- Key Challenge: {results['priority']}

Provide:

### 1. Best Export Opportunity
(product-market combination)

### 2. Why These Markets Fit

### 3. Key Gaps to Address

### 4. 30-Day Action Plan

Keep it practical and actionable.
"""

        with st.spinner("Generating export strategy..."):
            response = call_openai(
                messages=[{"role": "user", "content": prompt}],
                system_prompt="You are a global trade advisor helping exporters grow internationally."
            )

        st.markdown(response)

        st.markdown("---")

        # -----------------------------
        # NEXT STEPS
        # -----------------------------
        st.markdown("### 🚀 Next Steps")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🌍 Find Export Opportunities"):
                navigate_to("🌍 Opportunity Finder")
                st.rerun()

        with col2:
            if st.button("📬 Generate Outreach"):
                navigate_to("🛰️ AI Tour")
                st.rerun()

        with col3:
            if st.button("💰 Check Profitability"):
                navigate_to("💰 Profitability")
                st.rerun()

        st.markdown("---")

        # -----------------------------
        # RESET
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Retake Assessment"):
                st.session_state.assessment_answers = {}
                st.session_state.assessment_complete = False
                st.rerun()

        with col2:
            if st.button("🏠 Back to Home"):
                navigate_to("🏠 Home")
                st.rerun()         

# PROFITABILITY PAGE
elif current_page == "💲 Profitability Calculator":
    st.markdown("# 💲 Profitability Calculator")

    # -----------------------------
    # COUNTRY DATA (MVP)
    # -----------------------------
    country_data = {
        "USA": {"duty": 8, "logistics_per_unit": 0.9},
        "Germany": {"duty": 10, "logistics_per_unit": 1.1},
        "UAE": {"duty": 5, "logistics_per_unit": 0.7},
        "Saudi Arabia": {"duty": 6, "logistics_per_unit": 0.8},
        "UK": {"duty": 9, "logistics_per_unit": 1.0}
    }

    # -----------------------------
    # INPUT SECTION
    # -----------------------------
    st.header("📥 Enter Export Details")

    col1, col2 = st.columns(2)

    with col1:
        product_category = st.selectbox("Product Category", [
            "Textiles & Apparel",
            "Food & Agriculture",
            "Chemicals & Pharmaceuticals",
            "Engineering Goods",
            "Consumer Goods",
            "Other"
        ])

        country = st.selectbox("Target Market", list(country_data.keys()))

        selling_price = st.number_input(
            "Selling Price per Unit ($)", min_value=0.0, value=5.0
        )
        exchange_rate = st.number_input(
        "USD to INR Exchange Rate", min_value=50.0, max_value=100.0, value=83.0
        )

    with col2:
        cost_price = st.number_input(
            "Cost of Production per Unit ($)", min_value=0.0, value=2.5
        )

        quantity = st.number_input(
            "Quantity", min_value=1, value=10000
        )

        commission = st.slider(
            "Commission / Distributor (%)", 0, 30, 5
        )
        fx_variation = st.slider(
        "Expected Currency Fluctuation (%)", 0, 10, 3
        )
    # -----------------------------
    # AUTO DATA
    # -----------------------------
    duty_percent = country_data[country]["duty"]
    logistics_per_unit = country_data[country]["logistics_per_unit"]

    # -----------------------------
    # CALCULATION ENGINE
    # -----------------------------
    def calculate_profit():
        revenue_usd = selling_price * quantity
        revenue_inr = revenue_usd * exchange_rate

        product_cost = cost_price * quantity
        logistics = logistics_per_unit * quantity
        duty = revenue_usd * (duty_percent / 100)
        commission_cost = revenue_usd * (commission / 100)

        total_cost_usd = product_cost + logistics + duty + commission_cost
        total_cost_inr = total_cost_usd * exchange_rate

        profit_usd = revenue_usd - total_cost_usd
        profit_inr = revenue_inr - total_cost_inr

        margin = (profit_usd / revenue_usd) * 100 if revenue_usd > 0 else 0

        # -----------------------------
        # FX SCENARIOS
        # -----------------------------
        up_rate = exchange_rate * (1 + fx_variation / 100)
        down_rate = exchange_rate * (1 - fx_variation / 100)

        profit_up_inr = (revenue_usd * up_rate) - (total_cost_usd * up_rate)
        profit_down_inr = (revenue_usd * down_rate) - (total_cost_usd * down_rate)

        return {
        # Revenue
        "Revenue USD": revenue_usd,
        "Revenue INR": revenue_inr,

        # Costs (USD)
        "Product Cost USD": product_cost,
        "Logistics Cost USD": logistics,
        "Duty USD": duty,
        "Commission USD": commission_cost,

        # Costs (INR)
        "Product Cost INR": product_cost * exchange_rate,
        "Logistics Cost INR": logistics * exchange_rate,
        "Duty INR": duty * exchange_rate,
        "Commission INR": commission_cost * exchange_rate,

        # Totals
        "Total Cost USD": total_cost_usd,
        "Total Cost INR": total_cost_inr,

        # Profit
        "Profit USD": profit_usd,
        "Profit INR": profit_inr,

        # Margin
        "Margin": margin,

        # FX scenarios
        "Profit INR (Up)": profit_up_inr,
        "Profit INR (Down)": profit_down_inr
        }

    # -----------------------------
    # LLM Function
    # -----------------------------   

    def generate_ai_insights(results, country, product_category, exchange_rate, fx_variation):
        client = get_openai_client()

        if client is None:
            return "⚠️ OpenAI API key not found. Please add it in Streamlit secrets."

        prompt = f"""
    You are an expert international trade consultant.

    Analyze the export scenario below and provide a structured response with:

    ### 1. Profitability Assessment
    (Good / Moderate / Poor with reasoning)

    ### 2. Key Cost Drivers
    (Identify biggest cost contributors)

    ### 3. Pricing Recommendation
    (Suggest if price should increase/decrease)

    ### 4. Currency Risk Analysis
    (Explain impact of INR fluctuation on profit)

    ### 5. Key Risks
    (Operational, pricing, or market risks)

    ### 6. Actionable Recommendations
    (3 clear next steps)

    ---

    ### Data:

    Market: {country}  
    Product Category: {product_category}

    Revenue (USD): {results['Revenue USD']:.2f}  
    Total Cost (USD): {results['Total Cost USD']:.2f}  
    Profit (USD): {results['Profit USD']:.2f}  
    Margin: {results['Margin']:.2f}%

    Cost Breakdown (USD):
    - Product Cost: {results['Product Cost USD']:.2f}
    - Logistics: {results['Logistics Cost USD']:.2f}
    - Duty: {results['Duty USD']:.2f}
    - Commission: {results['Commission USD']:.2f}

    Currency:
    - Base Rate: {exchange_rate}
    - Variation: ±{fx_variation}%
    - Profit (INR - Base): {results['Profit INR']:.2f}
    - Profit (INR - Upside): {results['Profit INR (Up)']:.2f}
    - Profit (INR - Downside): {results['Profit INR (Down)']:.2f}

    ---

    Keep response concise, structured, and practical.
    """

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"⚠️ Error generating AI insights: {str(e)}"


    # -----------------------------
    # RUN CALCULATION
    # -----------------------------
    if st.button("🚀 Calculate Profitability"):

        results = calculate_profit()

        # -----------------------------
        # SUMMARY
        # -----------------------------
        st.header("📊 Profitability Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Revenue ($)", f"{results['Revenue USD']:.2f}")
        col2.metric("Total Cost ($)", f"{results['Total Cost USD']:.2f}")
        col3.metric("Profit ($)", f"{results['Profit USD']:.2f}")
        col4.metric("Margin (%)", f"{results['Margin']:.2f}%")

        # -----------------------------
        # CURRENCY RISK
        # -----------------------------
        st.subheader("💱 Currency Risk Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric("Base Profit (₹)", f"{results['Profit INR']:.2f}")

        col2.metric(
            f"Profit if ₹ weakens (+{fx_variation}%)",
            f"{results['Profit INR (Up)']:.2f}"
        )

        col3.metric(
            f"Profit if ₹ strengthens (-{fx_variation}%)",
            f"{results['Profit INR (Down)']:.2f}"
        )


        # -----------------------------
        # COST BREAKDOWN
        # -----------------------------
        st.subheader("📦 Cost Breakdown")

        df = pd.DataFrame({
            "Component": ["Product Cost", "Logistics", "Duty", "Commission"],
            "USD ($)": [
                results["Product Cost USD"],
                results["Logistics Cost USD"],
                results["Duty USD"],
                results["Commission USD"]
            ],
            "INR (₹)": [
                results["Product Cost INR"],
                results["Logistics Cost INR"],
                results["Duty INR"],
                results["Commission INR"]
            ]
        })

        st.table(df)

        # -----------------------------
        # AI INSIGHTS
        # -----------------------------
        st.subheader("🧠 AI Insights")

        with st.spinner("Generating insights..."):
            insights = insights = generate_ai_insights(
        results,
        country,
        product_category,
        exchange_rate,
        fx_variation
        )
            st.markdown(insights)
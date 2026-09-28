import streamlit as st
import textwrap
import pandas as pd
import pickle
import textwrap
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)


try:
    model = load_model()
    model_features = list(model.feature_names_in_)

except FileNotFoundError:
    st.error(
        "❌ model.pkl not found. Please keep model.pkl in the same folder as app.py."
    )
    st.stop()

except Exception as e:
    st.error(f"❌ Unable to load model: {e}")
    st.stop()


# ============================================================
# FRIENDLY CATEGORY NAMES
# ============================================================
friendly_names = {
    "Ex": "Excellent",
    "Gd": "Good",
    "TA": "Typical / Average",
    "Fa": "Fair",
    "Po": "Poor",
    "None": "No Feature",

    "RL": "Residential Low Density",
    "RM": "Residential Medium Density",
    "RH": "Residential High Density",
    "FV": "Floating Village Residential",
    "C": "Commercial",

    "Pave": "Paved Road",
    "Grvl": "Gravel Road",

    "Reg": "Regular Shape",
    "IR1": "Slightly Irregular",
    "IR2": "Moderately Irregular",
    "IR3": "Very Irregular",

    "AllPub": "All Public Utilities",
    "NoSeWa": "No Sewer and Water",

    "Inside": "Inside Lot",
    "Corner": "Corner Lot",
    "CulDSac": "Cul-de-sac",
    "FR2": "Frontage on 2 Sides",
    "FR3": "Frontage on 3 Sides",

    "1Story": "One Story",
    "1.5Fin": "One and a Half Story - Finished",
    "1.5Unf": "One and a Half Story - Unfinished",
    "2Story": "Two Story",
    "2.5Fin": "Two and a Half Story - Finished",
    "2.5Unf": "Two and a Half Story - Unfinished",
    "SFoyer": "Split Foyer",
    "SLvl": "Split Level",

    "Fin": "Finished",
    "RFn": "Rough Finished",
    "Unf": "Unfinished",

    "Y": "Yes",
    "N": "No",
    "Partial": "Partially Finished",

    "Typ": "Typical Functionality",
    "Min1": "Minor Deductions 1",
    "Min2": "Minor Deductions 2",
    "Mod": "Moderate Functionality",
    "Maj1": "Major Deductions 1",
    "Maj2": "Major Deductions 2",
    "Sev": "Severe Issues",

    "Wd Sdng": "Wood Siding",
    "MetalSd": "Metal Siding",
    "HdBoard": "Hardboard Siding",
    "Wd Shng": "Wood Shingles",
    "CemntBd": "Cement Board",
    "BrkFace": "Brick Face",
    "BrkComm": "Common Brick",
    "AsbShng": "Asbestos Shingles",
    "AsphShn": "Asphalt Shingles",
    "Stucco": "Stucco",
    "VinylSd": "Vinyl Siding",
    "Stone": "Stone",
    "ImStucc": "Imitation Stucco",

    "New": "New Construction",
    "WD": "Warranty Deed",
    "CWD": "Warranty Deed - Cash",
    "VWD": "Warranty Deed - VA Loan",
    "COD": "Court Officer Deed",
    "Con": "Contract",
    "ConLw": "Contract - Low Down Payment",
    "ConLI": "Contract - Low Interest",
    "ConLD": "Contract - Low Down Payment",
    "Oth": "Other"
}


# ============================================================
# CUSTOM CSS DESIGN
# ============================================================
st.markdown("""
<style>

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

/* Global Font */
* {
    font-family: 'DM Sans', sans-serif;
}

/* Main Page Background */
.stApp {
    background:
        radial-gradient(
            circle at 95% 5%,
            rgba(255, 211, 166, 0.60),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 95%,
            rgba(109, 24, 31, 0.28),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #f3d8ba 0%,
            #e9ad7d 42%,
            #bb5435 75%,
            #50191d 100%
        );
    background-attachment: fixed;
}

/* Main Container */
.main .block-container {
    max-width: 1240px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}

/* Hero Section */
.hero-section {
    min-height: 420px;
    padding: 56px 60px;
    border-radius: 28px;
    position: relative;
    overflow: hidden;
    margin-bottom: 30px;

    background:
        linear-gradient(
            90deg,
            rgba(47, 12, 15, 0.90) 0%,
            rgba(81, 24, 22, 0.70) 42%,
            rgba(137, 55, 35, 0.20) 100%
        ),
        url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1800&q=90");

    background-size: cover;
    background-position: center;

    border: 1px solid rgba(255, 234, 211, 0.58);

    box-shadow:
        0 25px 65px rgba(57, 14, 17, 0.38),
        inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

/* Shiny Light in Hero */
.hero-section::after {
    content: "";
    position: absolute;
    top: -110px;
    right: -105px;
    width: 460px;
    height: 460px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(255, 218, 174, 0.42),
        transparent 68%
    );
    pointer-events: none;
}

/* Hero Content */
.hero-content {
    position: relative;
    z-index: 2;
    max-width: 700px;
}

.hero-badge {
    display: inline-block;
    padding: 9px 18px;
    border-radius: 30px;
    color: #fff7ee;
    font-size: 13px;
    letter-spacing: 0.7px;

    background: rgba(255, 225, 197, 0.14);
    border: 1px solid rgba(255, 235, 215, 0.52);
    backdrop-filter: blur(10px);
}

.hero-title {
    color: #fff6eb;
    font-family: 'Playfair Display', serif;
    font-size: 50px;
    line-height: 1.12;
    margin-top: 22px;
    margin-bottom: 16px;

    text-shadow:
        0 4px 15px rgba(0, 0, 0, 0.42),
        0 0 20px rgba(255, 191, 127, 0.22);
}

.hero-subtitle {
    color: #ffe8d2;
    font-size: 18px;
    line-height: 1.75;
    max-width: 610px;
}

/* Form Card */
div[data-testid="stForm"] {
    padding: 32px;
    border-radius: 25px;

    background: rgba(255, 248, 239, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(15px);

    box-shadow:
        0 22px 55px rgba(67, 19, 17, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.94);
}

/* Section Header */
.section-header {
    padding: 14px 20px;
    margin-top: 22px;
    margin-bottom: 20px;
    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            #711e2a 0%,
            #a43a31 55%,
            #d07542 100%
        );

    box-shadow:
        0 9px 20px rgba(106, 29, 28, 0.25),
        inset 0 1px 0 rgba(255, 226, 194, 0.38);
}

.section-title {
    color: #fff8ef;
    font-size: 21px;
    font-weight: 700;
    margin: 0;
}

/* Labels */
label {
    color: #4a1b1c !important;
    font-weight: 600 !important;
}

/* Caption */
.stCaption,
small {
    color: #6e302a !important;
}

/* Number Input */
.stNumberInput input {
    color: #431718 !important;
    background: rgba(255, 252, 248, 0.96) !important;
    border: 1px solid #da9b73 !important;
    border-radius: 11px !important;

    box-shadow:
        inset 0 2px 5px rgba(93, 29, 18, 0.06),
        0 3px 10px rgba(93, 29, 18, 0.07);
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    color: #431718 !important;
    background: rgba(255, 252, 248, 0.96) !important;
    border: 1px solid #da9b73 !important;
    border-radius: 11px !important;

    box-shadow:
        inset 0 2px 5px rgba(93, 29, 18, 0.06),
        0 3px 10px rgba(93, 29, 18, 0.07);
}

/* Selectbox Dropdown Text */
div[data-baseweb="popover"] {
    color: #431718;
}

/* Input Focus */
.stNumberInput input:focus,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #8a272d !important;

    box-shadow:
        0 0 0 3px rgba(138, 39, 45, 0.16),
        0 6px 18px rgba(138, 39, 45, 0.14) !important;
}

/* Slider */
.stSlider [role="slider"] {
    background-color: #85252c !important;
    border-color: #85252c !important;
}

.stSlider div[data-baseweb="slider"] > div > div {
    background: #bd5438 !important;
}

/* Prediction Button */
.stFormSubmitButton > button,
.stButton > button {
    min-height: 54px;
    width: 100%;

    color: #fff9ef !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 15px !important;

    background:
        linear-gradient(
            135deg,
            #711e2a 0%,
            #a43a31 52%,
            #dc7c47 100%
        ) !important;

    box-shadow:
        0 11px 25px rgba(106, 28, 29, 0.34),
        inset 0 1px 0 rgba(255, 229, 200, 0.48) !important;

    transition: all 0.25s ease !important;
}

/* Button Hover */
.stFormSubmitButton > button:hover,
.stButton > button:hover {
    transform: translateY(-3px);
    background:
        linear-gradient(
            135deg,
            #84262e 0%,
            #bb4d35 52%,
            #ea955f 100%
        ) !important;

    box-shadow:
        0 17px 34px rgba(106, 28, 29, 0.42),
        0 0 20px rgba(246, 176, 115, 0.40) !important;
}

/* Divider */
.divider {
    height: 2px;
    border-radius: 10px;
    margin: 28px 0;

    background:
        linear-gradient(
            90deg,
            transparent,
            #a64432,
            #e7a06d,
            transparent
        );
}

/* Result Box */
.result-box {
    position: relative;
    overflow: hidden;
    margin-top: 28px;
    padding: 43px 30px;
    border-radius: 25px;
    text-align: center;

    background:
        linear-gradient(
            135deg,
            #591820 0%,
            #912f31 50%,
            #d87945 100%
        );

    border: 1px solid rgba(255, 224, 192, 0.40);

    box-shadow:
        0 24px 55px rgba(70, 16, 18, 0.38),
        inset 0 1px 0 rgba(255, 226, 197, 0.40);
}

/* Result Light Effect */
.result-box::before {
    content: "";
    position: absolute;
    top: -150px;
    right: -90px;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: rgba(255, 221, 180, 0.17);
}

.result-title {
    position: relative;
    color: #ffead5;
    font-size: 27px;
    margin-bottom: 10px;
}

.result-price {
    position: relative;
    color: #fff9ee;
    font-size: 56px;
    font-weight: 700;
    letter-spacing: 1px;

    text-shadow:
        0 4px 15px rgba(0, 0, 0, 0.34),
        0 0 20px rgba(255, 204, 155, 0.30);
}

.result-note {
    position: relative;
    color: #ffe3cc;
    font-size: 15px;
}

/* Information Card */
.info-box {
    margin-top: 23px;
    padding: 20px 24px;
    border-radius: 16px;

    background: rgba(255, 247, 235, 0.93);
    border-left: 5px solid #a94234;

    box-shadow:
        0 8px 22px rgba(78, 23, 17, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.info-text {
    color: #572321;
    font-size: 15px;
    line-height: 1.7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #541a21 0%,
            #8b332e 50%,
            #d57847 100%
        );

    border-right: 1px solid rgba(255, 229, 198, 0.28);
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: #fff5ea !important;
}

/* Sidebar Card */
.sidebar-card {
    padding: 23px;
    border-radius: 18px;

    background: rgba(255, 238, 217, 0.13);
    border: 1px solid rgba(255, 229, 202, 0.32);
    backdrop-filter: blur(12px);

    box-shadow:
        0 12px 27px rgba(43, 10, 12, 0.20),
        inset 0 1px 0 rgba(255, 255, 255, 0.20);
}

/* Alert Box */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #f0c39c;
}

::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: linear-gradient(#7c222b, #d67345);
}

/* Responsive Mobile Layout */
@media screen and (max-width: 768px) {
    .hero-section {
        min-height: 365px;
        padding: 35px 26px;
        border-radius: 20px;
    }

    .hero-title {
        font-size: 34px;
    }

    .hero-subtitle {
        font-size: 15px;
    }

    div[data-testid="stForm"] {
        padding: 20px;
    }

    .result-price {
        font-size: 40px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
<div class="sidebar-card">
<h2 style="margin-top: 0;">🏡 House Value AI</h2>
<p style="line-height: 1.7;">Estimate a home's market value using your trained machine learning model and property information.</p>
<hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.30);">
<p>⚡ Instant price prediction</p>
<p>📊 ML-based analysis</p>
<p>🏠 Property feature evaluation</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.info("""
    **How to use**

    1. Enter property details  
    2. Select quality features  
    3. Click Predict House Price  
    4. View your estimated value  
    """)


# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-section">
<div class="hero-content">
<span class="hero-badge">✨ AI-POWERED REAL ESTATE ANALYTICS</span>
<h1 class="hero-title">Find the Value<br>Behind Every Home</h1>
<p class="hero-subtitle">Add your property information and receive a smart, data-driven estimated house price within seconds.</p>
</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT FORM - EXACT 15 MODEL FEATURES
# ============================================================
with st.form("house_form"):

    # --------------------------------------------------------
    # BASIC PROPERTY INFORMATION
    # --------------------------------------------------------
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">📍 Basic Property Information</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        overall_qual = st.slider(
            "Overall Quality (1 to 10)",
            min_value=1,
            max_value=10,
            value=5,
            help="Overall material and finish quality of the property."
        )

        gr_liv_area = st.number_input(
            "Above Ground Living Area (sq ft)",
            min_value=100,
            max_value=10000,
            value=1500,
            step=50,
            help="Above-ground living area in square feet."
        )

    with c2:
        garage_cars = st.number_input(
            "Garage Capacity (Cars)",
            min_value=0,
            max_value=5,
            value=2,
            step=1,
            help="Number of cars that can fit in the garage."
        )

        garage_area = st.number_input(
            "Garage Area (sq ft)",
            min_value=0,
            max_value=2000,
            value=400,
            step=50,
            help="Garage area in square feet."
        )

    with c3:
        total_bsmt_sf = st.number_input(
            "Total Basement Area (sq ft)",
            min_value=0,
            max_value=5000,
            value=800,
            step=50,
            help="Total basement area in square feet."
        )

        first_floor_sf = st.number_input(
            "First Floor Area (sq ft)",
            min_value=0,
            max_value=5000,
            value=1000,
            step=50,
            help="First floor area in square feet."
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROOM & BATHROOM INFORMATION
    # --------------------------------------------------------
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">📐 Rooms & Property Details</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        full_bath = st.number_input(
            "Full Bathrooms",
            min_value=0,
            max_value=8,
            value=2,
            step=1,
            help="Number of full bathrooms."
        )

        total_rooms = st.number_input(
            "Total Rooms Above Ground",
            min_value=1,
            max_value=20,
            value=6,
            step=1,
            help="Total rooms above ground level."
        )

    with c2:
        mas_vnr_area = st.number_input(
            "Masonry Veneer Area (sq ft)",
            min_value=0,
            max_value=2000,
            value=0,
            step=10,
            help="Masonry veneer area in square feet."
        )

        fireplaces = st.number_input(
            "Number of Fireplaces",
            min_value=0,
            max_value=5,
            value=0,
            step=1,
            help="Number of fireplaces in the property."
        )

    with c3:
        year_built = st.number_input(
            "Year Built",
            min_value=1800,
            max_value=2026,
            value=2000,
            step=1,
            help="Year in which the house was originally constructed."
        )

        year_remod_add = st.number_input(
            "Year Remodeled",
            min_value=1800,
            max_value=2026,
            value=2000,
            step=1,
            help="Year of the latest remodeling or renovation."
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # QUALITY RATINGS
    # --------------------------------------------------------
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">⭐ Quality Ratings</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    quality_options = ["Ex", "Gd", "TA", "Fa"]
    bsmt_quality_options = ["Ex", "Fa", "Gd", "None", "TA"]

    with c1:
        exter_qual = st.selectbox(
            "Exterior Quality",
            options=quality_options,
            format_func=lambda x: friendly_names.get(x, x),
            help="Exterior material and finish quality."
        )

    with c2:
        bsmt_qual = st.selectbox(
            "Basement Quality",
            options=bsmt_quality_options,
            format_func=lambda x: friendly_names.get(x, x),
            help="Basement height and quality."
        )

    with c3:
        kitchen_qual = st.selectbox(
            "Kitchen Quality",
            options=quality_options,
            format_func=lambda x: friendly_names.get(x, x),
            help="Kitchen quality rating."
        )

    st.caption(
        "Quality values are converted to the numeric category codes used by the trained model."
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    predict_button = st.form_submit_button(
        "✨ Predict House Price",
        use_container_width=True
    )


# ============================================================
# PREDICTION LOGIC
# ============================================================
if predict_button:

    try:
        if year_remod_add < year_built:
            st.warning(
                "⚠️ Year Remodeled is earlier than Year Built. Please verify the entered years."
            )

        with st.spinner("🔍 Analyzing property details with AI model..."):

            # The saved LinearRegression model expects these exact 15 columns.
            # The three quality fields use the category order stored in the
            # saved OneHotEncoder (alphabetical category codes).
            exter_qual_code = {"Ex": 0, "Fa": 1, "Gd": 2, "TA": 3}[exter_qual]
            bsmt_qual_code = {"Ex": 0, "Fa": 1, "Gd": 2, "None": 3, "TA": 4}[bsmt_qual]
            kitchen_qual_code = {"Ex": 0, "Fa": 1, "Gd": 2, "TA": 3}[kitchen_qual]

            input_data = {
                "OverallQual": overall_qual,
                "GrLivArea": gr_liv_area,
                "GarageCars": garage_cars,
                "ExterQual": exter_qual_code,
                "GarageArea": garage_area,
                "TotalBsmtSF": total_bsmt_sf,
                "1stFlrSF": first_floor_sf,
                "BsmtQual": bsmt_qual_code,
                "KitchenQual": kitchen_qual_code,
                "FullBath": full_bath,
                "TotRmsAbvGrd": total_rooms,
                "YearBuilt": year_built,
                "YearRemodAdd": year_remod_add,
                "MasVnrArea": mas_vnr_area,
                "Fireplaces": fireplaces
            }

            # Keep the exact order used when the model was fitted.
            final_input = pd.DataFrame([input_data])
            final_input = final_input.reindex(columns=model_features)

            prediction = model.predict(final_input)[0]

        # ----------------------------------------------------
        # RESULT DISPLAY
        # ----------------------------------------------------
        st.success("✅ Prediction completed successfully!")

        # Convert only for display; the ML model still predicts in USD.
        USD_TO_INR = 95.89
        prediction_inr = prediction * USD_TO_INR

        st.markdown(f"""<div class="result-box"><h2 class="result-title">    Estimated Property Value</h2><div class="result-price">${prediction:,.0f}</div><p class="result-note">Approx. ₹{prediction_inr:,.0f} in Indian Rupees</p><p class="result-note">AI-generated estimate based on the property details you entered</p></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="info-box"><p class="info-text"><strong>⚠️ Important Notice:</strong> This is a machine-learning-based estimate, not an official property valuation. Actual prices can differ because of location, neighborhood demand, property condition, market conditions, legal factors and other real estate variables.</p></div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Something went wrong during prediction: {e}")
        st.info(
            "The input columns are matched directly with the 15 features used by model.pkl."
        )

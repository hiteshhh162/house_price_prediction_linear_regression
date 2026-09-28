
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="wide"
)

# ---------------- LOAD PICKLE FILES ----------------
@st.cache_resource
def load_files():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("preprocessing_info.pkl", "rb") as f:
        preprocessing = pickle.load(f)

    return model, preprocessing


model, preprocessing = load_files()

encoder = preprocessing["one_hot_encoder"]
top_features = preprocessing["top_features"]

# ---------------- FRIENDLY CATEGORY NAMES ----------------
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

    "Pave": "Paved",
    "Grvl": "Gravel",

    "Reg": "Regular",
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

    "Typ": "Typical",
    "Min1": "Minor Deductions 1",
    "Min2": "Minor Deductions 2",
    "Mod": "Moderate",
    "Maj1": "Major Deductions 1",
    "Maj2": "Major Deductions 2",
    "Sev": "Severe",

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

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background:
    linear-gradient(
        rgba(8, 15, 35, 0.78),
        rgba(12, 20, 45, 0.90)
    ),
    url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1150px;
}

.hero {
    padding: 28px;
    border-radius: 22px;
    background: #080B2B(
        120deg,
        rgba(32, 70, 130, 0.88),
        rgba(105, 55, 170, 0.88)
    );
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

.hero h1 {
    color: #e5f8ff;
    font-size: 38px;
    margin-bottom: 8px;
    text-shadow:
        0 0 10px rgba(120, 220, 255, 0.65),
        0 0 22px rgba(120, 180, 255, 0.45);
}

.hero p {
    color: #e4eaff;
    font-size: 17px;
}

section[data-testid="stSidebar"] {
    background: rgba(13, 25, 50, 0.96);
}

div[data-testid="stForm"] {
    background: rgba(20, 35, 65, 0.88);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(150, 180, 255, 0.3);
}

.stButton > button {
    background: linear-gradient(90deg, #3978f6, #9b4dff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 600;
}

h1, h2, h3, p, label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🏡 House Price Prediction</h1>
    <p>
        Looking for an estimated house price?
        Enter a few details about the property and
        let the model calculate an estimated value.
    </p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Every home has its own story. Add the property details "
    "below to get a price estimate based on the trained model."
)

# ---------------- INPUT FORM ----------------
st.subheader("🏠 Property Details")

categorical_columns = list(encoder.feature_names_in_)

with st.form("house_form"):

    st.markdown("### Basic Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        overall_qual = st.slider(
            "Overall Quality",
            min_value=1,
            max_value=10,
            value=5
        )

        living_area = st.number_input(
            "Above Ground Living Area (sq ft)",
            min_value=100,
            max_value=10000,
            value=1500
        )

    with c2:
        year_built = st.number_input(
            "Year Built",
            min_value=1800,
            max_value=2026,
            value=2000
        )

        year_remod = st.number_input(
            "Year Remodeled",
            min_value=1800,
            max_value=2026,
            value=2000
        )

    with c3:
        garage_cars = st.number_input(
            "Garage Capacity (Cars)",
            min_value=0,
            max_value=5,
            value=2
        )

        garage_area = st.number_input(
            "Garage Area (sq ft)",
            min_value=0,
            max_value=2000,
            value=400
        )

    st.markdown("### More Property Details")

    c1, c2, c3 = st.columns(3)

    with c1:
        total_bsmt = st.number_input(
            "Total Basement Area (sq ft)",
            min_value=0,
            max_value=5000,
            value=800
        )

        first_floor = st.number_input(
            "First Floor Area (sq ft)",
            min_value=0,
            max_value=5000,
            value=1000
        )

    with c2:
        second_floor = st.number_input(
            "Second Floor Area (sq ft)",
            min_value=0,
            max_value=5000,
            value=500
        )

        full_bath = st.number_input(
            "Full Bathrooms",
            min_value=0,
            max_value=8,
            value=2
        )

    with c3:
        total_rooms = st.number_input(
            "Total Rooms",
            min_value=1,
            max_value=20,
            value=6
        )

        sold_year = st.number_input(
            "Year Sold",
            min_value=2000,
            max_value=2030,
            value=2026
        )

    st.markdown("### Property Quality")

    exter_qual = st.selectbox(
        "Exterior Quality",
        ["Ex", "Gd", "TA", "Fa"],
        format_func=lambda x: friendly_names.get(x, x)
    )

    bsmt_qual = st.selectbox(
        "Basement Quality",
        ["Ex", "Gd", "TA", "Fa", "None"],
        format_func=lambda x: friendly_names.get(x, x)
    )

    kitchen_qual = st.selectbox(
        "Kitchen Quality",
        ["Ex", "Gd", "TA", "Fa"],
        format_func=lambda x: friendly_names.get(x, x)
    )

    st.markdown("### Additional Property Information")

    st.caption(
        "Choose the options that best describe the property."
    )

    categorical_inputs = {}

    for col, categories in zip(
        encoder.feature_names_in_,
        encoder.categories_
    ):
        options = list(categories)

        selected_value = st.selectbox(
            col.replace("_", " ").title(),
            options=options,
            format_func=lambda value: friendly_names.get(
                str(value), str(value)
            ),
            key=f"cat_{col}"
        )

        categorical_inputs[col] = selected_value

    predict_button = st.form_submit_button(
        "✨ Predict House Price",
        use_container_width=True
    )

# ---------------- PREDICTION ----------------
if predict_button:

    try:
        cat_df = pd.DataFrame([categorical_inputs])

        encoded_array = encoder.transform(cat_df)

        encoded_columns = encoder.get_feature_names_out(
            categorical_columns
        )

        encoded_df = pd.DataFrame(
            encoded_array,
            columns=encoded_columns
        )

        numeric_data = {
            "OverallQual": overall_qual,
            "TotalSF": total_bsmt + first_floor + second_floor,
            "GrLivArea": living_area,
            "GarageCars": garage_cars,
            "GarageArea": garage_area,
            "TotalBsmtSF": total_bsmt,
            "1stFlrSF": first_floor,
            "FullBath": full_bath,
            "TotRmsAbvGrd": total_rooms,
            "HouseAge": sold_year - year_built,
            "YearBuilt": year_built,
            "RemodAge": sold_year - year_remod
        }

        input_df = pd.DataFrame([numeric_data])

        final_input = pd.concat(
            [input_df, encoded_df],
            axis=1
        )

        final_input = final_input.reindex(
            columns=top_features,
            fill_value=0
        )

        prediction = model.predict(final_input)[0]

        st.success("Prediction completed!")

        st.markdown("### Estimated House Price")

        st.markdown(
            f"""
            <div style="
                padding: 25px;
                border-radius: 18px;
                background: linear-gradient(
                    120deg,
                    rgba(30, 100, 190, 0.95),
                    rgba(130, 65, 200, 0.95)
                );
                text-align: center;
                box-shadow: 0 8px 30px rgba(0,0,0,0.25);
            ">
                <h2 style="color:white;">
                    ${prediction:,.0f}
                </h2>
                <p style="color:#e8edff;">
                    Estimated value based on the details provided
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "This is a model-generated estimate, not an official "
            "property valuation. Actual prices may vary."
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
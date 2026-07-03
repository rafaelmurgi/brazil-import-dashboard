import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Brazil Imports Intelligence Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():

    consolidated = pd.read_excel(
        "consolidated_data_trade_br_fi_clean.xlsx"
    )

    return consolidated

consolidated = load_data()

st.title(
    "Brazil Imports Intelligence Dashboard – Trade, Tariffs and Forecasts"
)

st.caption(
    "Product-level insights on Brazilian imports, including trade structure and 5-year forecasts"
)

# -----------------------
# NCM selector
# -----------------------

consolidated["NCM Label"] = (
    consolidated["NCM Code"].astype(str)
    + " - "
    + consolidated["NCM Description"]
)

selected = st.selectbox(
    "NCM Code",
    consolidated["NCM Label"].sort_values()
)

selected_row = consolidated[
    consolidated["NCM Label"] == selected
].iloc[0]

# -----------------------
# Product description
# -----------------------

st.markdown(
    f"### {selected_row['NCM Description']}"
)

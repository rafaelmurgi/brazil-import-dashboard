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
st.markdown("---")

st.subheader(
    "Market Overview and Tariff Structure"
)

market_overview = pd.DataFrame({

    "Indicator": [

        "Brazilian total annual imports (USD mn)",

        "Brazilian imports from Finland (USD mn)",

        "Finland's share (%)",

        "Brazil applied tariff (%)",

        "EU-Mercosur base rate (%)",

        "Tariff elimination timeline (years)",

        "Note"

    ],

    "Value": [

    f"{selected_row['Brazilian total annual imports - USD millions']:.1f}",

    f"{selected_row['Brazilian annual imports from Finland - USD millions']:.1f}",

    f"{finland_share:.1f}",

    f"{selected_row['Brazil applied tariff (%)']:.1f}",

    f"{selected_row['EU-Mercosur agreement base rate of Brazil']}",

    selected_row["Tariff elimination timeline (years)"],

    selected_row["Note"]

]
})

st.dataframe(
    market_overview,
    hide_index=True,
    use_container_width=True
)

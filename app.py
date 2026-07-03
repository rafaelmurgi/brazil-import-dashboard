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

    forecast = pd.read_csv(
        "forecast_ncm_powerbi.csv"
    )

    return consolidated, forecast

consolidated, forecast = load_data()

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

selected_code = selected_row["NCM Code"]

fc = forecast[
    forecast["NCM Code"] == selected_code
]

if len(fc) == 0:
    st.error("No forecast data available for this product.")
    st.stop()

# -----------------------
# Product description
# -----------------------

st.markdown(
    f"### {selected_row['NCM Description']}"
)

tariff = selected_row["Brazil applied tariff (%)"]

if tariff == int(tariff):
    tariff_display = f"{int(tariff)}"
else:
    tariff_display = f"{tariff:.1f}"

st.markdown("---")

st.subheader(
    "Market Overview and Tariff Structure"
)

finland_share = selected_row["Finland's share of Brazilian imports (%)"]

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

        tariff_display,

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

st.markdown("---")

st.subheader(
    "Key Market Indicators"
)

imports_2025 = fc.loc[
    fc["Year"] == 2025,
    "imports_usd_2025"
].iloc[0]

forecast_2030 = fc.loc[
    fc["Year"] == 2030,
    "Forecast"
].iloc[0]

growth = (
    (forecast_2030 / imports_2025) - 1
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Brazilian Imports (2025, USD mn)",
        f"{imports_2025:,.0f}"
    )

with col2:
    st.metric(
        "Projected Imports (2030, USD mn)",
        f"{forecast_2030:,.0f}"
    )

with col3:

    if growth >= 0:
        growth_color = "green"
    else:
        growth_color = "red"

    st.markdown(
        f"""
        <div style='
            padding:10px;
            border:1px solid #d9d9d9;
            border-radius:5px;
        '>
        <strong>Projected Change (2025–2030, %)</strong><br>
        <span style='color:{growth_color}; font-size:24px;'>
        {growth:.1f}%
        </span>
        </div>
        """,
        unsafe_allow_html=True
    )

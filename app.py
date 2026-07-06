import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

    suppliers = pd.read_excel(
        "imports_brazil_2023_2025_countries_origin_clean.xlsx"
    )

    return consolidated, forecast, suppliers

consolidated, forecast, suppliers = load_data()

header_left, header_right = st.columns(
    [5, 1]
)

with header_left:

    st.markdown(
        """
        <h1 style="
            color:#002f87;
            font-size:28px;
            font-family: Arial;
            margin-bottom:0px;
        ">
        Brazil Imports Intelligence Dashboard – Trade, Tariffs and Forecasts
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color:gray;
            margin-top:0px;
        ">
        Product-level insights on Brazilian imports, including trade structure and 5-year forecasts
        </p>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.image(
    "team_finland_4.png",
    width=140
)

# -----------------------
# NCM selector
# -----------------------
st.markdown(
    """
    <hr style="
        margin-top:5px;
        margin-bottom:15px;
    ">
    """,
    unsafe_allow_html=True
)

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

sup = suppliers[
    suppliers["NCM Code"].astype(str)
    == str(selected_code)
]

if len(sup) == 0:
    st.warning(
        "No supplier information available for this product."
    )

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

col_left, col_center, col_right = st.columns(
    [1.2, 1.6, 1.2]
)

# ====================================
# LEFT COLUMN
# ====================================

with col_left:

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

    st.metric(
        "Brazilian Imports (2025, USD mn)",
        f"{imports_2025:,.0f}"
    )

    st.metric(
        "Projected Imports (2030, USD mn)",
        f"{forecast_2030:,.0f}"
    )

    st.metric(
        "Projected Change (2025–2030, %)",
        f"{growth:.1f}%"
    )

# ====================================
# CENTER COLUMN
# ====================================

with col_center:

    st.subheader(
        "Brazil Imports: Historical Trends and Outlook (1997–2030)"
    )

    historical = fc[
        fc["Type"] == "Historical"
    ]

    forecast_only = fc[
        fc["Type"] == "Forecast"
    ].copy()

    bridge_row = historical.tail(1).copy()

    bridge_row["Forecast"] = bridge_row["imports_usd_2025"]

    forecast_data = pd.concat(
        [bridge_row, forecast_only],
        ignore_index=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical["Year"],
            y=historical["imports_usd_2025"],
            mode="lines",
            name="Historical",
            line=dict(
                color="#1f77b4",
                width=3
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_data["Year"],
            y=forecast_data["Forecast"],
            mode="lines",
            name="Forecast",
            line=dict(
                color="#1f77b4",
                width=3,
                dash="dash"
            )
        )
    )

    fig.add_vline(
        x=2025,
        line_width=1,
        line_dash="dot",
        line_color="gray"
    )

    fig.update_layout(
        height=350,
        xaxis_title="Year",
        yaxis_title="USD mn",
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================
# RIGHT COLUMN
# ====================================

with col_right:

    st.subheader(
        "Top 5 Suppliers to Brazil (Average 2023–2025)"
    )

    top5 = (
        sup.sort_values(
            "average 2023-2025",
            ascending=False
        )
        .head(5)
    )

    suppliers_display = top5[
        ["Country", "average 2023-2025"]
    ].copy()

    suppliers_display.columns = [
        "Country",
        "Average imports (USD mn)"
    ]

    suppliers_display[
        "Average imports (USD mn)"
    ] = suppliers_display[
        "Average imports (USD mn)"
    ].round(1)

    st.dataframe(
        suppliers_display,
        hide_index=True,
        use_container_width=True
    )

    st.markdown(
        f"**Sum of Top Suppliers:** {top5['average 2023-2025'].sum():,.1f}"
    )

    st.subheader(
        "Global Supply Distribution (Average Imports, 2023–2025)"
    )

    map_data = sup.copy()

    fig_map = px.choropleth(

        map_data,

        locations="Country",

        locationmode="country names",

        color="average 2023-2025",

        hover_name="Country",

        color_continuous_scale="Blues"

    )

    fig_map.update_geos(
        showcountries=True,
        showcoastlines=True,
        showframe=False,
        projection_type="natural earth"
    )

    fig_map.update_layout(
        height=350,
        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------
# Page configuration and styling
# ------------------------------------------------------------
st.set_page_config(
    page_title="Global Space Missions | Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1500px; padding-top: 1.25rem; padding-bottom: 3rem;}
    .hero {
        padding: 1.4rem 1.6rem; border-radius: 18px;
        border: 1px solid rgba(128,145,170,.24);
        background: linear-gradient(110deg, rgba(42,105,155,.15), rgba(32,166,125,.08));
        margin-bottom: 1.2rem;
    }
    .eyebrow {font-size:.74rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:#24a77c;}
    .hero h1 {font-size:clamp(1.9rem,3vw,2.8rem); line-height:1.15; margin:.25rem 0;}
    .hero p {font-size:1rem; opacity:.78; margin:.45rem 0 0;}
    [data-testid="stMetric"] {
        border:1px solid rgba(128,145,170,.23); border-radius:14px;
        padding:14px 16px; background:rgba(128,145,170,.07); min-height:108px;
    }
    [data-testid="stPlotlyChart"] {border:1px solid rgba(128,145,170,.16); border-radius:13px; padding:5px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Dataset loading. Supports the repository layout and a flat
# layout where the CSV is beside this app.py file.
# ------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DATA_CANDIDATES = [
    PROJECT_DIR / "data" / "Global_Space_Exploration_Dataset.csv",
    APP_DIR / "Global_Space_Exploration_Dataset.csv",
    PROJECT_DIR / "Global_Space_Exploration_Dataset.csv",
    PROJECT_DIR / "data" / "Global_Space_Exploration_Dataset.CSV",
    APP_DIR / "Global_Space_Exploration_Dataset.CSV",
]
DATA_PATH = next((p for p in DATA_CANDIDATES if p.is_file()), None)

REQUIRED = [
    "Country", "Year", "Mission Name", "Mission Type", "Launch Site",
    "Satellite Type", "Budget (in Billion $)", "Success Rate (%)",
    "Technology Used", "Environmental Impact", "Collaborating Countries",
    "Duration (in Days)",
]
NUMERIC = ["Year", "Budget (in Billion $)", "Success Rate (%)", "Duration (in Days)"]
IMPACT_ORDER = ["Low", "Medium", "High"]
IMPACT_COLORS = {"Low": "#22A77B", "Medium": "#E5A43B", "High": "#D95D5D"}

@st.cache_data(show_spinner="Loading mission dataset...")
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    for col in NUMERIC:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

if DATA_PATH is None:
    st.error(
        "Dataset not found. Expected `data/Global_Space_Exploration_Dataset.csv`. "
        "Check that the `data` folder and CSV filename match this spelling."
    )
    st.stop()

df = load_data(str(DATA_PATH))
missing = [col for col in REQUIRED if col not in df.columns]
if missing:
    st.error("Dataset is missing required columns: " + ", ".join(missing))
    st.stop()
df = df.dropna(subset=["Year"]).copy()
if df.empty:
    st.error("No valid mission years were found in the dataset.")
    st.stop()

def draw(fig, height=360):
    fig.update_layout(
        height=height, autosize=True,
        margin=dict(l=25, r=25, t=35, b=40),
        font=dict(size=12), legend_title_text="",
    )
    st.plotly_chart(
        fig, use_container_width=True,
        config={"responsive": True, "displaylogo": False, "displayModeBar": False},
    )

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Introduction to Data Science · Interactive Explorer</div>
      <h1>🚀 Global Space Missions</h1>
      <p>Explore mission activity, budgets, success rates, technologies, launch sites,
      and environmental-impact categories in the supplied dataset.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
st.sidebar.title("Mission filters")
st.sidebar.caption("All charts and tables respond to these filters.")

year_min, year_max = int(df.Year.min()), int(df.Year.max())
if year_min == year_max:
    year_range = (year_min, year_max)
else:
    year_range = st.sidebar.slider(
        "Mission year", year_min, year_max, (year_min, year_max), step=1
    )

def options_for(column):
    return sorted(df[column].dropna().astype(str).unique().tolist())

countries = st.sidebar.multiselect("Country", options_for("Country"))
mission_types = st.sidebar.multiselect("Mission type", options_for("Mission Type"))
satellites = st.sidebar.multiselect("Satellite type", options_for("Satellite Type"))
impacts_available = [v for v in IMPACT_ORDER if v in options_for("Environmental Impact")]
impacts = st.sidebar.multiselect("Environmental impact", impacts_available)

filtered = df[df.Year.between(*year_range)].copy()
if countries:
    filtered = filtered[filtered.Country.isin(countries)]
if mission_types:
    filtered = filtered[filtered["Mission Type"].isin(mission_types)]
if satellites:
    filtered = filtered[filtered["Satellite Type"].isin(satellites)]
if impacts:
    filtered = filtered[filtered["Environmental Impact"].isin(impacts)]

if filtered.empty:
    st.warning("No records match these filters. Clear or change a filter.")
    st.stop()

# ------------------------------------------------------------
# KPI summary
# ------------------------------------------------------------
avg_success = filtered["Success Rate (%)"].mean()
avg_budget = filtered["Budget (in Billion $)"].mean()
high_share = filtered["Environmental Impact"].eq("High").mean() * 100
kpis = st.columns(5)
kpis[0].metric("Missions", f"{len(filtered):,}")
kpis[1].metric("Countries", f"{filtered.Country.nunique():,}")
kpis[2].metric("Average success rate", f"{avg_success:.1f}%" if pd.notna(avg_success) else "N/A")
kpis[3].metric("Average budget", f"${avg_budget:.2f}B" if pd.notna(avg_budget) else "N/A")
kpis[4].metric("High-impact label share", f"{high_share:.1f}%")
st.caption(f"Showing {len(filtered):,} of {len(df):,} records · {year_range[0]}–{year_range[1]}")

# ------------------------------------------------------------
# Dashboard tabs
# ------------------------------------------------------------
overview, geography, mission, records = st.tabs(
    ["📊 Overview", "🌍 Countries & Technology", "🛰 Mission Analysis", "📋 Data Explorer"]
)

with overview:
    st.subheader("Mission activity and impact profile")
    left, right = st.columns([1, 1.35], gap="large")
    with left:
        counts = (
            filtered["Environmental Impact"].value_counts()
            .reindex(IMPACT_ORDER, fill_value=0)
            .rename_axis("Impact category").reset_index(name="Missions")
        )
        counts = counts[counts.Missions > 0]
        fig = px.pie(
            counts, names="Impact category", values="Missions", hole=.58,
            color="Impact category", color_discrete_map=IMPACT_COLORS,
        )
        fig.update_traces(textposition="inside", textinfo="label+percent")
        draw(fig)
        st.caption("Share of the existing impact labels in the filtered data.")
    with right:
        annual = (
            filtered.groupby(["Year", "Environmental Impact"])
            .size().reset_index(name="Missions")
        )
        fig = px.line(
            annual, x="Year", y="Missions", color="Environmental Impact",
            markers=True, category_orders={"Environmental Impact": IMPACT_ORDER},
            color_discrete_map=IMPACT_COLORS,
        )
        fig.update_layout(xaxis_title="Year", yaxis_title="Missions", hovermode="x unified")
        draw(fig)
        st.caption("Annual mission counts grouped by the dataset's impact labels.")

    left, right = st.columns(2, gap="large")
    with left:
        mix = filtered.groupby(["Mission Type", "Environmental Impact"]).size().reset_index(name="Missions")
        fig = px.bar(
            mix, x="Mission Type", y="Missions", color="Environmental Impact",
            barmode="stack", category_orders={"Environmental Impact": IMPACT_ORDER},
            color_discrete_map=IMPACT_COLORS,
        )
        fig.update_layout(xaxis_title="", yaxis_title="Missions")
        draw(fig)
        st.caption("Mission types split by impact category.")
    with right:
        top = filtered.Country.value_counts().head(10).sort_values().rename_axis("Country").reset_index(name="Missions")
        fig = px.bar(top, x="Missions", y="Country", orientation="h", text="Missions")
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(xaxis_title="Number of missions", yaxis_title="", margin=dict(l=25, r=45, t=30, b=35))
        draw(fig)
        st.caption("Ten countries with the most missions in the current selection.")

with geography:
    st.subheader("Country participation and mission infrastructure")
    left, right = st.columns(2, gap="large")
    with left:
        top_countries = filtered.Country.value_counts().head(10).index
        country_mix = filtered[filtered.Country.isin(top_countries)].groupby(
            ["Country", "Environmental Impact"]
        ).size().reset_index(name="Missions")
        fig = px.bar(
            country_mix, x="Country", y="Missions", color="Environmental Impact",
            barmode="group", category_orders={"Environmental Impact": IMPACT_ORDER},
            color_discrete_map=IMPACT_COLORS,
        )
        fig.update_layout(xaxis_title="", yaxis_title="Missions")
        fig.update_xaxes(tickangle=-25)
        draw(fig, 390)
    with right:
        tech = filtered["Technology Used"].value_counts().sort_values().rename_axis("Technology").reset_index(name="Missions")
        fig = px.bar(tech, x="Missions", y="Technology", orientation="h", text="Missions")
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(xaxis_title="Missions", yaxis_title="", margin=dict(l=30, r=45, t=30, b=35))
        draw(fig, 390)

    left, right = st.columns(2, gap="large")
    with left:
        sites = filtered["Launch Site"].value_counts().head(10).sort_values().rename_axis("Launch site").reset_index(name="Missions")
        fig = px.bar(sites, x="Missions", y="Launch site", orientation="h", text="Missions")
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(xaxis_title="Missions", yaxis_title="", margin=dict(l=30, r=45, t=30, b=35))
        draw(fig, 390)
    with right:
        satellite_counts = filtered["Satellite Type"].value_counts().rename_axis("Satellite type").reset_index(name="Missions")
        fig = px.pie(satellite_counts, names="Satellite type", values="Missions", hole=.48)
        fig.update_traces(textposition="inside", textinfo="label+percent")
        draw(fig, 390)

with mission:
    st.subheader("Budget, success rate and duration")
    left, right = st.columns(2, gap="large")
    with left:
        scatter_data = filtered.dropna(subset=["Budget (in Billion $)", "Success Rate (%)"])
        fig = px.scatter(
            scatter_data, x="Budget (in Billion $)", y="Success Rate (%)",
            color="Environmental Impact", color_discrete_map=IMPACT_COLORS,
            hover_name="Mission Name", hover_data=["Country", "Year", "Mission Type"],
            opacity=.72,
        )
        fig.update_layout(xaxis_title="Budget (in billion $)", yaxis_title="Success rate (%)")
        draw(fig, 390)
        st.caption("Each point represents a mission. Association does not establish causation.")
    with right:
        success = filtered.groupby("Mission Type", as_index=False)["Success Rate (%)"].mean().sort_values("Success Rate (%)")
        fig = px.bar(success, x="Success Rate (%)", y="Mission Type", orientation="h", text_auto=".1f")
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(xaxis_title="Average success rate (%)", yaxis_title="", margin=dict(l=30, r=45, t=30, b=35))
        draw(fig, 390)

    left, right = st.columns(2, gap="large")
    with left:
        fig = px.box(
            filtered.dropna(subset=["Budget (in Billion $)", "Environmental Impact"]),
            x="Environmental Impact", y="Budget (in Billion $)",
            color="Environmental Impact", category_orders={"Environmental Impact": IMPACT_ORDER},
            color_discrete_map=IMPACT_COLORS, points="outliers",
        )
        fig.update_layout(xaxis_title="Impact label", yaxis_title="Budget (in billion $)", showlegend=False)
        draw(fig)
    with right:
        fig = px.box(
            filtered.dropna(subset=["Duration (in Days)", "Mission Type"]),
            x="Mission Type", y="Duration (in Days)", color="Mission Type", points="outliers",
        )
        fig.update_layout(xaxis_title="Mission type", yaxis_title="Duration (days)", showlegend=False)
        draw(fig)

with records:
    st.subheader("Search and inspect mission records")
    query = st.text_input(
        "Search mission name, country, launch site or technology",
        placeholder="Enter a keyword...",
    )
    table = filtered.copy()
    if query.strip():
        searchable = ["Mission Name", "Country", "Launch Site", "Technology Used", "Mission Type", "Satellite Type"]
        mask = pd.Series(False, index=table.index)
        for col in searchable:
            mask |= table[col].astype("string").str.contains(query.strip(), case=False, na=False, regex=False)
        table = table[mask]

    st.caption(f"{len(table):,} matching records")
    display_cols = [
        "Year", "Country", "Mission Name", "Mission Type", "Launch Site",
        "Satellite Type", "Budget (in Billion $)", "Success Rate (%)",
        "Environmental Impact", "Technology Used", "Duration (in Days)",
    ]
    st.dataframe(
        table[display_cols].sort_values("Year", ascending=False),
        use_container_width=True, hide_index=True, height=520,
    )
    st.download_button(
        "⬇ Download filtered records (CSV)",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="filtered_space_missions.csv",
        mime="text/csv",
    )
    with st.expander("Dataset quality summary"):
        q1, q2, q3 = st.columns(3)
        q1.metric("Rows", f"{len(df):,}")
        q2.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
        q3.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")
        quality = pd.DataFrame({
            "Column": df.columns,
            "Data type": [str(t) for t in df.dtypes],
            "Missing values": [int(df[c].isna().sum()) for c in df.columns],
            "Unique values": [int(df[c].nunique()) for c in df.columns],
        })
        st.dataframe(quality, use_container_width=True, hide_index=True)

with st.expander("Data interpretation and model limitations"):
    st.markdown(
        """
        - `Environmental Impact` is an existing categorical label in this dataset, not a measured emissions quantity.
        - The high-impact share is the percentage of selected records labelled `High`.
        - Charts describe patterns in this dataset; they do not establish cause and effect.
        - The companion notebook reports 35.50% held-out accuracy for its best tested classifier (Logistic Regression).
          This is weak performance and should not be used for operational, scientific, or policy decisions.
        """
    )

st.divider()
st.caption("Global Space Missions · Introduction to Data Science Project")

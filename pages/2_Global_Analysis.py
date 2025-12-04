import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ─────────────────────────────────────────────────────────────────────────────
# Country to Continent Mapping
# ─────────────────────────────────────────────────────────────────────────────
COUNTRY_TO_CONTINENT = {
    # Europe
    "Albania": "Europe", "Andorra": "Europe", "Armenia": "Europe", "Austria": "Europe",
    "Azerbaijan": "Europe", "Belarus": "Europe", "Belgium": "Europe", "Bosnia and Herzegovina": "Europe",
    "Bulgaria": "Europe", "Croatia": "Europe", "Cyprus": "Europe", "Czechia": "Europe",
    "Denmark": "Europe", "Estonia": "Europe", "Finland": "Europe", "France": "Europe",
    "Georgia": "Europe", "Germany": "Europe", "Greece": "Europe", "Hungary": "Europe",
    "Iceland": "Europe", "Ireland": "Europe", "Italy": "Europe", "Kosovo": "Europe",
    "Latvia": "Europe", "Liechtenstein": "Europe", "Lithuania": "Europe", "Luxembourg": "Europe",
    "Malta": "Europe", "Republic of Moldova": "Europe", "Monaco": "Europe", "Montenegro": "Europe",
    "Netherlands": "Europe", "North Macedonia": "Europe", "Norway": "Europe", "Poland": "Europe",
    "Portugal": "Europe", "Romania": "Europe", "San Marino": "Europe", "Serbia": "Europe",
    "Slovakia": "Europe", "Slovenia": "Europe", "Spain": "Europe", "Sweden": "Europe",
    "Switzerland": "Europe", "Ukraine": "Europe", "Great Britain": "Europe",
    "Türkiye": "Europe", "Russian Federation": "Europe",
    
    # Asia
    "Afghanistan": "Asia", "Bahrain": "Asia", "Bangladesh": "Asia", "Bhutan": "Asia",
    "Brunei Darussalam": "Asia", "Cambodia": "Asia", "China": "Asia", 
    "People's Republic of China": "Asia", "Hong Kong, China": "Asia", "India": "Asia",
    "Indonesia": "Asia", "Islamic Republic of Iran": "Asia", "IR Iran": "Asia",
    "Iraq": "Asia", "Israel": "Asia", "Japan": "Asia", "Jordan": "Asia",
    "Kazakhstan": "Asia", "Republic of Korea": "Asia", "Korea": "Asia",
    "Democratic People's Republic of Korea": "Asia", "DPR Korea": "Asia",
    "Kuwait": "Asia", "Kyrgyzstan": "Asia", "Lao People's Democratic Republic": "Asia",
    "Lebanon": "Asia", "Malaysia": "Asia", "Maldives": "Asia", "Mongolia": "Asia",
    "Myanmar": "Asia", "Nepal": "Asia", "Oman": "Asia", "Pakistan": "Asia",
    "Palestine": "Asia", "Philippines": "Asia", "Qatar": "Asia", "Saudi Arabia": "Asia",
    "Singapore": "Asia", "Sri Lanka": "Asia", "Syrian Arab Republic": "Asia",
    "Chinese Taipei": "Asia", "Tajikistan": "Asia", "Thailand": "Asia",
    "Democratic Republic of Timor-Leste": "Asia", "Timor-Leste": "Asia",
    "Turkmenistan": "Asia", "United Arab Emirates": "Asia", "Uzbekistan": "Asia",
    "Vietnam": "Asia", "Yemen": "Asia",
    
    # Africa
    "Algeria": "Africa", "Angola": "Africa", "Benin": "Africa", "Botswana": "Africa",
    "Burkina Faso": "Africa", "Burundi": "Africa", "Cabo Verde": "Africa",
    "Cameroon": "Africa", "Central African Republic": "Africa", "Chad": "Africa",
    "Comoros": "Africa", "Congo": "Africa", "Democratic Republic of the Congo": "Africa",
    "Côte d'Ivoire": "Africa", "Djibouti": "Africa", "Egypt": "Africa",
    "Equatorial Guinea": "Africa", "Eritrea": "Africa", "Eswatini": "Africa",
    "Ethiopia": "Africa", "Gabon": "Africa", "Gambia": "Africa", "Ghana": "Africa",
    "Guinea": "Africa", "Guinea-Bissau": "Africa", "Kenya": "Africa", "Lesotho": "Africa",
    "Liberia": "Africa", "Libya": "Africa", "Madagascar": "Africa", "Malawi": "Africa",
    "Mali": "Africa", "Mauritania": "Africa", "Mauritius": "Africa", "Morocco": "Africa",
    "Mozambique": "Africa", "Namibia": "Africa", "Niger": "Africa", "Nigeria": "Africa",
    "Rwanda": "Africa", "Sao Tome and Principe": "Africa", "Senegal": "Africa",
    "Seychelles": "Africa", "Sierra Leone": "Africa", "Somalia": "Africa",
    "South Africa": "Africa", "South Sudan": "Africa", "Sudan": "Africa",
    "United Republic of Tanzania": "Africa", "Tanzania": "Africa", "Togo": "Africa",
    "Tunisia": "Africa", "Uganda": "Africa", "Zambia": "Africa", "Zimbabwe": "Africa",
    
    # North America
    "Antigua and Barbuda": "North America", "Bahamas": "North America", "Barbados": "North America",
    "Belize": "North America", "Canada": "North America", "Costa Rica": "North America",
    "Cuba": "North America", "Dominica": "North America", "Dominican Republic": "North America",
    "El Salvador": "North America", "Grenada": "North America", "Guatemala": "North America",
    "Haiti": "North America", "Honduras": "North America", "Jamaica": "North America",
    "Mexico": "North America", "Nicaragua": "North America", "Panama": "North America",
    "Saint Kitts and Nevis": "North America", "Saint Lucia": "North America",
    "St Vincent and the Grenadines": "North America", "Trinidad and Tobago": "North America",
    "United States": "North America", "United States of America": "North America",
    "Puerto Rico": "North America", "Virgin Islands, US": "North America",
    "Virgin Islands, British": "North America", "Cayman Islands": "North America",
    "Aruba": "North America", "Bermuda": "North America", "Guam": "North America",
    
    # South America
    "Argentina": "South America", "Bolivia": "South America", "Brazil": "South America",
    "Chile": "South America", "Colombia": "South America", "Ecuador": "South America",
    "Guyana": "South America", "Paraguay": "South America", "Peru": "South America",
    "Suriname": "South America", "Uruguay": "South America", "Venezuela": "South America",
    
    # Oceania
    "Australia": "Oceania", "Fiji": "Oceania", "Kiribati": "Oceania",
    "Federated States of Micronesia": "Oceania", "Marshall Islands": "Oceania",
    "Nauru": "Oceania", "New Zealand": "Oceania", "Palau": "Oceania",
    "Papua New Guinea": "Oceania", "Samoa": "Oceania", "Solomon Islands": "Oceania",
    "Tonga": "Oceania", "Tuvalu": "Oceania", "Vanuatu": "Oceania", "Cook Islands": "Oceania",
    "American Samoa": "Oceania",
    
    # Special cases
    "AIN": "Europe",  # Individual Neutral Athletes (mostly from Russia)
    "Refugee Olympic Team": "Other", "EOR": "Other",
}

# NOC code to ISO code mapping for choropleth
NOC_TO_ISO = {
    "USA": "USA", "CHN": "CHN", "JPN": "JPN", "AUS": "AUS", "FRA": "FRA",
    "NED": "NLD", "GBR": "GBR", "KOR": "KOR", "ITA": "ITA", "GER": "DEU",
    "NZL": "NZL", "CAN": "CAN", "UZB": "UZB", "HUN": "HUN", "ESP": "ESP",
    "SWE": "SWE", "KEN": "KEN", "NOR": "NOR", "IRL": "IRL", "BRA": "BRA",
    "IRI": "IRN", "UKR": "UKR", "ROU": "ROU", "GEO": "GEO", "BEL": "BEL",
    "BUL": "BGR", "SRB": "SRB", "CZE": "CZE", "DEN": "DNK", "AZE": "AZE",
    "CRO": "HRV", "CUB": "CUB", "BRN": "BHR", "SLO": "SVN", "TPE": "TWN",
    "AUT": "AUT", "HKG": "HKG", "PHI": "PHL", "ALG": "DZA", "INA": "IDN",
    "ISR": "ISR", "POL": "POL", "KAZ": "KAZ", "JAM": "JAM", "RSA": "ZAF",
    "THA": "THA", "ETH": "ETH", "SUI": "CHE", "ECU": "ECU", "POR": "PRT",
    "GRE": "GRC", "ARG": "ARG", "EGY": "EGY", "TUN": "TUN", "BOT": "BWA",
    "CHI": "CHL", "LCA": "LCA", "UGA": "UGA", "DOM": "DOM", "GUA": "GTM",
    "MAR": "MAR", "DMA": "DMA", "PAK": "PAK", "TUR": "TUR", "MEX": "MEX",
    "ARM": "ARM", "COL": "COL", "PRK": "PRK", "KGZ": "KGZ", "LTU": "LTU",
    "IND": "IND", "MDA": "MDA", "KOS": "XKX", "CYP": "CYP", "FIJ": "FJI",
    "JOR": "JOR", "MGL": "MNG", "PAN": "PAN", "TJK": "TJK", "ALB": "ALB",
    "GRN": "GRD", "MAS": "MYS", "PUR": "PRI", "CPV": "CPV", "CIV": "CIV",
    "PER": "PER", "QAT": "QAT", "SGP": "SGP", "SVK": "SVK", "ZAM": "ZMB",
}


# ─────────────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_nocs():
    return pd.read_csv("data/nocs.csv")


@st.cache_data
def load_events():
    return pd.read_csv("data/events.csv")


@st.cache_data
def load_medals_total():
    return pd.read_csv("data/medals_total.csv")


@st.cache_data
def load_medals():
    return pd.read_csv("data/medals.csv")


def get_continent(country):
    """Get continent for a country, handling various name formats."""
    if pd.isna(country):
        return "Other"
    
    # Direct lookup
    if country in COUNTRY_TO_CONTINENT:
        return COUNTRY_TO_CONTINENT[country]
    
    # Try partial matching for complex names
    for key, continent in COUNTRY_TO_CONTINENT.items():
        if key in country or country in key:
            return continent
    
    return "Other"


def add_continent_column(df, country_col="country"):
    """Add continent column to dataframe."""
    df = df.copy()
    df["Continent"] = df[country_col].apply(get_continent)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────────────────────────────────────
def create_sidebar_filters(nocs_df, events_df):
    st.sidebar.header("🎯 Filters")
    
    # Continent filter (Creative addition)
    continents = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]
    selected_continents = st.sidebar.multiselect(
        "🌍 Select Continents",
        options=continents,
        default=[],
        help="Filter by continent. Leave empty to show all."
    )
    
    # Country filter
    countries = sorted(nocs_df["country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "🏳️ Select Countries",
        options=countries,
        default=[],
        help="Filter by country. Leave empty to show all."
    )
    
    # Sport filter
    sports = sorted(events_df["sport"].dropna().unique().tolist())
    selected_sports = st.sidebar.multiselect(
        "🏅 Select Sports",
        options=sports,
        default=[],
        help="Filter by sport. Leave empty to show all."
    )
    
    # Medal type filter
    st.sidebar.subheader("🥇 Medal Types")
    show_gold = st.sidebar.checkbox("Gold Medal", value=True)
    show_silver = st.sidebar.checkbox("Silver Medal", value=True)
    show_bronze = st.sidebar.checkbox("Bronze Medal", value=True)
    
    medal_types = []
    if show_gold:
        medal_types.append("Gold Medal")
    if show_silver:
        medal_types.append("Silver Medal")
    if show_bronze:
        medal_types.append("Bronze Medal")
    
    return selected_continents, selected_countries, selected_sports, medal_types


# ─────────────────────────────────────────────────────────────────────────────
# Filter Functions
# ─────────────────────────────────────────────────────────────────────────────
def filter_medals(df, selected_continents, selected_countries, selected_sports, medal_types):
    filtered = df.copy()
    
    # Add continent if not present
    if "Continent" not in filtered.columns:
        filtered = add_continent_column(filtered)
    
    if selected_continents:
        filtered = filtered[filtered["Continent"].isin(selected_continents)]
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    if selected_sports:
        filtered = filtered[filtered["discipline"].isin(selected_sports)]
    
    if medal_types:
        filtered = filtered[filtered["medal_type"].isin(medal_types)]
    
    return filtered


def filter_medals_total(df, selected_continents, selected_countries):
    filtered = df.copy()
    
    # Add continent if not present
    if "Continent" not in filtered.columns:
        filtered = add_continent_column(filtered)
    
    if selected_continents:
        filtered = filtered[filtered["Continent"].isin(selected_continents)]
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# World Medal Map (Choropleth)
# ─────────────────────────────────────────────────────────────────────────────
def create_world_medal_map(medals_total_df):
    df = medals_total_df.copy()
    
    # Map NOC codes to ISO codes
    df["iso_code"] = df["country_code"].map(NOC_TO_ISO)
    
    # Filter out entries without valid ISO codes
    df = df[df["iso_code"].notna()]
    
    fig = px.choropleth(
        df,
        locations="iso_code",
        color="Total",
        hover_name="country",
        hover_data={
            "iso_code": False,
            "Gold Medal": True,
            "Silver Medal": True,
            "Bronze Medal": True,
            "Total": True
        },
        color_continuous_scale=[
            [0, "#f7fbff"],
            [0.2, "#c6dbef"],
            [0.4, "#6baed6"],
            [0.6, "#2171b5"],
            [0.8, "#08519c"],
            [1, "#08306b"]
        ],
        title="🌍 World Medal Map"
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#888",
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)"
        ),
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        height=500,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(
            title="Total Medals",
            tickformat="d"
        )
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Medal Hierarchy Sunburst
# ─────────────────────────────────────────────────────────────────────────────
def create_medal_sunburst(medals_df):
    # Add continent column
    df = add_continent_column(medals_df.copy())
    
    # Aggregate by Continent -> Country -> Sport
    hierarchy_data = df.groupby(
        ["Continent", "country", "discipline"]
    ).size().reset_index(name="Medal Count")
    
    # Filter out "Other" continent
    hierarchy_data = hierarchy_data[hierarchy_data["Continent"] != "Other"]
    
    fig = px.sunburst(
        hierarchy_data,
        path=["Continent", "country", "discipline"],
        values="Medal Count",
        color="Continent",
        color_discrete_map={
            "Europe": "#0055A4",
            "Asia": "#EF4135",
            "Africa": "#FFD700",
            "North America": "#28a745",
            "South America": "#6f42c1",
            "Oceania": "#17a2b8"
        },
        title="🌐 Medal Hierarchy: Continent → Country → Sport (Sunburst)"
    )
    
    fig.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        height=550,
        margin=dict(t=50, b=20)
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        insidetextorientation="radial"
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Medal Hierarchy Treemap
# ─────────────────────────────────────────────────────────────────────────────
def create_medal_treemap(medals_df):
    # Add continent column
    df = add_continent_column(medals_df.copy())
    
    # Aggregate by Continent -> Country -> Sport
    hierarchy_data = df.groupby(
        ["Continent", "country", "discipline"]
    ).size().reset_index(name="Medal Count")
    
    # Filter out "Other" continent
    hierarchy_data = hierarchy_data[hierarchy_data["Continent"] != "Other"]
    
    fig = px.treemap(
        hierarchy_data,
        path=[px.Constant("World"), "Continent", "country", "discipline"],
        values="Medal Count",
        color="Continent",
        color_discrete_map={
            "Europe": "#0055A4",
            "Asia": "#EF4135",
            "Africa": "#FFD700",
            "North America": "#28a745",
            "South America": "#6f42c1",
            "Oceania": "#17a2b8"
        },
        title="🗺️ Medal Hierarchy: Continent → Country → Sport (Treemap)"
    )
    
    fig.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        height=550,
        margin=dict(t=50, b=20)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Continent vs Medals Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_continent_medals_chart(medals_total_df):
    df = add_continent_column(medals_total_df.copy())
    
    # Aggregate by continent
    continent_medals = df.groupby("Continent").agg({
        "Gold Medal": "sum",
        "Silver Medal": "sum",
        "Bronze Medal": "sum",
        "Total": "sum"
    }).reset_index()
    
    # Filter out "Other" and sort by total
    continent_medals = continent_medals[continent_medals["Continent"] != "Other"]
    continent_medals = continent_medals.sort_values("Total", ascending=False)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Gold",
        x=continent_medals["Continent"],
        y=continent_medals["Gold Medal"],
        marker_color="#FFD700",
        hovertemplate="<b>%{x}</b><br>Gold: %{y}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        name="Silver",
        x=continent_medals["Continent"],
        y=continent_medals["Silver Medal"],
        marker_color="#C0C0C0",
        hovertemplate="<b>%{x}</b><br>Silver: %{y}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        name="Bronze",
        x=continent_medals["Continent"],
        y=continent_medals["Bronze Medal"],
        marker_color="#CD7F32",
        hovertemplate="<b>%{x}</b><br>Bronze: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": "🌍 Medals by Continent",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        barmode="group",
        xaxis_title="Continent",
        yaxis_title="Medal Count",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=450
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Country vs Medals Bar Chart (Top 20)
# ─────────────────────────────────────────────────────────────────────────────
def create_country_medals_chart(medals_total_df, top_n=20):
    # Get top N countries by total medals
    df = medals_total_df.nlargest(top_n, "Total").copy()
    
    # Sort for display (ascending so highest is at top in horizontal bar)
    df = df.sort_values("Total", ascending=True)
    
    # Create grouped horizontal bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Bronze",
        y=df["country"],
        x=df["Bronze Medal"],
        orientation="h",
        marker_color="#CD7F32",
        hovertemplate="<b>%{y}</b><br>Bronze: %{x}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        name="Silver",
        y=df["country"],
        x=df["Silver Medal"],
        orientation="h",
        marker_color="#C0C0C0",
        hovertemplate="<b>%{y}</b><br>Silver: %{x}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        name="Gold",
        y=df["country"],
        x=df["Gold Medal"],
        orientation="h",
        marker_color="#FFD700",
        hovertemplate="<b>%{y}</b><br>Gold: %{x}<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": f"🏆 Top {top_n} Countries by Medal Count",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        barmode="stack",
        xaxis_title="Total Medals",
        yaxis_title="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=600,
        margin=dict(l=150)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Global Analysis - Paris 2024",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E3A5F;
            text-align: center;
            padding: 1rem 0;
        }
        .sub-title {
            font-size: 1.1rem;
            color: #555;
            text-align: center;
            padding-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-title">🗺️ Global Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Analyze medal distribution from geographical and continental perspectives. '
        'Explore hierarchical views and compare performance across regions.</p>',
        unsafe_allow_html=True
    )
    
    # Load data
    nocs_df = load_nocs()
    events_df = load_events()
    medals_total_df = load_medals_total()
    medals_df = load_medals()
    
    # Create sidebar filters
    selected_continents, selected_countries, selected_sports, medal_types = create_sidebar_filters(
        nocs_df, events_df
    )
    
    # Apply filters
    filtered_medals = filter_medals(medals_df, selected_continents, selected_countries, selected_sports, medal_types)
    filtered_medals_total = filter_medals_total(medals_total_df, selected_continents, selected_countries)
    
    # Show active filters
    if selected_continents or selected_countries or selected_sports:
        with st.expander("📌 Active Filters", expanded=False):
            if selected_continents:
                st.write(f"**Continents:** {', '.join(selected_continents)}")
            if selected_countries:
                st.write(f"**Countries:** {', '.join(selected_countries)}")
            if selected_sports:
                st.write(f"**Sports:** {', '.join(selected_sports)}")
    
    st.markdown("---")
    
    # 1. World Medal Map
    st.subheader("🌍 World Medal Map")
    if len(filtered_medals_total) > 0:
        world_map = create_world_medal_map(filtered_medals_total)
        st.plotly_chart(world_map, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")
    
    st.markdown("---")
    
    # 2. Medal Hierarchy (Sunburst and Treemap)
    st.subheader("🌐 Medal Hierarchy by Continent")
    st.markdown("*Explore the hierarchy: Continent → Country → Sport → Medal Count*")
    
    tab1, tab2 = st.tabs(["☀️ Sunburst View", "🗺️ Treemap View"])
    
    with tab1:
        if len(filtered_medals) > 0:
            sunburst = create_medal_sunburst(filtered_medals)
            st.plotly_chart(sunburst, use_container_width=True)
        else:
            st.warning("No data available for sunburst chart.")
    
    with tab2:
        if len(filtered_medals) > 0:
            treemap = create_medal_treemap(filtered_medals)
            st.plotly_chart(treemap, use_container_width=True)
        else:
            st.warning("No data available for treemap chart.")
    
    st.markdown("---")
    
    # 3. Continent vs Medals & Country vs Medals
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Continent Performance")
        if len(filtered_medals_total) > 0:
            continent_chart = create_continent_medals_chart(filtered_medals_total)
            st.plotly_chart(continent_chart, use_container_width=True)
        else:
            st.warning("No data available for continent chart.")
    
    with col2:
        st.subheader("🏆 Top 20 Countries")
        if len(filtered_medals_total) > 0:
            country_chart = create_country_medals_chart(filtered_medals_total)
            st.plotly_chart(country_chart, use_container_width=True)
        else:
            st.warning("No data available for country chart.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Data Source: Paris 2024 Olympic Games Dataset | "
        "Built with Streamlit & Plotly"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

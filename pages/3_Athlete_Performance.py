import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


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
}

# Country code to flag emoji mapping
COUNTRY_FLAGS = {
    "USA": "🇺🇸", "CHN": "🇨🇳", "JPN": "🇯🇵", "AUS": "🇦🇺", "FRA": "🇫🇷",
    "NED": "🇳🇱", "GBR": "🇬🇧", "KOR": "🇰🇷", "ITA": "🇮🇹", "GER": "🇩🇪",
    "NZL": "🇳🇿", "CAN": "🇨🇦", "UZB": "🇺🇿", "HUN": "🇭🇺", "ESP": "🇪🇸",
    "SWE": "🇸🇪", "KEN": "🇰🇪", "NOR": "🇳🇴", "IRL": "🇮🇪", "BRA": "🇧🇷",
    "IRI": "🇮🇷", "UKR": "🇺🇦", "ROU": "🇷🇴", "GEO": "🇬🇪", "BEL": "🇧🇪",
    "BUL": "🇧🇬", "SRB": "🇷🇸", "CZE": "🇨🇿", "DEN": "🇩🇰", "AZE": "🇦🇿",
    "CRO": "🇭🇷", "CUB": "🇨🇺", "BRN": "🇧🇭", "SLO": "🇸🇮", "TPE": "🇹🇼",
    "AUT": "🇦🇹", "HKG": "🇭🇰", "PHI": "🇵🇭", "ALG": "🇩🇿", "INA": "🇮🇩",
    "ISR": "🇮🇱", "POL": "🇵🇱", "KAZ": "🇰🇿", "JAM": "🇯🇲", "RSA": "🇿🇦",
    "THA": "🇹🇭", "ETH": "🇪🇹", "SUI": "🇨🇭", "ECU": "🇪🇨", "POR": "🇵🇹",
    "GRE": "🇬🇷", "ARG": "🇦🇷", "EGY": "🇪🇬", "TUN": "🇹🇳", "ARM": "🇦🇲",
    "MEX": "🇲🇽", "COL": "🇨🇴", "IND": "🇮🇳", "TUR": "🇹🇷", "NGR": "🇳🇬",
    "MAR": "🇲🇦", "PAK": "🇵🇰", "DOM": "🇩🇴", "PER": "🇵🇪", "CHI": "🇨🇱",
}


# ─────────────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_athletes():
    df = pd.read_csv("data/athletes.csv")
    # Calculate age from birth_date
    df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
    # Age at Paris 2024 (July 2024)
    reference_date = datetime(2024, 7, 26)
    df["age"] = df["birth_date"].apply(
        lambda x: (reference_date - x).days // 365 if pd.notna(x) else None
    )
    return df


@st.cache_data
def load_nocs():
    return pd.read_csv("data/nocs.csv")


@st.cache_data
def load_events():
    return pd.read_csv("data/events.csv")


@st.cache_data
def load_medallists():
    return pd.read_csv("data/medallists.csv")


def get_continent(country):
    """Get continent for a country."""
    if pd.isna(country):
        return "Other"
    if country in COUNTRY_TO_CONTINENT:
        return COUNTRY_TO_CONTINENT[country]
    for key, continent in COUNTRY_TO_CONTINENT.items():
        if key in country or country in key:
            return continent
    return "Other"


def add_continent_column(df, country_col="country"):
    """Add continent column to dataframe."""
    df = df.copy()
    df["Continent"] = df[country_col].apply(get_continent)
    return df


def get_flag(country_code):
    """Get flag emoji for country code."""
    return COUNTRY_FLAGS.get(country_code, "🏳️")


def parse_disciplines(disciplines_str):
    """Parse disciplines from string format like ['Wrestling']."""
    if pd.isna(disciplines_str):
        return []
    try:
        # Remove brackets and quotes, split by comma
        cleaned = disciplines_str.strip("[]").replace("'", "").replace('"', "")
        return [d.strip() for d in cleaned.split(",") if d.strip()]
    except:
        return []


def get_primary_sport(disciplines_str):
    """Get the primary sport from disciplines."""
    disciplines = parse_disciplines(disciplines_str)
    return disciplines[0] if disciplines else "Unknown"


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────────────────────────────────────
def create_sidebar_filters(athletes_df, nocs_df, events_df):
    st.sidebar.header("🎯 Filters")
    
    # Continent filter
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
    
    # Gender filter
    st.sidebar.subheader("👤 Gender")
    show_male = st.sidebar.checkbox("Male", value=True)
    show_female = st.sidebar.checkbox("Female", value=True)
    
    genders = []
    if show_male:
        genders.append("Male")
    if show_female:
        genders.append("Female")
    
    return selected_continents, selected_countries, selected_sports, genders


# ─────────────────────────────────────────────────────────────────────────────
# Filter Functions
# ─────────────────────────────────────────────────────────────────────────────
def filter_athletes(df, selected_continents, selected_countries, selected_sports, genders):
    filtered = df.copy()
    
    # Add continent if not present
    if "Continent" not in filtered.columns:
        filtered = add_continent_column(filtered)
    
    if selected_continents:
        filtered = filtered[filtered["Continent"].isin(selected_continents)]
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    if selected_sports:
        filtered = filtered[filtered["disciplines"].apply(
            lambda x: any(sport in str(x) for sport in selected_sports)
        )]
    
    if genders:
        filtered = filtered[filtered["gender"].isin(genders)]
    
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# Athlete Profile Card
# ─────────────────────────────────────────────────────────────────────────────
def display_athlete_profile(athletes_df):
    st.subheader("👤 Athlete Profile Card")
    
    # Search/Select athlete
    athlete_names = sorted(athletes_df["name"].dropna().unique().tolist())
    
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        selected_athlete = st.selectbox(
            "🔍 Search and Select an Athlete",
            options=[""] + athlete_names,
            format_func=lambda x: "Type to search..." if x == "" else x
        )
    
    if selected_athlete:
        athlete = athletes_df[athletes_df["name"] == selected_athlete].iloc[0]
        
        # Create profile card
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            # Profile image placeholder with avatar
            st.markdown(
                f"""
                <div style="
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                ">
                    <span style="font-size: 60px; color: white;">
                        {"👨" if athlete["gender"] == "Male" else "👩"}
                    </span>
                </div>
                <p style="text-align: center; margin-top: 10px; font-weight: bold; font-size: 1.1rem;">
                    {get_flag(athlete["country_code"])} {athlete["country"]}
                </p>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(f"### {athlete['name']}")
            
            # Basic info
            st.markdown(f"**🏳️ Country:** {get_flag(athlete['country_code'])} {athlete['country']}")
            
            # Height and Weight
            height = athlete.get("height", 0)
            weight = athlete.get("weight", 0)
            height_str = f"{height:.0f} cm" if pd.notna(height) and height > 0 else "N/A"
            weight_str = f"{weight:.0f} kg" if pd.notna(weight) and weight > 0 else "N/A"
            st.markdown(f"**📏 Height:** {height_str}")
            st.markdown(f"**⚖️ Weight:** {weight_str}")
            
            # Age
            age = athlete.get("age")
            age_str = f"{int(age)} years" if pd.notna(age) else "N/A"
            st.markdown(f"**🎂 Age:** {age_str}")
        
        with col3:
            # Sports and Disciplines
            disciplines = parse_disciplines(athlete.get("disciplines", ""))
            sports_str = ", ".join(disciplines) if disciplines else "N/A"
            st.markdown(f"**🏅 Sport(s):** {sports_str}")
            
            # Events
            events = athlete.get("events", "")
            if pd.notna(events) and events:
                events_cleaned = events.strip("[]").replace("'", "").replace('"', "")
                events_list = [e.strip() for e in events_cleaned.split(",")][:3]  # Show max 3
                events_str = ", ".join(events_list)
                if len(events_cleaned.split(",")) > 3:
                    events_str += "..."
            else:
                events_str = "N/A"
            st.markdown(f"**🎯 Event(s):** {events_str}")
            
            # Coach
            coach = athlete.get("coach", "")
            if pd.notna(coach) and coach:
                # Clean up coach string (might be long)
                coach_clean = str(coach)[:100]
                if len(str(coach)) > 100:
                    coach_clean += "..."
            else:
                coach_clean = "N/A"
            st.markdown(f"**🎓 Coach:** {coach_clean}")
            
            # Birth place
            birth_place = athlete.get("birth_place", "")
            birth_country = athlete.get("birth_country", "")
            if pd.notna(birth_place) and birth_place:
                birthplace_str = f"{birth_place}"
                if pd.notna(birth_country) and birth_country:
                    birthplace_str += f", {birth_country}"
            else:
                birthplace_str = "N/A"
            st.markdown(f"**📍 Birthplace:** {birthplace_str}")
        
        st.markdown("---")
    else:
        st.info("👆 Select an athlete from the dropdown above to view their profile.")


# ─────────────────────────────────────────────────────────────────────────────
# Age Distribution Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_age_distribution_chart(athletes_df, by="gender"):
    # Filter out null ages
    df = athletes_df[athletes_df["age"].notna()].copy()
    
    if len(df) == 0:
        return None
    
    if by == "gender":
        fig = px.violin(
            df,
            x="gender",
            y="age",
            color="gender",
            box=True,
            points="outliers",
            color_discrete_map={"Male": "#0055A4", "Female": "#EF4135"},
            title="🎂 Age Distribution by Gender"
        )
    else:  # by sport
        # Get top 10 sports by athlete count
        df["primary_sport"] = df["disciplines"].apply(get_primary_sport)
        top_sports = df["primary_sport"].value_counts().head(10).index.tolist()
        df_filtered = df[df["primary_sport"].isin(top_sports)]
        
        fig = px.box(
            df_filtered,
            x="primary_sport",
            y="age",
            color="primary_sport",
            title="🎂 Age Distribution by Sport (Top 10)"
        )
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        xaxis_title="" if by == "gender" else "Sport",
        yaxis_title="Age (years)",
        height=450
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Gender Distribution Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_gender_distribution_chart(athletes_df, view_by="World"):
    df = athletes_df.copy()
    
    if "Continent" not in df.columns:
        df = add_continent_column(df)
    
    if view_by == "World":
        # Overall gender distribution
        gender_counts = df["gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        
        fig = px.pie(
            gender_counts,
            values="Count",
            names="Gender",
            color="Gender",
            color_discrete_map={"Male": "#0055A4", "Female": "#EF4135"},
            title="👥 Gender Distribution (World)",
            hole=0.4
        )
    elif view_by == "By Continent":
        # Gender by continent
        gender_continent = df.groupby(["Continent", "gender"]).size().reset_index(name="Count")
        gender_continent = gender_continent[gender_continent["Continent"] != "Other"]
        
        fig = px.bar(
            gender_continent,
            x="Continent",
            y="Count",
            color="gender",
            barmode="group",
            color_discrete_map={"Male": "#0055A4", "Female": "#EF4135"},
            title="👥 Gender Distribution by Continent"
        )
        fig.update_layout(xaxis_tickangle=-45)
    else:  # By Country (Top 20)
        # Get top 20 countries by athlete count
        top_countries = df["country"].value_counts().head(20).index.tolist()
        df_filtered = df[df["country"].isin(top_countries)]
        
        gender_country = df_filtered.groupby(["country", "gender"]).size().reset_index(name="Count")
        
        # Sort by total
        country_order = df_filtered["country"].value_counts().index.tolist()
        
        fig = px.bar(
            gender_country,
            x="country",
            y="Count",
            color="gender",
            barmode="stack",
            color_discrete_map={"Male": "#0055A4", "Female": "#EF4135"},
            title="👥 Gender Distribution by Country (Top 20)",
            category_orders={"country": country_order}
        )
        fig.update_layout(xaxis_tickangle=-45)
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        legend_title="Gender",
        height=450
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Top Athletes by Medals
# ─────────────────────────────────────────────────────────────────────────────
def create_top_athletes_chart(medallists_df, top_n=10):
    # Count medals per athlete
    athlete_medals = medallists_df.groupby(["name", "country"]).agg({
        "medal_type": "count",
        "country_code": "first"
    }).reset_index()
    athlete_medals.columns = ["Athlete", "Country", "Total Medals", "country_code"]
    
    # Get top N
    top_athletes = athlete_medals.nlargest(top_n, "Total Medals")
    top_athletes = top_athletes.sort_values("Total Medals", ascending=True)
    
    # Add flag to name
    top_athletes["Athlete_Display"] = top_athletes.apply(
        lambda x: f"{get_flag(x['country_code'])} {x['Athlete']}", axis=1
    )
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_athletes["Athlete_Display"],
        x=top_athletes["Total Medals"],
        orientation="h",
        marker=dict(
            color=top_athletes["Total Medals"],
            colorscale=[[0, "#667eea"], [0.5, "#764ba2"], [1, "#f093fb"]],
            showscale=False
        ),
        text=top_athletes["Total Medals"],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Medals: %{x}<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": f"🏆 Top {top_n} Athletes by Medal Count",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        xaxis_title="Total Medals",
        yaxis_title="",
        height=500,
        margin=dict(l=200)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Medal Breakdown for Top Athletes
# ─────────────────────────────────────────────────────────────────────────────
def create_top_athletes_medal_breakdown(medallists_df, top_n=10):
    # Count medals by type per athlete
    medal_breakdown = medallists_df.groupby(["name", "medal_type"]).size().reset_index(name="Count")
    
    # Get total medals per athlete
    totals = medal_breakdown.groupby("name")["Count"].sum().reset_index()
    totals.columns = ["name", "Total"]
    
    # Get top N athletes
    top_names = totals.nlargest(top_n, "Total")["name"].tolist()
    
    # Filter for top athletes
    df = medal_breakdown[medal_breakdown["name"].isin(top_names)]
    
    # Pivot for stacked bar
    pivot = df.pivot(index="name", columns="medal_type", values="Count").fillna(0)
    pivot["Total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("Total", ascending=True)
    
    fig = go.Figure()
    
    # Add bars in order: Bronze, Silver, Gold
    for medal, color in [("Bronze Medal", "#CD7F32"), ("Silver Medal", "#C0C0C0"), ("Gold Medal", "#FFD700")]:
        if medal in pivot.columns:
            fig.add_trace(go.Bar(
                y=pivot.index,
                x=pivot[medal],
                name=medal.replace(" Medal", ""),
                orientation="h",
                marker_color=color,
                hovertemplate="<b>%{y}</b><br>" + medal + ": %{x}<extra></extra>"
            ))
    
    fig.update_layout(
        title={
            "text": f"🥇 Medal Breakdown - Top {top_n} Athletes",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        barmode="stack",
        xaxis_title="Medal Count",
        yaxis_title="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=500,
        margin=dict(l=200)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Athlete Performance - Paris 2024",
        page_icon="👤",
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
    st.markdown('<h1 class="main-title">👤 Athlete Performance</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Explore athlete profiles, demographics, and medal achievements. '
        'Discover the human stories behind the Paris 2024 Olympics.</p>',
        unsafe_allow_html=True
    )
    
    # Load data
    athletes_df = load_athletes()
    nocs_df = load_nocs()
    events_df = load_events()
    medallists_df = load_medallists()
    
    # Create sidebar filters
    selected_continents, selected_countries, selected_sports, genders = create_sidebar_filters(
        athletes_df, nocs_df, events_df
    )
    
    # Apply filters
    filtered_athletes = filter_athletes(athletes_df, selected_continents, selected_countries, selected_sports, genders)
    
    # Show active filters
    if selected_continents or selected_countries or selected_sports:
        with st.expander("📌 Active Filters", expanded=False):
            if selected_continents:
                st.write(f"**Continents:** {', '.join(selected_continents)}")
            if selected_countries:
                st.write(f"**Countries:** {', '.join(selected_countries)}")
            if selected_sports:
                st.write(f"**Sports:** {', '.join(selected_sports)}")
    
    # 1. Athlete Profile Card
    display_athlete_profile(athletes_df)  # Use full dataset for search
    
    st.markdown("---")
    
    # 2. Age Distribution
    st.subheader("🎂 Athlete Age Distribution")
    
    col_age1, col_age2 = st.columns([1, 4])
    with col_age1:
        age_view = st.radio(
            "View by:",
            ["Gender", "Sport"],
            horizontal=False
        )
    
    with col_age2:
        if len(filtered_athletes) > 0:
            age_chart = create_age_distribution_chart(
                filtered_athletes, 
                by="gender" if age_view == "Gender" else "sport"
            )
            if age_chart:
                st.plotly_chart(age_chart, use_container_width=True)
            else:
                st.warning("No age data available.")
        else:
            st.warning("No athletes match the selected filters.")
    
    st.markdown("---")
    
    # 3. Gender Distribution
    st.subheader("👥 Gender Distribution")
    
    col_gender1, col_gender2 = st.columns([1, 4])
    with col_gender1:
        gender_view = st.radio(
            "View:",
            ["World", "By Continent", "By Country"],
            horizontal=False
        )
    
    with col_gender2:
        if len(filtered_athletes) > 0:
            gender_chart = create_gender_distribution_chart(filtered_athletes, gender_view)
            st.plotly_chart(gender_chart, use_container_width=True)
        else:
            st.warning("No athletes match the selected filters.")
    
    st.markdown("---")
    
    # 4. Top Athletes by Medals
    st.subheader("🏆 Top Athletes by Medals")
    
    tab1, tab2 = st.tabs(["📊 Total Medals", "🥇 Medal Breakdown"])
    
    with tab1:
        if len(medallists_df) > 0:
            top_chart = create_top_athletes_chart(medallists_df)
            st.plotly_chart(top_chart, use_container_width=True)
        else:
            st.warning("No medallist data available.")
    
    with tab2:
        if len(medallists_df) > 0:
            breakdown_chart = create_top_athletes_medal_breakdown(medallists_df)
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.warning("No medallist data available.")
    
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

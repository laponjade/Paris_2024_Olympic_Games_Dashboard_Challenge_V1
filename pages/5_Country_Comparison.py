import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ─────────────────────────────────────────────────────────────────────────────
# Country Flags Mapping
# ─────────────────────────────────────────────────────────────────────────────
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
def load_medals_total():
    return pd.read_csv("data/medals_total.csv")


@st.cache_data
def load_medallists():
    return pd.read_csv("data/medallists.csv")


@st.cache_data
def load_athletes():
    return pd.read_csv("data/athletes.csv")


@st.cache_data
def load_medals():
    return pd.read_csv("data/medals.csv")


def get_flag(country_code):
    """Get flag emoji for country code."""
    return COUNTRY_FLAGS.get(country_code, "🏳️")


# ─────────────────────────────────────────────────────────────────────────────
# Comparison Metrics
# ─────────────────────────────────────────────────────────────────────────────
def get_country_stats(country_code, medals_total_df, medallists_df, athletes_df):
    """Get comprehensive stats for a country."""
    stats = {}
    
    # Medal totals
    country_medals = medals_total_df[medals_total_df["country_code"] == country_code]
    if len(country_medals) > 0:
        row = country_medals.iloc[0]
        stats["gold"] = int(row["Gold Medal"])
        stats["silver"] = int(row["Silver Medal"])
        stats["bronze"] = int(row["Bronze Medal"])
        stats["total"] = int(row["Total"])
        stats["country_name"] = row["country"]
    else:
        stats["gold"] = 0
        stats["silver"] = 0
        stats["bronze"] = 0
        stats["total"] = 0
        stats["country_name"] = country_code
    
    # Rank
    medals_total_df_sorted = medals_total_df.sort_values("Total", ascending=False).reset_index(drop=True)
    rank_idx = medals_total_df_sorted[medals_total_df_sorted["country_code"] == country_code].index
    stats["rank"] = int(rank_idx[0] + 1) if len(rank_idx) > 0 else "N/A"
    
    # Athletes count
    country_athletes = athletes_df[athletes_df["country_code"] == country_code]
    stats["athletes"] = len(country_athletes)
    
    # Gender distribution
    if len(country_athletes) > 0:
        gender_counts = country_athletes["gender"].value_counts()
        stats["male_athletes"] = gender_counts.get("Male", 0)
        stats["female_athletes"] = gender_counts.get("Female", 0)
    else:
        stats["male_athletes"] = 0
        stats["female_athletes"] = 0
    
    # Unique medallists
    country_medallists = medallists_df[medallists_df["country_code"] == country_code]
    stats["unique_medallists"] = country_medallists["name"].nunique()
    
    # Sports with medals
    stats["sports_with_medals"] = country_medallists["discipline"].nunique()
    
    # Medal efficiency (medals per athlete)
    stats["medal_efficiency"] = round(stats["total"] / stats["athletes"] * 100, 1) if stats["athletes"] > 0 else 0
    
    return stats


def get_medals_by_sport(country_code, medallists_df):
    """Get medal breakdown by sport for a country."""
    country_medals = medallists_df[medallists_df["country_code"] == country_code]
    
    sport_medals = country_medals.groupby(["discipline", "medal_type"]).size().reset_index(name="Count")
    
    # Pivot for easier comparison
    pivot = sport_medals.pivot(index="discipline", columns="medal_type", values="Count").fillna(0)
    
    for col in ["Gold Medal", "Silver Medal", "Bronze Medal"]:
        if col not in pivot.columns:
            pivot[col] = 0
    
    pivot["Total"] = pivot["Gold Medal"] + pivot["Silver Medal"] + pivot["Bronze Medal"]
    pivot = pivot.sort_values("Total", ascending=False).reset_index()
    
    return pivot


def get_top_athletes(country_code, medallists_df, top_n=5):
    """Get top athletes by medal count for a country."""
    country_medals = medallists_df[medallists_df["country_code"] == country_code]
    
    athlete_medals = country_medals.groupby("name").agg({
        "medal_type": "count",
        "discipline": lambda x: ", ".join(x.unique()[:2])
    }).reset_index()
    athlete_medals.columns = ["Athlete", "Medals", "Sport(s)"]
    
    return athlete_medals.nlargest(top_n, "Medals")


# ─────────────────────────────────────────────────────────────────────────────
# Visualization Functions
# ─────────────────────────────────────────────────────────────────────────────
def create_medal_comparison_chart(stats1, stats2, code1, code2):
    """Create side-by-side medal comparison bar chart."""
    
    categories = ["Gold", "Silver", "Bronze", "Total"]
    values1 = [stats1["gold"], stats1["silver"], stats1["bronze"], stats1["total"]]
    values2 = [stats2["gold"], stats2["silver"], stats2["bronze"], stats2["total"]]
    
    fig = go.Figure()
    
    # Country 1 bars
    fig.add_trace(go.Bar(
        name=f"{get_flag(code1)} {stats1['country_name']}",
        x=categories,
        y=values1,
        marker_color=["#FFD700", "#C0C0C0", "#CD7F32", "#0055A4"],
        text=values1,
        textposition="outside"
    ))
    
    # Country 2 bars
    fig.add_trace(go.Bar(
        name=f"{get_flag(code2)} {stats2['country_name']}",
        x=categories,
        y=values2,
        marker_color=["#FFE55C", "#D4D4D4", "#D9986A", "#EF4135"],
        text=values2,
        textposition="outside"
    ))
    
    fig.update_layout(
        title={
            "text": "🏅 Medal Comparison",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        barmode="group",
        xaxis_title="Medal Type",
        yaxis_title="Count",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=400
    )
    
    return fig


def create_radar_comparison(stats1, stats2, code1, code2):
    """Create radar chart comparing various metrics."""
    
    # Normalize metrics for radar chart
    max_vals = {
        "gold": max(stats1["gold"], stats2["gold"], 1),
        "athletes": max(stats1["athletes"], stats2["athletes"], 1),
        "sports": max(stats1["sports_with_medals"], stats2["sports_with_medals"], 1),
        "medallists": max(stats1["unique_medallists"], stats2["unique_medallists"], 1),
        "efficiency": max(stats1["medal_efficiency"], stats2["medal_efficiency"], 1)
    }
    
    categories = ["Gold Medals", "Total Athletes", "Sports with Medals", 
                  "Unique Medallists", "Medal Efficiency (%)"]
    
    values1 = [
        stats1["gold"] / max_vals["gold"] * 100,
        stats1["athletes"] / max_vals["athletes"] * 100,
        stats1["sports_with_medals"] / max_vals["sports"] * 100,
        stats1["unique_medallists"] / max_vals["medallists"] * 100,
        stats1["medal_efficiency"] / max_vals["efficiency"] * 100 if max_vals["efficiency"] > 0 else 0
    ]
    
    values2 = [
        stats2["gold"] / max_vals["gold"] * 100,
        stats2["athletes"] / max_vals["athletes"] * 100,
        stats2["sports_with_medals"] / max_vals["sports"] * 100,
        stats2["unique_medallists"] / max_vals["medallists"] * 100,
        stats2["medal_efficiency"] / max_vals["efficiency"] * 100 if max_vals["efficiency"] > 0 else 0
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values1 + [values1[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=f"{get_flag(code1)} {stats1['country_name']}",
        line_color="#0055A4",
        fillcolor="rgba(0, 85, 164, 0.3)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values2 + [values2[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=f"{get_flag(code2)} {stats2['country_name']}",
        line_color="#EF4135",
        fillcolor="rgba(239, 65, 53, 0.3)"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title={
            "text": "📊 Performance Comparison Radar",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=450
    )
    
    return fig


def create_sport_comparison_chart(medals1, medals2, stats1, stats2, code1, code2):
    """Create sport-by-sport comparison."""
    
    # Merge the two dataframes
    if len(medals1) == 0 and len(medals2) == 0:
        return None
    
    # Get all sports from both countries
    all_sports = set()
    if len(medals1) > 0:
        all_sports.update(medals1["discipline"].tolist())
    if len(medals2) > 0:
        all_sports.update(medals2["discipline"].tolist())
    
    comparison_data = []
    for sport in all_sports:
        row1 = medals1[medals1["discipline"] == sport]
        row2 = medals2[medals2["discipline"] == sport]
        
        total1 = int(row1["Total"].iloc[0]) if len(row1) > 0 else 0
        total2 = int(row2["Total"].iloc[0]) if len(row2) > 0 else 0
        
        comparison_data.append({
            "Sport": sport,
            stats1["country_name"]: total1,
            stats2["country_name"]: total2,
            "Difference": total1 - total2
        })
    
    df = pd.DataFrame(comparison_data)
    df = df.sort_values("Difference", ascending=True)
    
    # Create diverging bar chart
    fig = go.Figure()
    
    # Bars for country 1 (positive direction)
    fig.add_trace(go.Bar(
        y=df["Sport"],
        x=df[stats1["country_name"]],
        name=f"{get_flag(code1)} {stats1['country_name']}",
        orientation="h",
        marker_color="#0055A4",
        hovertemplate=f"<b>%{{y}}</b><br>{stats1['country_name']}: %{{x}}<extra></extra>"
    ))
    
    # Bars for country 2 (negative direction for visual effect)
    fig.add_trace(go.Bar(
        y=df["Sport"],
        x=[-x for x in df[stats2["country_name"]]],
        name=f"{get_flag(code2)} {stats2['country_name']}",
        orientation="h",
        marker_color="#EF4135",
        hovertemplate=f"<b>%{{y}}</b><br>{stats2['country_name']}: %{{customdata}}<extra></extra>",
        customdata=df[stats2["country_name"]]
    ))
    
    fig.update_layout(
        title={
            "text": "🏆 Sport-by-Sport Medal Comparison",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        barmode="overlay",
        xaxis_title="Medal Count",
        yaxis_title="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=max(400, len(all_sports) * 25),
        margin=dict(l=150)
    )
    
    return fig


def create_gender_comparison(stats1, stats2, code1, code2):
    """Create gender distribution comparison."""
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        subplot_titles=[
            f"{get_flag(code1)} {stats1['country_name']}",
            f"{get_flag(code2)} {stats2['country_name']}"
        ]
    )
    
    # Country 1
    fig.add_trace(go.Pie(
        labels=["Male", "Female"],
        values=[stats1["male_athletes"], stats1["female_athletes"]],
        marker_colors=["#0055A4", "#EF4135"],
        hole=0.4,
        textinfo="percent+value"
    ), row=1, col=1)
    
    # Country 2
    fig.add_trace(go.Pie(
        labels=["Male", "Female"],
        values=[stats2["male_athletes"], stats2["female_athletes"]],
        marker_colors=["#0055A4", "#EF4135"],
        hole=0.4,
        textinfo="percent+value"
    ), row=1, col=2)
    
    fig.update_layout(
        title={
            "text": "👥 Athlete Gender Distribution",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        height=400,
        showlegend=True
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Display Functions
# ─────────────────────────────────────────────────────────────────────────────
def display_country_card(stats, country_code, position="left"):
    """Display a country stats card."""
    
    color = "#0055A4" if position == "left" else "#EF4135"
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
            <h2 style="margin: 0; font-size: 2.5rem;">{get_flag(country_code)}</h2>
            <h3 style="margin: 0.5rem 0;">{stats['country_name']}</h3>
            <p style="margin: 0; opacity: 0.9;">Rank: #{stats['rank']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Medal counts
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🥇 Gold", stats["gold"])
    with col2:
        st.metric("🥈 Silver", stats["silver"])
    with col3:
        st.metric("🥉 Bronze", stats["bronze"])
    
    # Additional stats
    st.metric("🏅 Total Medals", stats["total"])
    st.metric("👥 Total Athletes", stats["athletes"])
    st.metric("🎯 Sports with Medals", stats["sports_with_medals"])
    st.metric("⚡ Medal Efficiency", f"{stats['medal_efficiency']}%")


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Country Comparison - Paris 2024",
        page_icon="⚔️",
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
        .vs-text {
            font-size: 3rem;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-title">⚔️ Country Comparison</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Compare the Olympic performance of two countries head-to-head. '
        'Select two nations to see detailed side-by-side statistics.</p>',
        unsafe_allow_html=True
    )
    
    # Load data
    medals_total_df = load_medals_total()
    medallists_df = load_medallists()
    athletes_df = load_athletes()
    
    # Get list of countries with medals
    countries_with_medals = medals_total_df.sort_values("Total", ascending=False)
    country_options = [
        f"{get_flag(row['country_code'])} {row['country']} ({row['Total']} medals)"
        for _, row in countries_with_medals.iterrows()
    ]
    country_codes = countries_with_medals["country_code"].tolist()
    
    # Country selection
    st.markdown("### 🌍 Select Countries to Compare")
    
    col1, col_vs, col2 = st.columns([2, 1, 2])
    
    with col1:
        selected1_idx = st.selectbox(
            "Country 1",
            options=range(len(country_options)),
            format_func=lambda x: country_options[x],
            index=0,
            key="country1"
        )
    
    with col_vs:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="vs-text">VS</p>', unsafe_allow_html=True)
    
    with col2:
        selected2_idx = st.selectbox(
            "Country 2",
            options=range(len(country_options)),
            format_func=lambda x: country_options[x],
            index=1 if len(country_options) > 1 else 0,
            key="country2"
        )
    
    # Get selected country codes
    code1 = country_codes[selected1_idx]
    code2 = country_codes[selected2_idx]
    
    if code1 == code2:
        st.warning("⚠️ Please select two different countries to compare.")
        return
    
    # Get stats for both countries
    stats1 = get_country_stats(code1, medals_total_df, medallists_df, athletes_df)
    stats2 = get_country_stats(code2, medals_total_df, medallists_df, athletes_df)
    
    st.markdown("---")
    
    # Country Cards
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        display_country_card(stats1, code1, "left")
    
    with col_card2:
        display_country_card(stats2, code2, "right")
    
    st.markdown("---")
    
    # Medal Comparison Chart
    medal_chart = create_medal_comparison_chart(stats1, stats2, code1, code2)
    st.plotly_chart(medal_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Two column layout for radar and gender charts
    col_radar, col_gender = st.columns(2)
    
    with col_radar:
        radar_chart = create_radar_comparison(stats1, stats2, code1, code2)
        st.plotly_chart(radar_chart, use_container_width=True)
    
    with col_gender:
        gender_chart = create_gender_comparison(stats1, stats2, code1, code2)
        st.plotly_chart(gender_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Sport-by-Sport Comparison
    medals1 = get_medals_by_sport(code1, medallists_df)
    medals2 = get_medals_by_sport(code2, medallists_df)
    
    sport_chart = create_sport_comparison_chart(medals1, medals2, stats1, stats2, code1, code2)
    if sport_chart:
        st.plotly_chart(sport_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Top Athletes from each country
    st.subheader("🌟 Top Athletes")
    
    col_athletes1, col_athletes2 = st.columns(2)
    
    with col_athletes1:
        st.markdown(f"### {get_flag(code1)} {stats1['country_name']}")
        top1 = get_top_athletes(code1, medallists_df)
        if len(top1) > 0:
            st.dataframe(
                top1,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Athlete": st.column_config.TextColumn("Athlete", width="medium"),
                    "Medals": st.column_config.NumberColumn("Medals", width="small"),
                    "Sport(s)": st.column_config.TextColumn("Sport(s)", width="medium")
                }
            )
        else:
            st.info("No medallists found.")
    
    with col_athletes2:
        st.markdown(f"### {get_flag(code2)} {stats2['country_name']}")
        top2 = get_top_athletes(code2, medallists_df)
        if len(top2) > 0:
            st.dataframe(
                top2,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Athlete": st.column_config.TextColumn("Athlete", width="medium"),
                    "Medals": st.column_config.NumberColumn("Medals", width="small"),
                    "Sport(s)": st.column_config.TextColumn("Sport(s)", width="medium")
                }
            )
        else:
            st.info("No medallists found.")
    
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


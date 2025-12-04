import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ─────────────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_athletes():
    return pd.read_csv("data/athletes.csv")


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


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────────────────────────────────────
def create_sidebar_filters(athletes_df, events_df, nocs_df):
    st.sidebar.header("🎯 Filters")
    
    # Country filter
    countries = sorted(nocs_df["country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries",
        options=countries,
        default=[],
        help="Filter data by country. Leave empty to show all."
    )
    
    # Sport filter
    sports = sorted(events_df["sport"].dropna().unique().tolist())
    selected_sports = st.sidebar.multiselect(
        "🏅 Select Sports",
        options=sports,
        default=[],
        help="Filter data by sport. Leave empty to show all."
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
    
    return selected_countries, selected_sports, medal_types


# ─────────────────────────────────────────────────────────────────────────────
# Filter Functions
# ─────────────────────────────────────────────────────────────────────────────
def filter_athletes(df, selected_countries, selected_sports):
    filtered = df.copy()
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    if selected_sports:
        # Athletes have disciplines in a list format like "['Wrestling']"
        filtered = filtered[filtered["disciplines"].apply(
            lambda x: any(sport in str(x) for sport in selected_sports)
        )]
    
    return filtered


def filter_medals(df, selected_countries, selected_sports, medal_types):
    filtered = df.copy()
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    if selected_sports:
        filtered = filtered[filtered["discipline"].isin(selected_sports)]
    
    if medal_types:
        filtered = filtered[filtered["medal_type"].isin(medal_types)]
    
    return filtered


def filter_medals_total(df, selected_countries):
    filtered = df.copy()
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    return filtered


def filter_events(df, selected_sports):
    filtered = df.copy()
    
    if selected_sports:
        filtered = filtered[filtered["sport"].isin(selected_sports)]
    
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# KPI Section
# ─────────────────────────────────────────────────────────────────────────────
def display_kpis(athletes_df, nocs_df, events_df, medals_total_df, medals_df, 
                 selected_countries, selected_sports, medal_types):
    
    # Filter data based on selections
    filtered_athletes = filter_athletes(athletes_df, selected_countries, selected_sports)
    filtered_events = filter_events(events_df, selected_sports)
    filtered_medals_total = filter_medals_total(medals_total_df, selected_countries)
    filtered_medals = filter_medals(medals_df, selected_countries, selected_sports, medal_types)
    
    # Calculate KPIs
    total_athletes = len(filtered_athletes)
    
    if selected_countries:
        total_countries = len(selected_countries)
    else:
        total_countries = len(nocs_df[nocs_df["note"] == "P"])  # Only participating countries
    
    total_sports = filtered_events["sport"].nunique()
    
    # Total medals awarded
    total_medals = len(filtered_medals)
    
    # Number of events
    num_events = len(filtered_events)
    
    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🏃 Total Athletes",
            value=f"{total_athletes:,}",
            help="Total number of athletes"
        )
    
    with col2:
        st.metric(
            label="🌍 Total Countries",
            value=f"{total_countries:,}",
            help="Total participating countries"
        )
    
    with col3:
        st.metric(
            label="🎾 Total Sports",
            value=f"{total_sports:,}",
            help="Total number of sports"
        )
    
    with col4:
        st.metric(
            label="🏅 Total Medals",
            value=f"{total_medals:,}",
            help="Total medals awarded"
        )
    
    with col5:
        st.metric(
            label="📅 Number of Events",
            value=f"{num_events:,}",
            help="Total number of events"
        )
    
    return filtered_medals, filtered_medals_total


# ─────────────────────────────────────────────────────────────────────────────
# Medal Distribution Donut Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_medal_distribution_chart(medals_df, medal_types):
    # Count medals by type
    medal_counts = medals_df["medal_type"].value_counts().reset_index()
    medal_counts.columns = ["Medal Type", "Count"]
    
    # Filter by selected medal types
    if medal_types:
        medal_counts = medal_counts[medal_counts["Medal Type"].isin(medal_types)]
    
    # Define colors for medals
    color_map = {
        "Gold Medal": "#FFD700",
        "Silver Medal": "#C0C0C0",
        "Bronze Medal": "#CD7F32"
    }
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=medal_counts["Medal Type"],
        values=medal_counts["Count"],
        hole=0.5,
        marker_colors=[color_map.get(m, "#888888") for m in medal_counts["Medal Type"]],
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title={
            "text": "🏅 Global Medal Distribution",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=450,
        annotations=[dict(
            text="Medals",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )]
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Top 10 Medal Standings Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_top10_medal_chart(medals_total_df, selected_countries):
    # Filter and get top 10
    filtered_df = medals_total_df.copy()
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]
    
    # Sort by total and get top 10
    top10 = filtered_df.nlargest(10, "Total")
    
    # Reverse order for horizontal bar chart (highest at top)
    top10 = top10.iloc[::-1]
    
    # Create figure with stacked horizontal bars
    fig = go.Figure()
    
    # Add Bronze bars
    fig.add_trace(go.Bar(
        y=top10["country"],
        x=top10["Bronze Medal"],
        name="Bronze",
        orientation="h",
        marker_color="#CD7F32",
        hovertemplate="<b>%{y}</b><br>Bronze: %{x}<extra></extra>"
    ))
    
    # Add Silver bars
    fig.add_trace(go.Bar(
        y=top10["country"],
        x=top10["Silver Medal"],
        name="Silver",
        orientation="h",
        marker_color="#C0C0C0",
        hovertemplate="<b>%{y}</b><br>Silver: %{x}<extra></extra>"
    ))
    
    # Add Gold bars
    fig.add_trace(go.Bar(
        y=top10["country"],
        x=top10["Gold Medal"],
        name="Gold",
        orientation="h",
        marker_color="#FFD700",
        hovertemplate="<b>%{y}</b><br>Gold: %{x}<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": "🏆 Top 10 Countries by Medal Count",
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
        height=500,
        margin=dict(l=150)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Paris 2024 Olympics Dashboard",
        page_icon="🏅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E3A5F;
            text-align: center;
            padding: 1rem 0;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            padding-bottom: 2rem;
        }
        /* KPI Card Styling */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        div[data-testid="stMetric"] > div {
            color: white !important;
        }
        div[data-testid="stMetric"] label {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: white !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        /* Alternate colors for KPI cards */
        div[data-testid="column"]:nth-child(1) div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #0055A4 0%, #003d7a 100%);
        }
        div[data-testid="column"]:nth-child(2) div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #EF4135 0%, #c72c21 100%);
        }
        div[data-testid="column"]:nth-child(3) div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #FFD700 0%, #e6c200 100%);
        }
        div[data-testid="column"]:nth-child(3) div[data-testid="stMetric"] label,
        div[data-testid="column"]:nth-child(3) div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #1a1a1a !important;
        }
        div[data-testid="column"]:nth-child(4) div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
        }
        div[data-testid="column"]:nth-child(5) div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(
        '<h1 class="main-header">🏅 Paris 2024 Olympic Games Dashboard</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">Explore comprehensive data and insights from the Paris 2024 Summer Olympics.<br>'
        'Use the filters in the sidebar to customize your view.</p>',
        unsafe_allow_html=True
    )
    
    # Load data
    athletes_df = load_athletes()
    nocs_df = load_nocs()
    events_df = load_events()
    medals_total_df = load_medals_total()
    medals_df = load_medals()
    
    # Create sidebar filters
    selected_countries, selected_sports, medal_types = create_sidebar_filters(
        athletes_df, events_df, nocs_df
    )
    
    # Display applied filters info
    if selected_countries or selected_sports:
        with st.expander("📌 Active Filters", expanded=False):
            if selected_countries:
                st.write(f"**Countries:** {', '.join(selected_countries)}")
            if selected_sports:
                st.write(f"**Sports:** {', '.join(selected_sports)}")
    
    st.markdown("---")
    
    # KPI Section
    st.subheader("📊 Key Performance Indicators")
    filtered_medals, filtered_medals_total = display_kpis(
        athletes_df, nocs_df, events_df, medals_total_df, medals_df,
        selected_countries, selected_sports, medal_types
    )
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # Medal Distribution Donut Chart
        if len(filtered_medals) > 0:
            medal_dist_fig = create_medal_distribution_chart(filtered_medals, medal_types)
            st.plotly_chart(medal_dist_fig, use_container_width=True)
        else:
            st.warning("No medal data available for the selected filters.")
    
    with col2:
        # Top 10 Medal Standings
        if len(filtered_medals_total) > 0:
            top10_fig = create_top10_medal_chart(medals_total_df, selected_countries)
            st.plotly_chart(top10_fig, use_container_width=True)
        else:
            st.warning("No medal standings data available for the selected filters.")
    
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

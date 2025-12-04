import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ─────────────────────────────────────────────────────────────────────────────
# Venue Coordinates (Paris 2024 Olympic Venues)
# ─────────────────────────────────────────────────────────────────────────────
VENUE_COORDINATES = {
    "Aquatics Centre": {"lat": 48.9283, "lon": 2.3558, "city": "Saint-Denis"},
    "Bercy Arena": {"lat": 48.8386, "lon": 2.3788, "city": "Paris"},
    "Bordeaux Stadium": {"lat": 44.8976, "lon": -0.5616, "city": "Bordeaux"},
    "Champ de Mars Arena": {"lat": 48.8556, "lon": 2.2986, "city": "Paris"},
    "Château de Versailles": {"lat": 48.8049, "lon": 2.1204, "city": "Versailles"},
    "Chateauroux Shooting Centre": {"lat": 46.8103, "lon": 1.6913, "city": "Châteauroux"},
    "Eiffel Tower Stadium": {"lat": 48.8584, "lon": 2.2945, "city": "Paris"},
    "Elancourt Hill": {"lat": 48.7839, "lon": 1.9589, "city": "Élancourt"},
    "Geoffroy-Guichard Stadium": {"lat": 45.4608, "lon": 4.3903, "city": "Saint-Étienne"},
    "Grand Palais": {"lat": 48.8662, "lon": 2.3125, "city": "Paris"},
    "Hôtel de Ville": {"lat": 48.8566, "lon": 2.3522, "city": "Paris"},
    "Invalides": {"lat": 48.8567, "lon": 2.3128, "city": "Paris"},
    "La Beaujoire Stadium": {"lat": 47.2561, "lon": -1.5251, "city": "Nantes"},
    "La Concorde": {"lat": 48.8656, "lon": 2.3212, "city": "Paris"},
    "Le Bourget Sport Climbing Venue": {"lat": 48.9372, "lon": 2.4253, "city": "Le Bourget"},
    "Golf National": {"lat": 48.7544, "lon": 2.0739, "city": "Guyancourt"},
    "Lyon Stadium": {"lat": 45.7653, "lon": 4.9822, "city": "Lyon"},
    "Marseille Marina": {"lat": 43.2965, "lon": 5.3698, "city": "Marseille"},
    "Marseille Stadium": {"lat": 43.2699, "lon": 5.3959, "city": "Marseille"},
    "Nice Stadium": {"lat": 43.7050, "lon": 7.1926, "city": "Nice"},
    "North Paris Arena": {"lat": 48.9714, "lon": 2.5164, "city": "Villepinte"},
    "Parc des Princes": {"lat": 48.8414, "lon": 2.2530, "city": "Paris"},
    "Paris La Defense Arena": {"lat": 48.8958, "lon": 2.2299, "city": "Nanterre"},
    "Pierre Mauroy Stadium": {"lat": 50.6119, "lon": 3.1303, "city": "Lille"},
    "Pont Alexandre III": {"lat": 48.8637, "lon": 2.3134, "city": "Paris"},
    "Porte de La Chapelle Arena": {"lat": 48.8989, "lon": 2.3595, "city": "Paris"},
    "Stade Roland-Garros": {"lat": 48.8469, "lon": 2.2527, "city": "Paris"},
    "Saint-Quentin-en-Yvelines BMX Stadium": {"lat": 48.7866, "lon": 2.0352, "city": "Montigny-le-Bretonneux"},
    "Saint-Quentin-en-Yvelines Velodrome": {"lat": 48.7866, "lon": 2.0352, "city": "Montigny-le-Bretonneux"},
    "South Paris Arena": {"lat": 48.8320, "lon": 2.2870, "city": "Paris"},
    "Stade de France": {"lat": 48.9244, "lon": 2.3601, "city": "Saint-Denis"},
    "Teahupo'o, Tahiti": {"lat": -17.8352, "lon": -149.2577, "city": "Tahiti"},
    "Trocadéro": {"lat": 48.8616, "lon": 2.2892, "city": "Paris"},
    "Vaires-sur-Marne Nautical Stadium": {"lat": 48.8635, "lon": 2.6372, "city": "Vaires-sur-Marne"},
    "Yves-du-Manoir Stadium": {"lat": 48.9276, "lon": 2.2636, "city": "Colombes"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_schedules():
    df = pd.read_csv("data/schedules.csv")
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
    df["day"] = pd.to_datetime(df["day"], errors="coerce")
    return df


@st.cache_data
def load_venues():
    return pd.read_csv("data/venues.csv")


@st.cache_data
def load_medals():
    return pd.read_csv("data/medals.csv")


@st.cache_data
def load_events():
    return pd.read_csv("data/events.csv")


@st.cache_data
def load_nocs():
    return pd.read_csv("data/nocs.csv")


def parse_sports_list(sports_str):
    """Parse sports from string format like ['Sport1', 'Sport2']."""
    if pd.isna(sports_str):
        return []
    try:
        cleaned = sports_str.strip("[]").replace("'", "").replace('"', "")
        return [s.strip() for s in cleaned.split(",") if s.strip()]
    except:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────────────────────────────────────
def create_sidebar_filters(schedules_df, events_df, nocs_df):
    st.sidebar.header("🎯 Filters")
    
    # Country filter
    countries = sorted(nocs_df["country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries",
        options=countries,
        default=[],
        help="Filter medal data by country."
    )
    
    # Sport filter
    sports = sorted(events_df["sport"].dropna().unique().tolist())
    selected_sports = st.sidebar.multiselect(
        "🏅 Select Sports",
        options=sports,
        default=[],
        help="Filter data by sport."
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
def filter_medals(df, selected_countries, selected_sports, medal_types):
    filtered = df.copy()
    
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]
    
    if selected_sports:
        filtered = filtered[filtered["discipline"].isin(selected_sports)]
    
    if medal_types:
        filtered = filtered[filtered["medal_type"].isin(medal_types)]
    
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# Event Schedule Gantt Chart
# ─────────────────────────────────────────────────────────────────────────────
def create_event_schedule_gantt(schedules_df, filter_by, filter_value):
    df = schedules_df.copy()
    
    # Filter based on selection
    if filter_by == "Sport":
        df = df[df["discipline"] == filter_value]
    else:  # Venue
        df = df[df["venue"] == filter_value]
    
    if len(df) == 0:
        return None
    
    # Aggregate events by day to reduce chart complexity
    # Group by discipline, event, phase and take min start, max end
    df_agg = df.groupby(["discipline", "event", "phase", "venue"]).agg({
        "start_date": "min",
        "end_date": "max",
        "gender": "first"
    }).reset_index()
    
    # Limit to reasonable number of events for display
    if len(df_agg) > 50:
        df_agg = df_agg.head(50)
    
    # Create display label
    df_agg["Task"] = df_agg.apply(
        lambda x: f"{x['event']} - {x['phase']}" if pd.notna(x['phase']) else x['event'], 
        axis=1
    )
    
    # Create Gantt chart
    fig = px.timeline(
        df_agg,
        x_start="start_date",
        x_end="end_date",
        y="Task",
        color="discipline" if filter_by == "Venue" else "venue",
        hover_data=["event", "phase", "venue"],
        title=f"📅 Event Schedule - {filter_value}"
    )
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        xaxis_title="Date",
        yaxis_title="",
        height=max(400, len(df_agg) * 25),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig


def create_sport_timeline(schedules_df, sport_name):
    """Create a timeline for a specific sport showing all events."""
    df = schedules_df[schedules_df["discipline"] == sport_name].copy()
    
    if len(df) == 0:
        return None
    
    # Get unique events and their date ranges
    event_timeline = df.groupby(["event", "venue"]).agg({
        "start_date": "min",
        "end_date": "max"
    }).reset_index()
    
    # Create timeline
    fig = px.timeline(
        event_timeline,
        x_start="start_date",
        x_end="end_date",
        y="event",
        color="venue",
        title=f"📅 {sport_name} Event Timeline"
    )
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        xaxis_title="Date",
        yaxis_title="Event",
        height=max(400, len(event_timeline) * 35),
        showlegend=True
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Medal Count by Sport Treemap
# ─────────────────────────────────────────────────────────────────────────────
def create_medal_treemap(medals_df):
    # Count medals by discipline and medal type
    medal_counts = medals_df.groupby(["discipline", "medal_type"]).size().reset_index(name="Count")
    
    if len(medal_counts) == 0:
        return None
    
    # Create treemap
    fig = px.treemap(
        medal_counts,
        path=[px.Constant("All Sports"), "discipline", "medal_type"],
        values="Count",
        color="discipline",
        title="🏅 Medal Count by Sport"
    )
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 20}},
        height=600
    )
    
    fig.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Medals: %{value}<extra></extra>"
    )
    
    return fig


def create_sport_medal_bar(medals_df):
    """Create a bar chart of medals by sport."""
    medal_counts = medals_df.groupby(["discipline", "medal_type"]).size().reset_index(name="Count")
    
    if len(medal_counts) == 0:
        return None
    
    # Pivot for grouped bar
    sport_totals = medals_df.groupby("discipline").size().reset_index(name="Total")
    sport_totals = sport_totals.sort_values("Total", ascending=False).head(15)
    top_sports = sport_totals["discipline"].tolist()
    
    medal_counts_filtered = medal_counts[medal_counts["discipline"].isin(top_sports)]
    
    fig = px.bar(
        medal_counts_filtered,
        x="discipline",
        y="Count",
        color="medal_type",
        barmode="stack",
        color_discrete_map={
            "Gold Medal": "#FFD700",
            "Silver Medal": "#C0C0C0",
            "Bronze Medal": "#CD7F32"
        },
        title="🏅 Medal Distribution by Sport (Top 15)",
        category_orders={"discipline": top_sports}
    )
    
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        xaxis_title="Sport",
        yaxis_title="Medal Count",
        xaxis_tickangle=-45,
        height=500,
        legend_title="Medal Type"
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Venue Map
# ─────────────────────────────────────────────────────────────────────────────
def create_venue_map(venues_df, map_style="France", show_all=True):
    # Create dataframe with coordinates
    venue_data = []
    
    for _, row in venues_df.iterrows():
        venue_name = row["venue"]
        if venue_name in VENUE_COORDINATES:
            coords = VENUE_COORDINATES[venue_name]
            sports = parse_sports_list(row.get("sports", ""))
            venue_data.append({
                "Venue": venue_name,
                "Latitude": coords["lat"],
                "Longitude": coords["lon"],
                "City": coords["city"],
                "Sports": ", ".join(sports) if sports else "N/A",
                "Num_Sports": len(sports)
            })
    
    df = pd.DataFrame(venue_data)
    
    if len(df) == 0:
        return None
    
    # Filter for Paris area or show all
    if not show_all:
        # Focus on Paris metropolitan area
        df = df[(df["Latitude"] > 48.5) & (df["Latitude"] < 49.1) & 
                (df["Longitude"] > 1.8) & (df["Longitude"] < 2.8)]
    
    # Create scatter mapbox
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Venue",
        hover_data={
            "City": True,
            "Sports": True,
            "Latitude": False,
            "Longitude": False,
            "Num_Sports": False
        },
        size="Num_Sports",
        size_max=20,
        color="Num_Sports",
        color_continuous_scale="Viridis",
        title="🗺️ Paris 2024 Olympic Venues"
    )
    
    # Set map center and zoom based on view
    if show_all:
        center_lat = 46.5
        center_lon = 2.5
        zoom = 4.5
    else:
        center_lat = 48.86
        center_lon = 2.35
        zoom = 10
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom
        ),
        title={"x": 0.5, "xanchor": "center", "font": {"size": 20}},
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(title="Sports Count")
    )
    
    return fig


def create_venue_table(venues_df):
    """Create a formatted venue table."""
    venue_data = []
    
    for _, row in venues_df.iterrows():
        venue_name = row["venue"]
        sports = parse_sports_list(row.get("sports", ""))
        city = VENUE_COORDINATES.get(venue_name, {}).get("city", "N/A")
        
        venue_data.append({
            "Venue": venue_name,
            "City": city,
            "Sports": ", ".join(sports) if sports else "N/A",
            "Number of Sports": len(sports)
        })
    
    return pd.DataFrame(venue_data).sort_values("Number of Sports", ascending=False)


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Sports & Events - Paris 2024",
        page_icon="🏟️",
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
    st.markdown('<h1 class="main-title">🏟️ Sports and Events</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Explore the competition schedule, venues, and medal distribution across sports. '
        'Discover where the action happened at Paris 2024.</p>',
        unsafe_allow_html=True
    )
    
    # Load data
    schedules_df = load_schedules()
    venues_df = load_venues()
    medals_df = load_medals()
    events_df = load_events()
    nocs_df = load_nocs()
    
    # Create sidebar filters
    selected_countries, selected_sports, medal_types = create_sidebar_filters(
        schedules_df, events_df, nocs_df
    )
    
    # Apply filters to medals
    filtered_medals = filter_medals(medals_df, selected_countries, selected_sports, medal_types)
    
    # Show active filters
    if selected_countries or selected_sports:
        with st.expander("📌 Active Filters", expanded=False):
            if selected_countries:
                st.write(f"**Countries:** {', '.join(selected_countries)}")
            if selected_sports:
                st.write(f"**Sports:** {', '.join(selected_sports)}")
    
    st.markdown("---")
    
    # 1. Event Schedule (Gantt Chart)
    st.subheader("📅 Event Schedule")
    st.markdown("*Explore the timeline of events by sport or venue*")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        filter_type = st.radio(
            "Filter by:",
            ["Sport", "Venue"],
            horizontal=False
        )
        
        if filter_type == "Sport":
            options = sorted(schedules_df["discipline"].dropna().unique().tolist())
            default_idx = options.index("Athletics") if "Athletics" in options else 0
        else:
            options = sorted(schedules_df["venue"].dropna().unique().tolist())
            default_idx = 0
        
        selected_filter = st.selectbox(
            f"Select {filter_type}:",
            options=options,
            index=default_idx
        )
    
    with col2:
        if selected_filter:
            if filter_type == "Sport":
                gantt_chart = create_sport_timeline(schedules_df, selected_filter)
            else:
                gantt_chart = create_event_schedule_gantt(schedules_df, filter_type, selected_filter)
            
            if gantt_chart:
                st.plotly_chart(gantt_chart, use_container_width=True)
            else:
                st.warning(f"No schedule data available for {selected_filter}.")
    
    st.markdown("---")
    
    # 2. Medal Count by Sport
    st.subheader("🏅 Medal Count by Sport")
    
    tab1, tab2 = st.tabs(["🗺️ Treemap View", "📊 Bar Chart View"])
    
    with tab1:
        if len(filtered_medals) > 0:
            treemap = create_medal_treemap(filtered_medals)
            if treemap:
                st.plotly_chart(treemap, use_container_width=True)
            else:
                st.warning("No medal data available.")
        else:
            st.warning("No medals match the selected filters.")
    
    with tab2:
        if len(filtered_medals) > 0:
            bar_chart = create_sport_medal_bar(filtered_medals)
            if bar_chart:
                st.plotly_chart(bar_chart, use_container_width=True)
            else:
                st.warning("No medal data available.")
        else:
            st.warning("No medals match the selected filters.")
    
    st.markdown("---")
    
    # 3. Venue Map
    st.subheader("🗺️ Olympic Venues Map")
    
    col_map1, col_map2 = st.columns([1, 4])
    
    with col_map1:
        map_view = st.radio(
            "Map View:",
            ["Paris Area", "All France"],
            horizontal=False
        )
        
        st.markdown("---")
        st.markdown("**📍 Venue Stats**")
        total_venues = len(venues_df)
        st.metric("Total Venues", total_venues)
        
        # Count sports
        all_sports = set()
        for sports in venues_df["sports"].dropna():
            all_sports.update(parse_sports_list(sports))
        st.metric("Sports Hosted", len(all_sports))
    
    with col_map2:
        show_all = map_view == "All France"
        venue_map = create_venue_map(venues_df, show_all=show_all)
        if venue_map:
            st.plotly_chart(venue_map, use_container_width=True)
        else:
            st.warning("No venue data available.")
    
    # Venue Table
    with st.expander("📋 View All Venues", expanded=False):
        venue_table = create_venue_table(venues_df)
        st.dataframe(
            venue_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Venue": st.column_config.TextColumn("Venue", width="medium"),
                "City": st.column_config.TextColumn("City", width="small"),
                "Sports": st.column_config.TextColumn("Sports", width="large"),
                "Number of Sports": st.column_config.NumberColumn("# Sports", width="small")
            }
        )
    
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

# 🏅 Paris 2024 Olympic Games Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://paris2024olympicgamesdashboardchallengev1-fpatiwwa6xkh6gu7d2pw.streamlit.app/)

An interactive, multi-page Streamlit dashboard for exploring comprehensive data and insights from the **Paris 2024 Summer Olympic Games**. Built as part of the LA28 Volunteer Selection Challenge for the Software Engineering for Data Science module.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52.0-FF4B4B.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75.svg)

---

## 🌐 Live Demo

**[🚀 View Live Dashboard](https://paris2024olympicgamesdashboardchallengev1-fpatiwwa6xkh6gu7d2pw.streamlit.app/)**

---

## 📋 Table of Contents

- [Features](#-features)
- [Pages Overview](#-pages-overview)
- [Installation](#-installation)
- [Running Locally](#-running-locally)
- [Project Structure](#-project-structure)
- [Design Choices](#-design-choices)
- [Creative Features](#-creative-features)
- [Data Sources](#-data-sources)
- [Technologies Used](#-technologies-used)
- [Team](#-team)

---

## ✨ Features

- **📊 Interactive Visualizations**: Choropleth maps, sunbursts, treemaps, bar charts, and more
- **🔍 Global Filters**: Filter by country, sport, continent, and medal type across all pages
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🎨 Modern UI**: Clean, professional design with French flag color themes
- **⚡ Real-time Updates**: All charts react dynamically to filter changes

---

## 📄 Pages Overview

### 1. 🏠 Overview (Home)

The command center providing a high-level summary of the Games:

- **5 Key Performance Indicators** (Athletes, Countries, Sports, Medals, Events)
- **Global Medal Distribution** (Donut Chart)
- **Top 10 Medal Standings** (Stacked Horizontal Bar Chart)

### 2. 🗺️ Global Analysis

Geographical and hierarchical analysis:

- **World Medal Map** (Choropleth)
- **Medal Hierarchy** (Sunburst & Treemap: Continent → Country → Sport)
- **Continent vs. Medals** (Grouped Bar Chart)
- **Top 20 Countries** (Stacked Bar Chart)

### 3. 👤 Athlete Performance

The human story behind the Games:

- **Athlete Profile Card** (Searchable athlete details)
- **Age Distribution** (Violin/Box Plot by gender/sport)
- **Gender Distribution** (Pie/Bar charts by continent/country)
- **Top 10 Athletes by Medals** (Bar Chart with medal breakdown)

### 4. 🏟️ Sports and Events

The competition arena:

- **Event Schedule** (Gantt/Timeline Chart by sport or venue)
- **Medal Count by Sport** (Treemap & Bar Chart)
- **Olympic Venues Map** (Interactive Scatter Mapbox)

### 5. ⚔️ Country Comparison (Creative Feature)

Head-to-head country analysis:

- **Side-by-side Country Cards** with flags and stats
- **Medal Comparison** (Grouped Bar Chart)
- **Performance Radar Chart** (5 metrics comparison)
- **Gender Distribution Comparison** (Dual Pie Charts)
- **Sport-by-Sport Medal Comparison** (Diverging Bar Chart)
- **Top Athletes from Each Country**

### 6. 🎯 Quiz Challenge (Creative Feature)

Interactive knowledge quiz:

- **20 Questions** about Paris 2024 Olympics
- **Scoring System** with achievement levels
- **Instant Feedback** with explanations
- **Results Summary** with answer review

---

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/your-username/paris-2024-olympics-dashboard.git
cd paris-2024-olympics-dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running Locally

1. **Navigate to the project directory:**

   ```bash
   cd /path/to/test_01_seds
   ```

2. **Run the Streamlit application:**

   ```bash
   streamlit run 1_Overview.py
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

### Alternative: Using Python Module

```bash
python -m streamlit run 1_Overview.py
```

---

## 📁 Project Structure

```
test_01_seds/
├── 1_Overview.py                 # Main entry point (Overview page)
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── data/                         # Dataset files
│   ├── athletes.csv              # Athlete information
│   ├── coaches.csv               # Coach information
│   ├── events.csv                # Event details
│   ├── medals.csv                # Individual medal records
│   ├── medals_total.csv          # Medal counts by country
│   ├── medallists.csv            # Medallist details
│   ├── nocs.csv                  # National Olympic Committees
│   ├── schedules.csv             # Event schedules
│   ├── teams.csv                 # Team information
│   ├── venues.csv                # Venue information
│   └── results/                  # Sport-specific results
└── pages/                        # Additional dashboard pages
    ├── 2_Global_Analysis.py      # Global & continental analysis
    ├── 3_Athlete_Performance.py  # Athlete-focused analysis
    ├── 4_Sports_and_Events.py    # Sports & venue analysis
    ├── 5_Country_Comparison.py   # Head-to-head comparison
    └── 6_Quiz_Challenge.py       # Interactive quiz game
```

---

## 🎨 Design Choices

### Color Scheme

- **Primary Colors**: French flag colors (Blue #0055A4, White, Red #EF4135)
- **Medal Colors**: Gold (#FFD700), Silver (#C0C0C0), Bronze (#CD7F32)
- **Accent Colors**: Purple (#6f42c1), Green (#28a745), Teal (#17a2b8)

### Typography & Layout

- Clean, readable fonts with proper contrast
- Wide layout for better visualization display
- Consistent spacing and card-based design
- Responsive columns for organized content

### Visualization Philosophy

- **Interactive**: All charts support hover, zoom, and click interactions
- **Informative**: Tooltips provide detailed information
- **Accessible**: Color-blind friendly palettes where possible
- **Hierarchical**: Drill-down capabilities for complex data

### User Experience

- **Global Filters**: Sidebar filters affect all visualizations on each page
- **Active Filter Display**: Expandable section showing applied filters
- **Consistent Navigation**: Multi-page structure with intuitive page names
- **Loading Optimization**: `@st.cache_data` for efficient data loading

---

## 🌟 Creative Features

### 1. Country Comparison Tool (Page 5)

A comprehensive head-to-head comparison feature allowing users to:

- Select any two countries from a dropdown
- View side-by-side statistics with flag emojis
- Compare performance across multiple dimensions via radar chart
- Analyze sport-by-sport dominance
- See top athletes from each nation

### 2. Interactive Quiz Challenge (Page 6)

A gamified learning experience featuring:

- 20 curated questions about Paris 2024
- Randomized question selection (5-20 questions per game)
- Real-time scoring with instant feedback
- Educational explanations for each answer
- Achievement levels (Olympic Champion, Silver/Bronze Medalist, Participant)
- Complete answer review at the end

### 3. Continent-Level Analysis

Added continental perspective throughout the dashboard:

- Continent filter in sidebar (beyond the required country/sport filters)
- Medal hierarchy showing Continent → Country → Sport
- Continent performance comparison charts
- Country-to-continent mapping for 200+ nations

### 4. Athlete Profile Cards

Rich athlete profiles with:

- Searchable dropdown for 11,000+ athletes
- Avatar placeholder with gender-specific icons
- Flag emojis for country representation
- Physical stats, coach info, birth details
- Multi-sport/event display

### 5. Olympic Venues Interactive Map

Complete venue visualization:

- GPS coordinates for all 36 Olympic venues
- OpenStreetMap integration
- Two view modes: Paris Area and All France (including Tahiti!)
- Marker size based on number of sports hosted
- Expandable venue details table

---

## 📊 Data Sources

This dashboard uses the **Paris 2024 Olympic Summer Games** dataset from Kaggle:

**[https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)**

### Dataset Files Used:

| File               | Description                             | Records |
| ------------------ | --------------------------------------- | ------- |
| `athletes.csv`     | Personal information about all athletes | 11,114  |
| `medals_total.csv` | Medal counts grouped by country         | 93      |
| `medals.csv`       | Individual medal records                | 1,045   |
| `medallists.csv`   | Detailed medallist information          | 2,316   |
| `events.csv`       | All Olympic events                      | 330     |
| `nocs.csv`         | National Olympic Committees             | 225     |
| `schedules.csv`    | Event schedules                         | 3,896   |
| `venues.csv`       | Olympic venue information               | 36      |

---

## 🔧 Technologies Used

- **[Streamlit](https://streamlit.io/)** (v1.52.0) - Web application framework
- **[Pandas](https://pandas.pydata.org/)** (v2.0+) - Data manipulation and analysis
- **[Plotly](https://plotly.com/python/)** (v5.18+) - Interactive visualizations
- **Python 3.9+** - Programming language

### Key Plotly Chart Types:

- `px.choropleth` - World medal map
- `px.sunburst` - Hierarchical medal visualization
- `px.treemap` - Medal distribution by sport
- `px.timeline` - Event schedule Gantt chart
- `px.scatter_mapbox` - Venue locations
- `px.violin` / `px.box` - Age distribution
- `go.Bar` - Various bar charts
- `go.Pie` - Medal distribution
- `go.Scatterpolar` - Radar comparison chart

---

## participant

**Module**: Software Engineering for Data Science  
**Institution**: ESI-SBA  
**Instructor**: Dr. Belkacem KHALDI
**Student**:Dib Mehdi G02

---

## 📝 License

This project is created for educational purposes as part of the LA28 Volunteer Selection Challenge.

---

## 🙏 Acknowledgments

- Paris 2024 Olympic Games organizing committee for inspiring this challenge
- Kaggle for hosting the comprehensive dataset
- Streamlit team for the amazing framework
- Plotly for powerful visualization capabilities

---

<div align="center">

🥇🥈🥉

</div>

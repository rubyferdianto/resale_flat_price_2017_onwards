"""
Comprehensive Singapore Resale Flat Price Analysis Dashboard
Built with Streamlit for interactive data exploration and analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import time
import requests
from data_fetcher import ResaleFlatDataFetcher

# Page configuration
st.set_page_config(
    page_title="Singapore Resale Flat Price Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
    /* Enhanced CSS for right-aligning price columns */
    div[data-testid="stDataFrame"] table tbody tr td:nth-child(5),
    div[data-testid="stDataFrame"] table tbody tr td:nth-child(6),
    .stDataFrame table tbody tr td:nth-child(5),
    .stDataFrame table tbody tr td:nth-child(6) {
        text-align: right !important;
        font-family: monospace !important;
    }
    
    /* Target cells containing S$ currency with higher specificity */
    div[data-testid="stDataFrame"] table tbody tr td:contains("S$"),
    .stDataFrame table tbody tr td:contains("S$") {
        text-align: right !important;
        font-family: monospace !important;
    }
    
    /* Additional targeting for different Streamlit versions */
    [data-testid="stTable"] table tbody tr td:nth-child(5),
    [data-testid="stTable"] table tbody tr td:nth-child(6) {
        text-align: right !important;
        font-family: monospace !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Load data with caching for better performance."""
    try:
        fetcher = ResaleFlatDataFetcher()
        
        # Try to load from CSV first
        df = fetcher.load_from_csv()
        
        # If CSV doesn't exist, fetch from API and save
        if df is None:
            st.info("CSV file not found. Fetching data from API... This may take a moment.")
            data = fetcher.fetch_all_data()
            if data:
                fetcher.save_to_csv(data)
                df = pd.DataFrame(data)
            else:
                st.error("Failed to fetch data from API")
                return None
        
        # Data preprocessing
        if df is not None:
            try:
                # Convert month to datetime
                df['month'] = pd.to_datetime(df['month'])
                
                # Convert resale_price to numeric
                df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')
                
                # Convert floor_area_sqm to numeric
                df['floor_area_sqm'] = pd.to_numeric(df['floor_area_sqm'], errors='coerce')
                
                # Calculate price per sqm
                df['price_per_sqm'] = df['resale_price'] / df['floor_area_sqm']
                
                # Extract year from month
                df['year'] = df['month'].dt.year
                
                # Clean up lease_commence_date
                df['lease_commence_date'] = pd.to_numeric(df['lease_commence_date'], errors='coerce')
                
                # Calculate flat age
                current_year = datetime.now().year
                df['flat_age'] = current_year - df['lease_commence_date']
                
                # Remove rows with missing critical data
                original_count = len(df)
                df = df.dropna(subset=['resale_price', 'floor_area_sqm', 'month'])
                cleaned_count = len(df)
                
                return df
                
            except Exception as e:
                st.error(f"Error processing data: {str(e)}")
                st.error("Please check the data format and try refreshing the data.")
                return None
        
        return None
        
    except Exception as e:
        st.error(f"Critical error loading data: {str(e)}")
        st.error("Please check your environment setup and data files.")
        return None

def refresh_data_from_api():
    """Force refresh data from API, bypassing cache."""
    fetcher = ResaleFlatDataFetcher()
    
    # Create containers for progress display
    progress_container = st.empty()
    status_container = st.empty()
    
    try:
        with progress_container.container():
            # Create progress bar and status text
            progress_bar = st.progress(0)
            
        with status_container.container():
            status_text = st.empty()
            
            status_text.text("🔄 Connecting to data.gov.sg API...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            status_text.text("📡 Fetching latest data from Singapore HDB...")
            progress_bar.progress(20)
            
            # Fetch data with better error handling
            data = fetcher.fetch_all_data()
            progress_bar.progress(70)
            
            if data and len(data) > 0:
                status_text.text(f"💾 Saving {len(data):,} records to local cache...")
                success = fetcher.save_to_csv(data)
                progress_bar.progress(90)
                
                if success:
                    status_text.text("✅ Data refresh completed successfully!")
                    progress_bar.progress(100)
                    time.sleep(1)
                    
                    # Clear Streamlit cache to force reload
                    st.cache_data.clear()
                    
                    # Clean up progress indicators
                    progress_container.empty()
                    status_container.empty()
                    
                    return True
                else:
                    status_text.error("❌ Failed to save data to cache")
                    return False
            else:
                status_text.error("❌ No data received from API")
                return False
                
    except requests.RequestException as e:
        status_container.error(f"❌ Network error: Unable to connect to data.gov.sg API")
        return False
    except Exception as e:
        status_container.error(f"❌ Unexpected error during data refresh: {str(e)}")
        return False
    finally:
        # Clean up after delay
        time.sleep(2)
        progress_container.empty()
        status_container.empty()

def get_data_freshness_info():
    """Get information about when data was last updated."""
    try:
        import json
        with open('data_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        last_updated = pd.to_datetime(metadata['last_updated'])
        days_old = (datetime.now() - last_updated).days
        
        return {
            'last_updated': last_updated,
            'days_old': days_old,
            'total_records': metadata.get('total_records', 'Unknown')
        }
    except:
        return None

def update_sidebar_data_info(data_info_placeholder, df, selected_year="All Years"):
    """Update the sidebar data information based on selected year."""
    # Filter data based on selected year
    if selected_year == "All Years":
        filtered_df = df
        year_suffix = " (All Years)"
    else:
        try:
            filtered_df = df[df['year'] == int(selected_year)]
            year_suffix = f" ({selected_year})"
        except:
            filtered_df = df
            year_suffix = " (All Years)"
    
    # Update session state
    st.session_state.current_selected_year = selected_year
    
    # Update the data information
    with data_info_placeholder.container():
        if len(filtered_df) > 0:
            st.write(f"**Total Records:** {len(filtered_df):,}{year_suffix}")
            st.write(f"**Date Range:** {filtered_df['month'].min().strftime('%Y-%m')} to {filtered_df['month'].max().strftime('%Y-%m')}")
            st.write(f"**Towns:** {filtered_df['town'].nunique()}")
            st.write(f"**Flat Types:** {filtered_df['flat_type'].nunique()}")
        else:
            st.write(f"**No data available for {selected_year}**")
            st.write("Please select a different year.")

def create_overview_metrics(df, year=None):
    """Create overview metrics for the dashboard."""
    if df is None:
        return
    
    # Filter by year if specified
    if year and year != "All Years":
        filtered_df = df[df['year'] == year]
        year_text = f" ({year})"
    else:
        filtered_df = df
        year_text = " (All Years)"
        
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"Total Transactions{year_text}",
            value=f"{len(filtered_df):,}"
        )
    
    with col2:
        avg_price = filtered_df['resale_price'].mean()
        st.metric(
            label=f"Average Price{year_text}",
            value=f"S${avg_price:,.0f}"
        )
    
    with col3:
        avg_price_per_sqm = filtered_df['price_per_sqm'].mean()
        st.metric(
            label=f"Avg Price per sqm{year_text}",
            value=f"S${avg_price_per_sqm:,.0f}"
        )
    
    with col4:
        if year and year != "All Years":
            # For specific year, show month range within that year
            year_data = filtered_df['month']
            if len(year_data) > 0:
                date_range = f"{year_data.min().strftime('%b-%Y')} to {year_data.max().strftime('%b-%Y')}"
            else:
                date_range = f"No data for {year}"
        else:
            # For all years, show full range
            date_range = f"{df['month'].min().strftime('%b-%Y')} to {df['month'].max().strftime('%b-%Y')}"
        st.metric(
            label="Data Period",
            value=date_range
        )

def create_price_trends(df, data_info_placeholder=None):
    """Create price trend visualizations."""
    st.subheader("📈 Price Trends Analysis")
    
    # Year selector for Price Trends Analysis
    col1_filter, col2_filter = st.columns([1, 3])
    with col1_filter:
        available_years = sorted(df['year'].unique(), reverse=True)
        year_options = ["All Years"] + [str(year) for year in available_years]
        
        # Set default to 2025 if available, otherwise "All Years"
        default_index = 0  # Default to "All Years"
        if "2025" in year_options:
            default_index = year_options.index("2025")
        
        selected_year = st.selectbox(
            "Select Year for Price Trends:",
            options=year_options,
            index=default_index,
            key="price_trends_year_filter"
        )
        
        # Update sidebar data information when year changes
        if data_info_placeholder:
            update_sidebar_data_info(data_info_placeholder, df, selected_year)
    
    with col2_filter:
        # Use CSS to align the info message to the bottom
        if selected_year != "All Years":
            info_message = f"📅 Showing price trends for **{selected_year}** only. Switch to 'All Years' for complete trend analysis."
        else:
            info_message = f"📅 Showing price trends for **all available years** ({min(available_years)}-{max(available_years)})"
        
        # Create a container with bottom alignment
        st.markdown(f"""
        <div style="
            height: 80px; 
            display: flex; 
            align-items: flex-end; 
            padding-bottom: 8px;
            margin-top: -10px;
        ">
            <div style="
                background-color: transparent; 
                border: 1px solid transparent; 
                border-radius: 0.375rem; 
                padding: 0.75rem; 
                color: #cc9966;
                width: 100%;
                font-size: 0.875rem;
            ">
                {info_message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data based on selected year
    if selected_year == "All Years":
        filtered_df = df
        year_suffix = " (All Years)"
    else:
        filtered_df = df[df['year'] == int(selected_year)]
        year_suffix = f" ({selected_year})"
    
    # Check if data is available for the selected year
    if len(filtered_df) == 0:
        st.warning(f"⚠️ No data available for {selected_year}")
        return
    
    # Monthly average price trend
    monthly_avg = filtered_df.groupby('month')['resale_price'].mean().reset_index()
    
    fig = px.line(
        monthly_avg,
        x='month',
        y='resale_price',
        title=f'Monthly Average Resale Price Trend{year_suffix}',
        labels={'resale_price': 'Average Resale Price (S$)', 'month': 'Month'}
    )
    fig.update_layout(height=500)
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Price: S$%{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True)
    
    # Price trends by flat type
    col1, col2 = st.columns(2)
    
    with col1:
        flat_type_trends = filtered_df.groupby(['month', 'flat_type'])['resale_price'].mean().reset_index()
        fig = px.line(
            flat_type_trends,
            x='month',
            y='resale_price',
            color='flat_type',
            title=f'Price Trends by Flat Type{year_suffix}',
            labels={'resale_price': 'Average Resale Price (S$)', 'month': 'Month'}
        )
        fig.update_layout(height=400)
        fig.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}<br>Price: S$%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price distribution by flat type
        fig = px.box(
            filtered_df,
            x='flat_type',
            y='resale_price',
            title=f'Price Distribution by Flat Type{year_suffix}'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Price: S$%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)

def create_geographic_analysis(df, data_info_placeholder=None):
    """Create geographic analysis visualizations."""
    st.subheader("🗺️ Geographic Analysis")
    
    # Year selector for Geographic Analysis
    col1_filter, col2_filter = st.columns([1, 3])
    with col1_filter:
        available_years = sorted(df['year'].unique(), reverse=True)
        year_options = ["All Years"] + [str(year) for year in available_years]
        
        # Set default to 2025 if available, otherwise "All Years"
        default_index = 0  # Default to "All Years"
        if "2025" in year_options:
            default_index = year_options.index("2025")
        
        selected_year = st.selectbox(
            "Select Year for Geographic Analysis:",
            options=year_options,
            index=default_index,
            key="geo_year_filter"
        )
        
        # Update sidebar data information when year changes
        if data_info_placeholder:
            update_sidebar_data_info(data_info_placeholder, df, selected_year)
    
    with col2_filter:
        # Use CSS to align the info message to the bottom
        if selected_year != "All Years":
            info_message = f"📅 Showing geographic analysis for **{selected_year}** only. Switch to 'All Years' for complete analysis."
        else:
            info_message = f"📅 Showing geographic analysis for **all available years** ({min(available_years)}-{max(available_years)})"
        
        # Create a container with bottom alignment
        st.markdown(f"""
        <div style="
            height: 80px; 
            display: flex; 
            align-items: flex-end; 
            padding-bottom: 8px;
            margin-top: -10px;
        ">
            <div style="
                background-color: transparent; 
                border: 1px solid transparent; 
                border-radius: 0.375rem; 
                padding: 0.75rem; 
                color: #cc9966;
                width: 100%;
                font-size: 0.875rem;
            ">
                {info_message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data based on selected year
    if selected_year == "All Years":
        filtered_df = df
        year_suffix = " (All Years)"
    else:
        filtered_df = df[df['year'] == int(selected_year)]
        year_suffix = f" ({selected_year})"
    
    # Check if data is available for the selected year
    if len(filtered_df) == 0:
        st.warning(f"⚠️ No data available for {selected_year}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average price by town
        town_avg = filtered_df.groupby('town')['resale_price'].mean().sort_values(ascending=False).head(15)
        
        fig = px.bar(
            x=town_avg.values,
            y=town_avg.index,
            orientation='h',
            title=f'Top 15 Towns by Average Resale Price{year_suffix}',
            labels={'x': 'Average Resale Price (S$)', 'y': 'Town'}
        )
        fig.update_layout(height=500)
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Avg Price: S$%{x:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Transaction volume by town
        town_volume = filtered_df['town'].value_counts().head(15)
        
        fig = px.bar(
            x=town_volume.values,
            y=town_volume.index,
            orientation='h',
            title=f'Top 15 Towns by Transaction Volume{year_suffix}',
            labels={'x': 'Number of Transactions', 'y': 'Town'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def create_flat_analysis(df, data_info_placeholder=None):
    """Create flat-specific analysis."""
    st.subheader("🏢 Flat Analysis")
    
    # Year selector for Flat Analysis
    col1_filter, col2_filter = st.columns([1, 3])
    with col1_filter:
        available_years = sorted(df['year'].unique(), reverse=True)
        year_options = ["All Years"] + [str(year) for year in available_years]
        
        # Set default to 2025 if available, otherwise "All Years"
        default_index = 0  # Default to "All Years"
        if "2025" in year_options:
            default_index = year_options.index("2025")
        
        selected_year = st.selectbox(
            "Select Year for Flat Analysis:",
            options=year_options,
            index=default_index,
            key="flat_analysis_year_filter"
        )
        
        # Update sidebar data information when year changes
        if data_info_placeholder:
            update_sidebar_data_info(data_info_placeholder, df, selected_year)
    
    with col2_filter:
        # Use CSS to align the info message to the bottom
        if selected_year != "All Years":
            info_message = f"📅 Showing flat analysis for **{selected_year}** only. Switch to 'All Years' for complete analysis."
        else:
            info_message = f"📅 Showing flat analysis for **all available years** ({min(available_years)}-{max(available_years)})"
        
        # Create a container with bottom alignment
        st.markdown(f"""
        <div style="
            height: 80px; 
            display: flex; 
            align-items: flex-end; 
            padding-bottom: 8px;
            margin-top: -10px;
        ">
            <div style="
                background-color: transparent; 
                border: 1px solid transparent; 
                border-radius: 0.375rem; 
                padding: 0.75rem; 
                color: #cc9966;
                width: 100%;
                font-size: 0.875rem;
            ">
                {info_message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data based on selected year
    if selected_year == "All Years":
        filtered_df = df
        year_suffix = " (All Years)"
    else:
        filtered_df = df[df['year'] == int(selected_year)]
        year_suffix = f" ({selected_year})"
    
    # Check if data is available for the selected year
    if len(filtered_df) == 0:
        st.warning(f"⚠️ No data available for {selected_year}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Floor Area
        sample_df = filtered_df.sample(n=min(5000, len(filtered_df)))  # Sample for performance
        fig = px.scatter(
            sample_df,
            x='floor_area_sqm',
            y='resale_price',
            color='flat_type',
            title=f'Resale Price vs Floor Area{year_suffix}',
            labels={'floor_area_sqm': 'Floor Area (sqm)', 'resale_price': 'Resale Price (S$)'}
        )
        fig.update_layout(height=400)
        fig.update_traces(hovertemplate='<b>%{fullData.name}</b><br>Area: %{x} sqm<br>Price: S$%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price vs Flat Age
        fig = px.scatter(
            sample_df,
            x='flat_age',
            y='resale_price',
            color='flat_type',
            title=f'Resale Price vs Flat Age{year_suffix}',
            labels={'flat_age': 'Flat Age (years)', 'resale_price': 'Resale Price (S$)'}
        )
        fig.update_layout(height=400)
        fig.update_traces(hovertemplate='<b>%{fullData.name}</b><br>Age: %{x} years<br>Price: S$%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)

def create_market_insights(df, data_info_placeholder=None):
    """Create market insights and statistics."""
    st.subheader("💡 Market Insights")
    
    # Year selector for Market Insights
    col1_filter, col2_filter = st.columns([1, 3])
    with col1_filter:
        available_years = sorted(df['year'].unique(), reverse=True)
        year_options = ["All Years"] + [str(year) for year in available_years]
        
        # Set default to 2025 if available, otherwise "All Years"
        default_index = 0  # Default to "All Years"
        if "2025" in year_options:
            default_index = year_options.index("2025")
        
        selected_year = st.selectbox(
            "Select Year for Market Insights:",
            options=year_options,
            index=default_index,
            key="market_insights_year_filter"
        )
        
        # Update sidebar data information when year changes
        if data_info_placeholder:
            update_sidebar_data_info(data_info_placeholder, df, selected_year)
    
    with col2_filter:
        # Use CSS to align the info message to the bottom
        if selected_year != "All Years":
            info_message = f"📅 Showing market insights for **{selected_year}** only. Switch to 'All Years' for complete market analysis."
        else:
            info_message = f"📅 Showing market insights for **all available years** ({min(available_years)}-{max(available_years)})"
        
        # Create a container with bottom alignment
        st.markdown(f"""
        <div style="
            height: 80px; 
            display: flex; 
            align-items: flex-end; 
            padding-bottom: 8px;
            margin-top: -10px;
        ">
            <div style="
                background-color: transparent; 
                border: 1px solid transparent; 
                border-radius: 0.375rem; 
                padding: 0.75rem; 
                color: #cc9966;
                width: 100%;
                font-size: 0.875rem;
            ">
                {info_message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter data based on selected year
    if selected_year == "All Years":
        filtered_df = df
        year_suffix = " (All Years)"
    else:
        filtered_df = df[df['year'] == int(selected_year)]
        year_suffix = f" ({selected_year})"
    
    # Check if data is available for the selected year
    if len(filtered_df) == 0:
        st.warning(f"⚠️ No data available for {selected_year}")
        return
    
    # Calculate year-over-year changes (only for All Years view)
    if selected_year == "All Years":
        yearly_avg = df.groupby('year')['resale_price'].mean()
        yoy_change = yearly_avg.pct_change().iloc[-1] * 100
    else:
        # For specific year, show comparison with previous year if available
        current_year_data = filtered_df['resale_price'].mean()
        prev_year = int(selected_year) - 1
        prev_year_data = df[df['year'] == prev_year]['resale_price'].mean() if prev_year in df['year'].values else None
        if prev_year_data:
            yoy_change = ((current_year_data - prev_year_data) / prev_year_data) * 100
        else:
            yoy_change = 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"YoY Price Change{year_suffix}",
            value=f"{yoy_change:+.1f}%",
            delta=f"{yoy_change:+.1f}%"
        )
    
    with col2:
        most_expensive_town = filtered_df.groupby('town')['resale_price'].mean().idxmax()
        most_expensive_price = filtered_df.groupby('town')['resale_price'].mean().max()
        st.metric(
            label=f"Most Expensive Town{year_suffix}",
            value=most_expensive_town,
            delta=f"S${most_expensive_price:,.0f}"
        )
    
    with col3:
        most_active_town = filtered_df['town'].value_counts().idxmax()
        most_active_count = filtered_df['town'].value_counts().iloc[0]
        st.metric(
            label=f"Most Active Town{year_suffix}",
            value=most_active_town,
            delta=f"{most_active_count:,} transactions"
        )
    
    # Market summary
    st.write("### 📊 Market Summary")
    
    # Recent trends - adjust based on selected year
    if selected_year == "All Years":
        # Recent trends (last 12 months)
        recent_data = df[df['month'] >= (df['month'].max() - pd.DateOffset(months=12))]
        trend_title = "Recent Price Trends (Last 12 Months)"
        flat_type_title = "Popular Flat Types (Last 12 Months)"
    else:
        # Use the entire selected year
        recent_data = filtered_df
        trend_title = f"Price Trends for {selected_year}"
        flat_type_title = f"Popular Flat Types in {selected_year}"
    
    if len(recent_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            recent_monthly = recent_data.groupby('month')['resale_price'].mean()
            
            fig = px.line(
                x=recent_monthly.index,
                y=recent_monthly.values,
                title=trend_title
            )
            fig.update_layout(height=300)
            fig.update_traces(hovertemplate='<b>%{x}</b><br>Price: S$%{y:,.0f}<extra></extra>')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            recent_flat_types = recent_data['flat_type'].value_counts()
            
            fig = px.pie(
                values=recent_flat_types.values,
                names=recent_flat_types.index,
                title=flat_type_title
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def create_data_explorer(df, data_info_placeholder=None):
    """Create interactive data explorer."""
    st.subheader("🔍 Data Explorer")
    
    # Year filter
    available_years = sorted(df['month'].dt.year.unique(), reverse=True)
    selected_year = st.selectbox(
        "Filter by Year:",
        options=['All Years'] + available_years,
        index=1,  # Default to first year (2025)
        key="data_explorer_year_filter"
    )
    
    # Update sidebar data information when year changes
    if data_info_placeholder:
        update_sidebar_data_info(data_info_placeholder, df, selected_year)
    
    # Apply year filter
    if selected_year != 'All Years':
        df = df[df['month'].dt.year == selected_year]
        year_suffix = f" ({selected_year})"
    else:
        year_suffix = " (All Years)"
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_towns = st.multiselect(
            "Select Towns",
            options=sorted(df['town'].unique()),
            default=[]
        )
    
    with col2:
        selected_flat_types = st.multiselect(
            "Select Flat Types",
            options=sorted(df['flat_type'].unique()),
            default=[]
        )
    
    with col3:
        # Month filter - get unique months and format them in descending order
        unique_months = sorted(df['month'].unique(), reverse=True)  # Most recent first
        month_options = [month.strftime('%b-%Y') for month in unique_months]
        selected_months = st.multiselect(
            "Select Months",
            options=month_options,
            default=[]
        )
    
    with col4:
        price_range = st.slider(
            "Price Range (S$)",
            min_value=int(df['resale_price'].min()),
            max_value=int(df['resale_price'].max()),
            value=(int(df['resale_price'].min()), int(df['resale_price'].max())),
            step=10000,
            format="S$%d"
        )
        
        # Display formatted price range for better readability
        st.caption(f"Selected range: S${price_range[0]:,} - S${price_range[1]:,}")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_towns:
        filtered_df = filtered_df[filtered_df['town'].isin(selected_towns)]
    
    if selected_flat_types:
        filtered_df = filtered_df[filtered_df['flat_type'].isin(selected_flat_types)]
    
    if selected_months:
        # Convert selected month strings back to datetime for filtering
        selected_month_dates = []
        for month_str in selected_months:
            # Parse "Jan-2017" format back to datetime
            try:
                month_date = pd.to_datetime(month_str, format='%b-%Y')
                selected_month_dates.append(month_date)
            except:
                continue
        
        if selected_month_dates:
            filtered_df = filtered_df[filtered_df['month'].isin(selected_month_dates)]
    
    filtered_df = filtered_df[
        (filtered_df['resale_price'] >= price_range[0]) &
        (filtered_df['resale_price'] <= price_range[1])
    ]
    
    if len(filtered_df) > 0:
        st.write(f"**Filtered Results{year_suffix}: {len(filtered_df):,} transactions**")
        
        # Display sample data
        st.write(f"### Sample Data{year_suffix}")
        
        # Download option - moved to top left after Sample Data heading
        csv = filtered_df.to_csv(index=False)
        filename_suffix = f"_{selected_year}" if selected_year != 'All Years' else "_all_years"
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"filtered_resale_data{filename_suffix}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Sorting and pagination controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            sort_column = st.selectbox(
                "Sort by:",
                options=['month', 'town', 'flat_type', 'floor_area_sqm', 'resale_price', 'price_per_sqm'],
                index=0,  # Default to month
                format_func=lambda x: {
                    'month': 'Month',
                    'town': 'Town',
                    'flat_type': 'Flat Type',
                    'floor_area_sqm': 'Floor Area (sqm)',
                    'resale_price': 'Resale Price',
                    'price_per_sqm': 'Price per sqm'
                }[x]
            )
        
        with col2:
            sort_order = st.selectbox(
                "Order:",
                options=['desc', 'asc'],
                index=0,  # Default to descending
                format_func=lambda x: 'Descending' if x == 'desc' else 'Ascending'
            )
        
        with col3:
            # Calculate total pages
            records_per_page = 15
            total_records = len(filtered_df)
            total_pages = (total_records - 1) // records_per_page + 1 if total_records > 0 else 1
            
            page_number = st.selectbox(
                "Page:",
                options=list(range(1, total_pages + 1)),
                format_func=lambda x: f"Page {x} of {total_pages}"
            )
        
        # Apply sorting - always sort by month first (descending), then by selected column
        ascending = sort_order == 'asc'
        
        if sort_column == 'month':
            # If month is selected, sort by month and then by resale_price (both descending)
            sorted_df = filtered_df.sort_values(by=['month', 'resale_price'], ascending=[False, False])
        else:
            # For other columns, sort by month first (descending), then by selected column
            sorted_df = filtered_df.sort_values(by=['month', sort_column], ascending=[False, ascending])
        
        # Apply pagination
        start_idx = (page_number - 1) * records_per_page
        end_idx = start_idx + records_per_page
        
        display_columns = ['month', 'town', 'flat_type', 'block', 'street_name', 'storey_range', 
                          'floor_area_sqm', 'flat_model', 'lease_commence_date', 'remaining_lease', 
                          'resale_price', 'price_per_sqm']
        
        # Format the display dataframe with custom styling
        display_df = sorted_df[display_columns].iloc[start_idx:end_idx].copy()
        
        # Show pagination info
        st.write(f"**Showing records {start_idx + 1}-{min(end_idx, total_records)} of {total_records:,} total records**")
        
        # Format the month column to display as "Jan-2017" format
        display_df['month'] = display_df['month'].dt.strftime('%b-%Y')
        
        # Format floor area - convert to integer if it's a whole number, otherwise keep as float
        def format_floor_area(val):
            if pd.isna(val):
                return ''
            if isinstance(val, (int, float)):
                # Check if it's a whole number (no decimal part)
                if val == int(val):
                    return str(int(val))
                else:
                    return f"{val:.1f}"  # Keep one decimal place if needed
            return str(val)
        
        display_df['floor_area_sqm'] = display_df['floor_area_sqm'].apply(format_floor_area)
        
        # Create styled dataframe using pandas styling
        def style_price_columns(val):
            if pd.isna(val):
                return ''
            if isinstance(val, (int, float)):
                return f"S${val:,.0f}"
            return str(val)
        
        # Apply formatting and create styled version
        styled_df = display_df.copy()
        styled_df['resale_price'] = styled_df['resale_price'].apply(style_price_columns)
        styled_df['price_per_sqm'] = styled_df['price_per_sqm'].apply(style_price_columns)
        
        # Rename columns for better display
        styled_df = styled_df.rename(columns={
            'month': 'Month',
            'town': 'Town', 
            'flat_type': 'Flat Type',
            'block': 'Block',
            'street_name': 'Street Name',
            'storey_range': 'Storey Range',
            'floor_area_sqm': 'Floor Area (sqm)',
            'flat_model': 'Flat Model',
            'lease_commence_date': 'Lease Start Year',
            'remaining_lease': 'Remaining Lease',
            'resale_price': 'Resale Price',
            'price_per_sqm': 'Price per sqm'
        })
        
        # Style the dataframe with pandas styler
        def highlight_price_cols(s):
            styles = [''] * len(s)
            for i, col in enumerate(s.index):
                if 'Price' in col:
                    styles[i] = 'text-align: right; font-family: monospace;'
            return styles
        
        styled = styled_df.style.apply(highlight_price_cols, axis=1)
        
        # Create HTML table with proper alignment for price columns
        def create_aligned_table(df):
            if len(df) == 0:
                return '<p style="text-align: center; color: #666; font-style: italic;">No records to display on this page.</p>'
            
            html = '<table style="width: 100%; border-collapse: collapse;">'
            
            # Header with transparent background and red text
            html += '<thead><tr style="background-color: transparent;">'
            for col in df.columns:
                html += f'<th style="padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent; color: #dc3545; font-weight: bold;">{col}</th>'
            html += '</tr></thead>'
            
            # Body
            html += '<tbody>'
            for _, row in df.iterrows():
                html += '<tr>'
                for i, (col, value) in enumerate(row.items()):
                    # Right align price columns and Floor Area column
                    if 'Price' in col or 'Floor Area' in col:
                        style = 'padding: 8px; text-align: right; font-family: monospace; border: 1px solid #ddd; background-color: transparent;'
                    else:
                        style = 'padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent;'
                    html += f'<td style="{style}">{value}</td>'
                html += '</tr>'
            html += '</tbody></table>'
            return html
        
        # Use the HTML table for perfect alignment
        st.markdown(create_aligned_table(styled_df), unsafe_allow_html=True)
        
        # Enhanced JavaScript for right alignment
        st.markdown("""
        <script>
        function forceAlignPriceColumns() {
            // Wait for DOM to be ready
            setTimeout(function() {
                // Find the dataframe container
                const dataframes = document.querySelectorAll('[data-testid="stDataFrame"]');
                
                dataframes.forEach(df => {
                    const table = df.querySelector('table');
                    if (!table) return;
                    
                    // Get all header cells to find price columns
                    const headerCells = table.querySelectorAll('thead tr th');
                    let priceColumnIndices = [];
                    
                    headerCells.forEach((header, index) => {
                        const headerText = header.textContent || '';
                        if (headerText.includes('Resale Price') || headerText.includes('Price per sqm')) {
                            priceColumnIndices.push(index);
                        }
                    });
                    
                    // Apply styles to data rows
                    const dataRows = table.querySelectorAll('tbody tr');
                    dataRows.forEach(row => {
                        const cells = row.querySelectorAll('td');
                        
                        // Method 1: By column index
                        priceColumnIndices.forEach(colIndex => {
                            if (cells[colIndex]) {
                                cells[colIndex].style.cssText = 'text-align: right !important; font-family: monospace !important; font-weight: normal !important;';
                            }
                        });
                        
                        // Method 2: By content (cells containing S$)
                        cells.forEach(cell => {
                            if (cell.textContent && cell.textContent.includes('S$')) {
                                cell.style.cssText = 'text-align: right !important; font-family: monospace !important; font-weight: normal !important;';
                            }
                        });
                    });
                    
                    // Force style application with highest specificity
                    const style = document.createElement('style');
                    style.textContent = `
                        [data-testid="stDataFrame"] table tbody tr td:nth-child(5),
                        [data-testid="stDataFrame"] table tbody tr td:nth-child(6) {
                            text-align: right !important;
                            font-family: monospace !important;
                        }
                    `;
                    document.head.appendChild(style);
                });
            }, 100);
        }
        
        // Run multiple times to catch all rendering states
        forceAlignPriceColumns();
        setTimeout(forceAlignPriceColumns, 200);
        setTimeout(forceAlignPriceColumns, 500);
        setTimeout(forceAlignPriceColumns, 1000);
        
        // Watch for changes
        const observer = new MutationObserver(forceAlignPriceColumns);
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """, unsafe_allow_html=True)
        
        # Year filter info
        st.markdown(
            f'<div style="text-align: right; color: #666; font-size: 0.9em; margin-top: 10px;">Showing data for {selected_year if selected_year != "All Years" else "all years"}</div>',
            unsafe_allow_html=True
        )
        
        # Map visualization with displayed table records - moved to bottom
        st.write(f"### 🗺️ Map Explorer (Showing Table Records)")
        
        # Use the same paginated and sorted data that's displayed in the table
        map_data = sorted_df.iloc[start_idx:end_idx].copy()
        
        # Create approximate coordinates for Singapore towns (you can enhance this with actual geocoding)
        town_coordinates = {
            'ANG MO KIO': {'lat': 1.3691, 'lon': 103.8454},
            'BEDOK': {'lat': 1.3236, 'lon': 103.9273},
            'BISHAN': {'lat': 1.3506, 'lon': 103.8484},
            'BUKIT BATOK': {'lat': 1.3587, 'lon': 103.7454},
            'BUKIT MERAH': {'lat': 1.2797, 'lon': 103.8120},
            'BUKIT PANJANG': {'lat': 1.3774, 'lon': 103.7718},
            'BUKIT TIMAH': {'lat': 1.3294, 'lon': 103.8008},
            'CENTRAL AREA': {'lat': 1.2867, 'lon': 103.8545},
            'CHOA CHU KANG': {'lat': 1.3840, 'lon': 103.7470},
            'CLEMENTI': {'lat': 1.3162, 'lon': 103.7649},
            'GEYLANG': {'lat': 1.3201, 'lon': 103.8918},
            'HOUGANG': {'lat': 1.3613, 'lon': 103.8936},
            'JURONG EAST': {'lat': 1.3329, 'lon': 103.7436},
            'JURONG WEST': {'lat': 1.3404, 'lon': 103.7090},
            'KALLANG/WHAMPOA': {'lat': 1.3083, 'lon': 103.8635},
            'MARINE PARADE': {'lat': 1.3020, 'lon': 103.9067},
            'PASIR RIS': {'lat': 1.3721, 'lon': 103.9474},
            'PUNGGOL': {'lat': 1.4012, 'lon': 103.9020},
            'QUEENSTOWN': {'lat': 1.2950, 'lon': 103.7857},
            'SEMBAWANG': {'lat': 1.4491, 'lon': 103.8185},
            'SENGKANG': {'lat': 1.3868, 'lon': 103.8914},
            'SERANGOON': {'lat': 1.3554, 'lon': 103.8697},
            'TAMPINES': {'lat': 1.3496, 'lon': 103.9568},
            'TOA PAYOH': {'lat': 1.3343, 'lon': 103.8563},
            'WOODLANDS': {'lat': 1.4382, 'lon': 103.7890},
            'YISHUN': {'lat': 1.4304, 'lon': 103.8354}
        }
        
        # Add coordinates to map data
        map_data['lat'] = map_data['town'].map(lambda x: town_coordinates.get(x, {'lat': 1.3521})['lat'])
        map_data['lon'] = map_data['town'].map(lambda x: town_coordinates.get(x, {'lon': 103.8198})['lon'])
        
        # Add some random offset to avoid overlapping points
        import numpy as np
        np.random.seed(42)  # For consistent results
        map_data['lat'] += np.random.normal(0, 0.005, len(map_data))  # Small random offset
        map_data['lon'] += np.random.normal(0, 0.005, len(map_data))
        
        # Create the map
        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            color='resale_price',
            size='floor_area_sqm',
            hover_name='town',
            hover_data={
                'flat_type': True,
                'resale_price': ':$,.0f',
                'floor_area_sqm': ':.0f',
                'price_per_sqm': ':$,.0f',
                'month': True,
                'lat': False,
                'lon': False
            },
            color_continuous_scale='Viridis',
            size_max=20,
            zoom=10,
            center={'lat': 1.3521, 'lon': 103.8198},  # Singapore center
            mapbox_style='open-street-map',
            title=f'Resale Flat Locations and Prices (Showing Table Records Page {page_number}){year_suffix}',
            labels={
                'resale_price': 'Resale Price (S$)',
                'floor_area_sqm': 'Floor Area (sqm)',
                'price_per_sqm': 'Price per sqm (S$)'
            }
        )
        
        fig_map.update_layout(
            height=500,
            margin={'r': 0, 't': 30, 'l': 0, 'b': 0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning(f"No data matches the selected filters{year_suffix.lower()}.")

def main():
    """Main Streamlit application."""
    st.markdown('<h1 class="main-header">🏠 Singapore Resale Flat Price Analysis</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check your internet connection and try again.")
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Overview", "Price Trends", "Geographic Analysis", "Flat Analysis", "Market Insights", "Data Explorer"]
    )
    
    # Initialize session state for selected year tracking across pages
    if 'current_selected_year' not in st.session_state:
        st.session_state.current_selected_year = "All Years"
    
    # Create empty placeholder for compatibility (no longer used)
    data_info_placeholder = st.empty()
    
    # Smart Data Refresh Section - Check if refresh is needed
    current_date = datetime.now()
    current_month = current_date.replace(day=1)  # First day of current month
    last_data_month = df['month'].max()
    
    # Calculate months behind
    months_behind = (current_month.year - last_data_month.year) * 12 + (current_month.month - last_data_month.month)
    
    # Data is outdated if it's from a previous month
    data_is_outdated = months_behind > 0
    
    if data_is_outdated:
        st.sidebar.markdown("---")
        st.sidebar.write("### 🔄 Data Update Available")
        
        # Show data freshness info based on calculated months_behind
        if months_behind == 1:
            st.sidebar.warning(f"📅 Data is 1 month behind (latest: {last_data_month.strftime('%b %Y')})")
        else:
            st.sidebar.error(f"📅 Data is {months_behind} months behind (latest: {last_data_month.strftime('%b %Y')})")
        
        st.sidebar.info(f"💡 Current month: {current_month.strftime('%b %Y')}")
        
        # Initialize session state for refresh confirmation
        if 'show_refresh_warning' not in st.session_state:
            st.session_state.show_refresh_warning = False
        
        # Refresh button - only enabled when data is outdated
        if st.sidebar.button("🔄 Refresh Data from API", help="Fetch the latest data from data.gov.sg"):
            st.session_state.show_refresh_warning = True
        
        # Show warning and confirmation if button was clicked
        if st.session_state.show_refresh_warning:
            st.sidebar.warning("⚠️ **Warning**: This will fetch fresh data from the API.")
            st.sidebar.write("**This process will:**")
            st.sidebar.write("• Take 1-2 minutes to complete")
            st.sidebar.write("• Download all latest records")
            st.sidebar.write("• Replace your current cache")
            
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                if st.button("✅ Continue", key="confirm_refresh"):
                    st.session_state.show_refresh_warning = False
                    
                    # Show refresh process
                    with st.spinner("🔄 Refreshing data from API..."):
                        refresh_container = st.container()
                        with refresh_container:
                            if refresh_data_from_api():
                                st.success("✅ **Data refreshed successfully!**")
                                st.info("🔄 **Please refresh your browser** to see the updated data.")
                                st.balloons()
                                # Auto-refresh the page after 3 seconds
                                time.sleep(3)
                                st.rerun()
                            else:
                                st.error("❌ **Data refresh failed.** Please try again later.")
            
            with col2:
                if st.button("❌ Cancel", key="cancel_refresh"):
                    st.session_state.show_refresh_warning = False
                    st.sidebar.info("Data refresh cancelled.")
                    st.rerun()
    else:
        # Data is current but show refresh button with special warning (0 months behind)
        st.sidebar.markdown("---")
        st.sidebar.write("### 🔄 Data Management")
        st.sidebar.success(f"📅 Data is current (latest: {last_data_month.strftime('%b %Y')})")
        
        # Use the already calculated months_behind
        if months_behind == 0:
            # Initialize session state for special refresh warning
            if 'show_current_month_warning' not in st.session_state:
                st.session_state.show_current_month_warning = False
            
            # Show refresh button even when current
            if st.sidebar.button("🔄 Refresh Data from API", help="Check for any new data from data.gov.sg"):
                st.session_state.show_current_month_warning = True
            
            # Show special warning for current month refresh
            if st.session_state.show_current_month_warning:
                st.sidebar.warning("⚠️ **Data is already current for this month**")
                st.sidebar.info("📅 **New data will be available next month only**")
                st.sidebar.write("**Note:** Refreshing now may not fetch new records since HDB updates monthly.")
                
                col1, col2 = st.sidebar.columns(2)
                
                with col1:
                    if st.button("🚫 Understood", key="acknowledge_current"):
                        st.session_state.show_current_month_warning = False
                        st.sidebar.info("💡 Try refreshing next month for new data.")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", key="cancel_current_refresh"):
                        st.session_state.show_current_month_warning = False
                        st.rerun()
        else:
            # Data is somehow ahead (shouldn't happen normally)
            st.sidebar.info("🔒 Refresh is disabled - data is up to date")
    
    # API Info
    st.sidebar.markdown("---")
    st.sidebar.write("### 📡 API Information")
    st.sidebar.write("**Source:** data.gov.sg")
    st.sidebar.write("**Update Frequency:** Monthly by HDB")
    st.sidebar.write("**Dataset:** Resale Flat Prices (2017 onwards)")
    
    # Main content based on selection
    if page == "Overview":
        st.write("## 📊 Dataset Overview")
        
        # Year selector for Overview
        col1, col2 = st.columns([1, 3])
        with col1:
            available_years = sorted(df['year'].unique(), reverse=True)
            year_options = ["All Years"] + [str(year) for year in available_years]
            
            # Set default to 2025 if available, otherwise "All Years"
            default_index = 0  # Default to "All Years"
            if "2025" in year_options:
                default_index = year_options.index("2025")
            
            selected_year = st.selectbox(
                "Select Year for Analysis:",
                options=year_options,
                index=default_index
            )
            
            # Update sidebar data information when year changes
            update_sidebar_data_info(data_info_placeholder, df, selected_year)
        
        with col2:
            # Use CSS to align the info message to the bottom
            if selected_year != "All Years":
                info_message = f"📅  Showing analysis for **{selected_year}** only. Switch to 'All Years' for complete dataset overview."
            else:
                info_message = f"📅  Showing analysis for **all available years** ({min(available_years)}-{max(available_years)})"
            
            # Create a container with bottom alignment
            st.markdown(f"""
            <div style="
                height: 80px; 
                display: flex; 
                align-items: flex-end; 
                padding-bottom: 8px;
                margin-top: -10px;
            ">
                <div style="
                    background-color: transparent; 
                    border: 1px solid transparent; 
                    border-radius: 0.375rem; 
                    padding: 0.75rem; 
                    color: #cc9966;
                    width: 100%;
                    font-size: 0.875rem;
                ">
                    {info_message}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Create metrics with year filter
        if selected_year == "All Years":
            create_overview_metrics(df)
            filtered_df_for_stats = df
        else:
            create_overview_metrics(df, int(selected_year))
            filtered_df_for_stats = df[df['year'] == int(selected_year)]
        
        # Basic statistics
        st.write("### 📈 Basic Statistics")
        
        # Show data availability message for specific years
        if selected_year != "All Years" and len(filtered_df_for_stats) == 0:
            st.warning(f"⚠️ No data available for {selected_year}")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            year_suffix = f" ({selected_year})" if selected_year != "All Years" else " (All Years)"
            st.write(f"**Price Statistics{year_suffix}**")
            price_stats = filtered_df_for_stats['resale_price'].describe()
            # Remove count from statistics and format price statistics with commas
            price_stats = price_stats.drop('count')
            price_stats_formatted = price_stats.apply(lambda x: f"S${x:,.0f}")
            
            # Create custom HTML table for proper alignment (same as Data Explorer)
            def create_price_stats_table(stats_series):
                html = '<table style="width: 70%; border-collapse: collapse; margin: 0; padding: 0;">'
                
                # Header with red styling and optimized column widths
                html += '<thead><tr style="background-color: transparent;">'
                html += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent; color: #dc3545; font-weight: bold; width: 20%;">Statistic</th>'
                html += '<th style="padding: 8px; text-align: right; border: 1px solid #ddd; background-color: transparent; color: #dc3545; font-weight: bold; width: 80%;">Resale Price</th>'
                html += '</tr></thead>'
                
                # Body
                html += '<tbody>'
                for stat_name, value in stats_series.items():
                    html += '<tr>'
                    html += f'<td style="padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent; width: 20%;">{stat_name}</td>'
                    html += f'<td style="padding: 8px 16px; text-align: right; font-family: monospace; border: 1px solid #ddd; background-color: transparent; width: 80%;">{value}</td>'
                    html += '</tr>'
                html += '</tbody></table>'
                return html
            
            st.markdown(create_price_stats_table(price_stats_formatted), unsafe_allow_html=True)
        
        with col2:
            st.write(f"**Floor Area Statistics{year_suffix}**")
            area_stats = filtered_df_for_stats['floor_area_sqm'].describe()
            # Remove count from statistics and format area statistics with proper units and smart decimal handling
            area_stats = area_stats.drop('count')
            def format_area_value(x):
                if x == int(x):  # If it's a whole number
                    return f"{int(x)} sqm"
                else:  # If it has decimal places
                    return f"{x:.1f} sqm"
            
            area_stats_formatted = area_stats.apply(format_area_value)
            
            # Create custom HTML table for proper alignment (same as Price Statistics)
            def create_area_stats_table(stats_series):
                html = '<table style="width: 70%; border-collapse: collapse; margin: 0; padding: 0;">'
                
                # Header with red styling and optimized column widths
                html += '<thead><tr style="background-color: transparent;">'
                html += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent; color: #dc3545; font-weight: bold; width: 20%;">Statistic</th>'
                html += '<th style="padding: 8px; text-align: right; border: 1px solid #ddd; background-color: transparent; color: #dc3545; font-weight: bold; width: 80%;">Floor Area</th>'
                html += '</tr></thead>'
                
                # Body
                html += '<tbody>'
                for stat_name, value in stats_series.items():
                    html += '<tr>'
                    html += f'<td style="padding: 8px; text-align: left; border: 1px solid #ddd; background-color: transparent; width: 20%;">{stat_name}</td>'
                    html += f'<td style="padding: 8px 16px; text-align: right; font-family: monospace; border: 1px solid #ddd; background-color: transparent; width: 80%;">{value}</td>'
                    html += '</tr>'
                html += '</tbody></table>'
                return html
            
            st.markdown(create_area_stats_table(area_stats_formatted), unsafe_allow_html=True)
    
    elif page == "Price Trends":
        # Get the data info placeholder from main function scope
        create_price_trends(df, data_info_placeholder)
    
    elif page == "Geographic Analysis":
        create_geographic_analysis(df, data_info_placeholder)
    
    elif page == "Flat Analysis":
        create_flat_analysis(df, data_info_placeholder)
    
    elif page == "Market Insights":
        create_market_insights(df, data_info_placeholder)
    
    elif page == "Data Explorer":
        create_data_explorer(df, data_info_placeholder)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Data source: <a href='https://data.gov.sg'>data.gov.sg</a> | 
            Built using Streamlit | 
            Last updated: {}</p>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M")),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

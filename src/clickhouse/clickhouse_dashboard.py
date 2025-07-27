import clickhouse_connect
import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="ClickStream Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize ClickHouse connection
@st.cache_resource
def init_clickhouse_client():
    """Initialize ClickHouse client with caching"""
    return clickhouse_connect.get_client(
        host=os.environ['CLICKHOUSE_HOST'],
        user=os.environ['CLICKHOUSE_USER'],
        password=os.environ['CLICKHOUSE_PASSWORD'],
        secure=False  # Set to True if using HTTPS
    )


@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_total_metrics():
    """Fetch overall metrics"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        COUNT(*) as total_interactions,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(DISTINCT item_id) as unique_items,
        SUM(CASE WHEN interaction_type = 'click' THEN 1 ELSE 0 END) as total_clicks,
        SUM(CASE WHEN interaction_type = 'view' THEN 1 ELSE 0 END) as total_views,
        SUM(CASE WHEN interaction_type = 'purchase' THEN 1 ELSE 0 END) as total_purchases
    FROM default.clickstream_data
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

@st.cache_data(ttl=30)
def fetch_interaction_breakdown():
    """Fetch interaction type breakdown"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        interaction_type,
        COUNT(*) as count
    FROM default.clickstream_data
    GROUP BY interaction_type
    ORDER BY count DESC
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

@st.cache_data(ttl=30)
def fetch_top_items():
    """Fetch top items by interaction type"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        item_id,
        interaction_type,
        COUNT(*) as interactions
    FROM default.clickstream_data
    GROUP BY item_id, interaction_type
    ORDER BY interactions DESC
    LIMIT 20
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

@st.cache_data(ttl=30)
def fetch_user_activity():
    """Fetch user activity metrics"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        user_id,
        COUNT(*) as total_interactions,
        SUM(CASE WHEN interaction_type = 'click' THEN 1 ELSE 0 END) as clicks,
        SUM(CASE WHEN interaction_type = 'view' THEN 1 ELSE 0 END) as views,
        SUM(CASE WHEN interaction_type = 'purchase' THEN 1 ELSE 0 END) as purchases
    FROM default.clickstream_data
    GROUP BY user_id
    ORDER BY total_interactions DESC
    LIMIT 20
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

@st.cache_data(ttl=30)
def fetch_time_series():
    """Fetch time series data"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        substring(timestamp, 1, 10) as date,
        interaction_type,
        COUNT(*) as interactions
    FROM default.clickstream_data
    GROUP BY date, interaction_type
    ORDER BY date, interaction_type
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

@st.cache_data(ttl=30)
def fetch_conversion_funnel():
    """Fetch conversion funnel data"""
    client = init_clickhouse_client()
    query = """
    SELECT 
        item_id,
        SUM(CASE WHEN interaction_type = 'click' THEN 1 ELSE 0 END) as clicks,
        SUM(CASE WHEN interaction_type = 'view' THEN 1 ELSE 0 END) as views,
        SUM(CASE WHEN interaction_type = 'purchase' THEN 1 ELSE 0 END) as purchases
    FROM default.clickstream_data
    GROUP BY item_id
    HAVING clicks > 0 OR views > 0 OR purchases > 0
    ORDER BY purchases DESC
    LIMIT 20
    """
    result = client.query(query)
    return pd.DataFrame(result.result_rows, columns=result.column_names)

# Main dashboard
def main():
    # Header
    st.title("📊 ClickStream Analytics Dashboard")
    st.markdown("Real-time analytics for user interactions")
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=True)
    refresh_button = st.sidebar.button("🔄 Refresh Now")
    
    if auto_refresh:
        # Auto refresh every 30 seconds
        time.sleep(30)
        st.rerun()
    
    if refresh_button:
        st.cache_data.clear()
        st.rerun()
    
    # Fetch data
    try:
        metrics_df = fetch_total_metrics()
        interaction_df = fetch_interaction_breakdown()
        top_items_df = fetch_top_items()
        user_activity_df = fetch_user_activity()
        time_series_df = fetch_time_series()
        funnel_df = fetch_conversion_funnel()
        
        # Key Metrics Row
        st.header("📈 Key Metrics")
        if not metrics_df.empty:
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("Total Interactions", 
                         f"{metrics_df.iloc[0]['total_interactions']:,}")
            with col2:
                st.metric("Unique Users", 
                         f"{metrics_df.iloc[0]['unique_users']:,}")
            with col3:
                st.metric("Unique Items", 
                         f"{metrics_df.iloc[0]['unique_items']:,}")
            with col4:
                st.metric("Total Clicks", 
                         f"{metrics_df.iloc[0]['total_clicks']:,}")
            with col5:
                st.metric("Total Views", 
                         f"{metrics_df.iloc[0]['total_views']:,}")
            with col6:
                st.metric("Total Purchases", 
                         f"{metrics_df.iloc[0]['total_purchases']:,}")
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Interaction Type Distribution")
            if not interaction_df.empty:
                fig_pie = px.pie(interaction_df, 
                               values='count', 
                               names='interaction_type',
                               color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📊 Interaction Volume")
            if not interaction_df.empty:
                fig_bar = px.bar(interaction_df, 
                               x='interaction_type', 
                               y='count',
                               color='interaction_type',
                               color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Top Items by Interactions")
            if not top_items_df.empty:
                # Pivot the data for better visualization
                pivot_items = top_items_df.pivot_table(
                    index='item_id', 
                    columns='interaction_type', 
                    values='interactions', 
                    fill_value=0
                ).head(10)
                
                fig_items = px.bar(pivot_items, 
                                 barmode='group',
                                 color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
                fig_items.update_layout(xaxis_title="Item ID", yaxis_title="Interactions")
                st.plotly_chart(fig_items, use_container_width=True)
        
        with col2:
            st.subheader("👥 Top Active Users")
            if not user_activity_df.empty:
                top_users = user_activity_df.head(10)
                fig_users = px.bar(top_users, 
                                 x='user_id', 
                                 y='total_interactions',
                                 color='total_interactions',
                                 color_continuous_scale='viridis')
                fig_users.update_layout(xaxis_title="User ID", yaxis_title="Total Interactions")
                st.plotly_chart(fig_users, use_container_width=True)
        
        # Time Series Chart
        st.subheader("📅 Daily Interaction Trends")
        if not time_series_df.empty:
            fig_time = px.line(time_series_df, 
                             x='date', 
                             y='interactions', 
                             color='interaction_type',
                             color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            fig_time.update_layout(xaxis_title="Date", yaxis_title="Interactions")
            st.plotly_chart(fig_time, use_container_width=True)
        
        # Conversion Funnel
        st.subheader("🔄 Item Conversion Funnel (Top 10 Items)")
        if not funnel_df.empty:
            funnel_top = funnel_df.head(10)
            
            fig_funnel = make_subplots(
                rows=1, cols=1,
                specs=[[{"secondary_y": False}]]
            )
            
            fig_funnel.add_trace(
                go.Bar(name='Clicks', x=funnel_top['item_id'], y=funnel_top['clicks'], 
                      marker_color='#FF6B6B'),
            )
            fig_funnel.add_trace(
                go.Bar(name='Views', x=funnel_top['item_id'], y=funnel_top['views'], 
                      marker_color='#4ECDC4'),
            )
            fig_funnel.add_trace(
                go.Bar(name='Purchases', x=funnel_top['item_id'], y=funnel_top['purchases'], 
                      marker_color='#45B7D1'),
            )
            
            fig_funnel.update_layout(
                title="Clicks → Views → Purchases by Item",
                xaxis_title="Item ID",
                yaxis_title="Count",
                barmode='group'
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Data Tables
        st.header("📋 Detailed Data")
        
        tab1, tab2, tab3 = st.tabs(["User Activity", "Item Performance", "Recent Data"])
        
        with tab1:
            st.subheader("User Activity Summary")
            st.dataframe(user_activity_df, use_container_width=True)
        
        with tab2:
            st.subheader("Item Performance")
            if not top_items_df.empty:
                item_summary = top_items_df.pivot_table(
                    index='item_id',
                    columns='interaction_type',
                    values='interactions',
                    fill_value=0
                ).reset_index()
                st.dataframe(item_summary, use_container_width=True)
        
        with tab3:
            st.subheader("Recent Interactions")
            client = init_clickhouse_client()
            recent_query = """
            SELECT * FROM default.clickstream_data 
            ORDER BY timestamp DESC 
            LIMIT 100
            """
            recent_result = client.query(recent_query)
            recent_df = pd.DataFrame(recent_result.result_rows, columns=recent_result.column_names)
            st.dataframe(recent_df, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        st.error(f"Error connecting to ClickHouse: {str(e)}")
        st.info("Please ensure ClickHouse is running and environment variables are set:")
        st.code("""
        export CLICKHOUSE_HOST="your_host"
        export CLICKHOUSE_USER="your_user"  
        export CLICKHOUSE_PASSWORD="your_password"
        """)

if __name__ == "__main__":
    main()








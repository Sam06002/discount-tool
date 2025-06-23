import pandas as pd
import plotly.express as px
import streamlit as st
from typing import Union, Dict, Any

def load_excel_data(uploaded_file) -> pd.DataFrame:
    """
    Load and validate the uploaded Excel file.
    
    Args:
        uploaded_file: Uploaded file object from Streamlit
        
    Returns:
        pd.DataFrame: Processed DataFrame with standardized column names
    """
    # Read the Excel file
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        raise
    
    # Standardize column names (case-insensitive)
    column_mapping = {
        'customer_name': ['customer_name', 'name', 'customer name', 'full name'],
        'phone': ['phone', 'mobile', 'contact', 'phone number', 'mobile number'],
        'email': ['email', 'email address', 'e-mail'],
        'total_orders': ['total_orders', 'order_count', 'orders', 'number of orders'],
        'total_spent': ['total_spent', 'total_amount', 'amount', 'total spending'],
        'last_order_date': ['last_order_date', 'last_order', 'order_date', 'date of last order'],
        'avg_order_value': ['avg_order_value', 'average_order_value', 'aov']
    }
    
    # Create a mapping of original column names to standardized names
    standardized_columns = {}
    for std_name, possible_names in column_mapping.items():
        for col in df.columns:
            if col.lower() in [name.lower() for name in possible_names]:
                standardized_columns[col] = std_name
                break
    
    # Rename columns
    df = df.rename(columns=standardized_columns)
    
    # Ensure required columns exist
    required_columns = ['total_orders', 'total_spent', 'last_order_date']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.error("Please ensure your file contains columns for: "
                "total orders, total spent, and last order date.")
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Ensure customer_name and phone have reasonable defaults if missing
    if 'customer_name' not in df.columns:
        df['customer_name'] = 'Valued Customer'
    if 'phone' not in df.columns:
        df['phone'] = 'Not Provided'
    
    return df

def create_charts(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create visualizations for the dashboard.
    
    Args:
        df: Processed DataFrame with discount recommendations
        
    Returns:
        dict: Dictionary containing Plotly figures
    """
    charts = {}
    
    # Segment distribution pie chart
    segment_counts = df['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    
    charts['segment_distribution'] = px.pie(
        segment_counts,
        values='count',
        names='segment',
        title='Customer Segment Distribution',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    # Discount distribution histogram
    charts['discount_distribution'] = px.histogram(
        df,
        x='discount_pct',
        nbins=10,
        title='Discount Distribution',
        labels={'discount_pct': 'Discount Percentage'},
        color_discrete_sequence=['#1f77b4']
    )
    
    # Segment-wise average discount
    segment_avg = df.groupby('segment')['discount_pct'].mean().reset_index()
    charts['segment_avg_discount'] = px.bar(
        segment_avg,
        x='segment',
        y='discount_pct',
        title='Average Discount by Segment',
        labels={'discount_pct': 'Average Discount %', 'segment': 'Customer Segment'},
        color='segment',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Validity days distribution
    charts['validity_distribution'] = px.box(
        df,
        x='segment',
        y='validity_days',
        title='Campaign Validity by Segment',
        labels={'validity_days': 'Validity (Days)', 'segment': 'Customer Segment'},
        color='segment'
    )
    
    return charts

def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"₹{amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1f}%"

def display_metric_card(title: str, value, delta=None, delta_label: str = None):
    """Display a metric card with optional delta indicator"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(
            label=title,
            value=value,
            delta=delta,
            delta_color="normal"
        )
    if delta_label and delta is not None:
        with col2:
            st.caption(delta_label)

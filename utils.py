import pandas as pd
import plotly.express as px
import streamlit as st
from typing import Union, Dict, Any
import re
from datetime import datetime

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
    
    # Handle the specific format of customer spend reports
    # Check if this is a customer spend report format
    if 'Customer Phone' in str(df.values):
        # This is a customer spend report, read with skiprows=5
        if hasattr(uploaded_file, 'seek'):
            uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file, engine='openpyxl', skiprows=5)
    
    # Filter out summary rows (Total, Min, Max, Avg)
    summary_indicators = ['Total', 'Min.', 'Max.', 'Avg.']
    df = df[~df.iloc[:, 0].isin(summary_indicators)]
    
    # Reset index after filtering
    df = df.reset_index(drop=True)
    
    # Standardize column names (case-insensitive and more flexible matching)
    column_mapping = {
        'customer_name': ['customer_name', 'name', 'customer name', 'full name', 'customer', 'client name', 'guest name'],
        'phone': ['phone', 'mobile', 'contact', 'phone number', 'mobile number', 'phone no', 'contact number', 'customer phone'],
        'email': ['email', 'email address', 'e-mail', 'email id', 'e mail'],
        'total_orders': ['total_orders', 'order_count', 'orders', 'number of orders', 'total orders', 'order count', 'no of orders', 'order qty'],
        'total_spent': ['total_spent', 'total_amount', 'amount', 'total spending', 'total spend', 'lifetime value', 'ltv', 'total revenue', 'total (₹)', 'total (rs)', 'total (inr)'],
        'last_order_date': ['last_order_date', 'last_order', 'order_date', 'date of last order', 'last visit', 'most recent order', 'last purchase date'],
        'avg_order_value': ['avg_order_value', 'average_order_value', 'aov', 'average spend', 'avg spend'],
        'address': ['address', 'customer address', 'location', 'delivery address']
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
    
    # Extract order information from Invoice column if it exists
    if 'invoice' in df.columns:
        df = extract_order_info_from_invoice(df)
    
    # Ensure required columns exist and provide helpful error message
    required_columns = ['total_spent']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        found_columns = [col for col in df.columns]
        st.error("⚠️ Could not find required columns in your file.")
        st.error(f"Missing columns: {', '.join(missing_columns)}")
        st.warning("Your file contains these columns: " + ", ".join(found_columns) if found_columns else "No columns found")
        st.info("\nCommon column name variations we look for:")
        st.info("- Total Spent: 'total_spent', 'total_amount', 'amount', 'total spending', 'total spend', 'lifetime value', 'Total (₹)'")
        st.error("\nPlease rename your columns to match one of these patterns and try again.")
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Ensure customer_name and phone have reasonable defaults if missing
    if 'customer_name' not in df.columns:
        df['customer_name'] = 'Valued Customer'
    if 'phone' not in df.columns:
        df['phone'] = 'Not Provided'
    
    # If total_orders is not available, estimate from invoice data or set default
    if 'total_orders' not in df.columns:
        df['total_orders'] = 1  # Default to 1 order per customer
    
    # If last_order_date is not available, set to current date
    if 'last_order_date' not in df.columns:
        df['last_order_date'] = datetime.now()
    
    return df

def extract_order_info_from_invoice(df):
    """
    Extract order count and last order date from the Invoice column.
    
    Args:
        df: DataFrame with invoice column
        
    Returns:
        DataFrame with extracted order information
    """
    df = df.copy()
    
    # Initialize new columns
    df['total_orders'] = 1  # Default to 1 order
    df['last_order_date'] = datetime.now()  # Default to current date
    
    if 'invoice' in df.columns:
        for idx, row in df.iterrows():
            invoice_text = str(row['invoice'])
            
            # Extract order count (number of invoice IDs)
            invoice_ids = re.findall(r'Invoice ID: ([^,]+)', invoice_text)
            if invoice_ids:
                df.at[idx, 'total_orders'] = len(invoice_ids)
            
            # Extract last order date from the most recent invoice
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
                r'(\d{2}-\d{2}-\d{4})',  # DD-MM-YYYY
                r'(\d{2}/\d{2}/\d{4})',  # DD/MM/YYYY
            ]
            
            for pattern in date_patterns:
                dates = re.findall(pattern, invoice_text)
                if dates:
                    try:
                        # Try to parse the date
                        if len(dates[0].split('-')[0]) == 4:  # YYYY-MM-DD
                            last_date = datetime.strptime(dates[-1], '%Y-%m-%d')
                        else:  # DD-MM-YYYY or DD/MM/YYYY
                            last_date = datetime.strptime(dates[-1], '%d-%m-%Y')
                        df.at[idx, 'last_order_date'] = last_date
                        break
                    except ValueError:
                        continue
    
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

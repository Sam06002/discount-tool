import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from discount_engine import segment_customers, generate_discounts
from utils import load_excel_data, create_charts

# Page configuration
st.set_page_config(
    page_title="AI Restaurant Discount Generator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("AI Restaurant Discount Generator")
    st.write("Upload your customer data and generate personalized discount campaigns.")
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # Sidebar for file upload and settings
    with st.sidebar:
        st.header("Upload Data")
        uploaded_file = st.file_uploader(
            "Upload Excel file with customer data",
            type=['xlsx', 'xls'],
            help="Upload an Excel file containing customer data with columns like 'Customer Name', 'Phone', 'Total Orders', etc."
        )
        
        if uploaded_file is not None:
            try:
                # Load and process the uploaded file
                df = load_excel_data(uploaded_file)
                st.session_state.df = df
                st.session_state.processed = False
                
                # Show column mapping options if needed
                st.success("File uploaded successfully!")
                
                # Add processing button
                if st.button("Process Data"):
                    with st.spinner("Processing data and generating recommendations..."):
                        # Apply segmentation
                        df_segmented = segment_customers(df)
                        # Generate discounts
                        df_with_discounts = generate_discounts(df_segmented)
                        # Store results in session state
                        st.session_state.df_processed = df_with_discounts
                        st.session_state.processed = True
                        st.rerun()
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # Main content area
    if st.session_state.df is not None:
        if not st.session_state.processed:
            st.subheader("Data Preview")
            st.dataframe(st.session_state.df.head(), use_container_width=True)
        else:
            display_results(st.session_state.df_processed)

def display_results(df):
    """Display the processed results and visualizations"""
    st.subheader("Campaign Summary")
    
    # Calculate metrics
    total_customers = len(df)
    avg_discount = df['discount_pct'].mean().round(2)
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", total_customers)
    with col2:
        st.metric("Average Discount", f"{avg_discount}%")
    with col3:
        total_estimated_cost = (df['total_spent'] * (df['discount_pct']/100)).sum().round(2)
        st.metric("Estimated Campaign Cost", f"₹{total_estimated_cost:,.2f}")
    
    # Show segment distribution
    st.subheader("Customer Segments")
    fig = px.pie(df, names='segment', title='Customer Segment Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Show discount recommendations
    st.subheader("Discount Recommendations")
    display_columns = [
        'customer_name', 'phone', 'segment', 'discount_pct', 
        'campaign_type', 'validity_days', 'min_order_value'
    ]
    st.dataframe(
        df[display_columns].rename(columns={
            'customer_name': 'Customer Name',
            'phone': 'Phone',
            'segment': 'Segment',
            'discount_pct': 'Discount %',
            'campaign_type': 'Campaign Type',
            'validity_days': 'Validity (Days)',
            'min_order_value': 'Min Order Value'
        }),
        use_container_width=True
    )
    
    # Add download button
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Discount_Recommendations')
        
        # Add summary sheet
        summary_df = pd.DataFrame({
            'Metric': ['Total Customers', 'Average Discount %', 'Estimated Campaign Cost (₹)'],
            'Value': [total_customers, avg_discount, total_estimated_cost]
        })
        summary_df.to_excel(writer, index=False, sheet_name='Summary')
    
    st.download_button(
        label="Download Recommendations",
        data=output.getvalue(),
        file_name=f"discount_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()

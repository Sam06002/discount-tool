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
            help="Upload an Excel file containing customer data with columns like 'Customer Name', 'Phone', 'Total (₹)', etc."
        )
        
        if uploaded_file is not None:
            try:
                # Load and process the uploaded file
                df = load_excel_data(uploaded_file)
                st.session_state.df = df
                st.session_state.processed = False
                
                # Show data summary
                st.success("File uploaded successfully!")
                st.info(f"📊 Found {len(df)} customers")
                st.info(f"💰 Total spend: ₹{df['total_spent'].sum():,.2f}")
                st.info(f"📅 Date range: {df['last_order_date'].min().strftime('%Y-%m-%d')} to {df['last_order_date'].max().strftime('%Y-%m-%d')}")
                
                # Add processing button
                if st.button("🚀 Process Data & Generate Discounts"):
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
                st.error("Please check your file format and try again.")
    
    # Main content area
    if st.session_state.df is not None:
        if not st.session_state.processed:
            st.subheader("📋 Data Preview")
            
            # Show data summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Customers", len(st.session_state.df))
            with col2:
                st.metric("Total Spend", f"₹{st.session_state.df['total_spent'].sum():,.2f}")
            with col3:
                st.metric("Average Spend", f"₹{st.session_state.df['total_spent'].mean():,.2f}")
            
            # Show data preview
            st.dataframe(
                st.session_state.df[['customer_name', 'phone', 'total_spent', 'total_orders', 'last_order_date']].head(10),
                use_container_width=True
            )
            
            st.info("💡 Click 'Process Data & Generate Discounts' in the sidebar to analyze your customers and create personalized discount campaigns.")
        else:
            display_results(st.session_state.df_processed)

def display_results(df):
    """Display the processed results and visualizations"""
    st.subheader("🎯 Campaign Summary")
    
    # Calculate metrics
    total_customers = len(df)
    avg_discount = df['discount_pct'].mean().round(2)
    total_estimated_cost = (df['total_spent'] * (df['discount_pct']/100)).sum().round(2)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", total_customers)
    with col2:
        st.metric("Average Discount", f"{avg_discount}%")
    with col3:
        st.metric("Estimated Campaign Cost", f"₹{total_estimated_cost:,.2f}")
    with col4:
        segment_counts = df['segment'].value_counts()
        most_common_segment = segment_counts.index[0]
        st.metric("Top Segment", most_common_segment)
    
    # Show segment distribution
    st.subheader("📊 Customer Segments")
    fig = px.pie(df, names='segment', title='Customer Segment Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Show segment-wise statistics
    st.subheader("📈 Segment Analysis")
    segment_stats = df.groupby('segment').agg({
        'total_spent': ['count', 'mean', 'sum'],
        'discount_pct': 'mean',
        'total_orders': 'mean'
    }).round(2)
    
    segment_stats.columns = ['Customer Count', 'Avg Spend', 'Total Spend', 'Avg Discount %', 'Avg Orders']
    st.dataframe(segment_stats, use_container_width=True)
    
    # Show discount recommendations
    st.subheader("🎁 Discount Recommendations")
    display_columns = [
        'customer_name', 'phone', 'segment', 'discount_pct', 
        'campaign_type', 'validity_days', 'min_order_value', 'message'
    ]
    
    # Filter columns that exist
    available_columns = [col for col in display_columns if col in df.columns]
    
    st.dataframe(
        df[available_columns].rename(columns={
            'customer_name': 'Customer Name',
            'phone': 'Phone',
            'segment': 'Segment',
            'discount_pct': 'Discount %',
            'campaign_type': 'Campaign Type',
            'validity_days': 'Validity (Days)',
            'min_order_value': 'Min Order Value',
            'message': 'Personalized Message'
        }),
        use_container_width=True
    )
    
    # Add download button
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Discount_Recommendations')
        
        # Add summary sheet
        summary_df = pd.DataFrame({
            'Metric': ['Total Customers', 'Average Discount %', 'Estimated Campaign Cost (₹)', 'Most Common Segment'],
            'Value': [total_customers, avg_discount, total_estimated_cost, most_common_segment]
        })
        summary_df.to_excel(writer, index=False, sheet_name='Summary')
        
        # Add segment analysis sheet
        segment_stats.to_excel(writer, sheet_name='Segment_Analysis')
    
    st.download_button(
        label="📥 Download Recommendations",
        data=output.getvalue(),
        file_name=f"discount_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()

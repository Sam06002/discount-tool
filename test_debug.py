import pandas as pd
import re

def test_column_mapping():
    # Read the Excel file
    df = pd.read_excel('Total_Customer_Spend_Report_2025_06_23_23_55_41.xlsx', skiprows=5)
    
    # Filter out summary rows
    summary_indicators = ['Total', 'Min.', 'Max.', 'Avg.']
    df = df[~df.iloc[:, 0].isin(summary_indicators)]
    df = df.reset_index(drop=True)
    
    print("Original columns:", df.columns.tolist())
    
    # Test column mapping
    column_mapping = {
        'customer_name': ['customer_name', 'name', 'customer name', 'full name', 'customer', 'client name', 'guest name'],
        'phone': ['phone', 'mobile', 'contact', 'phone number', 'mobile number', 'phone no', 'contact number', 'customer phone'],
        'total_spent': ['total_spent', 'total_amount', 'amount', 'total spending', 'total spend', 'lifetime value', 'ltv', 'total revenue', 'total (₹)', 'total (rs)', 'total (inr)'],
        'last_order_date': ['last_order_date', 'last_order', 'order_date', 'date of last order', 'last visit', 'most recent order', 'last purchase date'],
    }
    
    # Create a mapping of original column names to standardized names
    standardized_columns = {}
    for std_name, possible_names in column_mapping.items():
        for col in df.columns:
            print(f"Checking '{col}' against {possible_names}")
            if col.lower() in [name.lower() for name in possible_names]:
                standardized_columns[col] = std_name
                print(f"✓ Matched '{col}' to '{std_name}'")
                break
    
    print("\nStandardized columns:", standardized_columns)
    
    # Rename columns
    df = df.rename(columns=standardized_columns)
    print("\nAfter renaming, columns:", df.columns.tolist())
    
    return df

if __name__ == "__main__":
    df = test_column_mapping()
    print("\nFinal DataFrame:")
    print(df.head()) 
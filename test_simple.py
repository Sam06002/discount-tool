import pandas as pd

# Test reading the file step by step
print("Step 1: Reading file without skiprows")
df1 = pd.read_excel('Total_Customer_Spend_Report_2025_06_23_23_55_41.xlsx')
print("Columns:", df1.columns.tolist())
print("First few rows:")
print(df1.head())

print("\nStep 2: Reading file with skiprows=5")
df2 = pd.read_excel('Total_Customer_Spend_Report_2025_06_23_23_55_41.xlsx', skiprows=5)
print("Columns:", df2.columns.tolist())
print("First few rows:")
print(df2.head())

print("\nStep 3: Filtering summary rows")
summary_indicators = ['Total', 'Min.', 'Max.', 'Avg.']
df3 = df2[~df2.iloc[:, 0].isin(summary_indicators)]
print("After filtering:")
print(df3.head())

print("\nStep 4: Testing column mapping")
column_mapping = {
    'customer_name': ['customer_name', 'name', 'customer name', 'full name', 'customer', 'client name', 'guest name'],
    'phone': ['phone', 'mobile', 'contact', 'phone number', 'mobile number', 'phone no', 'contact number', 'customer phone'],
    'total_spent': ['total_spent', 'total_amount', 'amount', 'total spending', 'total spend', 'lifetime value', 'ltv', 'total revenue', 'total (₹)', 'total (rs)', 'total (inr)'],
}

standardized_columns = {}
for std_name, possible_names in column_mapping.items():
    for col in df3.columns:
        if col.lower() in [name.lower() for name in possible_names]:
            standardized_columns[col] = std_name
            print(f"Matched '{col}' to '{std_name}'")
            break

print("Standardized columns:", standardized_columns)
df4 = df3.rename(columns=standardized_columns)
print("Final columns:", df4.columns.tolist())
print("Final data:")
print(df4.head()) 
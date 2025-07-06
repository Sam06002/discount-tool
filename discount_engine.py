import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def segment_customers(df):
    """
    Segment customers based on their order history and spending patterns.
    
    Args:
        df (pd.DataFrame): Input DataFrame with customer data
        
    Returns:
        pd.DataFrame: DataFrame with an additional 'segment' column
    """
    # Make a copy to avoid modifying the original DataFrame
    df = df.copy()
    
    # Ensure required columns exist (case-insensitive)
    required_columns = {
        'total_orders': ['total_orders', 'order_count', 'orders'],
        'total_spent': ['total_spent', 'amount', 'total_amount', 'total (₹)', 'total (rs)', 'total (inr)'],
        'last_order_date': ['last_order_date', 'last_order', 'order_date']
    }
    
    # Map column names to standard names
    column_mapping = {}
    for std_name, possible_names in required_columns.items():
        for col in df.columns:
            if col.lower() in [name.lower() for name in possible_names]:
                column_mapping[std_name] = col
                break
    
    # Check if all required columns are found
    missing_columns = [col for col in required_columns if col not in column_mapping]
    if missing_columns:
        raise ValueError(f"Could not find required columns: {', '.join(missing_columns)}")
    
    # Standardize column names
    for std_name, orig_name in column_mapping.items():
        if std_name != orig_name:
            df[std_name] = df[orig_name]
    
    # Convert data types if needed
    if not pd.api.types.is_numeric_dtype(df['total_orders']):
        df['total_orders'] = pd.to_numeric(df['total_orders'], errors='coerce')
    
    if not pd.api.types.is_numeric_dtype(df['total_spent']):
        df['total_spent'] = pd.to_numeric(
            df['total_spent'].astype(str).str.replace(r'[^\d.]', '', regex=True),
            errors='coerce'
        )
    
    if not pd.api.types.is_datetime64_any_dtype(df['last_order_date']):
        df['last_order_date'] = pd.to_datetime(df['last_order_date'], errors='coerce')
    
    # Fill missing values with defaults
    df['total_orders'] = df['total_orders'].fillna(1)
    df['total_spent'] = df['total_spent'].fillna(0)
    df['last_order_date'] = df['last_order_date'].fillna(datetime.now())
    
    # Calculate days since last order
    current_date = datetime.now()
    df['days_since_last_order'] = (current_date - df['last_order_date']).dt.days
    
    # Initialize segment column
    df['segment'] = 'New'  # Default segment
    
    # Apply segmentation rules based on spending and order patterns
    # VIP: High spenders (₹5000+) or frequent customers (10+ orders with good spend)
    vip_mask = (
        (df['total_spent'] >= 5000) | 
        ((df['total_orders'] >= 10) & (df['total_spent'] >= 2000))
    )
    df.loc[vip_mask, 'segment'] = 'VIP'
    
    # Regular: Medium spenders (₹2000+) or moderate customers (5+ orders with decent spend)
    regular_mask = (
        (~vip_mask) & 
        ((df['total_spent'] >= 2000) | 
         ((df['total_orders'] >= 5) & (df['total_spent'] >= 1000)))
    )
    df.loc[regular_mask, 'segment'] = 'Regular'
    
    # Occasional: Low to medium spenders (₹500+) or occasional customers
    occasional_mask = (
        (~vip_mask & ~regular_mask) & 
        (df['total_spent'] >= 500)
    )
    df.loc[occasional_mask, 'segment'] = 'Occasional'
    
    # Lapsed: No orders in 14+ days (only for customers with some history)
    lapsed_mask = (
        (df['days_since_last_order'] >= 14) & 
        (df['total_orders'] > 0) & 
        (df['total_spent'] > 0)
    )
    df.loc[lapsed_mask, 'segment'] = 'Lapsed'
    
    # New: Everyone else (low spend, few orders, recent activity)
    new_mask = (
        (df['total_spent'] < 500) & 
        (df['total_orders'] <= 2) & 
        (df['days_since_last_order'] < 14)
    )
    df.loc[new_mask, 'segment'] = 'New'
    
    return df

def generate_discounts(df):
    """
    Generate personalized discount recommendations for each customer segment.
    
    Args:
        df (pd.DataFrame): DataFrame with customer data and segments
        
    Returns:
        pd.DataFrame: DataFrame with discount recommendations
    """
    # Define discount rules by segment
    discount_rules = {
        'VIP': {
            'base_discount': 25,
            'max_discount': 40,
            'min_order_value': 500,
            'validity_days': 30,
            'campaign_type': 'VIP Exclusive'
        },
        'Regular': {
            'base_discount': 20,
            'max_discount': 30,
            'min_order_value': 400,
            'validity_days': 21,
            'campaign_type': 'Loyalty Reward'
        },
        'Occasional': {
            'base_discount': 15,
            'max_discount': 25,
            'min_order_value': 300,
            'validity_days': 14,
            'campaign_type': 'Comeback Offer'
        },
        'Lapsed': {
            'base_discount': 30,
            'max_discount': 50,
            'min_order_value': 200,
            'validity_days': 45,
            'campaign_type': 'We Miss You!'
        },
        'New': {
            'base_discount': 20,
            'max_discount': 35,
            'min_order_value': 200,
            'validity_days': 30,
            'campaign_type': 'Welcome Offer'
        }
    }
    
    # Make a copy of the DataFrame
    df = df.copy()
    
    # Initialize discount columns
    df['discount_pct'] = 0.0
    df['min_order_value'] = 0.0
    df['validity_days'] = 0
    df['campaign_type'] = ''
    
    # Apply discount rules based on segment
    for segment, rules in discount_rules.items():
        mask = df['segment'] == segment
        
        # Base discount for the segment
        df.loc[mask, 'discount_pct'] = rules['base_discount']
        
        # Apply personalization based on spending
        if segment in ['VIP', 'Regular']:
            # Higher spenders get higher discounts (capped at max_discount)
            df.loc[mask, 'discount_pct'] = df.loc[mask].apply(
                lambda row: min(
                    rules['base_discount'] + int(row['total_spent'] / 1000),
                    rules['max_discount']
                ),
                axis=1
            )
        
        # Set other campaign parameters
        df.loc[mask, 'min_order_value'] = rules['min_order_value']
        df.loc[mask, 'validity_days'] = rules['validity_days']
        df.loc[mask, 'campaign_type'] = rules['campaign_type']
    
    # Ensure discount doesn't exceed 50% and maintains at least 15% margin
    df['discount_pct'] = df['discount_pct'].clip(upper=50)
    
    # Add a personalized message
    df['message'] = df.apply(
        lambda row: (
            f"Hi {row.get('customer_name', 'Valued Customer')}, "
            f"as a {row['segment']} customer, we're offering you {int(row['discount_pct'])}% off "
            f"your next order of ₹{int(row['min_order_value'])} or more! "
            f"Valid for {row['validity_days']} days. "
            "Use code: "
            f"{row['campaign_type'].upper().replace(' ', '')[:4]}{np.random.randint(1000, 9999)}"
        ),
        axis=1
    )
    
    return df

# Example usage
if __name__ == "__main__":
    # Create sample data for testing
    data = {
        'customer_name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Johnson', 'Mike Brown'],
        'phone': ['1234567890', '2345678901', '3456789012', '4567890123', '5678901234'],
        'total_orders': [25, 15, 8, 2, 1],
        'total_spent': [7500, 3500, 1500, 400, 100],
        'last_order_date': [
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=10),
            datetime.now() - timedelta(days=20),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=60)
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Test segmentation
    df_segmented = segment_customers(df)
    print("\nSegmented Customers:")
    print(df_segmented[['customer_name', 'segment']])
    
    # Test discount generation
    df_with_discounts = generate_discounts(df_segmented)
    print("\nDiscount Recommendations:")
    print(df_with_discounts[['customer_name', 'segment', 'discount_pct', 'campaign_type']])

# AI Restaurant Discount Generator - Project Documentation

## Project Overview
This is a Streamlit-based web application that helps restaurants analyze customer data and generate personalized discount campaigns. The application processes customer transaction data, segments customers based on their spending patterns, and generates targeted discount offers.

## Project Structure
```
discount-tool/
├── app.py                 # Main Streamlit application
├── discount_engine.py     # Core logic for customer segmentation and discount generation
├── utils.py               # Utility functions for data loading and visualization
├── requirements.txt       # Python dependencies
├── README.md              # Basic project documentation
└── AI_PROJECT_DOCS.md     # This comprehensive documentation file
```

## Dependencies
```
streamlit==1.31.1
pandas==2.1.0
numpy==1.26.0
plotly==5.17.0
openpyxl==3.1.2
python-dateutil==2.8.2
python-multipart==0.0.6
```

## File Details

### 1. app.py
Main Streamlit application that provides the user interface and handles the application flow.

#### Key Components:
- **Main Application Flow**:
  - File upload and data loading
  - Data processing and segmentation
  - Results display with interactive visualizations
  - Export functionality

- **UI Components**:
  - File uploader
  - Data preview
  - Processing controls
  - Results display with tabs
  - Interactive charts and metrics

### 2. discount_engine.py
Contains the core business logic for customer segmentation and discount generation.

#### Key Functions:
1. **segment_customers(df)**
   - Segments customers based on spending patterns and order history
   - Handles flexible column naming
   - Returns DataFrame with 'segment' column added

2. **generate_discounts(df)**
   - Generates personalized discount offers based on customer segments
   - Implements discount rules for different customer segments
   - Returns DataFrame with discount recommendations

### 3. utils.py
Contains utility functions for data processing and visualization.

#### Key Functions:
1. **load_excel_data(uploaded_file)**
   - Loads and validates Excel files
   - Handles different file formats and column naming conventions
   - Returns standardized DataFrame

2. **create_charts(df)**
   - Generates Plotly visualizations
   - Creates customer segment distribution charts
   - Generates spending analysis charts

## Data Flow
1. User uploads Excel file with customer data
2. Data is loaded and standardized
3. Customers are segmented based on spending patterns
4. Personalized discounts are generated for each segment
5. Results are displayed with interactive visualizations

## Key Features
- **Flexible Data Import**: Supports various Excel formats and column naming conventions
- **Customer Segmentation**: Automatically segments customers into VIP, Regular, Occasional, Lapsed, and New categories
- **Smart Discounting**: Generates context-aware discount offers based on customer value
- **Interactive Visualizations**: Provides insights through interactive charts and metrics
- **Export Functionality**: Allows exporting results for further analysis

## Usage Example
```python
# Sample code to use the core functionality
from discount_engine import segment_customers, generate_discounts
import pandas as pd

# Load your customer data
df = pd.read_excel('customer_data.xlsx')

# Segment customers
segmented = segment_customers(df)

# Generate discounts
with_discounts = generate_discounts(segmented)

# View results
print(with_discounts[['customer_name', 'segment', 'discount_pct', 'campaign_type']])
```

## Common Issues and Solutions
1. **File Format Issues**:
   - Ensure the Excel file is not password protected
   - Verify that required columns are present (customer_name, phone, total_spent, etc.)

2. **Processing Errors**:
   - Check for missing or invalid data in the input file
   - Ensure date columns are in a recognizable format

3. **Performance**:
   - For large datasets, consider processing in batches
   - Enable watchdog for better file monitoring during development

## Future Enhancements
1. Add support for CSV and database connections
2. Implement A/B testing for discount strategies
3. Add more sophisticated segmentation algorithms
4. Include customer lifetime value prediction
5. Add user authentication and multi-tenant support

## Notes for AI Understanding
- The application uses Streamlit's session state to maintain state between interactions
- Error handling is implemented at multiple levels to provide meaningful feedback
- The code includes extensive logging for debugging purposes
- The architecture is modular, making it easy to extend or modify functionality

---
*This documentation provides a comprehensive overview of the project for AI understanding. For more detailed information, please refer to the inline documentation in each source file.*

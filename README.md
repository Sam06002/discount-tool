# AI Restaurant Discount Generator

An intelligent web application that analyzes customer data and generates personalized discount recommendations for restaurant customers.

## Features

- **Excel Data Import**: Upload customer data in Excel format
- **Smart Customer Segmentation**: Automatically categorizes customers into segments (VIP, Regular, Occasional, New, Lapsed)
- **Personalized Discounts**: Generates tailored discount offers based on customer value and behavior
- **Interactive Dashboard**: Visualize customer segments and discount distributions
- **Export Results**: Download recommendations as Excel files

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd streamlit_discount_app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your customer data in an Excel file with these columns (case-insensitive):
   - Customer Name/ID
   - Phone/Mobile/Contact
   - Total Orders/Order Count
   - Total Spent/Amount
   - Last Order Date
   - Average Order Value (optional)

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to the provided local URL (usually http://localhost:8501)

4. Upload your Excel file through the sidebar and click "Process Data"

5. View the generated recommendations and download the results

## Data Processing

The application performs the following steps:

1. **Data Loading**: Reads the uploaded Excel file and standardizes column names
2. **Customer Segmentation**: Categorizes customers based on order history and spending patterns
3. **Discount Generation**: Applies business rules to generate personalized discounts
4. **Visualization**: Creates interactive charts to analyze customer segments and discount distribution

## Business Rules

### Customer Segments

- **VIP**: 20+ orders, ₹5000+ spent
- **Regular**: 10+ orders, ₹2000+ spent
- **Occasional**: 3+ orders, ₹500+ spent
- **New**: <3 orders
- **Lapsed**: No orders in 14+ days

### Discount Rules

- Maximum discount: 50%
- Minimum margin: 15%
- Campaign validity: 14-45 days based on segment
- Minimum order value: ₹200-500 based on segment

## Customization

You can modify the following files to customize the application:

- `discount_engine.py`: Update segmentation and discount rules
- `app.py`: Modify the user interface and dashboard
- `utils.py`: Adjust data loading and visualization settings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact [your-email@example.com] or create an issue in the repository.

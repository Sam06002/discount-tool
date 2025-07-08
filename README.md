# 🎯 Discount Insight Builder

An intelligent web application that analyzes customer data and generates personalized discount recommendations for restaurant customers. Built with Streamlit and Python.

## 🚀 Features

- **📊 Data Import**: Upload customer data in Excel or CSV format
- **🎯 Smart Customer Segmentation**: Categorizes customers into segments (VIP, Loyal, Regular, New, Lapsed)
- **💰 Personalized Discounts**: Generates tailored discount offers based on customer value and behavior
- **📱 Interactive Interface**: User-friendly dashboard with real-time feedback
- **🔍 Data Analysis**: Automatic data validation and column mapping
- **📥 Export Results**: Download recommendations as CSV files
- **🐛 Debug Tools**: Built-in debugging and logging for troubleshooting

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sam06002/discount-tool.git
   cd discount-tool
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   The main dependencies are:
   - streamlit
   - pandas
   - openpyxl (for Excel support)
   - plotly (for visualizations)

## 🚀 Usage

1. **Prepare your data**:
   - Supported formats: Excel (.xlsx, .xls) or CSV
   - Required columns (case-insensitive):
     - Customer Name/ID
     - Phone/Mobile/Contact
     - Total Orders/Order Count
     - Total Spent/Amount
     - Last Order Date

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   This will start the web server and open the app in your default browser.

3. **Using the application**:
   - Upload your customer data file
   - The app will automatically detect and map columns
   - Click "Process Data & Generate Discounts" to analyze the data
   - View the customer segments and discount recommendations
   - Download the results as a CSV file

4. **Debugging**:
   - Check the sidebar for detailed debug logs
   - Use `test_button.py` to test button functionality
   - Review the debug output in the console where Streamlit is running

## 🔍 Recent Updates

- Added comprehensive debug logging
- Improved error handling and user feedback
- Added test scripts for debugging
- Enhanced data validation and column mapping
- Updated documentation

## 🏗️ Project Structure

- `app.py`: Main Streamlit application
- `discount_engine.py`: Core logic for customer segmentation and discount generation
- `utils.py`: Utility functions for data processing
- `test_button.py`: Debugging tool for UI components
- `requirements.txt`: Project dependencies
- `AI_PROJECT_DOCS.md`: Detailed project documentation

## 📊 Business Rules

### Customer Segments

- **VIP**: 20+ orders, ₹5000+ spent
- **Loyal**: 10-19 orders, ₹2000+ spent
- **Regular**: 3-9 orders, ₹500+ spent
- **New**: <3 orders
- **Lapsed**: No orders in 14+ days

### Discount Rules

- Maximum discount: 50%
- Minimum margin: 15%
- Campaign validity: 14-45 days based on segment
- Minimum order value: ₹200-500 based on segment
- Discount range: 10-30% based on customer value

## 🛠️ Customization

You can modify the following files to customize the application:

- `discount_engine.py`: Update segmentation and discount rules
- `app.py`: Modify the user interface and dashboard
- `utils.py`: Adjust data loading and visualization settings
- `test_button.py`: Add more UI component tests

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

For support, please [open an issue](https://github.com/Sam06002/discount-tool/issues) in the GitHub repository.

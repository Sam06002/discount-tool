import streamlit as st
import pandas as pd
import time
from datetime import datetime

def log_debug(message, is_error=False):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    debug_text = f"{timestamp} - {message}"
    st.sidebar.text(debug_text)
    if is_error:
        st.sidebar.error(debug_text)

def test_button():
    st.title("Button Test")
    
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    
    if st.button("Test Button"):
        st.session_state.clicked = True
        with st.spinner("Processing..."):
            try:
                log_debug("Button clicked!")
                log_debug("This is a test message")
                time.sleep(2)  # Simulate processing
                st.session_state.test_result = "Success!"
                st.rerun()
            except Exception as e:
                log_debug(f"Error: {str(e)}", is_error=True)
    
    if st.session_state.clicked:
        if 'test_result' in st.session_state:
            st.success(st.session_state.test_result)
        else:
            st.warning("Processing complete but no result found")

if __name__ == "__main__":
    test_button()

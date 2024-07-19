import streamlit as st
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from FinMind.data import DataLoader

# # Set some options for printing all the columns
# np.set_printoptions(precision=10, threshold=sys.maxsize)
# np.set_printoptions(linewidth=np.inf)

# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('max_colwidth', None)

# pd.options.display.float_format = '{:,.5f}'.format


# Set default layout to wide mode
st.set_page_config(layout="wide")

# Streamlit user input for year_MG
st.title("Taiwan Stock Data Viewer")

stock_id = st.sidebar.text_input('Enter the stock ID:', value='0050') # default to 0050

start_year_MG = st.sidebar.number_input('Enter the START ROC year (e.g., 113 for 2024):', min_value=1, max_value=200, value=113) # default to MG 113
start_month = st.sidebar.selectbox('Select START Month:', list(range(1, 13)), index=6)  # default to July

end_year_MG = st.sidebar.number_input('Enter the END ROC year (e.g., 113 for 2024):', min_value=1, max_value=200, value=113) # default to MG 113
end_month = st.sidebar.selectbox('Select END Month:', list(range(1, 13)), index=6)  # default to July

# Sidebar inputs
if st.sidebar.button('Confirm'):
    # Date calculation
    start_year = start_year_MG + 1911
    formatted_start_month = f"{start_month:02d}"
    start_date = f"{start_year}-{formatted_start_month}-01"

    end_year = end_year_MG + 1911
    formatted_end_month = f"{end_month:02d}"
    end_date = f"{end_year}-{formatted_end_month}-31"

    st.session_state['start_date'] = start_date
    st.session_state['end_date'] = end_date

# Check if dates are set
if 'start_date' in st.session_state and 'end_date' in st.session_state:
    start_date = st.session_state['start_date']
    end_date = st.session_state['end_date']

    st.write(f"Start Date: {start_date}")
    st.write(f"End Date: {end_date}")

    # FinMind data loading
    dl = DataLoader()
    stock_data = dl.taiwan_stock_daily(stock_id=stock_id, start_date=start_date, end_date=end_date)
    stock_data.set_index('date', inplace=True)
    stock_data = stock_data.set_index(pd.DatetimeIndex(pd.to_datetime(stock_data.index)))
    st.write(f"Data retrieved. Total Rows: {stock_data.shape[0]} / Total Columns: {stock_data.shape[1]}")

    # List of columns
    columns = list(stock_data.columns)

    # Checkbox for 'All' option
    select_all = st.sidebar.checkbox('All', key='select_all')

    # Checkbox for each column
    selected_columns = []
    if select_all:
        selected_columns = columns
    else:
        selected_columns = [col for col in columns if st.sidebar.checkbox(col, key=col)]

    if selected_columns:
        st.write("Selected columns:", str(selected_columns))
        st.dataframe(stock_data[selected_columns], height=500, use_container_width=True)
    else:
        st.write("No columns selected.")
else:
    st.write("Please fill in the requirements!")
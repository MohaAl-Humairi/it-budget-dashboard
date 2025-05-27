import pandas as pd
import streamlit as st

# Load the Excel file
file_path = 'CHWZK MBE Budget.xlsx'
xls = pd.ExcelFile(file_path, engine='openpyxl')
df_data = pd.read_excel(xls, 'Data', engine='openpyxl')
df_data.columns = df_data.columns.str.strip()

# Function to recalculate totals
def recalculate_totals(df):
    df['*Totalt SEK'] = df['Pcs'] * df['Price SEK']
    return df

# Function to display and edit a category
def display_category(df, category):
    st.header(category)
    category_df = df[df['Parts'] == category]
    edited_df = st.data_editor(category_df, key=f"editor_{category}")
    return edited_df

# Streamlit app layout
st.title('IT Infrastructure Integration Budget')

# Define categories
categories = ['Switches', 'Support', 'Wifi', 'Clients', 'Server']

# Display and edit each category
edited_dfs = [display_category(df_data, cat) for cat in categories]

# Concatenate edited dataframes and recalculate totals
df_data = pd.concat(edited_dfs)
df_data = recalculate_totals(df_data)

# Display summary
st.header('Summary')
summary = df_data.groupby('Parts')['*Totalt SEK'].sum()
st.write(summary)

# File uploader for new Excel files
uploaded_file = st.file_uploader("Upload a new Excel file", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file, engine='openpyxl')
    df_data = pd.read_excel(xls, 'Data', engine='openpyxl')
    df_data.columns = df_data.columns.str.strip()
    st.success("File uploaded successfully!")

# Export and download the modified budget
st.header('Export and Download')
df_data.to_excel('Modified_Budget.xlsx', index=False)
with open('Modified_Budget.xlsx', 'rb') as f:
    st.download_button('Download Modified Budget', f, file_name='Modified_Budget.xlsx')


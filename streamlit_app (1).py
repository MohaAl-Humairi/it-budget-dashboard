
import pandas as pd
import streamlit as st

file_path = 'CHWZK MBE Budget.xlsx'
xls = pd.ExcelFile(file_path, engine='openpyxl')
df_data = pd.read_excel(xls, 'Data', engine='openpyxl')
df_data.columns = df_data.columns.str.strip()

def recalculate_totals(df):
    df['*Totalt SEK'] = df['Pcs'] * df['Price SEK']
    return df

def display_category(df, category):
    st.header(category)
    category_df = df[df['Parts'] == category]
    edited_df = st.data_editor(category_df)
    return edited_df

st.title('IT Infrastructure Integration Budget')
categories = ['Switches', 'Support', 'Wifi', 'Clients', 'Server']
edited_dfs = [display_category(df_data, cat) for cat in categories]
df_data = pd.concat(edited_dfs)
df_data = recalculate_totals(df_data)

st.header('Summary')
summary = df_data.groupby('Parts')['*Totalt SEK'].sum()
st.write(summary)

uploaded_file = st.file_uploader("Upload a new Excel file", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file, engine='openpyxl')
    df_data = pd.read_excel(xls, 'Data', engine='openpyxl')
    df_data.columns = df_data.columns.str.strip()
    st.success("File uploaded successfully!")

st.header('Export and Download')
df_data.to_excel('Modified_Budget.xlsx', index=False)
with open('Modified_Budget.xlsx', 'rb') as f:
    st.download_button('Download Modified Budget', f, file_name='Modified_Budget.xlsx')

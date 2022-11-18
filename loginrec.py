import streamlit as st
import mysql.connector
import pandas as pd
connection = st.session_state['connection'] 
cursor = st.session_state['cursor']

def is_empty(df):
    if df.empty:
        print('Empty table')

def logrec():
    cursor.callproc('user_logins')
    result = ''
    for i in cursor.stored_results():
        result = i.fetchall()
        df = pd.DataFrame(result)
        is_empty(df)
        st.write(df.to_markdown())


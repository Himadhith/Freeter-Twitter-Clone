import streamlit as st
import pandas as pd
connection = st.session_state['connection'] 
cursor = st.session_state['cursor']
col1,col2 = st.columns(2)


def sql_executor(raw_code):
	cursor.execute(raw_code)
	data = cursor.fetchall()
	return data 
def sql():
    with col1:
        with st.form(key='query_form'):
            raw_code = st.text_area("SQL Code Here")
            submit_code = st.form_submit_button("Execute")
    with col2:
        if submit_code:
            st.info("Query Submitted")
            st.code(raw_code)

				# Results 
            
            query_results = sql_executor(raw_code)
            # with st.beta_expander("Results"):
            #     st.write(query_results)
            cols=cursor.column_names
            with st.expander("Result",expanded=True):
                query_df = pd.DataFrame(query_results,columns=cols)
                st.dataframe(query_df)

if(st.session_state['login'] == 'None'):
    st.write("Please login first to access this feature!")
else:
    sql()
import streamlit as st
import pandas as pd

connection = st.session_state['connection'] 
cursor = st.session_state['cursor']
users=[]
def is_empty(df):
    if df.empty:
        print('Empty table')
def view_following():
    cursor.execute('SELECT following FROM FOLLOW where follower="%s"'%(st.session_state['login']))
    data = cursor.fetchall()
    for i in data:
        users.append(i) 
def dm():
    arguments = []
    fol = pd.DataFrame(users,columns=['Following'])
    st.dataframe(fol)
    username = st.text_input("Enter the user you want to send a direct message to")
    arguments.append(username)
    messsage = st.text_area("Enter the message")
    arguments.append(messsage)
    if st.button("Send"):
        cursor.callproc('direct_text_message', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        st.success(result)
        connection.commit()
def dms():
    cursor.callproc('list_of_message_sender')
    result = ''
    for i in cursor.stored_results():
        result = i.fetchall()
        df = pd.DataFrame(result)
        is_empty(df)
        for i in result:
            st.header(i[1])
            st.subheader(i[2])
            st.write("---")


if(st.session_state['login'] == 'None'):
    st.write("Please login first to access this feature!")
else:
    view_following()
    dm()
    st.header("Messages")
    if st.button("Dms"):
        dms()
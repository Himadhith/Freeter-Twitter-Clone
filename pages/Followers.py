import streamlit as st
import mysql.connector
import pandas as pd
connection = st.session_state['connection'] 
cursor = st.session_state['cursor']

def is_empty(df):
    if df.empty:
        print('Empty table')
def follow():
        arguments = []
        username = st.text_input('Enter the username of the person you want to follow:')
        arguments.append(username)
        col1,col2 = st.columns(2)
        with col1:
            follow = st.button("Follow",key="UF11")
        with col2:
            fol_list = st.button("Show followers",key="FL11")
            if fol_list:
                view_following()
        if follow:
            cursor.callproc('follow', arguments)
            result = ''
            for i in cursor.stored_results():
                result = i.fetchone()[0]
            st.success(result)
            connection.commit()
def unfollow():
        arguments = []
        username = st.text_input('Enter the username of the person you want to unfollow:')
        arguments.append(username)
        col1,col2 = st.columns(2)
        with col1:
            unfollow = st.button("Unfollow",key="UF1")
        with col2:
            fol_list2 = st.button("Show following","FL")
        if fol_list2:
            view_follower()
        if unfollow:
            cursor.callproc('stop_follow', arguments)
            result = ''
            for i in cursor.stored_results():
                result = i.fetchone()[0]
            st.success(result)
            connection.commit()

            
def view_following():
    cursor.execute('SELECT follower FROM FOLLOW where following="%s"'%(st.session_state['login']))
    data = cursor.fetchall()
    st.table(data)
def view_follower():
    cursor.execute('SELECT following FROM FOLLOW where follower="%s"'%(st.session_state['login']))
    data = cursor.fetchall()
    st.table(data)

def block():
    arguments = []
    username = st.text_input('Enter the username of the person you want to unfollow:',key="b")
    arguments.append(username)
    if st.button("Block"):
        cursor.callproc('block', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        st.success(result)
        connection.commit()

def unblock():
    arguments = []
    username = st.text_input('Enter the username of the person you want to unfollow:',key="ub")
    arguments.append(username)
    if st.button("Unlock"):
        cursor.callproc('stop_block', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        st.write(result)
        connection.commit()



def followers():
    follow()
    unfollow()
if(st.session_state['login'] == 'None'):
    st.write("Please login first to access this feature!")
else:
    st.title("Follow or unfollow accounts")
    followers()
    st.title("Block or Unblock accounts")
    block()
    unblock()



import streamlit as st
import mysql.connector
import pandas as pd
connection = st.session_state['connection'] 
cursor = st.session_state['cursor']
cursor1 = st.session_state['cursor']


def show_comm(n):
    arguments = []
    arguments.append(n)
    cursor.callproc('get_comments_of_tweet', arguments)
    result = ''
    for i in cursor.stored_results():
        result = i.fetchall()
        df = pd.DataFrame(result)
        is_empty(df)
        st.write(df.to_markdown())
def comm(msg,n):
        arguments = []
        arguments.append(n)
        arguments.append(msg)
        cursor.callproc('comment', arguments)
        result = ''
        for i in cursor.stored_results():
            result = i.fetchone()[0]
        st.success(result)
        connection.commit()
def fr_act():
    cursor.callproc('get_following_activity')
    result = ''
    j=0
    for i in cursor.stored_results():
        result = i.fetchall()
        df = pd.DataFrame(result)
        is_empty(df)
        for i in tweets:
            st.title(i[2])
            st.header(i[3])
            reply_msg=st.text_input("Comment on this",key="%sj+1"%(j))
            j+=1
            col1,col2=st.columns(2)
            with col1:
                if(st.button("Like",key="10%s"%(j))):
                    like(i[0])
            with col2:
                if(st.button("Comment",key="20%s"%(j))):
                    comm(reply_msg,i[0])
            
            st.write("---")


    
def like(n):
    arguments = []
    tweet_id = n
    arguments.append(tweet_id)
    cursor.callproc('liking', arguments)
    result = ''
    for i in cursor.stored_results():
        result = i.fetchone()[0]
    st.success(result)
    connection.commit()

def is_empty(df):
    if df.empty:
        print('Empty table')

def tweet():
    arguments = []
    result = st.text_input("Enter your tweet ")
    tweet = st.button("Tweet")
    
    if tweet:
        if(st.session_state['login']!='None'):
            arguments = [result]
            cursor.callproc('send_tweet', arguments)
            for i in cursor.stored_results():
                result = i.fetchone()[0]
            st.write(result)
            connection.commit()

if(st.session_state['login'] == 'None'):
    st.write("Please login first to access this feature!")
    
else:
    tweet()
    cursor.execute("Select tweetid from tweet where username='%s' and type='T'"%(st.session_state['login']))
    data = cursor.fetchall()
    # data=data[::-1] 
    with st.expander("Show My tweets"):
        cursor.callproc('get_own_tweets')
        result_tweet = ''
        for i in cursor.stored_results():
            result_tweet = i.fetchall()
            df = pd.DataFrame(result_tweet,columns=['Tweet','Time'])
            
            is_empty(df)
        if df.empty:
            st.write("Empty set")
        else:
            df['tweetid'] = data
            st.write(df)
            
        
        # st.write(df.to_markdown())
    with st.expander("Show tweet and replies"):
        arguments = []
        # print('')
        # tweet_id = int(input())
        # st.write(data)
        if df.empty:
            st.write("Empty")
        else:
            for i in data:
                # arguments.append(i)
                cursor.callproc('get_comments_of_tweet', i)
                result = ''
            for i in cursor.stored_results():
                result = i.fetchall()
                
            df3 = pd.DataFrame(result)

            st.dataframe(df3)
            # final = pd.merge(df,df3)

    with st.expander("Show all the tweets"):
        cursor.execute("Select * from tweet where username != '%s' and type='T'"%(st.session_state['login']))
        tweets=cursor.fetchall()
        j=0
        
        for i in tweets:
            st.title(i[2])
            st.header(i[3])
            reply_msg=st.text_input("Comment on this",key=j)
            col1,col2=st.columns(2)
            with col1:
                if(st.button("Like",key="1%s"%(j))):
                    like(i[0])
            with col2:
                if(st.button("Comment",key="2%s"%(j))):
                    comm(reply_msg,i[0])
            j+=1
            st.write("---")
    with st.expander("See what your friends are saying, %s"%(st.session_state['login'])):
        fr_act()
            
            

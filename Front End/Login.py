import streamlit as st
import mysql.connector
import datetime


st.set_page_config(initial_sidebar_state="collapsed")
connection = mysql.connector.connect(host='localhost', user = "root", password = "", db='freeter')
cursor = connection.cursor()  

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.pinimg.com/originals/fa/40/5e/fa405e983146d7a786667978befa1f74.jpg");
             background-attachment: fixed;
             background-size: cover;
             top:-50px;

            #  opacity:0.5
         }}
         .css-af4qln span
         {{
            text-align:center;
            font-size:100px;
         }}
         
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

result_log = ''
col1, col2= st.columns(2)
st.session_state['cursor'] = cursor
st.session_state['connection'] = connection
st.session_state['login'] ='None'
st.session_state['expand']=False 

with col1:
    with st.expander("Login",expanded=st.session_state['expand']):
        arguments = []
        
        userName = st.text_input("Enter your username",key='login1')
        arguments.append(userName)

        password = st.text_input("Enter your password",key='login2',type="password")
        arguments.append(password)

        login = st.button("Login")
        if login:
            cursor.callproc('login',arguments)
            
            for i in cursor.stored_results():
                result_log = i.fetchone()[0]

            if 'invalid'not in result_log:
                st.success(result_log)
                st.session_state['login'] = userName
                st.session_state['expand'] = False
                connection.commit()

                    
            else:
                st.warning(result_log)
                connection.rollback()
if st.session_state['login']=="admin":
    # if st.button("Show Login records"):
    from loginrec import logrec
    with st.expander("Show login records"):
        logrec()



if result_log == "Login successfully.":
    # menu = ["Home","Tweet", "Followers", "Message", "Likes"]
    # choice = st.sidebar.selectbox("Menu", menu)
    # if choice == "Tweet":
    #     if(st.session_state['login'] ==userName):
    
    st.title("Welcome to Freeter: " + userName)



with col2:
    with st.expander("Signup"):
            arguments = []
            userName1 = st.text_input("Enter your username",key="sign1")
            arguments.append(userName1)
            firstname = st.text_input("Enter your first name",key="sign2")
            arguments.append(firstname)
            lastname = st.text_input("Enter your last name",key="sign3")
            arguments.append(lastname)
            birthdate = st.text_input('Enter date of birth(YYYY-MM-DD):',key="sign4")
            # if checkbut:
            #     birthdate1 = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
            #     if birthdate1!=None:
            #         st.write("Inside none loop")
                    
                    
            #         st.write(birthdate)
            #         st.write(arguments)
            #     else:
            #             st.write('Please enter date of birth in valid format:')
            arguments.append(birthdate)
            bio = st.text_input('Enter bio(if you dont want to have bio, enter \"none\"):',key="sign5")
            if bio == 'none':
                bio = None
            arguments.append(bio)
            password = st.text_input('Enter password(128 character long ):',key="sign6",type="password")
            arguments.append(password)
            signup = st.button("Sign up")
            if signup:
                cursor.callproc('create_account', arguments)
                result = ''
                for i in cursor.stored_results():
                    result = i.fetchone()[0]
                if result != 'Sorry, this username is already taken.':
                    st.success(result)
                    connection.commit()

st.title('Freeter')
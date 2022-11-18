import streamlit as st
from streamlit_option_menu import option_menu
from login import login

def main():
    selected = option_menu(
        menu_title=None,
        options=['Login']
    )

if __name__ == '__main__':
    main()
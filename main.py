import streamlit as st
from streamlit_option_menu import option_menu
from extract_text import extract_text


def main():
    with st.sidebar:
        selected_option = option_menu(
            menu_title='My Tools',
            menu_icon='gear',
            options=['Home', 'Extract Text', 'About', 'Contact'],
            icons=["house-door", "file-text", "question-circle", "chat-dots"],)
    
        theme_radio = st.pills('Choose a theme:', ['Light', 'Dark', 'System Default'])
        layout_radio = st.pills('Choose a layout:', ['Centered', 'Wide'])

        if layout_radio == 'Centered':
            st.set_page_config(layout='centered')
        elif layout_radio == 'Wide':
            st.set_page_config(layout='wide')

        if theme_radio == 'Light':
            st.markdown(
                """
                <style>
                body {
                    background-color: #ffffff;
                    color: #000000;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        elif theme_radio == 'Dark':
            st.markdown(
                """
                <style>
                body {
                    background-color: #000000;
                    color: #ffffff;
                }
                </style>
                """,
                unsafe_allow_html=True)
        elif theme_radio == 'System Default':
            st.markdown(
                """
                <style>
                body {
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                </style>
                """,
                unsafe_allow_html=True)
        
        



    if selected_option == 'Extract Text':        
        extract_text()
        


main()


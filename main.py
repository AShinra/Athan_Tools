import streamlit as st
from streamlit_option_menu import option_menu
from extract_text import extract_text
from url_checker import url_checker
from url_fetcher import fetch_url

def main():
    # Initialize session state FIRST
    if 'layout' not in st.session_state:
        st.session_state.layout = 'Centered'
    
    layout_map = {
        'Centered': 'centered',
        'Wide': 'wide'
    }
    
    st.set_page_config(
        page_title='My Tools',
        layout=layout_map.get(st.session_state.layout, 'centered')
    )
    
    with st.sidebar:
        selected_option = option_menu(
            menu_title='My Tools',
            menu_icon='gear',
            options=['Home', 'Extract Text', 'URL Checker', 'URL Fetcher', 'About', 'Contact'],
            icons=["house-door", "file-text", "link-45deg", "browser-chrome","question-circle", "chat-dots"],)
    
        st.info('Theme is controlled via `.streamlit/config.toml`')
        layout_radio = st.pills('Choose a layout:', ['Centered', 'Wide'])

        if layout_radio != st.session_state.layout:
            st.session_state.layout = layout_radio
            st.rerun()
        
        



    if selected_option == 'Extract Text':        
        extract_text()
    elif selected_option == 'URL Checker':
        url_checker()
    elif selected_option == 'URL Fetcher':
        st.title("URL Fetcher")
        fetch_url(st.text_input("Enter URL to fetch:", key="fetch_url_input"), timeout=10)
    
if __name__ == "__main__":
    main()


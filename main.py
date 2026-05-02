import streamlit as st
from streamlit_option_menu import option_menu
from extract_text import extract_text
from url_checker import url_checker

def main():
    # Get layout preference from session state
    if 'layout' not in st.session_state:
        st.session_state.layout = 'Centered'
    
    layout_map = {
        'Centered': 'centered',
        'Wide': 'wide'
    }
    
    st.set_page_config(
        page_title='My Tools',
        layout=layout_map[st.session_state.layout]
    )
    
    with st.sidebar:
        selected_option = option_menu(
            menu_title='My Tools',
            menu_icon='gear',
            options=['Home', 'Extract Text', 'URL Checker', 'About', 'Contact'],
            icons=["house-door", "file-text", "link-45deg", "question-circle", "chat-dots"],)
    
        st.info('Theme is controlled via `.streamlit/config.toml`')
        layout_radio = st.pills('Choose a layout:', ['Centered', 'Wide'])

        if layout_radio != st.session_state.layout:
            st.session_state.layout = layout_radio
            st.rerun()
        
        



    if selected_option == 'Extract Text':        
        extract_text()
    elif selected_option == 'URL Checker':
        url_checker()


if __name__ == "__main__":
    main()


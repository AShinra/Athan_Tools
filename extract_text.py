import streamlit as st
from common import get_text_from_url, get_text_from_html, is_valid_url



def extract_text():
    pill_options = st.pills(
        label='Get Text', label_visibility='collapsed', options=['From URL', 'From HTML'], width=200 )

    if pill_options == 'From URL':
        st.title('Extract Text from URL')

        url = st.text_input('Enter the URL of the webpage you want to extract text from:')
        if is_valid_url(url):
            if st.button(label='Extract Text', key='extract_url_text_button'):
                with st.spinner('Extracting text...', show_time=True):
                    text = get_text_from_url(url)
                    st.text_area('Extracted Text', value=text, height=600)
        else:
            st.toast('Please enter a valid URL.', icon='⚠️')            

    elif pill_options == 'From HTML':
        st.title('Extract Text from HTML')

        html_input = st.text_area('Enter the HTML content you want to extract text from:', height=100)
        if html_input:
            if st.button(label='Extract Text', key='extract_html_text_button',):
                text = get_text_from_html(html_input)
                st.text_area('Extracted Text', value=text, height=600)
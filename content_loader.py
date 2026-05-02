import requests
import streamlit as st
from bs4 import BeautifulSoup

def load_content(result):
    # headers = {"User-Agent": "Mozilla/5.0"}
    # response = requests.get(url, headers=headers, timeout=10)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     st.write(soup.prettify())
        # try:
        #     html = response.text
        #     st.components.v1.html(html, height=600, scrolling=True)
        # except:
        #     st.components.v1.iframe(url, height=600, scrolling=True)
    
    st.components.v1.html(result, height=600, scrolling=True)

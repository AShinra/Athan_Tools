import jwt
import streamlit as st
import requests
import pandas as pd

# Make the API request
@st.cache_resource
def fetch_url(url):
    return requests.get(url, timeout=10)

def url_checker():
    url_input = st.text_area("Enter URL to check:", key="url_input")
    if url_input:
        if st.button("Check URL(s)", key="check_button"):
            url_list = url_input.splitlines()
            
            # Secret key for signing (also required inside the payload as access_token)
            secret = st.secrets["url_checker"]["access_token"]

            # JSON payload — API requires access_token in the body, not just as the signing key
            payload = {
                "urls": url_list,
                "access_token": secret,
            }

            # Encode to JWT
            token = jwt.encode(payload, secret, algorithm="HS256")
            # print("JWT Token:")
            # print(token)

            # API endpoint for URL checking
            api_url = st.secrets["url_checker"]["api_url"] + "?token=" + token
            
            try:
                response = fetch_url(api_url)
                response.raise_for_status()  # Raise an error for bad status codes
                result = response.json()
                # st.write("API Response:")
                # st.json(result)

                _dict = {}
                for _data in result.get("data", []):
                    article_url = _data.get("article_url", "N/A")
                    in_mongodb_state = _data.get("in_mongodb", False)
                    in_es_state = _data.get("in_es", False)
                    
                    if in_mongodb_state and in_es_state:
                        _dict.update({article_url: 'Existing'})
                    elif in_mongodb_state and not in_es_state:
                        _dict.update({article_url: 'Syncing'})
                    elif not in_mongodb_state and not in_es_state:
                        _dict.update({article_url: 'Not Existing'})
                
                df = pd.DataFrame(list(_dict.items()), columns=['Article URL', 'State'])
                st.dataframe(df, hide_index=True)

            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")

if __name__ == "__main__":
    st.title("URL Checker")
    url_checker()
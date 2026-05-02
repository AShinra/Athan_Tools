import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import streamlit as st
import tabula
import pandas as pd
from io import BytesIO
import streamlit as st

# check if url is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


# get text from url
def get_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Request error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # try:
    #     for tag in soup.select(["#related_block", ".related_stories", "#article_bottom_social-share", "#article_tags", '#header']):
    #         tag.decompose()
    # except:
    #     pass
    
    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "aside"]):
        tag.decompose()
    
    # Common content selectors (priority order)
    selectors = [
        ".article__content",
        "main",
        "article",
        "div.content",
        "div#content",
        "section.content",
        ".post-content",
        ".entry-content",
        ".article-body",
        ".post-body"]

    content = None

    # Try each selector
    for selector in selectors:
        content = soup.select_one(selector)
        if content and len(content.get_text(strip=True)) > 200:  # ensure it's meaningful
            break

    # Fallback to body if nothing found
    if not content:
        content = soup.body

    # Add spacing after paragraphs
    for p in content.find_all("p"):
        p.append("\n\n")

    text = content.get_text(separator="\n\n", strip=True)

    return text, content.prettify()

# get text from html input
def get_text_from_html(html):

    soup = BeautifulSoup(html, "html.parser")

    for p in soup.find_all("p"):
        p.append("\n\n")   # add newline after each <p>

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n\n", strip=True)

    return text

# convert pdf to excel
def convert_pdf_to_excel(pdf_file):
    uploaded_file = pdf_file
    
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("PDF uploaded successfully!")

    # Extract tables using Tabula
    try:
        tables = tabula.read_pdf("temp.pdf", pages="all", multiple_tables=True)
        
        if tables:
            all_tables = []
            for i, table in enumerate(tables, start=1):
                table['Table'] = i  # optional: track table number
                all_tables.append(table)
            
            result_df = pd.concat(all_tables, ignore_index=True)
            st.dataframe(result_df)  # Display the extracted tables
            
            # Save Excel in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, sheet_name='PDF_Tables')
            output.seek(0)
            
            # Download button
            st.download_button(
                label="Download Excel",
                data=output,
                file_name="converted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("Conversion completed!")
        else:
            st.warning("No tables found in the PDF.")
    
    except Exception as e:
        st.error(f"Error extracting tables: {e}")



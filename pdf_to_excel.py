import streamlit as st
from common import convert_pdf_to_excel



def pdf_to_excel():
    st.title('PDF to Excel Converter')
    st.write('Upload a PDF file to convert it to Excel format.')

    uploaded_file = st.file_uploader('Choose a PDF file', type='pdf')

    if uploaded_file is not None:
        # Here you would add the logic to convert the PDF to Excel
        if st.button(label='Convert', key='convert_pdf_to_excel_button'):
            convert_pdf_to_excel(uploaded_file)

import streamlit as st

languages = ['English', 'Portuguese']
selection = st.selectbox("Select language", languages)
st.write(f"Selected language: {selection}")
import streamlit as st
import numpy as np
import pandas as pd

html_temp = """
<style>
</style>
"""

st.set_page_config(
    page_title="Allergy-based Baby's Food Recommendation",
    layout='wide',
    initial_sidebar_state='auto',
)

st.title("Allergy-based Baby's Food Recommendation")
st.caption('Faraz Nurdini | 5026201007')

user_name = st.text_input("Enter your baby's name:")
st.text("Select one or many allergen:")
user_input = st.checkbox("Susu",label_visibility='visible')



# ---------------------------- library -----------------------------------------

import streamlit as st
import numpy as np
import pandas as pd
from recipe_sim_filtering import find_recipes_sim
# ---------------------------- library -----------------------------------------


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

user_name = st.text_input("Silahkan masukkan nama bayi anda:")
user_age = st.slider("Umur bayi (Dalam Bulan):",6,12)
st.text("Pilih satu alergen atau lebih:")

alergen_utama = ['susu','ikan','gluten','kerang','kacang','udang','telur']
turunan_map = {
    'susu': ['yogurt', 'krim', 'mentega', 'whey', 'kasein', 'keju'],
    'ikan': ['minyak ikan', 'gelatin ikan'],
    'gluten': ['roti', 'pasta', 'tepung', 'mie'],
    'kerang': ['saus tiram'],
    'kacang': ['minyak wijen', 'minyak kedelai', 'mustard', 'tahu', 'tofu', 'tempe', 
               'kerupuk kedelai', 'bumbu kacang', 'kecap'],
    'udang': ['ebi', 'petis', 'terasi', 'kerupuk udang', 'koya'],
    'telur': ['mayonnaise', 'meringue']
}

col1,col2, col3, col4 = st.columns(4)
user_input_values = []


for i in alergen_utama:
    if i not in st.session_state:
        st.session_state[i] = False

for i in alergen_utama:
    if st.session_state[i] == True :
         for x in turunan_map.get(i, []):
              st.session_state[x] = True

def delete_child() :
    for i in alergen_utama: 
        for x in turunan_map.get(i, []): 
            st.session_state[x] = False
               


for i in alergen_utama:
     with col1:
          if st.checkbox(i, value=st.session_state[i], on_change=delete_child ,key=i):
               user_input_values.append(i)

columns = [col2, col3, col4] 
for idx, (main_allergen, derivatives) in enumerate(turunan_map.items()):
    col_idx = idx % len(columns)  
    with columns[col_idx]:
        for derivative in derivatives:
            if st.checkbox(derivative, value=st.session_state.get(derivative, False), key=derivative):
                user_input_values.append(derivative)


user_input = ' '.join(user_input_values)


if user_input_values:
    st.write("Anda memilih:", ", ".join(user_input_values))
else:
    st.write("Tidak ada alergi yang terpilih.")

st.text('')

df = pd.read_excel('./Model/Concept_Data Resep_Updated.xlsx')

if st.button("Recommend Recipe"):
        st.subheader(f"Recommended Recipe for {user_name}")
        recommended_recipe = find_recipes_sim(df, user_input)
        recipe_result = pd.DataFrame( 
            [{**recipe[0].to_dict(), "similarity_score": recipe[1]} for recipe in recommended_recipe]
            )
        top_n = 10
        filtered_data = recipe_result[recipe_result['umur_resep'].apply(lambda x: user_age in x )]
        filtered_pd = pd.DataFrame(filtered_data)[:top_n]

        for index,row in filtered_pd.iterrows():
            with st.expander(row["nama_resep"]):
                st.write(f"**Nama Resep:** {row['nama_resep']}")
                st.write(f"**Bahan Resep:** {row['bahan_resep']}")
                st.write(f"**Bahan Alergen:** {row['bahan_alergen']}")
                #st.write(f"**Umur Resep:** {', '.join(map(str, row['umur_resep']))}")
                st.write(f"**Resep diperuntukkan bayi berumur:** {", ".join(f'{umur} Bulan' for umur in row['umur_resep'])}")
                st.write(f"**Similarity Score:** {row['similarity_score']}")




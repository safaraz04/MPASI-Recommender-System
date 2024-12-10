import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_excel('./Concept_Data Resep_Updated.xlsx')
df = df.replace(np.nan,"")
df['umur_resep'] = df['umur_resep'].astype(str)
df['umur_resep'] = df['umur_resep'].apply(lambda x: list(map(int, x.split(','))))
df_clean = df.copy()
df_clean[['bahan_resep','bahan_alergen']] = df_clean[['bahan_resep','bahan_alergen']].replace(to_replace=r'[^\w\s]', value=' ', regex=True)
data = pd.DataFrame(df_clean['bahan_resep'].astype(str)+ ' '+ df_clean['bahan_alergen'].astype(str),columns=['bahan_resep_dan_alergen'])


# turunan_alergi_input = {
#     'susu': ['yogurt','krim','mentega','whey','kasein','keju'],
#     'telur': ['mayonnaise','meringue'],
#     'ikan': ['minyak ikan','gelatin ikan'],
#     'gluten' : ['roti','pasta','tepung','mie'],
#     'udang': ['ebi','petis','terasi','kerupuk udang','koya'],
#     'kerang': ['saus tiram'],
#     'kacang': ['minyak wijen', 'minyak kedelai', 'mustard', 'tahu', 'tofu', 'tempe', 'kerupuk kedelai', 'bumbu kacang', 'kecap']
# }


# def expand_user_input(user_input, turunan_alergi_input):
#     parent_input = [user_input]
#     if user_input in turunan_alergi_input:
#         parent_input.extend(turunan_alergi_input[user_input])
#     return parent_input

def find_recipes_sim(data_matrix, user_input, min_similarity = 0):
    vectorizer = CountVectorizer()
    data_matrix = vectorizer.fit_transform(data['bahan_resep_dan_alergen'])
    user_matrix = vectorizer.transform([user_input])
    data_matrix_sets = [row.indices for row in data_matrix]
    user_matrix_sets = [row.indices for row in user_matrix][0]

    similarities = []
    for row in data_matrix_sets:
        intersection = len(list(set(user_matrix_sets).intersection(row)))
        similarity = 2*float(intersection)/(len(set(user_matrix_sets)) + len(set(row)))
        similarities.append(similarity)
    top_n = 10
    top_recipes = [(df.loc[i, ['nama_resep', 'bahan_resep', 'bahan_alergen', 'umur_resep']], similarities[i]) 
                   for i in np.argsort(similarities) if similarities[i] == min_similarity]

    return top_recipes

    # top_recipes = []
    # for i in top_indices:
    #     age_list = list(map(int, str(df.iloc[i]['umur_resep']).split(',')))
        
    #     if any(age <= user_age for age in age_list) and similarities[0, i] >= min_similarity:
    #         top_recipes.append((df[['nama_resep', 'bahan_resep', 'bahan_alergen', 'umur_resep']].iloc[i], similarities[0, i]))
    #         if len(top_recipes) >= top_n:
    #             break
                        
    # top_recipes = [(df[['nama_resep','bahan_resep','bahan_alergen','umur_resep']].iloc[i], similarities[0,i]) for i in top_indices if similarities [0,i] <= min_similarity][:top_n]

    # return top_recipes
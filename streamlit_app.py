import streamlit as st
import pandas as pd
from start import final_df

st.title("Top 5 Champions by Role")

# Sélection du rôle via un menu déroulant
role = st.selectbox("Select a Role", ['Top', 'Jgl', 'Mid', 'Bot', 'Sup'])

# Filtrer les 5 champions les plus joués dans le rôle sélectionné
role_data = final_df[final_df['role'] == role].nlargest(5, 'count')

# Affichage des 5 champions dans le rôle
st.write(f"Top 5 champions in {role} role:")
st.dataframe(role_data[['Champion', 'winrate', 'pickrate', 'count']])
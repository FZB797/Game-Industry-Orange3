import streamlit as st
import pandas as pd
import pickle
from Orange.data import Table, Domain, DiscreteVariable, ContinuousVariable, StringVariable

# ==============================
# LOAD MODEL
# ==============================
with open('game_industry.pkcls', 'rb') as file:
    model = pickle.load(file)

st.title("🎮 Game Trending Status Prediction App")
st.write("Aplikasi ini memprediksi apakah suatu game sedang **Trending** atau tidak, berdasarkan berbagai atribut.")

# ==============================
# INPUT FORM
# ==============================
st.header("Masukkan Data Game")

col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox("Genre", ["Action", "Adventure", "RPG", "Strategy", "Sports", "Simulation", "Shooter"])
    platform = st.selectbox("Platform", ["PC", "PlayStation", "Xbox", "Switch", "Mobile"])
    release_year = st.number_input("Release Year", min_value=1990, max_value=2025, step=1)
    developer = st.text_input("Developer", "Example Studio")

with col2:
    revenue = st.number_input("Revenue (Millions $)", min_value=0.0, step=0.1)
    players = st.number_input("Players (Millions)", min_value=0.0, step=0.1)
    peak_players = st.number_input("Peak Concurrent Players", min_value=0, step=1)
    metacritic = st.slider("Metacritic Score", 0, 100, 75)
    esports_pop = st.selectbox("Esports Popularity", ["Low", "Medium", "High"])

# ==============================
# KONVERSI INPUT KE Orange.data.Table
# ==============================
# Definisikan domain (struktur atribut sesuai model)
domain = Domain([
    DiscreteVariable("Genre", values=["Action", "Adventure", "RPG", "Strategy", "Sports", "Simulation", "Shooter"]),
    DiscreteVariable("Platform", values=["PC", "PlayStation", "Xbox", "Switch", "Mobile"]),
    ContinuousVariable("Release Year"),
    StringVariable("Developer"),
    ContinuousVariable("Revenue (Millions $)"),
    ContinuousVariable("Players (Millions)"),
    ContinuousVariable("Peak Concurrent Players"),
    ContinuousVariable("Metacritic Score"),
    DiscreteVariable("Esports Popularity", values=["Low", "Medium", "High"])
], 
DiscreteVariable("Trending Status", values=["Not Trending", "Trending"])
)

# Buat 1 baris data input sesuai domain
orange_data = Table(domain, [[
    genre, platform, release_year, developer,
    revenue, players, peak_players, metacritic,
    esports_pop, None
]])

st.write("### Data yang Dimasukkan:")
st.write(pd.DataFrame({
    "Genre": [genre],
    "Platform": [platform],
    "Release Year": [release_year],
    "Developer": [developer],
    "Revenue (Millions $)": [revenue],
    "Players (Millions)": [players],
    "Peak Concurrent Players": [peak_players],
    "Metacritic Score": [metacritic],
    "Esports Popularity": [esports_pop]
}))

# ==============================
# PREDIKSI
# ==============================
if st.button("🔮 Prediksi Trending Status"):
    pred = model(orange_data)[0]
    st.success(f"🎯 Prediksi: **{pred}**")

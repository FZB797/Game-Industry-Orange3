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
st.write("Prediksi status tren game berdasarkan data industri game global.")

# ==============================
# INPUT FORM
# ==============================
st.header("Masukkan Data Game")

col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox("Genre", ["Action", "Adventure", "RPG", "Strategy", "Shooter", "Simulation", "Sports", "Horror"])
    platform = st.selectbox("Platform", ["PC", "PlayStation", "Xbox", "Switch", "Mobile"])
    release_year = st.number_input("Release Year", min_value=1990, max_value=2025, step=1)
    developer = st.text_input("Developer", "Example Studio")

with col2:
    revenue = st.number_input("Revenue (Millions $)", min_value=0.0, step=0.1)
    players = st.number_input("Players (Millions)", min_value=0.0, step=0.1)
    peak_players = st.number_input("Peak Concurrent Players", min_value=0.0, step=0.1)
    metacritic = st.slider("Metacritic Score", 0, 100, 75)
    esports_pop = st.selectbox("Esports Popularity", ["Yes", "No"])

# ==============================
# KONVERSI KE ORANGE TABLE
# ==============================
# Developer dijadikan metas
domain = Domain(
    [
        DiscreteVariable("Genre", values=["Action", "Adventure", "RPG", "Strategy", "Shooter", "Simulation", "Sports", "Horror"]),
        DiscreteVariable("Platform", values=["PC", "PlayStation", "Xbox", "Switch", "Mobile"]),
        ContinuousVariable("Release Year"),
        ContinuousVariable("Revenue (Millions $)"),
        ContinuousVariable("Players (Millions)"),
        ContinuousVariable("Peak Concurrent Players"),
        ContinuousVariable("Metacritic Score"),
        DiscreteVariable("Esports Popularity", values=["Yes", "No"])
    ],
    DiscreteVariable("Trending Status", values=["Stable", "Declining", "Growing"]),
    metas=[StringVariable("Developer")]
)

# Data input dalam format Orange Table
orange_data = Table(domain, [[
    genre, platform, release_year,
    revenue, players, peak_players,
    metacritic, esports_pop,
    None,  # Target
    developer  # Metas
]])

st.write("### Data yang Dimasukkan:")
st.dataframe(pd.DataFrame({
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
    st.success(f"🎯 Prediksi Trending Status: **{pred}**")

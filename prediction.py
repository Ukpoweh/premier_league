import streamlit as st

import pickle
import time

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
#background = st.get_option('theme.backgroundColor')
#plt.style.use(background)

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))


def app():
    st.header("Welcome To Our Match Predictor!")
    st.text("Get predictions for upcoming Premier League matches")
    st.write("----")
    matches_df = pd.read_csv("datasets/matches.csv")
    matches_rolling = pd.read_csv('datasets/rolling.csv')
    teams = list(matches_df[matches_df["Season"]==2024]["Team"].unique())

    col1, col2= st.columns([1,1])
    with col1:
    
        home_team = st.selectbox("Select the home team", teams)
    with col2:

        away_team = st.selectbox("Select the away team", teams)



    

    predictors = ["GF_rolling", "GA_rolling", "Poss_rolling", "Sh_rolling", 
                  "SoT_rolling", "Dist_rolling", "FK_rolling", "PK_rolling", "PKatt_rolling"]
    
    rolling_stats = np.array(matches_rolling[matches_rolling["Team"]==home_team][predictors].iloc[-1, :]).reshape(1, -1)

    labeled_categories = np.array(encoder.transform([home_team, away_team])).reshape(1, -1)

    stats_and_teams = np.concatenate([labeled_categories, rolling_stats], axis=1)
    

    day_and_venue = [1]
    day_and_venue = np.array([day_and_venue]).reshape(1, -1)

    features = np.concatenate([day_and_venue, stats_and_teams], axis=1)

    features_scaled = scaler.transform(features)
    prediction = model.predict_proba(features_scaled)




    results_df = pd.DataFrame()
    home_team3 = home_team[:3]
    away_team3 = away_team[:3]
    results_df["Match"] = [f'{home_team3} vs {away_team3}']
    results_df[f"{home_team} win prob"] = np.round(prediction[:, 2] * 100, 2)
    results_df[f"{away_team} win prob"] = np.round(prediction[:, 1] * 100, 2)
    results_df[f"Draw prob"] = np.round(prediction[:, 0] * 100, 2)
    results_df.set_index("Match", inplace=True)

    

    if st.button('Predict match outcome'):
        with st.spinner(text="Fetching predictions..."):
            time.sleep(3)
        if home_team == away_team:
            st.error("You cannot have the same home and away team")

        else:
            st.success(f"Here's the predicted match outcome!")
            col4, col5 = st.columns([1, 1])
            with col4:
                st.dataframe(results_df, hide_index=True, use_container_width=True)
            with col5:

                labels = ['Draw prob', f'{away_team} win prob', f'{home_team} win prob']
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(np.reshape(prediction, -1), labels=labels, autopct='%1.1f%%')
                #st.pyplot(fig)
                st.bar_chart(results_df)
        



    



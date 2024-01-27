import streamlit as st
import time

import pandas as pd
import numpy as np


def app():
    st.header("Welcome to our Stats Checker!")


    overall_stats_df = pd.read_csv("overall_stats.csv")


    st.write("----")
    with st.container():
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### Current Season's Table")
            league_table = overall_stats_df[overall_stats_df["Season"]==2024][["Rk", "Squad", "MP", "W", "D", "L", "GD", "Pts"]]
            st.dataframe(league_table, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("### Other Seasons' Table")
            with st.expander("2022/2023"):
                table_2023 = overall_stats_df[overall_stats_df["Season"]==2023][["Rk", "Squad", "MP", "W", "D", "L", "GD", "Pts"]]
                st.dataframe(table_2023, hide_index=True, use_container_width=True)
            with st.expander("2021/2022"):
                table_2023 = overall_stats_df[overall_stats_df["Season"]==2022][["Rk", "Squad", "MP", "W", "D", "L", "GD", "Pts"]]
                st.dataframe(table_2023, hide_index=True, use_container_width=True)


    st.write("----")

    col3, col4 = st.columns([1,1])

    with col3:
        team = list(overall_stats_df["Squad"].unique())
        selected_team = st.selectbox("Select Team", team)
    with col4:
        year = list(overall_stats_df["Season"].unique())
        selected_year = st.selectbox("Select season", year)
    
    
    def generate_tables():
        
        filtered_stats = overall_stats_df[(overall_stats_df["Season"] == selected_year) & (overall_stats_df["Squad"] == selected_team)]
        try:                                                                                                                                
            position = filtered_stats["Rk"].values[0]
            matches_played = filtered_stats["MP"].values[0]
            points = filtered_stats["Pts"].values[0]
            attendance = filtered_stats["Attendance"].values[0]
            scorer = filtered_stats["Top Team Scorer"].values[0]

            labels_general = ["Position", "Number of matches played", "Total points", "Top Team Scorer", "Attendance"]
            values_general = [position, matches_played, points, scorer, attendance]
            general_zip = list(zip(labels_general, values_general))
            general_stats = pd.DataFrame(general_zip, columns=["General Stats", " "])

            number_of_wins = filtered_stats["W"].values[0]
            number_of_draws = filtered_stats["D"].values[0]
            number_of_losses = filtered_stats["L"].values[0]
            points_per_match = filtered_stats["Pts/MP"].values[0]

            labels_wins = ["Number of wins", "Number of draws", "Number of losses", "Points per match"]
            values_wins = [number_of_wins, number_of_draws, number_of_losses, points_per_match]
            wins_zip = list(zip(labels_wins, values_wins))
            wins_stats = pd.DataFrame(wins_zip, columns=["Wins and Losses", " "])

            goals = filtered_stats["Gls"].values[0]
            assists = filtered_stats["Ast"].values[0]
            sot_90 = filtered_stats["SoT/90"].values[0]
            g_sot = filtered_stats["G/SoT"].values[0]
            p_sot = filtered_stats["SoT%"].values[0]
            possesion = filtered_stats["Poss"].values[0]

            labels_shooting = ["Number of goals allowed", "Number of assists", "Shots on target per 90", "Goals per shots on target", "Percantage of shots on target", "Average Possesion"]
            values_shooting = [goals, assists, sot_90, g_sot, p_sot, possesion]
            shooting_zip = list(zip(labels_shooting, values_shooting))
            shooting_stats = pd.DataFrame(shooting_zip, columns=["Shooting Stats", " "])

            ga = filtered_stats["GA"].values[0]
            cs = filtered_stats["CS%"].values[0]
            goalkeeper = filtered_stats["Goalkeeper"].values[0]

            labels_gk = ["Number of goals against", "Percentage of clean sheets", "Goalkeeper"]
            values_gk = [ga, cs, goalkeeper]
            gk_zip = list(zip(labels_gk, values_gk))
            gk_stats = pd.DataFrame(gk_zip, columns=["Goalkeeping stats", " "])

            return general_stats, wins_stats, shooting_stats, gk_stats


        except:
            return f"{selected_team} do not have stats for {selected_year-1}/{selected_year}"
        
    general_stats, wins_stats, shooting_stats, gk_stats = generate_tables()
    if st.button("Check stats"):
        st.write("----")
        with st.spinner(text="Checking stats"):
            time.sleep(3)
        st.markdown(f"### {selected_team} stats for {selected_year-1}/{selected_year} season")
        st.dataframe(general_stats, use_container_width=True, hide_index=True)
        st.dataframe(wins_stats, use_container_width=True, hide_index=True)
        st.dataframe(shooting_stats, use_container_width=True, hide_index=True)
        st.dataframe(gk_stats, use_container_width=True, hide_index=True)

    
    

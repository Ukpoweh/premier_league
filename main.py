import streamlit as st

from streamlit_option_menu import option_menu

import home, stats, prediction

st.set_page_config(
    page_title="Bloom",
    layout="wide",
    page_icon=":soccer:"
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append(
            {
                "title":title, 
                "function": func
            }
        )

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title = "Menu",
                options = ['Home', 'Stats Checker', 'Match Predictor'],
                icons = ['house-fill', 'bar-chart-fill', 'box-arrow-right'],
                menu_icon = 'menu-up',
                default_index=1,
                styles = {
                    "container":{"padding":"5!important", "background-color":'black'},
                    "icon": {"color" : "white", "font-size":"23px"},
                    "nav-link" : {"color":"white", "font-size":"20px", "text-align":"left", "margin":"0px", "--hover-color":"blue", "font-family":"Monospace"},
                    "nav-link-selected":{"background-color":"#02ab21"}      
                }
            )
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write("-----")
        
        st.sidebar.markdown("Built by [Ukpoweh](https://github.com/Ukpoweh)")
        if app == "Home":
            home.app()
        if app == "Stats Checker":
            stats.app()
        if app == "Match Predictor":
            prediction.app()
    

    run()
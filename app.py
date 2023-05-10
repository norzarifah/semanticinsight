# import libraries
import streamlit as st
from PIL import Image
from pathlib import Path
from pages import data
from pages import analysis
from pages import timeline


def main():
   
    # add icon to every pages
    icon = Image.open(Path("./images/icon.png"))
    logo = Image.open(Path("./images/logo.png"))
    st.set_page_config(page_title="Semantic Insight", page_icon=icon, layout="wide")
    st.image(logo, width=500)

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)  

    # remove list of pages from the sidebar
    no_sidebar_style = """ <style>div[data-testid="stSidebarNav"] {display: none;}</style> """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)
    

    # add icon and pages to the sidebar
    st.text(" ")
    st.sidebar.image(logo, use_column_width=True)
    
    # create a menu with multiple tabs
    menu = ["Home", "Semantic Analysis", "Time Analysis"]
    choice = st.sidebar.selectbox(" ", menu)
    # show the tab content
    if choice == "Home":
        data.app()
    elif choice == "Semantic Analysis":
        analysis.app()
    else:
        timeline.app()
    

# run function
if __name__ == "__main__":
    main()

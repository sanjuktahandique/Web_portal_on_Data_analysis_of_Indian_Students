import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from io import StringIO
from scipy import stats
from scipy.stats import pearsonr
from streamlit_option_menu import option_menu

# Import sections
from sections.home import home_section
from sections.visualizations import visualizations_section
from sections.screen_time import screen_time_section
from sections.health_effects import health_effects_section

# Set page configuration
st.write("# Impact of Screentime on Indian Students:")




# Sidebar navigation
with st.sidebar:
    choice = option_menu(
        menu_title="",  # Title of the sidebar menu
        options=["Home", "Visualizations", "Screen Time Analysis", "Statistical Analysis"],  # Menu options
        icons=["house", "bar-chart", "clock", "gear"],  # Corresponding icons
        menu_icon="cast",  # Menu icon
        default_index=0,  # Default selected option
    )

# Display the selected section
if choice == "Home":
    home_section()
elif choice == "Visualizations":
    visualizations_section()
elif choice == "Screen Time Analysis":
    screen_time_section()
elif choice == "Statistical Analysis":
    health_effects_section()
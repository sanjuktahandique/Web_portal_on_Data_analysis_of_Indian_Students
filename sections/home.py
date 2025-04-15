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
from streamlit.components.v1 import html
from utils.data_loader import load_data





df = load_data()

def home_section():
    
    
    st.image("Analysis.png",  use_column_width=True)
    
    st.markdown("""
                <img src="C:/Users/sanju/Desktop/Analysis/Analysis.png" alt=""/>
    <h1>Understanding the Impact of Screentime on Indian Students</h1>
                
                
    <p>In an age dominated by digital interaction, understanding the effects of screentime on students is more critical than ever. This analysis delves into the habits and consequences of screentime among Indian students, examining diverse factors such as age, gender, education, and location. It explores daily screentime patterns for educational and entertainment purposes, correlating them with physical, mental, and social health. By mapping when students begin experiencing adverse effects—ranging from eye strain to psychological challenges—this study highlights the profound impact of prolonged screen exposure. It also sheds light on platform-specific risks, including cyberbullying, scams, and radical content, urging timely intervention and awareness.
    """, unsafe_allow_html=True)
    st.markdown("""

    
    <ul>
        <li>Exposure to cyberbullying and online harassment.</li>
        <li>Increased vulnerability to scams, fraud, and radical ideologies.</li>
        <li>Health concerns including nearsightedness and psychological stress.</li>
        <li>Health concerns including nearsightedness and psychological stress.</li>
    </ul>
                
    <h2>The Data Question</h2>
    <p>My aim was to collect data locally to identify patterns unique to our region, and answer the following questions about the Screentime of Indian Students</p>
    <ul><ol>
    <li>Does the gender category influence screen time?</li>
    <li>Does age influence the amount of screen time?</li>
    <li>Is there a relation between the type of screen time and the frequency of negative experiences?</li>
    <li>Does screen time impact the concentration levels of students?</li>
    <li>Is screen time a contributing factor to health and mental issues(i.e Myopia, Slow thinking/speaking,  less sleep duration, Severe headaches, reduced psycological well being, etc?</li>
    <li>Can screen time contribute to negative experiences?</li></ol>
    </ul>
                
    <h3>The Data Collection</h3>
    <p>Data was collected through a manual survey using Google Forms.</p>
    
     """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    


    # Data information
    st.subheader('Data Information')
    st.write("This is the data that has been collected in the following list.")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")
    st.write("Columns:")
    st.write(df.columns.tolist())
    st.dataframe(df.head())
    
    

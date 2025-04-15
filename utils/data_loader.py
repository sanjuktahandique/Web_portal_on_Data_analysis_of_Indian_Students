import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv('Screentime1.csv')
    df.drop(['Timestamp'], axis=1, inplace=True)
    df.rename(columns={
        'Age':'Age', 
        'Gender':'Gender',
        'Educational Qualification':'Education',
        'Address(City,State format)':'Address', 
        'Average time you spend(you think) in viewing electronic devices on daily basis (including Laptops and Mobile Phones)':'Avg_Screentime(daily)', 
        'How many hours do you spend on educational purposes? (per day)': 'Avg_screentime_for_educational_purpose', 
        'How many hours do you spend on personal entertainment on daily basis?(Game, Social Media, Streaming Platforms included)':'Avg Screentime for entertainment purpose', 
        'Are you currently experiencing any of the following issues? ':'Health_Effects',
        'If yes, at what age did you start experiencing these issues? [Less sleep duration]':'Age when-Less sleep duration-occured', 
        'If yes, at what age did you start experiencing these issues? [Severe headaches]':'Age when-Severe headaches-occured',  
        'If yes, at what age did you start experiencing these issues? [Myopia(Nearsightedness)]':'Age when-Myopia(Nearsightedness)-occured',
        'If yes, at what age did you start experiencing these issues? [Eye Fatigue]':'Age when-Eye Fatigue-occured',
        'If yes, at what age did you start experiencing these issues? [Dry eyes]':'Age when-Dry eyes-occured',
        'If yes, at what age did you start experiencing these issues? [ADHD/Difficulty in attention]':'Age when-ADHD/Difficulty in attention-occured',
        'If yes, at what age did you start experiencing these issues? [Slowed thinking, speaking, or body movements]':'Age when-Slowed thinking, speaking, or body movements-occured',
        'If yes, at what age did you start experiencing these issues? [Reduced Psychological well being]':'Age_when-Reduced_Psychological_well_being-occured', 
        'If yes, at what age did you start experiencing these issues? [Change in social behaviour]':'Age when-Change in social behaviour-occured', 
        'If yes, at what age did you start experiencing these issues? [Having no motivation or interest in things]':'Age when-Having no motivation or interest in things-occured',  
        'On average how long can you concentrate in one go?':'Concentration',
        'Have you ever encountered any of the given traumatic or violent experiences on the internet?':'Negative Experiences',
        'If yes, at what age did you first encounter these experiences/experience on the internet?':'Age of negative experience',
        'On which types of platforms have you encountered such activities? [Scams and Fraud leading to financial loss or loss personal data]':'Platforms-Scams and Fraud leading to financial loss or loss personal data-occured',
        'On which types of platforms have you encountered such activities? [Exploitation and Manipulation through Social Media]':'Platforms-Exploitation and Manipulation through Social Media-occured',
        'On which types of platforms have you encountered such activities? [Cyberbullying or Hate Speech]':'Platforms-Cyberbullying or Hate Speech-occured',
        'On which types of platforms have you encountered such activities? [Exposure to Radical Ideologies]':'Platforms-Exposure to Radical Ideologies-occured',
        'On which types of platforms have you encountered such activities? [Malware and Phishing Attacks]':'Platforms-Malware and Phishing Attacks-occured',
        'On which types of platforms have you encountered such activities? [Online Harassment]':'Platforms-Online Harassment-occured'
    }, inplace=True)
    df.replace(np.nan, '0', inplace=True)
    return df

    

df = load_data()
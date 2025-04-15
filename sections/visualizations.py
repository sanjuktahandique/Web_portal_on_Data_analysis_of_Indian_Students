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
import requests
from bs4 import BeautifulSoup


from utils.data_loader import load_data

df = load_data()


def visualizations_section():
    topics = ["Age","Gender", "Education", "Average ScreenTime","Health Issues", "Educational Screentime", "Entertainment Screentime","Concentration Level","Negative Online experiences","Health problems vs age"]

# Sidebar selectbox for navigation
    selected_topic = st.sidebar.selectbox("Select a topic", topics)
    
    st.header("Visualizations of from the Dataset")
    # List of subheaders (you can replace this with your actual subheader content)
    st.write("This section presents a visual analysis of the raw data in comparison to the percentage distribution of individuals across various categories such as age, educational qualification, screen time,negative online experiences and concentration levels. These visuals provide an intuitive understanding of the dataset, highlighting key trends and patterns. By comparing raw data to percentage-based distributions, the analysis offers insights into how these factors vary among the population, laying the groundwork for exploring potential correlations and relationships in subsequent sections.")
    
    #Age vs Percentage of People
    if selected_topic == "Age":
        st.subheader("Age vs Percentage of People")
        st.write("According to the dataset I have collected, the following age group people responded. The population vs. age graph displays the distribution of individuals across various age groups, revealing trends in population density across different age ranges. This graph provides insights into the demographic composition of the data.")

        age_counts = df['Age'].value_counts(normalize=True) * 100
        age_counts = age_counts.sort_index()

        fig, ax = plt.subplots(figsize=(6, 4))
        age_counts.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_xlabel('Age')
        ax.set_ylabel('Percentage of People')
        st.pyplot(fig)

    elif selected_topic == "Gender":
            # Gender distribution pie chart 
            st.subheader("Gender Distribution")
            gender_counts = df['Gender'].value_counts(normalize=True) * 100
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(
                gender_counts, 
                labels=gender_counts.index, 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=['#FF9999', '#66B3FF']
            )
            ax.axis("equal")
            st.pyplot(fig)


    
    
    elif selected_topic == "Education":
        st.subheader('Educational Qualification vs Percentage of People')
        st.write("The population vs. educational qualification graph shows the distribution of individuals across different education levels, highlighting trends in the educational attainment within the population. This graph offers a deeper understanding of the educational composition of the dataset.")
        edu_counts = df['Education'].value_counts(normalize=True) * 100

            # Plotting the bar chart using Matplotlib
        fig, ax = plt.subplots()
        edu_counts.plot(kind='bar', ax=ax)
        bars = ax.bar(edu_counts.index, edu_counts, color='skyblue')
            
            # Adding percentage labels on top of each bar
        for bar, percentage in zip(bars, edu_counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.3,  # Position above the bar
                f'{percentage:.1f}%', 
                ha='center', 
                va='bottom'
            )
            
            # Setting labels and title
        ax.set_xlabel('Educational Qualification')
        ax.set_ylabel('Percentage of People')

            
            # Display the plot in Streamlit
        st.pyplot(fig)



    elif selected_topic == "Average ScreenTime":
    # Define custom order for Avg_Screentime (daily)
        screentime_order = [
        'Less than 2 Hours',
        '2 to 4 Hours',
        '4 to 6 Hours',
        '6 to 8 Hours',
        '8 to 10 Hours',
        '10 to 14 Hours',
        'More than 14 Hours'
        ]

    # Define custom order for Avg_Screentime for educational and entertainment purposes
        educational_entertainment_order = [
        'Less than 2 Hours',
        '2 to 4 Hours',
        '4 to 6 Hours',
        '6 to 8 Hours',
        '8 to 10 Hours',
        'More than 10 Hours'
        ]

    # Define custom order for Age-related attributes
        age_order = [
        'Under 5 years old',
        '6 to 10 years old',
        '11 to 15 years old',
        '15 to 20 years old',
        'Over 20 years old'
        ]

        health_effects_order = [
        'Less sleep duration', 'Severe headaches', 'Myopia (Nearsightedness)', 'Eye Fatigue', 
        'Dry eyes', 'ADHD/Difficulty in attention', 'Slowed thinking, speaking, or body movements', 
        'Reduced Psychological well-being', 'Change in social behaviour', 'Having no motivation or interest in things'
        ]

    # Remove the dropdown and directly display visualizations for each column



    # Avg_Screentime (daily)
        st.subheader('Avg Screen Time (Daily) vs Percentage of People')
        st.write("The daily screen time data, as represented in the dataset, reflects the average time individuals spend on screens each day. It offers valuable insights into screen usage patterns across different demographic groups")
        df_filtered = df[['Avg_Screentime(daily)']].dropna()
        df_filtered['Avg_Screentime(daily)'] = pd.Categorical(df_filtered['Avg_Screentime(daily)'], categories=screentime_order, ordered=True)
        screentime_counts = df_filtered['Avg_Screentime(daily)'].value_counts(normalize=True) * 100
        screentime_counts = screentime_counts.sort_index()
        fig, ax = plt.subplots()
        screentime_counts.plot(kind='bar', ax=ax)
        bars = ax.bar(screentime_counts.index.astype(str), screentime_counts, color='skyblue')
        for bar, percentage in zip(bars, screentime_counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'{percentage:.1f}%', ha='center', va='bottom')
        st.pyplot(fig)

    elif selected_topic == "Health Issues":
    # Health Effects Cohort Matrix
        st.subheader('Health Effects Cohort Matrix')
        st.write("The graph represents the health effects experienced by individuals within the dataset, illustrating the prevalence and distribution of various health outcomes. It provides a comprehensive overview of how different health conditions are represented across the population, offering valuable insights into the potential factors influencing overall well-being.")
        health_effects_series = df['Health_Effects'].dropna().str.split(',')
        all_health_effects = [effect.strip() for sublist in health_effects_series for effect in sublist]
        all_health_effects = [effect for effect in all_health_effects if effect != "0"]
        health_effects_counts = pd.Series(all_health_effects).value_counts()
        health_effects_percentage = (health_effects_counts / len(df)) * 100
        health_effects_df = pd.DataFrame({
            'Health Effect': health_effects_percentage.index,
            'Occurences': health_effects_percentage.values
            })
        
        cohort_matrix = health_effects_df.set_index('Health Effect').T
        if '0' in cohort_matrix.index:
            cohort_matrix = cohort_matrix.drop('0')
        fig, ax = plt.subplots(figsize=(10, 1))
        sns.heatmap(cohort_matrix, annot=True, cmap="YlOrRd", fmt=".1f", cbar=True, ax=ax)
        ax.set_xlabel('Health Effects')
        ax.set_title('Health Effects Cohort Matrix: Percentage of People')
        
        st.pyplot(fig)

    elif selected_topic == "Educational Screentime":
        educational_entertainment_order = [
        'Less than 2 Hours',
        '2 to 4 Hours',
        '4 to 6 Hours',
        '6 to 8 Hours',
        '8 to 10 Hours',
        'More than 10 Hours'
        ]
# Avg_Screentime for educational purpose
        st.subheader('Avg Screen Time for Educational Purpose vs Percentage of People')
        st.write("Educational purpose screen time refers to the amount of time individuals spend using screens for activities aimed at learning, such as studying, attending online classes, or engaging with educational content. This data helps identify trends in how technology is utilized for academic purposes and its potential impact on learning outcomes.")

        st.write("For my dataset, I collected information on educational purpose screen time through a manual survey conducted using Google Forms. The survey included questions about the time spent on educational activities involving screens, capturing responses from a diverse group of participants across different age groups and educational backgrounds.")
        df_filtered = df[['Avg_screentime_for_educational_purpose']].dropna()
        df_filtered['Avg_screentime_for_educational_purpose'] = pd.Categorical(df_filtered['Avg_screentime_for_educational_purpose'], categories=educational_entertainment_order, ordered=True)
        educational_counts = df_filtered['Avg_screentime_for_educational_purpose'].value_counts(normalize=True) * 100
        educational_counts = educational_counts.sort_index()
        fig, ax = plt.subplots()
        educational_counts.plot(kind='bar', ax=ax)
        bars = ax.bar(educational_counts.index.astype(str), educational_counts, color='skyblue')
        for bar, percentage in zip(bars, educational_counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'{percentage:.1f}%', ha='center', va='bottom')
        st.pyplot(fig)

    elif selected_topic == "Entertainment Screentime":
        educational_entertainment_order = [
        'Less than 2 Hours',
        '2 to 4 Hours',
        '4 to 6 Hours',
        '6 to 8 Hours',
        '8 to 10 Hours',
        'More than 10 Hours'
        ]

# Avg_Screentime for entertainment purpose
        st.subheader('Avg Screen Time for Entertainment Purpose vs Percentage of People')
        df_filtered = df[['Avg Screentime for entertainment purpose']].dropna()
        df_filtered['Avg Screentime for entertainment purpose'] = pd.Categorical(df_filtered['Avg Screentime for entertainment purpose'], categories=educational_entertainment_order, ordered=True)
        entertainment_counts = df_filtered['Avg Screentime for entertainment purpose'].value_counts(normalize=True) * 100
        entertainment_counts = entertainment_counts.sort_index()
        fig, ax = plt.subplots()
        entertainment_counts.plot(kind='bar', ax=ax)
        bars = ax.bar(entertainment_counts.index.astype(str), entertainment_counts, color='skyblue')
        for bar, percentage in zip(bars, entertainment_counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'{percentage:.1f}%', ha='center', va='bottom')
        st.pyplot(fig)

    elif selected_topic == "Concentration Level":
        st.subheader('Concentration Level')
        st.write("The concentration level data, as presented in the dataset, examines how individuals' ability to focus. How long an individual can concentrate in one go is evaluated in this dataset")
        embed_code = """
        <div class='tableauPlaceholder' id='viz1734372550379' style='position: relative'>
    <noscript>
        <a href='#'>
        <img alt='Concentration level' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17343706624140&#47;Sheet1&#47;1_rss.png' style='border: none' />
        </a>
    </noscript>
    <object class='tableauViz'  style='display:none;'>
        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
        <param name='embed_code_version' value='3' /> 
        <param name='site_root' value='' />
        <param name='name' value='Book1_17343706624140&#47;Sheet1' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17343706624140&#47;Sheet1&#47;1.png' />
        <param name='animate_transition' value='yes' />
        <param name='display_static_image' value='yes' />
        <param name='display_spinner' value='yes' />
        <param name='display_overlay' value='yes' />
        <param name='display_count' value='yes' />
        <param name='language' value='en-US' />
        <param name='filter' value='publish=yes' />
    </object>
        </div>
        <script type='text/javascript'>
    var divElement = document.getElementById('viz1734372550379');                    
    var vizElement = divElement.getElementsByTagName('object')[0];                    
    vizElement.style.width='100%';
    vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    
    var scriptElement = document.createElement('script');                    
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
        """

    # Use Streamlit's HTML component to embed the Tableau report
        st.components.v1.html(embed_code, height=800)

    elif selected_topic == "Negative Online experiences":
# Negative Experiences Cohort Matrix
        st.subheader('Negative Experiences Cohort Matrix')
        st.write("According to my dataset, the cohort graph illustrates the recent occurrences of negative influences, highlighting the frequency and distribution of these events across different groups within the population.")
                # Drop rows with NaN in 'Negative Experiences' and split by commas
        negative_experiences_series = df['Negative Experiences'].dropna().str.split(',')
                
                # Flatten and clean the list of negative experiences
        all_negative_experiences = [experience.strip() for sublist in negative_experiences_series for experience in sublist]
        
                
                # Calculate the count and percentage of people for each unique negative experience
        negative_experiences_counts = pd.Series(all_negative_experiences).value_counts()
        negative_experiences_percentage = (negative_experiences_counts / len(df)) * 100
        negative_experiences_df = pd.DataFrame({
                'Negative Experience': negative_experiences_percentage.index,
                'Occurences': negative_experiences_percentage.values
            })
        negative_experiences_df = negative_experiences_df[~negative_experiences_df['Negative Experience'].isin(['No', "i haven't"])]

                # Pivot data for a cohort matrix representation
        cohort_matrix = negative_experiences_df.set_index('Negative Experience').T
                
                # Plotting the cohort matrix as a heatmap
        fig, ax = plt.subplots(figsize=(10, 1))  # Adjust the figure size as needed
        sns.heatmap(cohort_matrix, annot=True, cmap="YlOrRd", fmt=".1f", cbar=True, ax=ax)
        ax.set_xlabel('Negative Experiences')
        ax.set_title('Negative Experiences Cohort Matrix: Percentage of People')

                # Display the cohort matrix in Streamlit
        st.pyplot(fig)


    elif selected_topic == "Health problems vs age":
# Age-related attributes
        age_related_columns = [
        'Age when-Less sleep duration-occured',
        'Age when-Severe headaches-occured',
        'Age when-Myopia(Nearsightedness)-occured',
        'Age when-Eye Fatigue-occured',
        'Age when-Dry eyes-occured',
        'Age when-ADHD/Difficulty in attention-occured',
        'Age when-Slowed thinking, speaking, or body movements-occured',
        'Age_when-Reduced_Psychological_well_being-occured',
        'Age when-Change in social behaviour-occured',
        'Age when-Having no motivation or interest in things-occured'
        ]

        selected_column = st.selectbox('Select an Age-related Column to View', age_related_columns)

    # Check if the selected column exists in your dataframe (df)
        if selected_column in df.columns:
            st.subheader(f'{selected_column} vs Percentage of People')
            df_filtered = df[[selected_column]].dropna()
            df_filtered = df_filtered[df_filtered[selected_column] != '0']
            # Convert the selected column to a categorical variable with ordered categories
            df_filtered[selected_column] = pd.Categorical(df_filtered[selected_column],  ordered=True)
            
            # Calculate the percentage of each unique value
            age_counts = df_filtered[selected_column].value_counts(normalize=True) * 100
            age_counts = age_counts.sort_index()  # Sort by index to maintain the order
            
            # Plot the data using matplotlib
            fig, ax = plt.subplots()
            age_counts.plot(kind='bar', ax=ax)
            bars = ax.bar(age_counts.index.astype(str), age_counts, color='lightblue')
            
            # Add percentages above each bar
            for bar, percentage in zip(bars, age_counts):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f'{percentage:.1f}%', ha='center', va='bottom')
            
            # Display the plot in Streamlit
            st.pyplot(fig)





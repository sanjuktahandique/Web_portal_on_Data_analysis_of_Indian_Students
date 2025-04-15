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
import requests
from bs4 import BeautifulSoup
from scipy.stats import spearmanr
from utils.data_loader import load_data

df = load_data()

def screen_time_section():
    global df
    category_mapping={
    "Less than 2 Hours": "Low",
    "2 to 4 Hours": "Moderate",
    "4 to 6 Hours": "High",
    "6 to 8 Hours": "Severe",
    "8 to 10 Hours": "Severe",
    "10 to 14 Hours": "Severe",
    "More than 14 Hours": "Severe",
    "More than 10 Hours": "Severe",
    }

    df["ScreenTime Category"] = df["Avg_Screentime(daily)"].map(category_mapping)

    # Streamlit UI
    st.header("Categorization of Screen Time")
    st.write("According to research, screen time can be classified into various categories based on the duration of usage. These classifications help to better understand the impact of screen time on individuals:")
   

    # Show categorized data
    
    data = {
    "Low": ["Less than 2 Hours"],
    "Moderate": ["2 to 4 Hours"],
    "High": [ "4 to 6 Hours"],
    "Severe": ["6 to 8 Hours", "8 to 10 Hours", "10 to 14 Hours", "More than 14 Hours"],
    }
    # Streamlit app layout
    

  



# Loop through each category and display its items
    for category, items in data.items():
        st.subheader(category)
        for item in items:
            st.text(f"- {item}")

    st.write("These categories will be used to analyze the relationship between screen time duration and potential health or behavioral outcomes from the dataset")

    # Optional: Filter by category
    selected_category = st.selectbox("Filter by Category:", options=df["ScreenTime Category"].unique())
    filtered_data = df[df["ScreenTime Category"] == selected_category]
    st.subheader(f"Details for {selected_category} Screen Time")
    st.dataframe(filtered_data)

    st.subheader("Screen Time Category Distribution")
    def apply_custom_css():
        css = """
        <style>
            body {
            font-family: 'Times New Roman', sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
            }
            .main-container {
            max-width: 800px;
            font-family: 'Times New Roman', sans-serif;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            }
            h1 {
            color: #2c3e50;
            
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 20px;
            }
            h2 {
            color: #34495e;
            font-size: 1.8rem;
            margin-bottom: 15px;
            }
            h3 {
            color: #7f8c8d;
            font-size: 1.5rem;
            margin-bottom: 10px;
            }
            p {
            line-height: 1.6;
            font-family: 'Times New Roman', sans-serif, monospace !important;
            margin-bottom: 15px;
            }
            .insight {
            background-color: #ecf0f1;
            padding: 15px;
            border-left: 5px solid #3498db;
            margin-bottom: 20px;
            border-radius: 5px;
            }
            .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.9rem;
            color: #95a5a6;}
            .image-container {
            text-align: center;
            margin-bottom: 20px;
            }
            .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            
            }
        </style>
        """
        html(css)

    # Apply the CSS styling
    

    # Streamlit content with structure
    
    
    

    st.markdown("""
    
    <p>In the dataset I have collected, the distribution of screen time categories is as follows: 
    """, unsafe_allow_html=True)
    st.markdown("""

    
    <ul>
        <li>*Severe screen time(6 to 14+ hours)* accounts for 65% of the participants, indicating that a majority of individuals spend extended periods of time on screens daily, which may suggest potential concerns about excessive screen use.</li>
        <li>*High screen time (4 to 6 hours)* makes up 21% of the population, reflecting a significant portion of individuals who engage in lengthy screen usage but to a lesser extent than the severe category.</li>
        <li>*Moderate screen time (2 to 4 hours)* comprises 9% of the dataset, pointing to a smaller group of individuals with more balanced screen time habits.</li>
        <li>*Low screen time (less than 2 hours)* represents only 5%, indicating that very few individuals in the dataset limit their screen time to under two hours a day.</li>
    </ul>
     
                
    
    <p>This distribution highlights a significant portion of the population engaging in high to severe screen time.</p>
    
     """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    # Calculate the counts for each category
    category_counts = df["ScreenTime Category"].value_counts()

    # Plot the pie chart
    fig, ax = plt.subplots()
    ax.pie(
        category_counts, 
        labels=category_counts.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie is a circle
    ax.set_title("Distribution of Screen Time Categories")

    # Display the pie chart in Streamlit
    st.pyplot(fig)


    #filter experiences
    st.title("Exploring the Relationship Between Screen Time and Online Negative Experiences")
    st.write("Now we will analyse the relationship between Screen Time and Online Negative Experiences")
    screen_time_category = st.selectbox(
    "Filter by Screen Time Category",
    options=["All"] + df["ScreenTime Category"].unique().tolist(),
    key="4"
    )


    if screen_time_category != "All":
        filtered_df = df[df["ScreenTime Category"] == screen_time_category]
    else:
        filtered_df = df

# Display data
    st.text(f"Showing Data for: {screen_time_category if screen_time_category != 'All' else 'All Categories'}")


    def extract_experiences_with_counts(df, column_name, exclude_values=["0", "No", "i haven't"]):
    # Drop NaN values and split each entry by comma
        experiences_series = filtered_df[column_name].dropna().str.split(',')
    
    # Flatten the list and strip whitespace
        all_experiences = [effect.strip() for sublist in experiences_series for effect in sublist]
        filtered_effects = [effect for effect in all_experiences if effect not in exclude_values]
    # Count occurrences of each health effect
        experiences_counts = pd.Series(filtered_effects).value_counts()
        return experiences_counts

# Extract unique health effects with their counts
    experiences_counts = extract_experiences_with_counts(filtered_df, "Negative Experiences")

# Display the unique health effects and their counts in Streamlit
    
    st.write("The following table shows the unique health effects and their counts:")
    st.table(experiences_counts.reset_index().rename(columns={"index": "Negative Experiences", 0: "Count"}))

    st.markdown("""

    <p>The health and mental effects related to screen time also extend beyond physical and cognitive issues, encompassing significant risks associated with online interactions. These effects are observed across various categories of screen time usage, with the following counts:

 
    <ul>
        <li>Scams and Fraud leading to financial loss or loss of personal data: A significant number of individuals reported encountering online scams or fraudulent activities, which resulted in financial losses or compromised personal information. This issue is more prevalent in the higher screen time categories.</li>
        <li>Exposure to Radical Ideologies: Exposure to extreme or radical content is a concern for some users, especially those with higher screen time. This exposure can influence beliefs and opinions, leading to psychological distress or altered worldviews.</li>
        <li>Exploitation and Manipulation through Social Media: Many individuals, particularly those in the moderate to severe screen time categories, report being manipulated or exploited through social media platforms, often affecting their self-esteem, decision-making, and social behavior..</li>
        <li>Identity Theft: Instances of identity theft were noted in the dataset, with individuals experiencing the unauthorized use of personal information, especially among those who spend excessive time online, increasing their vulnerability.</li>
        <li>Cyberbullying or Hate Speech: Cyberbullying and exposure to hate speech were reported by participants, particularly those with higher screen time, leading to emotional distress, anxiety, and a decline in overall mental health.</li>
        <li>Malware and Phishing Attacks: The dataset reveals that individuals exposed to significant online activity are at a higher risk of falling victim to malware or phishing attacks, which can compromise their devices, data, and personal security.</li>
        <li>Online Harassment: Online harassment, including threats or verbal abuse, was reported by some users, particularly in high-screen time categories, contributing to feelings of fear, anxiety, and social withdrawal.</li>
        </ul>
     
                
    
    <p>These issues highlight significant risks related to online interactions and underscore the importance of awareness and precautions to protect personal safety and mental health.
        """, unsafe_allow_html=True)
    

    st.markdown('</div>', unsafe_allow_html=True)

    # Split multiple negative experiences into separate rows
    df_split = df.assign(
            NegativeExperiences=df['Negative Experiences'].fillna('').str.split(', ')
        ).explode('NegativeExperiences')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['NegativeExperiences'] != '0']
    df_split = df_split[df_split['NegativeExperiences'] != 'No']
    df_split = df_split[df_split['NegativeExperiences'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['NegativeExperiences'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
        
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
        
        # Display the updated contingency table
     # Dropdown to select a negative experience
    negative_experiences = contingency_table.columns.tolist()
    selected_experience = st.selectbox("Select a Negative Experience to Visualize", negative_experiences)
        
        # Visualization for the selected negative experience
    if selected_experience:
            fig, ax = plt.subplots()
            contingency_table[selected_experience].plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f"Distribution of {selected_experience} Across ScreenTime Categories")
            ax.set_xlabel("ScreenTime Category")
            ax.set_ylabel("Frequency")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)
    st.write(contingency_table)
    if 'ScreenTime Category' in df.columns and 'Negative Experiences' in df.columns:
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2

      
        # Perform Chi-Square Test
        
        # Calculate row and column totals
        row_totals = modified_data.sum(axis=1)
        col_totals = modified_data.sum(axis=0)
        grand_total = modified_data.values.sum()

        # Calculate expected frequencies
        expected_frequencies = pd.DataFrame(
        np.outer(row_totals, col_totals) / grand_total,
            index=modified_data.index,
            columns=modified_data.columns
        )
        # Calculate Chi-Square statistic
        observed = modified_data.values
        expected = expected_frequencies.values
        chi_square_table = (observed - expected) ** 2 / expected
        chi_square_statistic = np.nansum(chi_square_table)
        
        # Degrees of freedom
        dof = (modified_data.shape[0] - 1) * (modified_data.shape[1] - 1)
        
        # Automatically determine the critical value for alpha=0.05
        critical_value = chi2.ppf(0.95, dof)  # 0.95 is 1 - 0.05 for 5% significance level

        # Interpretation
        
        if chi_square_statistic > critical_value:
            st.write("Here the Chi Square test suggests that there is sufficient evidence to reject the null hypothesis. This indicates a statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time may play a role in influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is greater than the critical value.")
           
        else:
            st.write("Here the Chi Square test suggests that there is insufficient evidence to reject the null hypothesis. This indicates that there is no statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time does not appear to be a major factor influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
                   
        st.write("For Futher details refer to the Statistical Analysis")  
        st.write("The analysis indicates that the screen time field is too broad and vague to draw a definitive association with negative online experiences such as cyberbullying, phishing, or harassment. Screen time encompasses a wide range of activities, from educational purposes to entertainment, each potentially influencing behavior and experiences in different ways. Therefore, it is not accurate to attribute negative experiences solely to long hours of screen time. While extended screen time may contribute to certain risks, other factors—such as the type of content consumed, individual behaviors, and environmental influences—must also be considered when examining the relationship between screen time and negative online experiences.")      
    else:
        st.write("The Columns Doesnot exist.")





    st.write("## Types of Screentime")
    st.markdown("""
    
    <p>There are two main types of screen time based on purpose: educational and entertainment.
    
    <p>On the other hand, entertainment screen time involves the use of digital media for leisure and relaxation, such as watching TV shows, playing video games, or browsing social media. While entertainment screen time offers opportunities for stress relief and social interaction, excessive engagement can lead to negative outcomes like reduced physical activity, sleep disturbances, and impacts on mental health. Balancing both types of screen time is essential for maintaining a healthy lifestyle, ensuring that technology serves its purpose without overshadowing essential personal and academic development.
        
    """, unsafe_allow_html=True)
    st.subheader("Educational Screentime Analysis")
    st.write("Educational screen time refers to the use of digital devices for learning, skill development, or acquiring knowledge. This can include activities like online courses, reading e-books, or interactive learning apps designed to enhance cognitive development and academic performance. Educational screen time is generally considered beneficial when used in moderation, as it can provide valuable opportunities for growth and intellectual engagement.")
    category_mappin={
    "Less than 2 Hours": "Low",
    "2 to 4 Hours": "Moderate",
    "4 to 6 Hours": "High",
    "6 to 8 Hours": "Severe",
    "8 to 10 Hours": "Severe",
    "10 to 14 Hours": "Severe",
    "More than 14 Hours": "Severe",
    "More than 10 Hours": "Severe",
    }
    df["EDU_ScreenTime_Category"] = df["Avg_screentime_for_educational_purpose"].map(category_mappin)
    if 'EDU_ScreenTime_Category' in df.columns and 'Negative Experiences' in df.columns:
        # Split multiple negative experiences into separate rows
        df_split = df.assign(
            NegativeExperiences=df['Negative Experiences'].fillna('').str.split(', ')
        ).explode('NegativeExperiences')
        
        # Remove rows where NegativeExperiences is '0' or empty
        df_split = df_split[df_split['NegativeExperiences'] != '0']
        df_split = df_split[df_split['NegativeExperiences'] != 'No']
        df_split = df_split[df_split['NegativeExperiences'] != "i haven't"]
        
        # Generate the contingency table
        contingency_table = pd.crosstab(df_split['EDU_ScreenTime_Category'], df_split['NegativeExperiences'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
        contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
        
        # Reorder the screentime categories
        screentime_order = ['Severe', 'High', 'Moderate', 'Low']
        contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
        
        # Display the updated contingency table
        st.write("### Educational Screentime Table")
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2
        st.write(modified_data)
        st.markdown("""
    
    <p>Now, we will analyze if educational screen time has any relation to negative influences such as cyberbullying, phishing, scam fraud, online harassment, and other risks using a Chi-square test.
    <p>The Chi-square test is a statistical method used to determine if there is a significant association between two categorical variables. In this case, we will categorize individuals based on their educational screen time (e.g., high or low usage) and the presence or absence of negative online experiences (e.g., experienced cyberbullying, phishing attempts, etc.). By conducting the Chi-square test, we aim to assess whether these negative influences occur more frequently in those who engage in higher amounts of educational screen time compared to those with lower levels of engagement.
    
    
    """, unsafe_allow_html=True)
      
        # Perform Chi-Square Test
        
        # Calculate row and column totals
        row_totals = modified_data.sum(axis=1)
        col_totals = modified_data.sum(axis=0)
        grand_total = modified_data.values.sum()

        # Calculate expected frequencies
        expected_frequencies = pd.DataFrame(
        np.outer(row_totals, col_totals) / grand_total,
            index=modified_data.index,
            columns=modified_data.columns
        )
        # Calculate Chi-Square statistic
        observed = modified_data.values
        expected = expected_frequencies.values
        chi_square_table = (observed - expected) ** 2 / expected
        chi_square_statistic = np.nansum(chi_square_table)
        
        # Degrees of freedom
        dof = (modified_data.shape[0] - 1) * (modified_data.shape[1] - 1)
        
        # Automatically determine the critical value for alpha=0.05
        critical_value = chi2.ppf(0.95, dof)  # 0.95 is 1 - 0.05 for 5% significance level
        
       
        if chi_square_statistic > critical_value:
            st.write("Here the Chi Square test suggests that there is sufficient evidence to reject the null hypothesis. This indicates a statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time may play a role in influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is greater than the critical value.")
           
        else:
            st.write("Here the Chi Square test suggests that there is insufficient evidence to reject the null hypothesis. This indicates that there is no statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time does not appear to be a major factor influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
                   
        st.write("For Futher details refer to the Statistical Analysis")
    else:
        st.write("The Columns Doesnot exist.")
    
    
    #ENTERTAINMENT
    st.subheader("Entertainment Screentime Analysis")
    st.write("Entertainment screen time involves the use of digital media for leisure and relaxation, such as watching TV shows, playing video games, or browsing social media. While entertainment screen time offers opportunities for stress relief and social interaction, excessive engagement can lead to negative outcomes like reduced physical activity, sleep disturbances, and impacts on mental health. Balancing both types of screen time is essential for maintaining a healthy lifestyle, ensuring that technology serves its purpose without overshadowing essential personal and academic development.")
    category_mappin={
    "Less than 2 Hours": "Low",
    "2 to 4 Hours": "Moderate",
    "4 to 6 Hours": "High",
    "6 to 8 Hours": "Severe",
    "8 to 10 Hours": "Severe",
    "10 to 14 Hours": "Severe",
    "More than 14 Hours": "Severe",
    "More than 10 Hours": "Severe",
    }
    df["ENT_ScreenTime_Category"] = df["Avg Screentime for entertainment purpose"].map(category_mappin)


    if 'ENT_ScreenTime_Category' in df.columns and 'Negative Experiences' in df.columns:
        # Split multiple negative experiences into separate rows
        df_split = df.assign(
            NegativeExperiences=df['Negative Experiences'].fillna('').str.split(', ')
        ).explode('NegativeExperiences')
        
        # Remove rows where NegativeExperiences is '0' or empty
        df_split = df_split[df_split['NegativeExperiences'] != '0']
        df_split = df_split[df_split['NegativeExperiences'] != 'No']
        df_split = df_split[df_split['NegativeExperiences'] != "i haven't"]
        
        # Generate the contingency table
        contingency_table = pd.crosstab(df_split['ENT_ScreenTime_Category'], df_split['NegativeExperiences'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
        contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
        
        # Reorder the screentime categories
        screentime_order = ['Severe', 'High', 'Moderate', 'Low']
        contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
        
        # Display the updated contingency table
        
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2

        st.write(modified_data)
        st.markdown("""
    
    <p>Now, we will analyze if Entertainment screen time has any relation to negative influences such as cyberbullying, phishing, scam fraud, online harassment, and other risks using a Chi-square test.
    
    
    """, unsafe_allow_html=True)
      
        # Perform Chi-Square Test
        
        # Calculate row and column totals
        row_totals = modified_data.sum(axis=1)
        col_totals = modified_data.sum(axis=0)
        grand_total = modified_data.values.sum()

        # Calculate expected frequencies
        expected_frequencies = pd.DataFrame(
        np.outer(row_totals, col_totals) / grand_total,
            index=modified_data.index,
            columns=modified_data.columns
        )
        




        # Calculate Chi-Square statistic
        observed = modified_data.values
        expected = expected_frequencies.values
        chi_square_table = (observed - expected) ** 2 / expected
        chi_square_statistic = np.nansum(chi_square_table)
        
        # Degrees of freedom
        dof = (modified_data.shape[0] - 1) * (modified_data.shape[1] - 1)
        
        # Automatically determine the critical value for alpha=0.05
        critical_value = chi2.ppf(0.95, dof)  # 0.95 is 1 - 0.05 for 5% significance level
        
        # Display Chi-Square table, statistic, and critical value
              
        
        
        if chi_square_statistic > critical_value:
            st.write("Here the Chi Square test suggests that there is sufficient evidence to reject the null hypothesis. This indicates a statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time may play a role in influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is greater than the critical value.")
           
        else:
            st.write("Here the Chi Square test suggests that there is insufficient evidence to reject the null hypothesis. This indicates that there is no statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time does not appear to be a major factor influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
                   
        st.write("For Futher details refer to the Statistical Analysis")
    
        st.write("#### Overview")
        st.write("Based on the analysis, the Chi-square test reveals no statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. This suggests that educational screen time does not significantly impact an individual’s exposure to these risks. In contrast, it is likely that other factors, such as entertainment screen time, may have a more prominent effect on these experiences. The findings imply that while educational screen time can offer valuable learning opportunities, it does not appear to contribute substantially to the negative online influences that are often associated with excessive entertainment screen time.")
    else:
        st.write("The Columns Doesnot exist.")


#filter Health effects
    st.title("Health and Mental Effects Based on category of Screentime")
    st.write("Health issues, both physical and mental, have a profound impact on our daily lives, influencing not only individual well-being but also productivity, social interactions, and overall quality of life. These issues, ranging from chronic conditions to mental health challenges, can disrupt routine activities, hinder academic or professional performance, and lead to long-term consequences if not addressed effectively. In particular, the growing prevalence of screen time, especially among students, has raised concerns about its potential effects on both physical and mental health.")
    st.write("In this analysis, I aim to investigate the significant relationship between screen time and the health and mental issues faced by students. By examining this connection, I hope to uncover insights that can inform strategies to mitigate the adverse effects of excessive screen time on student health, ultimately promoting a healthier, more balanced lifestyle.")

    screen_time_category = st.selectbox(
    "Filter by Screen Time Category",
    options=["All"] + df["ScreenTime Category"].unique().tolist(),
    key="3"
    )


    if screen_time_category != "All":
        filtered_df = df[df["ScreenTime Category"] == screen_time_category]
    else:
        filtered_df = df

# Display data
    st.text(f"Showing Data for: {screen_time_category if screen_time_category != 'All' else 'All Categories'}")


    def extract_health_effects_with_counts(df, column_name, exclude_values=["0", "No", "i haven't"]):
    # Drop NaN values and split each entry by comma
        health_effects_series = filtered_df[column_name].dropna().str.split(',')
    
    # Flatten the list and strip whitespace
        all_health_effects = [effect.strip() for sublist in health_effects_series for effect in sublist]
        filtered_effects = [effect for effect in all_health_effects if effect not in exclude_values]
    # Count occurrences of each health effect
        health_effects_counts = pd.Series(filtered_effects).value_counts()
        return health_effects_counts

# Extract unique health effects with their counts
    health_effects_counts = extract_health_effects_with_counts(filtered_df, "Health_Effects")

# Display the unique health effects and their counts in Streamlit
    
    st.write("The following table shows the unique health effects and their counts:")
    st.table(health_effects_counts.reset_index().rename(columns={"index": "Health Effect", 0: "Count"}))
   
    st.markdown("""

    <p>According to the screen time categories in the dataset, individuals in the Severe screen time category (6 to 14+ hours) show the highest prevalence of health and mental effects. These effects include:
 
    <ul>
        <li>**Having no motivation or interest in things:** Individuals may experience a lack of enthusiasm or interest in activities outside of their usual routine, leading to disengagement from hobbies, work, or social interactions.</li>
        <li><b>Less sleep duration:* Some people may find themselves getting fewer hours of sleep due to difficulty falling asleep or staying asleep, which can lead to daytime fatigue and reduced overall well-being.</li>
        <li><B>ADHD/Difficulty in attention:* Difficulty in maintaining focus, frequent distractions, and trouble completing tasks are common signs of attention challenges, which can affect performance in school, work, and daily activities.</li>
        <li><B>Myopia (Nearsightedness):* This condition results in difficulty seeing distant objects clearly while close-up vision remains unaffected. It often progresses over time and can impact everyday activities such as driving and reading signs.</li>
        <li><B>Eye Fatigue:* Prolonged periods of visual concentration, especially on screens, can lead to discomfort, dry eyes, blurry vision, and general eye strain, often accompanied by headaches or soreness.</li>
        <li><B>Slowed thinking, speaking, or body movements:* Individuals may notice a decrease in cognitive processing speed, speech delay, or sluggish physical movements, which can affect their ability to perform tasks or engage in conversations effectively.</li>
        <li><B>Dry eyes:* Dryness and irritation in the eyes occur when there is insufficient moisture on the surface of the eyes, causing discomfort, redness, and sensitivity, often resulting in the need for frequent blinking or eye drops.</li>
        <li><B>Severe headaches:* Intense, recurring headaches may occur, which can be debilitating and interfere with daily activities, often accompanied by symptoms such as light sensitivity or nausea.</li>
        <li><B>Change in social behavior:* Changes in social behavior may include increased withdrawal from in-person interactions, less engagement in face-to-face communication, and alterations in how individuals interact with others online.</li>
        <li><B>Reduced psychological well-being:* This refers to a decline in emotional health, including feelings of anxiety, depression, and stress, which may lead to decreased satisfaction with life and difficulty managing emotions.</li>
    </ul>
     
                
    
    <p>The count for each effect is higher in the severe screen time category, suggesting a strong correlation between extended screen usage and negative health outcomes. A significant number of individuals in this group report experiencing these symptoms, highlighting the potential risks associated with prolonged screen exposure.
    <p>Meanwhile, the High screen time group (4 to 6 hours) also shows a moderate occurrence of these health and mental effects, while the Moderate (2 to 4 hours) and Low (less than 2 hours) groups report fewer symptoms, indicating a clear trend of increasing health issues with more screen time.
    <p>We can see and compare the Screentime Group with the help of the following table:-
    """, unsafe_allow_html=True)
    

    st.markdown('</div>', unsafe_allow_html=True)
    # # Split multiple health effects into separate rows
    df_split = df.assign(
            HealthEffects=df['Health_Effects'].fillna('').str.split(', ')
        ).explode('HealthEffects')
        # Remove rows where HealthEffects is '0' or empty
    df_split = df_split[df_split['HealthEffects'] != '0']
    df_split = df_split[df_split['HealthEffects'] != '']
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['HealthEffects'])
        
        # Remove zero-valued health effects (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
        
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
        
        # Display the updated contingency table
    
    
     # Dropdown to select a health effect
    health_effects = contingency_table.columns.tolist()
    selected_effect = st.selectbox("Select a Health Effect to Visualize", health_effects)
        
        # Visualization for the selected health effect
    if selected_effect:
            fig, ax = plt.subplots()
            contingency_table[selected_effect].plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f"Distribution of {selected_effect} Across ScreenTime Categories")
            ax.set_xlabel("ScreenTime Category")
            ax.set_ylabel("Frequency")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)
    st.write(contingency_table)
    st.write("Now, we will check the relationship of this fields by conducting a Chi-square test. The Chi-square test is used to determine whether there is a significant association between two categorical variables. In this case, we will examine if there is a relationship between the amount of screen time and the occurrence of health and mental issues among students. By using the Chi-square test, we aim to assess whether variations in screen time are associated with the frequency of specific health and mental concerns, providing statistical evidence to support or refute the hypothesis of a significant connection.")
     # Perform Chi-Square Test
    if 'ScreenTime Category' in df.columns and 'Health_Effects' in df.columns:
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2

      
        # Perform Chi-Square Test
        
        # Calculate row and column totals
        row_totals = modified_data.sum(axis=1)
        col_totals = modified_data.sum(axis=0)
        grand_total = modified_data.values.sum()

        # Calculate expected frequencies
        expected_frequencies = pd.DataFrame(
        np.outer(row_totals, col_totals) / grand_total,
            index=modified_data.index,
            columns=modified_data.columns
        )
        # Calculate Chi-Square statistic
        observed = modified_data.values
        expected = expected_frequencies.values
        chi_square_table = (observed - expected) ** 2 / expected
        chi_square_statistic = np.nansum(chi_square_table)
        
        # Degrees of freedom
        dof = (modified_data.shape[0] - 1) * (modified_data.shape[1] - 1)
        
        # Automatically determine the critical value for alpha=0.05
        critical_value = chi2.ppf(0.95, dof)  # 0.95 is 1 - 0.05 for 5% significance level

        # Interpretation
        
        if chi_square_statistic > critical_value:
            st.write("Here the Chi Square test suggests that there is sufficient evidence to reject the null hypothesis. This indicates a statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time may play a role in influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is greater than the critical value.")
           
        else:
            st.write("Here the Chi Square test suggests that there is insufficient evidence to reject the null hypothesis. This indicates that there is no statistically significant relationship between educational screen time and negative online experiences such as cyberbullying, phishing, or harassment. Consequently, the analysis suggests that educational screen time does not appear to be a major factor influencing the occurrence of these negative influences.")
            st.write(f"**Critical Value:** {critical_value:.4f}")
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
                   
    st.write("For Futher details refer to the Statistical Analysis")  
    st.write("The analysis indicates that the screen time field is too broad and vague to draw a definitive association with health and mental issues. Screen time includes a variety of activities, from educational use to entertainment, each potentially affecting physical and mental well-being in different ways. Therefore, it is not accurate to attribute health and mental issues solely to long hours of screen time. While excessive screen time may contribute to certain problems, other factors—such as the type of screen time, individual behaviors, and external influences—must also be considered when examining the relationship between screen time and health and mental issues.")      
    


  

    

    

    Avg_daily = {
    "Less than 2 Hours": 1,
    "2 to 4 Hours": 3,
    "4 to 6 Hours": 5,
    "6 to 8 Hours":7,
    "8 to 10 Hours":9,
    "10 to 14 Hours":12,
    "More than 14 Hours": 19
    }

    df['Daily_avg'] = df['Avg_Screentime(daily)'].map(Avg_daily)
    st.title("Numeric Data of Education")


# Display the updated DataFrame
    st.dataframe(df.head(10))

    
    
    
#ANOVA
    st.write("# Daily Avg Screen Time by Gender")
    st.write("To examine the whether the screentime consumption is different in both the genders, we conducted an ANOVA (Analysis of Variance) test. ANOVA is a statistical method used to determine whether there are significant differences between the means of two or more groups. In this analysis, it was employed to evaluate whether the average screen time differs significantly between male and female participants.")
    st.write("p-value=0.97")
    st.write("The results of the ANOVA test revealed no statistically significant difference in screen time between males and females. This finding suggests that gender does not play a major role in influencing the amount of time individuals spend on screens, at least within the scope of the analyzed data.")
    st.write("For Futher details refer to the Statistical Analysis") 


    #Concentration level
    st.write("# Concentration level")
    st.write("The relationship between concentration levels and screen time examines how prolonged exposure to screens impacts an individual’s ability to focus. Analyzing this correlation helps identify whether increased screen time is associated with diminished concentration or cognitive performance over time.")
    # Split multiple negative experiences into separate rows
    df_split = df.assign(
            concentrate=df['Concentration'].fillna('').str.split(', ')
        ).explode('concentrate')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['concentrate'] != '0']
    df_split = df_split[df_split['concentrate'] != 'No']
    df_split = df_split[df_split['concentrate'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['concentrate'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
    con_order = [
    'Less than 15 minutes', 
    '15 to 30 minutes', 
    '30 minutes to 1 hour', 
    '1 to 2 hours', 
    'More than 2 hours'
     ]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(con_order, axis=1).fillna(0).astype(int)
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']
    st.write(contingency_table)

    #Correlation between Daily screentime and Concentration
    Age = {
    "Less than 15 minutes": 7.5,
    "15 to 30 minutes": 22.5,
    "30 minutes to 1 hour": 45,
    "1 to 2 hours": 90,
    "More than 2 hours": 120
    
    }
    df['Concentration_age'] = df['Concentration'].map(Age)
    Avg_daily = {
    "Less than 2 Hours": 1,
    "2 to 4 Hours": 3,
    "4 to 6 Hours": 5,
    "6 to 8 Hours":7,
    "8 to 10 Hours":9,
    "10 to 14 Hours":12,
    "More than 14 Hours": 19
}

    df['Daily_avg'] = df['Avg_Screentime(daily)'].map(Avg_daily)

    df_cleaned = df.dropna(subset=['Concentration_age', 'Daily_avg'])
    correlation, p_value = spearmanr(df_cleaned['Daily_avg'], df_cleaned['Concentration_age'])

# Display the result
    st.write("### Correlation between Concentration Time and Daily Screen Time")
    

# Optional: Add a scatter plot for visualization
    if df['Daily_avg'].nunique() > 1 and df['Concentration_age'].nunique() > 1:
        
        st.write(f"P-value: {p_value:.4f}")

    else:
        st.write("Insufficient variability in data for correlation calculation.")
        correlation, p_value = None, None
    if p_value is not None:

        if p_value < 0.05:
            if correlation > 0:
                st.write("There is a significant positive correlation between screen time and the age of onset for the selected health issue.")
            else:
                st.write("There is a significant negative correlation between screen time and the age of onset for the selected health issue.")
        else:
            st.write("The analysis found no significant correlation between screen time and the age of onset for changes in concentration levels. This suggests that variations in screen time do not have a measurable impact on when individuals begin to experience shifts in their ability to concentrate. These findings imply that factors other than screen time, such as lifestyle habits, environmental influences, or inherent cognitive traits, may play a more critical role in determining changes in concentration levels over time.")
        st.write("For Futher details refer to the Statistical Analysis") 

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
    x=df_cleaned['Daily_avg'], 
    y=df_cleaned['Concentration_age'], 
    ax=ax, 
    color="blue", 
   alpha=0.7
    )
    
    ax.legend()
    ax.set_title("Scatter Plot: Concentration Time vs. Daily Screen Time")
    ax.set_xlabel("Daily Screen Time")
    ax.set_ylabel("Concentration Time")
    st.pyplot(fig)

    #Correlation between Age and screentime
    df_cleaned = df.dropna(subset=['Age', 'Daily_avg'])
    correlation, p_value = spearmanr(df_cleaned['Daily_avg'], df_cleaned['Age'])

# Display the result
    st.write("### Correlation between Age and Daily Screen Time")
    st.write("The relationship between age and screen time explores how screen usage patterns vary across different age groups, aiming to uncover potential behavioral trends or impacts.")
    
    
    if df['Daily_avg'].nunique() > 1 and df['Age'].nunique() > 1:
        correlation, p_value = pearsonr(df['Daily_avg'], df['Age'])
        
        st.write(f"P-value: {p_value:.4f}")
    else:
        st.write("Insufficient variability in data for correlation calculation.")
        correlation, p_value = None, None
    if p_value is not None:

        if p_value < 0.05:
            if correlation > 0:
                st.write("There is a significant positive correlation between screen time and the age of onset for the selected health issue.")
            else:
                st.write("There is a significant negative correlation between screen time and the age of onset for the selected health issue.")
        else:
            st.write(" The analysis revealed no significant correlation between screen time and the age of onset for changes in concentration levels, indicating that screen time is not a determining factor in when individuals begin to experience shifts in their concentration abilities.")
  
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
    y=df_cleaned['Daily_avg'], 
    x=df_cleaned['Age'], 
    ax=ax, 
    color="blue", 
   alpha=0.7
    )
    
    ax.legend()
    ax.set_title("Scatter Plot: Age vs. Daily Screen Time")
    ax.set_xlabel("Age")
    ax.set_ylabel("Daily Screen Time")
    st.pyplot(fig)


    st.title("Observation for Occurences of Online Negative Experiences on different Platforms")
    st.write("Following are the list of graphs that represent the different Online negative Experiences and the occurences in the respective platforms")
    st.write("#### Pie Chart of Total Scams")
    # Split multiple negative experiences into separate rows
    df_split = df.assign(
            Scam=df['Platforms-Scams and Fraud leading to financial loss or loss personal data-occured'].fillna('').str.split(', ')
        ).explode('Scam')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['Scam'] != '0']
    df_split = df_split[df_split['Scam'] != 'No']
    df_split = df_split[df_split['Scam'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Scam'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Scams", fontsize=14)
    st.pyplot(fig)



    
    st.write("#### Pie Chart of Total Exploitation and Manipulation")
    df_split = df.assign(
            Ex=df['Platforms-Exploitation and Manipulation through Social Media-occured'].fillna('').str.split(', ')
        ).explode('Ex')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['Ex'] != '0']
    df_split = df_split[df_split['Ex'] != 'No']
    df_split = df_split[df_split['Ex'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Ex'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Exploitation and Manipulation", fontsize=14)
    st.pyplot(fig)
    





    st.write("#### Pie Chart of Cyberbullying")
    # Split multiple negative experiences into separate rows
    df_split = df.assign(
            Cyber=df['Platforms-Cyberbullying or Hate Speech-occured'].fillna('').str.split(', ')
        ).explode('Cyber')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['Cyber'] != '0']
    df_split = df_split[df_split['Cyber'] != 'No']
    df_split = df_split[df_split['Cyber'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Cyber'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Cyberbullying", fontsize=14)
    st.pyplot(fig)




    st.write("#### Pie Chart of Total Radical Ideologies")
    df_split = df.assign(
            Rad=df['Platforms-Exposure to Radical Ideologies-occured'].fillna('').str.split(', ')
        ).explode('Rad')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['Rad'] != '0']
    df_split = df_split[df_split['Rad'] != 'No']
    df_split = df_split[df_split['Rad'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Rad'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Radical Ideologies", fontsize=14)
    st.pyplot(fig)






    
    st.write("#### Pie Chart of Total Malware and Phishing Attacks")
    df_split = df.assign(
            Phish=df['Platforms-Malware and Phishing Attacks-occured'].fillna('').str.split(', ')
        ).explode('Phish')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['Phish'] != '0']
    df_split = df_split[df_split['Phish'] != 'No']
    df_split = df_split[df_split['Phish'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Phish'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Malware and Phishing Attacks", fontsize=14)
    st.pyplot(fig)
    


    
    st.write("#### Pie Chart of Total Online Harassment")
    
    df_split = df.assign(
            On=df['Platforms-Online Harassment-occured'].fillna('').str.split(', ')
        ).explode('On')
        
        # Remove rows where NegativeExperiences is '0' or empty
    df_split = df_split[df_split['On'] != '0']
    df_split = df_split[df_split['On'] != 'No']
    df_split = df_split[df_split['On'] != "i haven't"]
        
        # Generate the contingency table
    contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['On'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
    contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
     
    
        # Reorder the screentime categories
    screentime_order = ['Severe', 'High', 'Moderate', 'Low']
    contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
    contingency_table.loc['Total'] = contingency_table.sum(axis=0)
    column_totals = contingency_table.loc['Total']

        # Display the updated contingency table
     # Dropdown to select a negative experience
    
    # Pie chart for totals
    
    fig, ax = plt.subplots()
    ax.pie(
        column_totals,
        labels=column_totals.index,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    ax.set_title("Distribution of Online Harassment", fontsize=14)
    st.pyplot(fig)
    st.write("The dataset reveals that the majority of the outlined problems are most prevalent on social media platforms compared to other digital environments such as video gaming, YouTube, online websites, and communities. Issues such as scams, exposure to radical ideologies, cyberbullying, and online harassment are reported with higher frequency among social media users. This trend suggests that social media has become a significant contributor to these challenges, given its widespread usage, interactive nature, and the anonymity it often affords.")
    st.write("As social media continues to grow in influence, it is increasingly evident that it plays a central role in the occurrence of these problems, highlighting the urgent need for targeted measures to promote safer and healthier online interactions.")
    


     
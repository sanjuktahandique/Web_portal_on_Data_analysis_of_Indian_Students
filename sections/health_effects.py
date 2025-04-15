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
from scipy.stats import spearmanr
from utils.data_loader import load_data

df = load_data()

def health_effects_section():
    global df


    #  TYPES OF SCREENTIME
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

    st.header("Contingency Table for Education ScreenTime and Negative Experiences")
    st.write("""
    
    1. **Education ScreenTime Category**: Categories like High, Low, Moderate, Severe.
    2. **Negative Experiences**: A comma-separated list of negative experiences.

    Here the system will process the data and display a contingency table showing the frequency of negative experiences for each screentime category.
    """)

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
        st.write("### Contingency Table")
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2

        st.write(modified_data)
      
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
        st.write("### Expected Table")
        st.write(expected_frequencies.round(2))




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
        st.write("### Chi-Square Table")
        st.write(pd.DataFrame(chi_square_table, 
                              index=modified_data.index, 
                              columns=modified_data.columns).round(2))
        
        st.write(f"**Chi-Square Statistic (X²):** {chi_square_statistic:.2f}")
        st.write(f"**Degrees of Freedom (df):** {dof}")
        st.write(f"**Critical Value (from Chi-Square Table, α=0.05):** {critical_value:.4f}")
        
        # Interpretation
        st.write("### Interpretation")
        if chi_square_statistic > critical_value:
            st.write("The Chi-Square statistic is greater than the critical value.")
            st.write("**Conclusion:** There is sufficient evidence to reject the null hypothesis. This suggests a statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        else:
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
            st.write("**Conclusion:** There is insufficient evidence to reject the null hypothesis. This suggests no statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        


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

    
    st.title("Contingency Table for Entertainment ScreenTime and Negative Experiences")
    st.write("""

1. **Entertainment ScreenTime Category**: Categories like High, Low, Moderate, Severe.
2. **Negative Experiences**: A comma-separated list of negative experiences 
             
Here the system will process the data and display a contingency table showing the frequency of negative experiences for each screentime category.
""")

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
        st.write("### Contingency Table")
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2

        st.write(modified_data)
      
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
        st.write("### Expected Table")
        st.write(expected_frequencies.round(2))





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
        st.write("### Chi-Square Table")
        st.write(pd.DataFrame(chi_square_table, 
                              index=modified_data.index, 
                              columns=modified_data.columns).round(2))
        
        st.write(f"**Chi-Square Statistic (X²):** {chi_square_statistic:.2f}")
        st.write(f"**Degrees of Freedom (df):** {dof}")
        st.write(f"**Critical Value (from Chi-Square Table, α=0.05):** {critical_value:.4f}")
        
        # Interpretation
        st.write("### Interpretation")
        if chi_square_statistic > critical_value:
            st.write("The Chi-Square statistic is greater than the critical value.")
            st.write("**Conclusion:** There is sufficient evidence to reject the null hypothesis. This suggests a statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        else:
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
            st.write("**Conclusion:** There is insufficient evidence to reject the null hypothesis. This suggests no statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        






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
    


#
    st.title("Contingency Table for ScreenTime and Health Effects")
    st.write("""
    
    1. **ScreenTime Category**: Categories like High, Low, Moderate, Severe.
    2. **Health Effects**: A comma-separated list of health effects (e.g., ADHD, Dry Eyes, etc.).

    Here the system will process the data and display a contingency table showing the frequency of health effects for each screentime category.
    """)
    
    # Validate required columns
    if 'ScreenTime Category' in df.columns and 'Health_Effects' in df.columns:
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
        
        

         # Perform Chi-Square Test
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2
        st.write("### Contingency Table")
        st.write(modified_data)
      
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
        st.write("### Expected Table")
        st.write(expected_frequencies.round(2))




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
        st.write("### Chi-Square Table")
        st.write(pd.DataFrame(chi_square_table, 
                              index=modified_data.index, 
                              columns=modified_data.columns).round(2))
        
        st.write(f"**Chi-Square Statistic (X²):** {chi_square_statistic:.2f}")
        st.write(f"**Degrees of Freedom (df):** {dof}")
        st.write(f"**Critical Value (from Chi-Square Table, α=0.05):** {critical_value:.4f}")
        
        # Interpretation
        st.write("### Interpretation")
        if chi_square_statistic > critical_value:
            st.write("The Chi-Square statistic is greater than the critical value.")
            st.write("**Conclusion:** There is sufficient evidence to reject the null hypothesis. This suggests a statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        else:
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
            st.write("**Conclusion:** There is insufficient evidence to reject the null hypothesis. This suggests no statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        
        
        # Option to download the table as CSV
        csv = contingency_table.to_csv().encode('utf-8')
        st.download_button(
            label="Download Contingency Table as CSV",
            data=csv,
            file_name='contingency_table.csv',
            mime='text/csv'
        )
    else:
        st.error("The uploaded file must contain 'ScreenTime Category' and 'Health Effects' columns.")





    st.title("Contingency Table for ScreenTime and Negative Experiences")
    st.write("""
    This app allows you to upload a CSV file with two columns:
    1. **ScreenTime Category**: Categories like High, Low, Moderate, Severe.
    2. **Negative Experiences**: A comma-separated list of negative experiences (e.g., ADHD, Dry Eyes, Less Sleep, etc.).

    Here the system will process the data and display a contingency table showing the frequency of negative experiences for each screentime category.
    """)

    if 'ScreenTime Category' in df.columns and 'Negative Experiences' in df.columns:
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
        
       
        
        
        # Perform Chi-Square Test
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        modified_data = contingency_table * 2
        st.write("### Contingency Table")
        st.write(modified_data)
      
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
        st.write("### Expected Table")
        st.write(expected_frequencies.round(2))




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
        st.write("### Chi-Square Table")
        st.write(pd.DataFrame(chi_square_table, 
                              index=modified_data.index, 
                              columns=modified_data.columns).round(2))
        
        st.write(f"**Chi-Square Statistic (X²):** {chi_square_statistic:.2f}")
        st.write(f"**Degrees of Freedom (df):** {dof}")
        st.write(f"**Critical Value (from Chi-Square Table, α=0.05):** {critical_value:.4f}")
        
        # Interpretation
        st.write("### Interpretation")
        if chi_square_statistic > critical_value:
            st.write("The Chi-Square statistic is greater than the critical value.")
            st.write("**Conclusion:** There is sufficient evidence to reject the null hypothesis. This suggests a statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        else:
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
            st.write("**Conclusion:** There is insufficient evidence to reject the null hypothesis. This suggests no statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        





        # Option to download the table as CSV
        csv = contingency_table.to_csv().encode('utf-8')
        st.download_button(
            label="Download Contingency Table as CSV",
            data=csv,
            file_name='contingency_tabl.csv',
            mime='text/csv'
        )
    else:
        st.error("The uploaded file must contain 'ScreenTime Category' and 'Negative Experiences' columns.")


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
    

#ANOVA
    st.title("ANOVA Analysis: Daily Avg Screen Time by Gender")
    df['Daily_avg'] = pd.to_numeric(df['Daily_avg'], errors='coerce')
    st.write(df['Daily_avg'].dtype)

 ######
    if 'Gender' in df.columns and 'Daily_avg' in df.columns:
        df['Daily_avg'] = pd.to_numeric(df['Daily_avg'], errors='coerce')
        df = df[df['Gender'].notnull() & df['Daily_avg'].notnull()]
        
# Group data by gender
        male_screen_time = df[df['Gender'].str.lower() == 'male']['Daily_avg']
        female_screen_time = df[df['Gender'].str.lower() == 'female']['Daily_avg']

# Drop NaN values in groups
        male_screen_time = male_screen_time.dropna()
        female_screen_time = female_screen_time.dropna()

        st.write("Number of male entries:", len(male_screen_time))
        st.write("Number of female entries:", len(female_screen_time))

# Check for empty groups
        if len(male_screen_time) == 0 or len(female_screen_time) == 0:
            st.error("One of the groups has no data for analysis.")
        else:
            mean_male = male_screen_time.mean()
            mean_female = female_screen_time.mean()
            st.write(f"Mean daily average screen time for males: {mean_male:.2f}")
            st.write(f"Mean daily average screen time for females: {mean_female:.2f}")
    # Perform ANOVA
            f_stat, p_value = stats.f_oneway(male_screen_time, female_screen_time)

    # Display ANOVA result
            

    # Interpretation of the p-value
    
            grand_mean = df['Daily_avg'].mean()

    # Between-group variation (SSB)
            ssb = len(male_screen_time) * (mean_male - grand_mean)**2 + len(female_screen_time) * (mean_female - grand_mean)**2

    # Within-group variation (SSW)
            ssw = ((male_screen_time - mean_male)**2).sum() + ((female_screen_time - mean_female)**2).sum()

    # Display the variations
            st.write(f"Between-group variation (SSB): {ssb:.2f}")
            st.write(f"Within-group variation (SSW): {ssw:.2f}")

            if p_value < 0.05:
                st.success("There is a statistically significant difference in daily average screen time between male and female.")
            else:
                st.warning("There is no statistically significant difference in daily average screen time between male and female.")
    
    #T-test
    st.title("T-test Analysis: Daily Average Screen Time by Gender")
    df['Daily_avg'] = pd.to_numeric(df['Daily_avg'], errors='coerce')
    st.write(df['Daily_avg'].dtype)

 ######
    if 'Gender' in df.columns and 'Daily_avg' in df.columns:
        df['Daily_avg'] = pd.to_numeric(df['Daily_avg'], errors='coerce')
        df = df[df['Gender'].notnull() & df['Daily_avg'].notnull()]
        
# Group data by gender
        male_screen_time = df[df['Gender'].str.lower() == 'male']['Daily_avg']
        female_screen_time = df[df['Gender'].str.lower() == 'female']['Daily_avg']

# Drop NaN values in groups
        male_screen_time = male_screen_time.dropna()
        female_screen_time = female_screen_time.dropna()

        
# Check for empty groups
        if len(male_screen_time) == 0 or len(female_screen_time) == 0:
            st.error("One of the groups has no data for analysis.")
        else:
            mean_male = male_screen_time.mean()
            mean_female = female_screen_time.mean()
            
    # Perform ANOVA
            f_stat, p_value = stats.f_oneway(male_screen_time, female_screen_time)

    # Display ANOVA result
            
            st.write(f"T-test p-value: {p_value:.4f}")

    # Interpretation of the p-value
    
            grand_mean = df['Daily_avg'].mean()

    # Between-group variation (SSB)
            ssb = len(male_screen_time) * (mean_male - grand_mean)**2 + len(female_screen_time) * (mean_female - grand_mean)**2

    # Within-group variation (SSW)
            ssw = ((male_screen_time - mean_male)**2).sum() + ((female_screen_time - mean_female)**2).sum()

    # Display the variations
           

            if p_value < 0.05:
                st.success("There is a statistically significant difference in daily average screen time between male and female.")
            else:
                st.write("There is no statistically significant difference in daily average screen time between male and female.")
    
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


    st.write("### Correlation between Concentration Time and Daily Screen Time")
    st.write(f"Spearman Correlation: **{correlation:.2f}**")

# Optional: Add a scatter plot for visualization
    if df['Daily_avg'].nunique() > 1 and df['Concentration_age'].nunique() > 1:
        
        st.write(f"Correlation coefficient between screen time and {'Concentration_age'}: {correlation:.2f}")
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
            st.write("No significant correlation found between screen time and the age of onset for the selected health issue.")
     

    #Correlation between Age and screentime
    df_cleaned = df.dropna(subset=['Age', 'Daily_avg'])
    correlation, p_value = spearmanr(df_cleaned['Daily_avg'], df_cleaned['Age'])

# Display the result
    st.write("### Correlation between Age and Daily Screen Time")
    
    st.write(f"Spearson Correlation: **{correlation:.2f}**")
    if df['Daily_avg'].nunique() > 1 and df['Age'].nunique() > 1:
        correlation, p_value = pearsonr(df['Daily_avg'], df['Age'])
        st.write(f"Correlation coefficient between screen time and {'Age'}: {correlation:.2f}")
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
            st.write("No significant correlation found between screen time and the age of onset for the selected health issue.")
  
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
    y=df_cleaned['Daily_avg'], 
    x=df_cleaned['Age'], 
    ax=ax, 
    color="blue", 
   alpha=0.7
    )
  


  ###
    if 'ScreenTime Category' in df.columns and 'Education' in df.columns:
        contingency_table = pd.crosstab(df_split['ScreenTime Category'], df_split['Education'])
        
        # Remove zero-valued negative experiences (columns where all values are 0)
        contingency_table = contingency_table.loc[:, (contingency_table != 0).any(axis=0)]
        
        # Reorder the screentime categories
        screentime_order = ['Severe', 'High', 'Moderate', 'Low']
        contingency_table = contingency_table.reindex(screentime_order, axis=0).fillna(0).astype(int)
        
       
        
        
        # Perform Chi-Square Test
        
        contingency_table = contingency_table.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

        # Apply to the contingency_table, not df
        contingency_table = contingency_table.loc[~(contingency_table.eq(0).all(axis=1)), :]  # Remove rows that are all zeros
        contingency_table = contingency_table.loc[:, ~(contingency_table.eq(0).all(axis=0))]  # Remove columns that are all zeros

        # Convert to integers after cleaning (if necessary)
        
        st.write("### Contingency Table")
        st.write(contingency_table)
      
        # Perform Chi-Square Test
        
        # Calculate row and column totals
        row_totals = contingency_table.sum(axis=1)
        col_totals = contingency_table.sum(axis=0)
        grand_total = contingency_table.values.sum()

        # Calculate expected frequencies
        expected_frequencies = pd.DataFrame(
        np.outer(row_totals, col_totals) / grand_total,
            index=contingency_table.index,
            columns=contingency_table.columns
        )
        st.write("### Expected Table")
        st.write(expected_frequencies.round(2))




        # Calculate Chi-Square statistic
        observed = contingency_table.values
        expected = expected_frequencies.values
        chi_square_table = (observed - expected) ** 2 / expected
        chi_square_statistic = np.nansum(chi_square_table)
        
        # Degrees of freedom
        dof = (contingency_table.shape[0] - 1) * (contingency_table.shape[1] - 1)
        
        # Automatically determine the critical value for alpha=0.05
        critical_value = chi2.ppf(0.95, dof)  # 0.95 is 1 - 0.05 for 5% significance level
        
        # Display Chi-Square table, statistic, and critical value
        st.write("### Chi-Square Table")
        st.write(pd.DataFrame(chi_square_table, 
                              index=contingency_table.index, 
                              columns=contingency_table.columns).round(2))
        
        st.write(f"**Chi-Square Statistic (X²):** {chi_square_statistic:.2f}")
        st.write(f"**Degrees of Freedom (df):** {dof}")
        st.write(f"**Critical Value (from Chi-Square Table, α=0.05):** {critical_value:.4f}")
        
        # Interpretation
        st.write("### Interpretation")
        if chi_square_statistic > critical_value:
            st.write("The Chi-Square statistic is greater than the critical value.")
            st.write("**Conclusion:** There is sufficient evidence to reject the null hypothesis. This suggests a statistically significant relationship between ScreenTime Categories and Negative Experiences.")
        else:
            st.write("The Chi-Square statistic is less than or equal to the critical value.")
            st.write("**Conclusion:** There is insufficient evidence to reject the null hypothesis. This suggests no statistically significant relationship between ScreenTime Categories and Negative Experiences.")

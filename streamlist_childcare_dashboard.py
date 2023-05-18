import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data():
    childcare = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/childcare_costs.csv")

    emp_df = childcare.filter(items=['state_name','county_fips_code', 'study_year'] + [col for col in childcare.columns if 'emp' in col])

    counties = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/counties.csv")

    merged_df = pd.merge(counties, emp_df, on='county_fips_code')
    merged_df = merged_df.drop(['county_fips_code', 'state_abbreviation'], axis=1)

    emp_rate_df = (childcare
                   .loc[:, ['state_name', 'study_year', 'emp_m', 'memp_m', 'emp_n', 'emp_sales', 'emp_service', 'femp_m']]
                   .groupby('study_year')
                   .mean()
                   .reset_index()
                  )

    return emp_rate_df

def create_dashboard():
    st.title("US (Childcare) Employment Rates")

    # Load data
    data = load_data()

    # Display dataframe
    st.subheader("Childcare Employment Rate Data")
    st.dataframe(data)

    # Plot 1
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    sns.set_style('whitegrid')
    sns.lineplot(x='study_year', y='emp_m', data=data, color='royalblue', ax=axes[0])
    axes[0].set_title('Percentage of Civilians Employed in Management, Business, Science, and Arts Occupations Aged 16 Years or Older in the County', fontsize=10, fontweight='bold')
    axes[0].set_xlabel('Survey Year', fontsize=8)
    axes[0].set_ylabel('Percent Employed', fontsize=8)
    axes[0].tick_params(labelsize=6)

    # Plot 2
    sns.lineplot(x='study_year', y='emp_n', data=data, color='royalblue', ax=axes[1])
    axes[1].set_title('Percent of Civilians Employed in Natural Resources, Construction, and Maintenance Occupations', fontsize=10, fontweight='bold')
    axes[1].set_xlabel('Survey Year', fontsize=8)
    axes[1].set_ylabel('Percent Employed', fontsize=8)
    axes[1].tick_params(labelsize=6)

    plt.tight_layout()

    # Plot 3
    plt.figure(figsize=(6, 4))
    sns.set_style('whitegrid')
    sns.lineplot(x='study_year', y='memp_m', data=data, color='royalblue', label='Male Employment')
    sns.lineplot(x='study_year', y='femp_m', data=data, color='red', label='Female Employment')
    plt.title('Percent of Civilians Employed in Natural Resources, Construction, and Maintenance Occupations', fontsize=10, fontweight='bold')
    plt.xlabel('Survey Year', fontsize=8)
    plt.ylabel('Percent Employed', fontsize=8)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()

    # Display the plot
    st.subheader("Employment Rate Trend")
    st.pyplot()

# Run the dashboard
create_dashboard()

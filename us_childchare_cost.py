import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Tidytuesday May 9, 2023: US Childcare Cost

childcare = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/childcare_costs.csv")

childcare.head()

## select columns that contain "emp" (i.e. employment data) in their column name
emp_df = childcare.filter(items=['county_fips_code', 'study_year'] + [col for col in childcare.columns if 'emp' in col])

counties = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/counties.csv")

## merge emp_df and countries on county_fips_code column
merged_df = pd.merge(counties,emp_df, on='county_fips_code')
## drop county_fips_code and state_abbreviation columns
merged_df = merged_df.drop(['county_fips_code', 'state_abbreviation'], axis=1)

merged_df.head()

##  assuming you have a pandas dataframe named 'childcare'
emp_rate_df = (childcare
               .loc[:, ['study_year', 'emp_m','memp_m','emp_n','emp_sales','emp_service','femp_m']]
               .groupby('study_year')
               .mean()
               .reset_index()
              )

emp_rate_df.head()


sns.set_style('whitegrid')
plt.figure(figsize=(6, 4))
sns.lineplot(x='study_year', y='emp_m', data=emp_rate_df, color='royalblue')
plt.title('Percentage of Civilians Employed in Management, Business, Science, \nand Arts Occupations Aged 16 Years or Older in the County', fontsize=10, fontweight='bold')
plt.xlabel('Survey Year', fontsize=8)
plt.ylabel('Percent Employed', fontsize=8)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
plt.show()
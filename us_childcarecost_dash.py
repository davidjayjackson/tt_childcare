import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html



childcare = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/childcare_costs.csv")
emp_df = childcare.filter(items=['county_fips_code', 'study_year'] + [col for col in childcare.columns if 'emp' in col])
counties = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-05-09/counties.csv")
merged_df = pd.merge(counties, emp_df, on='county_fips_code')
merged_df = merged_df.drop(['county_fips_code', 'state_abbreviation'], axis=1)
emp_rate_df = (childcare.loc[:, ['study_year', 'emp_m', 'memp_m', 'emp_n', 'emp_sales', 'emp_service', 'femp_m']]
               .groupby('study_year')
               .mean()
               .reset_index()
              )

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("US Childcare Cost Dashboard"),
    dcc.Dropdown(
        id="study-year-dropdown",
        options=[{'label': str(year), 'value': year} for year in emp_rate_df['study_year']],
        value=emp_rate_df['study_year'].min(),  # Set the default value to the minimum study year
    ),
    dcc.Graph(id="employment-graph"),
])

@app.callback(
    Output(component_id="employment-graph", component_property="figure"),
    [Input(component_id="study-year-dropdown", component_property="value")]
)
def update_graph(study_year):
    filtered_data = emp_rate_df[emp_rate_df['study_year'] == study_year]
    fig = plt.figure(figsize=(6, 4))
    sns.lineplot(x='study_year', y='emp_m', data=filtered_data, color='royalblue')
    plt.title('Percentage of Civilians Employed in Management, Business, Science, and Arts Occupations Aged 16 Years or Older in the County', fontsize=10, fontweight='bold')
    plt.xlabel('Survey Year', fontsize=8)
    plt.ylabel('Percent Employed', fontsize=8)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()  # Add this line to improve the layout
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


import pandas as pd

# Group by county and state, and compute sum/mean as necessary for each column
grouped = acs_df.groupby(['County', 'State'])

# Create County_Info DataFrame
County_Info = grouped.agg({
    'Population': 'sum',
    'Poverty': 'mean', 
    'PerCapitaIncome': 'mean'
}).reset_index()

# Add ID column
County_Info['ID'] = range(1, len(County_Info) + 1)

# Create a 'Month' column from the date
covid_df['Month'] = pd.to_datetime(covid_df['date']).dt.month

# Group by county and month, then compute sum for each column
grouped_covid = covid_df.groupby(['county', 'Month'])

# Create COVID_monthly DataFrame
COVID_monthly = grouped_covid.agg({
    'Cases': 'sum',
    'Deaths': 'sum'
}).reset_index()

# Add ID column based on County_Info
COVID_monthly = COVID_monthly.merge(County_Info[['ID', 'Name', 'State']], left_on='county', right_on='Name')

COVID_summary = County_Info.merge(COVID_monthly.groupby('ID').agg({
    'Cases': 'sum',
    'Deaths': 'sum'
}), on='ID')

COVID_summary['TotalCasesPer100K'] = COVID_summary['Cases'] / (COVID_summary['Population'] / 100000)
COVID_summary['TotalDeathsPer100K'] = COVID_summary['Deaths'] / (COVID_summary['Population'] / 100000)

#Analysis
#R = COVID_summary['TotalCasesPer100K'].corr(COVID_summary['Poverty'])



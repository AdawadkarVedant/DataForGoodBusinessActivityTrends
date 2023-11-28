import pandas as pd
from os import walk
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
from matplotlib.dates import MonthLocator

# Set pandas display options
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# Read files from dataset
dir_path = ''
filename_list = []
for (dirpath, dirnames, filenames) in walk('Datasets'):
    filename_list = filenames
    dir_path = dirpath

df_dfg = pd.DataFrame(
    columns=['gadm_id', 'gadm_name', 'gadm_level', 'gadm0_name', 'gadm1_name', 'gadm2_name', 'country',
             'business_vertical', 'activity_quantile', 'activity_percentage', 'crisis_ds', 'ds'])
data_list = []

# Read the dataset from DFG and represent the data
for file_name in filename_list:
    df = pd.read_csv(dir_path + '//' + file_name)
    data_list.append(df)

df_dfg = pd.concat(data_list)
df_dfg['ds'] = pd.to_datetime(df_dfg['ds'])
df_dfg['crisis_ds'] = pd.to_datetime(df_dfg['crisis_ds'])
df_dfg.columns = df_dfg.columns.str.strip()
df_dfg.set_index('ds', inplace=True, drop=False)

# Q2 Answer
# Part 1
q2_result = df_dfg.groupby(['country', 'business_vertical']).agg({'ds': ['min', 'max']}).reset_index()
# print(q2_result)

# Part 2
has_duplicate_rows = df_dfg.duplicated().any()
# print(has_duplicate_rows)

# Part 3
has_null_values = df_dfg.isnull().values.any()
null_column_list = []
if has_null_values:
    null_column_list.append(df_dfg.columns[df_dfg.isna().any()].tolist())

df_dfg['country'] = df_dfg['country'].fillna(df_dfg['gadm_id'])
df_dfg.dropna(axis=1, how='all', inplace=True)
print(df_dfg.isnull().values.any())

# Q5 Answer - Part 2
# Use the same countries and the same business verticals to find trends in weekdays versus weekends.
# Extract min and max years from the DataFrame index
min_year, max_year = pd.DatetimeIndex([df_dfg.index.values.min(), df_dfg.index.values.max()]).year

# Create a list of missing years between min and max years
missing_years = list(range(min_year + 1, max_year))

# Extend the min_max_years list with missing years and sort it
min_max_years = sorted([min_year, *missing_years, max_year])

# Loop through years and countries to create line charts for weekends
for year in min_max_years:
    date_mask = df_dfg['ds'].dt.year == year
    df_dfg_weekend = df_dfg[(df_dfg['ds'].dt.dayofweek.isin([5, 6])) & date_mask]

    for country in ['Australia', 'Germany', 'India', 'United Kingdom', 'United States']:
        country_mask_weekend = df_dfg_weekend['gadm0_name'] == country
        data_frame_weekend_coll = []

        for business in ['Travel', 'Restaurants', 'Retail']:
            df_dfg_weekend_iter = df_dfg_weekend[
                (df_dfg_weekend['business_vertical'] == business) & country_mask_weekend]
            data_frame_weekend_coll.append(df_dfg_weekend_iter)

        businesses = ['Travel', 'Restaurants', 'Retail']
        plt.figure(figsize=(24, 10))

        for business, df in zip(businesses, data_frame_weekend_coll):
            sns.lineplot(data=df, x='ds', y='activity_percentage', label=business, linestyle='-')

        plt.axhline(y=100, color='black', linestyle='--')
        plt.gca().xaxis.set_major_locator(MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.gca().xaxis.set_tick_params(rotation=30)
        plt.xlabel('Years (Month - Year)')
        plt.ylabel('Activity Percentages')
        plt.title(
            f'Line chart with Business Verticals - {", ".join(businesses)} - For {country} Displaying Activity Percentages for Weekends in {year}')
        plt.grid()
        plt.legend()

        # Save the plot with a filename based on country and weekends for the year
        plt.savefig(f'Line Chart - {country} - Weekends For The Year {year}.png', bbox_inches='tight')
        plt.close()  # Close the plot to avoid displaying multiple plots at once

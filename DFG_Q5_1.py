import pandas as pd
from os import walk
from matplotlib import pyplot as plt
import seaborn as sns

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

# Q5 Answer - Part 1
# Use the same countries and the same business verticals
# Create a box plot country-wise for the business verticals separately
# Extract min and max years from the DataFrame index
min_year, max_year = pd.DatetimeIndex([df_dfg.index.values.min(), df_dfg.index.values.max()]).year

# Create a list of missing years between min and max years
missing_years = list(range(min_year + 1, max_year))

# Extend the min_max_years list with missing years and sort it
min_max_years = sorted([min_year, *missing_years, max_year])

# Loop through years and businesses to create box plots
for year in min_max_years:
    date_mask = df_dfg['ds'].dt.year == year

    for business in ['Travel', 'Restaurants', 'Retail']:
        business_mask = df_dfg['business_vertical'] == business
        country_mask = df_dfg['gadm0_name'].isin(['Australia', 'Germany', 'India', 'United Kingdom', 'United States'])
        df_box = df_dfg[business_mask & country_mask & date_mask]

        plt.figure(figsize=(14, 8))
        sns.boxplot(x='gadm0_name', y='activity_percentage', data=df_box)

        plt.title(f'{business} Boxplot For The Year {year}')
        plt.xlabel('Countries')
        plt.ylabel('Activity Percentage')

        # Save the plot with a filename based on business, year, and activity percentage
        plt.savefig(f'Box Plot - {business} For The Year {year}.png', bbox_inches='tight')
        plt.close()  # Close the plot to avoid displaying multiple plots at once

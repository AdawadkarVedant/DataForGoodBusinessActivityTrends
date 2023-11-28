import glob
from datetime import datetime
import pandas as pd
import os
from os import walk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
import geopandas as gpd

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
# print(df_dfg.isnull().values.any())

# Q6 Answer
# Choose the first and the last day of the dataset
min_date = df_dfg.index.values.min()
max_date = df_dfg.index.values.max()

# Filter DataFrame for the first and last dates
df_dfg_first = df_dfg[df_dfg['ds'] == min_date]
df_dfg_last = df_dfg[df_dfg['ds'] == max_date]

# Load world map data
worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Rename the column for merging
df_dfg_first.rename(columns={'gadm_id': 'iso_a3'}, inplace=True)
df_dfg_last.rename(columns={'gadm_id': 'iso_a3'}, inplace=True)

# Merge world map with the data for the first and last dates
merged_df_first = pd.merge(worldmap, df_dfg_first, on='iso_a3')
merged_df_last = pd.merge(worldmap, df_dfg_last, on='iso_a3')

# Get unique business verticals
merged_business_verticals = set(merged_df_first['business_vertical'])

# Plot for each business vertical
for business in merged_business_verticals:
    # Filter data for the specific business vertical
    merged_df_first_business = merged_df_first[merged_df_first['business_vertical'] == business]
    merged_df_last_business = merged_df_last[merged_df_last['business_vertical'] == business]

    # Plotting
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))

    # Plot for df_dfg_first
    plot_first = merged_df_first_business.plot(column='activity_quantile', ax=axes[0], legend=True)
    axes[0].set_title(f'{business} Activity Percentage on {pd.to_datetime(str(min_date)).strftime("%d-%m-%Y")}', fontsize=12)
    axes[0].set_xlabel('Longitude', fontsize=8)
    axes[0].set_ylabel('Latitude', fontsize=8)

    # Plot for df_dfg_last
    plot_last = merged_df_last_business.plot(column='activity_quantile', ax=axes[1], legend=True)
    axes[1].set_title(f'{business} Activity Percentage on {pd.to_datetime(str(max_date)).strftime("%d-%m-%Y")}', fontsize=12)
    axes[1].set_xlabel('Longitude', fontsize=8)
    axes[1].set_ylabel('Latitude', fontsize=8)

    # Adjust layout for better spacing
    plt.tight_layout(pad=3)

    plt.savefig(f'World Map - {business} using activity quantiles.png', bbox_inches='tight')
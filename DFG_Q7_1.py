import pandas as pd
from os import walk
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
from matplotlib.dates import MonthLocator
from matplotlib.ticker import MultipleLocator

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
has_duplicate_rows = df_dfg.duplicated().any()

# Part 2
has_null_values = df_dfg.isnull().values.any()
null_column_list = []
if has_null_values:
    null_column_list.append(df_dfg.columns[df_dfg.isna().any()].tolist())

df_dfg['country'] = df_dfg['country'].fillna(df_dfg['gadm_id'])
df_dfg.dropna(axis=1, how='all', inplace=True)
print(df_dfg.isnull().values.any())

# Q7_1 Answer
for business in ['Travel', 'Retail', 'Restaurants']:
    business_mask = df_dfg['business_vertical'] == business
    data_frame_coll = []

    for country in ['India', 'United States']:
        df_data = df_dfg[(df_dfg['gadm_name'] == country) & business_mask]
        data_frame_coll.append(df_data)

    countries = ['India', 'United States']
    plt.figure(figsize=(24, 10))

    for country, df in zip(countries, data_frame_coll):
        sns.lineplot(data=df, x='ds', y='activity_quantile', label=country, linestyle='-', errorbar=None)

    plt.axhline(y=0.5, color='black', linestyle='--')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_tick_params(rotation=30)
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.xlabel('Time Period (Month and Year)')
    plt.ylabel('Activity Quantile')
    plt.title(
        f'Line Chart - {business} - Activity Quantiles for India and United States')
    plt.grid()
    plt.legend()

    # Save the plot with a filename based on country and activity quantiles
    plt.savefig(f'Line Chart - {business} - Activity Quantiles for India and United States.png', bbox_inches='tight')
    plt.close()
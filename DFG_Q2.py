import pandas as pd
from os import walk

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
min_date = df_dfg.index.values.min()
max_date = df_dfg.index.values.max()
print('Missing Dates - ', pd.date_range(start=min_date, end=max_date).difference(df_dfg.index))
print('--------------------------------------------------------------------------------------')
q2_result = df_dfg.groupby(['country', 'business_vertical']).agg({'ds': ['min', 'max']}).reset_index()
print(q2_result)

# Part 2
has_duplicate_rows = df_dfg.duplicated().any()
print(has_duplicate_rows)

# Part 3
has_null_values = df_dfg.isnull().values.any()
null_column_list = []
if has_null_values:
    null_column_list.append(df_dfg.columns[df_dfg.isna().any()].tolist())
print('Empty Columns - ', null_column_list)

df_dfg['country'] = df_dfg['country'].fillna(df_dfg['gadm_id'])
df_dfg.dropna(axis=1, how='all', inplace=True)
print('Check if any null values exist - ', df_dfg.isnull().values.any())

grouped_data_df = df_dfg.groupby(['gadm_id', 'business_vertical']).agg(total_dates=('ds', 'count'), min_date=('ds', 'min'), max_date=('ds', 'max'))
print(grouped_data_df)

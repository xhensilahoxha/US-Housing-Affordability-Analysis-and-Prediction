import pandas as pd
import numpy as np
import matplotlib as plt
# --------------------- HAR

# df_cost_of_living['family_size'] = df_cost_of_living['parents_per_household'] + df_cost_of_living['children_per_household']


# # Group by state and areaname to compute weighted housing expenses
# area_housing_expenses = df_cost_of_living.groupby(['state', 'areaname']).apply(
#     lambda x: (x['housing_expenses'] * x['family_size']).sum() / x['family_size'].sum()
# ).reset_index(name='Weighted_Housing_Expenses')


# # Extract unique median family income for each area
# area_income = df_cost_of_living[['state', 'areaname', 'median_family_income']].drop_duplicates()

# # Merge housing expenses and median family income
# area_data = area_housing_expenses.merge(area_income, on=['state', 'areaname'])

# # Calculate HAR for each area
# area_data['HAR_area'] = (area_data['Weighted_Housing_Expenses'] / area_data['median_family_income']) * 100

# # Calculate total housing expenses for each area
# total_housing_expenses = df_cost_of_living.groupby(['state', 'areaname'])['housing_expenses'].sum().reset_index(name='Total_Housing_Expenses')

# # Merge with area data
# area_data = area_data.merge(total_housing_expenses, on=['state', 'areaname'])

# # Group by state and calculate weighted HAR
# state_har = area_data.groupby('state').apply(
#     lambda x: (x['HAR_area'] * x['Total_Housing_Expenses']).sum() / x['Total_Housing_Expenses'].sum()
# ).reset_index(name='HAR_state')

# print(state_har)

# plt.figure(figsize=(12, 6))
# state_har.sort_values(by='HAR_state', ascending=False).plot(kind='bar', x='state', y='HAR_state', legend=False)
# plt.title('State-Level Housing Affordability Ratio (HAR)')
# plt.ylabel('HAR (%)')
# plt.xlabel('State')
# plt.show()

 
#  ---------------------------------------------ECLB

#-------------- correlation median-income
# Group by 'areaname' and check the number of unique 'median_family_income' values within each area
# inconsistent_areas = df_cost_of_living.groupby('areaname')['median_family_income'].nunique().reset_index()

# # Filter for areas where there is more than one unique 'median_family_income' value
# inconsistent_areas = inconsistent_areas[inconsistent_areas['median_family_income'] > 1]

# # Display inconsistent areas
# print(inconsistent_areas)

# Aggregate the data by 'areaname' and take the first value for 'median_family_income'
df_cleaned = df_cost_of_living.groupby('areaname').agg({
    'median_family_income': 'median',  # You can use 'mean', 'min', or other aggregation methods
}).reset_index()

# # Verify that there is now only one row per 'areaname'
# print(df_cleaned[['areaname', 'median_family_income']].drop_duplicates())




# --------------------- ECLB

# Calculate the median of each expense at the area level
area_expenses_median = df_cost_of_living.groupby(['state', 'areaname']).agg({
    'food_expenses': 'median',
    'transport_expenses': 'median',
    'healthcare_expenses': 'median',
    'other_necessities_expenses': 'median',
    'childcare_expenses': 'median'
}).reset_index()


# Calculate total median essential expenses for each area
area_expenses_median['Total_Median_Essential_Expenses'] = (
    area_expenses_median['food_expenses'] +
    area_expenses_median['transport_expenses'] +
    area_expenses_median['healthcare_expenses'] +
    area_expenses_median['other_necessities_expenses'] +
    area_expenses_median['childcare_expenses']
)

# Merge with area-level median family income
area_income = df_cost_of_living[['state', 'areaname', 'median_family_income']].drop_duplicates()

area_data = area_expenses_median.merge(area_income, on=['state', 'areaname'])

# Calculate area-level ECLB
area_data['ECLB_area'] = (area_data['Total_Median_Essential_Expenses'] / area_data['median_family_income']) * 100

# Calculate total household expenses for each area
total_area_expenses = df_cost_of_living.groupby(['state', 'areaname'])['total_household_expenses'].sum().reset_index(name='Total_Area_Expenses')

# Merge with area-level ECLB
area_data = area_data.merge(total_area_expenses, on=['state', 'areaname'])

# Calculate state-level ECLB using weighted average
state_eclb = area_data.groupby('state').apply(
    lambda x: (x['ECLB_area'] * x['Total_Area_Expenses']).sum() / x['Total_Area_Expenses'].sum()
).reset_index(name='State_ECLB')

print(state_eclb)

# Visualizing state-level ECLB
plt.figure(figsize=(12, 6))
state_eclb.sort_values(by='State_ECLB', ascending=False).plot(kind='bar', x='state', y='State_ECLB', legend=False)
plt.title('State-Level Essential Cost of Living Burden (ECLB)')
plt.ylabel('ECLB (%)')
plt.xlabel('State')
plt.show()



# -------------------- HAR

# Calculate the median of housing expenses at the area level
area_housing_expenses_median = df_cost_of_living.groupby(['state', 'areaname'])['housing_expenses'].median().reset_index(name='Median_Housing_Expenses_area')

# Merge area housing expenses with area-level median family income
area_income = df_cost_of_living[['state', 'areaname', 'median_family_income']].drop_duplicates()
area_data = area_housing_expenses_median.merge(area_income, on=['state', 'areaname'])

# Calculate HAR for each area
area_data['HAR_area'] = (area_data['Median_Housing_Expenses_area'] / area_data['median_family_income']) * 100

# Calculate total housing expenses for each area
total_area_expenses = df_cost_of_living.groupby(['state', 'areaname'])['housing_expenses'].sum().reset_index(name='Total_Area_Expenses')

# Merge area-level HAR with total area expenses
area_data = area_data.merge(total_area_expenses, on=['state', 'areaname'])

# Calculate state-level HAR using weighted average
state_har = area_data.groupby('state').apply(
    lambda x: (x['HAR_area'] * x['Total_Area_Expenses']).sum() / x['Total_Area_Expenses'].sum()
).reset_index(name='State_HAR')

# results for state-level HAR
print(state_har)

# Visualizing state-level HAR
plt.figure(figsize=(12, 6))
state_har.sort_values(by='State_HAR', ascending=False).plot(kind='bar', x='state', y='State_HAR', legend=False)
plt.title('State-Level Housing Affordability Ratio (HAR)')
plt.ylabel('HAR (%)')
plt.xlabel('State')
plt.show()




# ---------------- price-to-income ratio

# Calculate the median family income for each state
state_income_median = df_cost_of_living.groupby('state')['median_family_income'].median().reset_index(name='Median_Family_Income_state')

# Calculate the median house price for each state
state_house_price_median = df_house_listings.groupby('state')['property_price'].median().reset_index(name='Median_House_Price_state')

# Merge the median house price with the state-level median family income
state_data = pd.merge(state_income_median, state_house_price_median, on='state', how='inner')

# Calculate Price-to-Income Ratio for each state
state_data['Price_to_Income_Ratio'] = state_data['Median_House_Price_state'] / state_data['Median_Family_Income_state']

print(state_data)
# Visualizing the Price-to-Income Ratio for each state
plt.figure(figsize=(12, 6))
state_data.sort_values(by='Price_to_Income_Ratio', ascending=False).plot(kind='bar', x='state', y='Price_to_Income_Ratio', legend=False)
plt.title('State-Level Price-to-Income Ratio')
plt.ylabel('Price-to-Income Ratio')
plt.xlabel('State')
plt.show()


# Merge HAR and ECLB data on 'state'
state_data = pd.merge(state_har, state_eclb, on='state')
state_data['State_ECLB'] = state_data['State_ECLB'].clip(upper=99.99)


# # Calculate Affordability Index
state_data['Affordability_Index'] = (state_data['State_HAR'] / (100 - state_data['State_ECLB'])) * 100

# # Check the result
print(state_data[['state', 'Affordability_Index']])

# # Visualize the Affordability Index
# # plt.figure(figsize=(12, 6))
# # state_data.sort_values(by='Affordability_Index', ascending=False).plot(kind='bar', x='state', y='Affordability_Index', legend=False)
# # plt.title('State-Level Affordability Index')
# # plt.ylabel('Affordability Index')
# # plt.xlabel('State')
# # plt.show()

# AFFORDABILITY INDEX
# Merge the HAR and ECLB DataFrames (based on 'state')
state_data = pd.merge(state_har, state_eclb, on='state', how='inner')

# ---------------------- Step 1: Calculate the Affordability Index ----------------------

# Calculate the Affordability Index for each state
state_data['Affordability_Index'] = (state_data['State_HAR'] / (100 - state_data['State_ECLB'])) * 100

# Print the Affordability Index for each state
print(state_data[['state', 'Affordability_Index']])

# ---------------------- Step 2: Visualizing the Affordability Index ----------------------

# Visualizing the Affordability Index for each state
# plt.figure(figsize=(12, 6))
# state_data.sort_values(by='Affordability_Index', ascending=False).plot(kind='bar', x='state', y='Affordability_Index', legend=False)
# plt.title('State-Level Affordability Index')
# plt.ylabel('Affordability Index')
# plt.xlabel('State')
# plt.show()


#treechart
import plotly.express as px
import pandas as pd

# Step 1: Group by state and count the number of unique areas
area_count_per_state = df_cost_of_living.groupby('state')['areaname'].nunique().reset_index(name='Area_Count')

# Step 2: Create a Treemap
fig = px.treemap(area_count_per_state, 
                  path=['state', 'Area_Count'], 
                  values='Area_Count',
                  color='Area_Count',
                  color_continuous_scale='Purples',
                  title='Distribution of Areas per State in the US')

# Step 3: Show the Treemap
fig.show()


# boxplots

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Assuming df_cost_of_living is already loaded with necessary columns
# Expense categories to be plotted
expense_categories = ['housing_expenses', 'food_expenses', 'transport_expenses', 'healthcare_expenses', 'other_necessities_expenses', 'childcare_expenses']

# Create a directory to save the plots if it doesn't already exist
output_dir = './expense_boxplots/'
os.makedirs(output_dir, exist_ok=True)

# Create a boxplot for each expense category and save it as a separate file
for category in expense_categories:
    plt.figure(figsize=(10, 6))  # Adjust the figure size
    sns.boxplot(data=df_cost_of_living, x='state', y=category, palette="Set3")

    # Setting plot title and labels
    plt.title(f'Boxplot of {category.replace("_", " ").title()} by State', fontsize=14)
    plt.xlabel('State', fontsize=12)
    plt.ylabel(f'{category.replace("_", " ").title()}', fontsize=12)
    plt.xticks(rotation=90)  # Rotate state names for better readability

    # Save the plot as a PNG file
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{category}_boxplot.png'))

    # Close the plot to avoid overlapping with the next one
    plt.close()

print(f"Boxplots have been saved in the '{output_dir}' folder.")


mean_income = df_cost_of_living.groupby('areaname')['median_family_income'].mean().reset_index(name='Mean_Family_Income_area')

area_expenses_median = df_cost_of_living.groupby(['state', 'areaname']).agg({
    'housing_expenses': 'sum',
    'household_taxes': 'sum',
    'food_expenses': 'sum',
    'transport_expenses': 'sum',
    'healthcare_expenses': 'sum',
    'other_necessities_expenses': 'sum',
    'childcare_expenses': 'sum'
}).reset_index()

area_data = area_expenses_median.merge(mean_income, on=['areaname'], how='inner')

area_data['Total_Median_Essential_Expenses'] = (
    area_data['housing_expenses'] +
    area_data['household_taxes'] +
    area_data['food_expenses'] +
    area_data['transport_expenses'] +
    area_data['healthcare_expenses'] +
    area_data['other_necessities_expenses'] +
    area_data['childcare_expenses']
)
state_data = area_data.merge(mean_income, on=['areaname'], how='inner')


# # AREAS STATES
# area_count_per_state = df_cost_of_living.groupby('state')['areaname'].nunique().reset_index(name='Area_Count')
# fig = px.scatter(area_count_per_state, 
#                  x='state', 
#                  y='Area_Count', 
#                  size='Area_Count', 
#                  text= 'Area_Count',
#                  color='Area_Count', 
#                  hover_name='state', 
#                  title='Areas per State',
#                  size_max=60, 
#                  color_continuous_scale='Purples')
# fig.show()


# #EXPENSES
# # all expense categories
# expense_categories = ['food_expenses', 'transport_expenses', 
#                       'healthcare_expenses', 'other_necessities_expenses', 
#                       'childcare_expenses', 'housing_expenses', 'household_taxes']


# # density plot
# for category in expense_categories:

#     plt.figure(figsize=(10, 6))
#     sns.kdeplot(df_cost_of_living[category], shade=True, color='#BDB5D5')
    
#     plt.title(f'Density Plot of {category.replace("_", " ").title()}', fontsize=14)
#     plt.xlabel(f'{category.replace("_", " ").title()}', fontsize=12)
#     plt.ylabel('Density', fontsize=12)

#     plt.show()


# INCOME VS EXPENSES
# area_data = df_cost_of_living.groupby(['state', 'areaname']).agg(
#     total_income=('median_family_income', 'sum'),
#     total_costs=('total_household_expenses', 'sum')
# ).reset_index()

# state_total = area_data.groupby('state').agg(
#     total_income=('total_income', 'sum'),
#     total_costs=('total_costs', 'sum')
# ).reset_index()

# plt.figure(figsize=(14, 7))

# plt.plot(state_total['state'], state_total['total_income'], label='Total Income', color='purple', marker='x', linewidth=1)
# plt.plot(state_total['state'], state_total['total_costs'], label='Total Costs', color='black', marker='o', linewidth=2)

# plt.title('Comparison of Total Income and Total Costs by State', fontsize=14)
# plt.xlabel('State', fontsize=14)
# plt.ylabel('Amount ($)', fontsize=14)
# plt.xticks(rotation=90)
# plt.legend()
# plt.tight_layout()
# plt.show()

# state_total['income_vs_costs'] = state_total['total_income'] - state_total['total_costs']

# higher_income_states = state_total[state_total['income_vs_costs'] > 0]
# print("States with higher income than costs:")
# print(higher_income_states[['state', 'total_income', 'total_costs', 'income_vs_costs']])

# higher_costs_states = state_total[state_total['income_vs_costs'] < 0]
# print("\nStates with higher costs than income:")
# print(higher_costs_states[['state', 'total_income', 'total_costs', 'income_vs_costs']])

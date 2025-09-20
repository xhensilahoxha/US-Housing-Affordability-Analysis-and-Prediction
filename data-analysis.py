# handling the data
import pandas as pd
import sqlite3
import json
from urllib.request import urlopen

# math
import numpy as np

# visualizing
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# <--------------------------------------Connection-------------------------------------->
# start connection
db_path = './data/train_data.sqlite'

database_connection = sqlite3.connect(db_path)

df_cost_of_living = pd.read_sql_query("SELECT * FROM cost_of_living", database_connection)
df_house_listings = pd.read_sql_query("SELECT * FROM house_listings", database_connection)

# close the db connection
database_connection.close()
# <---------------------------------------------------------------------------->

# <--------------------------------------Representation of data-------------------------------------->  
#1: df_cost_of_living
unnecessary_columns = ['total_household_expenses', 
                       'parents_per_household', 
                       'children_per_household'
                       ] #irrelevant to analysis later

# new dataframe
df_needed_columns = df_cost_of_living.drop(columns=unnecessary_columns)

# 15 first rows
df_print = df_needed_columns.head(15) 

# to string ""
df_print_str = df_print.applymap(str)

# table figure
fig, ax = plt.subplots(figsize=(18, 6))  
ax.axis('off') 
expenses_table = ax.table(cellText=df_print_str.values, colLabels=df_print.columns, loc='center')
expenses_table.auto_set_font_size(False) 
expenses_table.set_fontsize(6) 

# column width
for i, j in enumerate(df_print.columns):
    max_length_calc = max(df_print[j].apply(str).apply(len).max(), len(j))

    expenses_table.auto_set_column_width([i])
    expenses_table[0, i].set_text_props(weight='bold', color='lavender')
    expenses_table[0, i].set_facecolor('black')

# design cells
for i in range(1, len(df_print) + 1):  # skip header
    for j in range(len(df_print.columns)):
        one_cell = expenses_table[i, j]
        if i % 2 == 0:
            one_cell.set_facecolor('#f3f3f9')  # Light-purple even rows
        else:
            one_cell.set_facecolor('#ffffff')  # White odd rows

plt.text(0.5, 0.85, "Cost of Living in the U.S", ha='center', va='center', fontsize=16, weight='bold')
plt.tight_layout() 

plt.show()

#2: df_house_listings

# 15 first rows
df_print = df_house_listings.head(15) 

# to string ""
df_print_str = df_print.applymap(str)

# table figure
fig, ax = plt.subplots(figsize=(18, 6))  
ax.axis('off')  
housing_table = ax.table(cellText=df_print_str.values, colLabels=df_print.columns, loc='center')
housing_table.auto_set_font_size(False) 
housing_table.set_fontsize(6) 

# column width 
for i, j in enumerate(df_print.columns):
    max_length_calc = max(df_print[j].apply(str).apply(len).max(), len(j))

    housing_table.auto_set_column_width([i])
    housing_table[0, i].set_text_props(weight='bold', color='lavender')
    housing_table[0, i].set_facecolor('black')

# design cells
for i in range(1, len(df_print) + 1):  # Skip header
    for j in range(len(df_print.columns)):
        one_cell = housing_table[i, j]
        if i % 2 == 0:
            one_cell.set_facecolor('#f3f3f9')  # Light-purple even rows
        else:
            one_cell.set_facecolor('#ffffff')  # White odd rows

plt.text(0.5, 0.85, "House Prices in the U.S", ha='center', va='center', fontsize=16, weight='bold')
plt.tight_layout()  

plt.show()
# <---------------------------------------------------------------------------->

# <--------------------------------------MAP AREAS-------------------------------------->

# group unique areas per state
area_count_per_state = df_cost_of_living.groupby('state')['areaname'].nunique().reset_index(name='Area_Count')

map_abbr_table_to_name_map = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", 
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", 
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", 
    "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", 
    "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", 
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", 
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", 
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", 
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", 
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", 
    "WY": "Wyoming"
}

# mapping
area_count_per_state['state_long_name'] = area_count_per_state['state'].map(map_abbr_table_to_name_map)

# retrieve and open geoJSON 
with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    states = json.load(response)

# details of the choropleth map
fig_map = px.choropleth(area_count_per_state, 
                        geojson=states, 
                        locations='state_long_name', 
                        featureidkey="properties.name",
                        color='Area_Count', 
                        hover_name='state',               #details when hovering
                        color_continuous_scale='Purples', #palette of purples
                        title='Areas per State')

# zoom to U.S locations only
fig_map.update_geos(fitbounds="locations", visible=False)

# more detailed customization of the map
fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    title="Area Count per State"
)
fig_map.show()
# <---------------------------------------------------------------------------->


# <--------------------------------------Distribution of expenses/ state-------------------------------------->

# group the expenses by area 
area_expenses = df_cost_of_living.groupby(['state', 'areaname'])[['food_expenses', 'transport_expenses', 
                                                                      'healthcare_expenses', 'other_necessities_expenses', 
                                                                      'childcare_expenses', 'housing_expenses', 
                                                                      'household_taxes']].sum().reset_index()

# plus housing taxes
area_expenses['the_housing_expenses'] = area_expenses['housing_expenses'] + area_expenses['household_taxes']
area_expenses = area_expenses.drop(columns=['housing_expenses', 'household_taxes'])

# group the expenses by state
state_expenses = area_expenses.groupby('state')[['food_expenses', 'transport_expenses', 
                                                     'healthcare_expenses', 'other_necessities_expenses', 
                                                     'childcare_expenses', 'the_housing_expenses']].sum()

# rotate to horizontal bar
ax = state_expenses.plot(kind='barh', stacked=True, figsize=(14, 7), colormap='twilight_shifted')

# visualization of the stack-plot
plt.title('Total Living Expenses by State', fontsize=16)
plt.xlabel('Total Expenses ($)', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.legend(title='Expense Categories', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
# <---------------------------------------------------------------------------->

# <--------------------------------------Property prices boxplot-------------------------------------->

# pastel to purple
my_palette = [
    "#800080",  
    "#9B30FF",  
    "#DDA0DD",
    "#FAD6A5", 
    "#F8C8B5",
    "#5D3FD3",  
    "#F5F5DC",  
    "#D8BFD8", 
    "#777777"   
]

plt.figure(figsize=(10, 6))

# use of sns for aesthetic presentation
sns.boxplot(x='state', y='property_price', data=df_house_listings, palette=my_palette)

# visualization of the boxplot
plt.title('Property Prices by State', fontsize=16)
plt.xlabel('State', fontsize=14)
plt.ylabel('Property Price', fontsize=14)
plt.xticks(rotation=90)
plt.ylim(0, 2000000) # for clearer visualization
plt.tight_layout()

plt.show()
# <---------------------------------------------------------------------------->


# <--------------------------------------Essential Cost of Living to Income Ratio-------------------------------------->

# mean of 'median_family_income' for each 'areaname' for any rare case that the 'median_family_income' is not the same within an area
# mean() is the best choice because median family income values are very similar within an area
mean_of_income = df_cost_of_living.groupby('areaname')['median_family_income'].mean().reset_index(name='Median_Income_Area')

# group by area & find medians of each category
area_expenses_medians = df_cost_of_living.groupby(['state', 'areaname']).agg({
    'housing_expenses': 'median',
    'food_expenses': 'median',
    'transport_expenses': 'median',
    'healthcare_expenses': 'median',
    'other_necessities_expenses': 'median',
    'childcare_expenses': 'median'
}).reset_index()

# new dataframe
area_data = area_expenses_medians.merge(mean_of_income, on=['areaname'], how='inner')

# new column
area_data['Median_Essential_Expenses'] = (
    area_data['housing_expenses'] +
    area_data['food_expenses'] +
    area_data['transport_expenses'] +
    area_data['healthcare_expenses'] +
    area_data['other_necessities_expenses'] +
    area_data['childcare_expenses']
)

# Find ECLIR per area
area_data['ECLIR_area'] = (area_data['Median_Essential_Expenses'] / area_data['Median_Income_Area']) * 100

# group total expenses column by area
total_area_expenses = df_cost_of_living.groupby(['state', 'areaname'])['total_household_expenses'].sum().reset_index(name='Total_Area_Expenses')

# new dataframe
area_data = area_data.merge(total_area_expenses, on=['state', 'areaname'])

# Find weighted ECLIR per state
state_ECLIR = area_data.groupby('state').apply(
    lambda x: (x['ECLIR_area'] * x['Total_Area_Expenses']).sum() / x['Total_Area_Expenses'].sum()
).reset_index(name='state_ECLIR')

# print(state_ECLIR)
state_ECLIR_sorted = state_ECLIR.sort_values(by='state_ECLIR', ascending=True)

# sns for aesthetic
purple_palette = sns.color_palette("ch:s=-.2,r=.6", len(state_ECLIR_sorted))

# visualize by barchart
plt.figure(figsize=(16, 10)) 
plt.bar(state_ECLIR_sorted['state'], state_ECLIR_sorted['state_ECLIR'], color=purple_palette)
plt.title('State-Level Essential Cost of Living to Income Ratio (ECLIR)', fontsize=16)
plt.xlabel('State', fontsize=14)
plt.ylabel('ECLIR (%)', fontsize=14)
plt.xticks(rotation=90)
plt.ylim(0, 120) #limit bar to max value pretty print
plt.yticks(np.arange(10, 130, 6)) #step 6

# horizontal dashed lines on limit bars for clearer picture (---)
first_bar_position = 0
last_bar_position = len(state_ECLIR_sorted) - 1
first_bar_value = state_ECLIR_sorted.iloc[0]['state_ECLIR']
last_bar_value = state_ECLIR_sorted.iloc[-1]['state_ECLIR']

# plot
plt.plot([first_bar_position-1, first_bar_position], [first_bar_value, first_bar_value], color='purple', linestyle='dashed', linewidth=2)  # First bar lines --
plt.plot([last_bar_position, last_bar_position + 1], [last_bar_value, last_bar_value], color='purple', linestyle='dashed', linewidth=2)  # Last bar lines --
plt.tight_layout()

plt.show()
# <---------------------------------------------------------------------------->


# <--------------------------------------Housing Cost Burden-------------------------------------->
#  https://www.jchs.harvard.edu/sites/default/files/Harvard_JCHS_Herbert_Hermann_McCue_measuring_housing_affordability.pdf

# median of house expenses: area
area_housing_expenses_median = df_cost_of_living.groupby(['state', 'areaname'])['housing_expenses'].median().reset_index(name='Median_Housing_Expenses_area')
area_housing_taxes_median = df_cost_of_living.groupby(['state', 'areaname'])['household_taxes'].median().reset_index(name='Median_Housing_Taxes_area')

area_data = area_housing_expenses_median.merge(area_housing_taxes_median, on=['state', 'areaname'])

# median of housing expenses in total
area_data['Total_Median_Housing_Expenses'] = area_data['Median_Housing_Expenses_area'] + area_data['Median_Housing_Taxes_area']

# new df
area_data = area_data.merge(mean_of_income, on=['areaname'])

# HCB for area
area_data['HCB_area'] = (area_data['Total_Median_Housing_Expenses'] / area_data['Median_Income_Area']) * 100

# total housing expenses
df_cost_of_living['Total_Housing_Expenses'] = df_cost_of_living['housing_expenses'] + df_cost_of_living['household_taxes']

# group housing expenses for area
total_area_expenses = df_cost_of_living.groupby(['state', 'areaname'])['Total_Housing_Expenses'].sum().reset_index(name='Total_Area_Expenses')

# new df
area_data = area_data.merge(total_area_expenses, on=['state', 'areaname'])

# group by state, HCB weighted by housing expenses
state_hcb = area_data.groupby('state').apply(
    lambda x: (x['HCB_area'] * x['Total_Area_Expenses']).sum() / x['Total_Area_Expenses'].sum() 
).reset_index(name='State_HCB')

# print(state_hcb )
state_hcb_sorted = state_hcb.sort_values(by='State_HCB', ascending=True)

# visualize by barplot graph
plt.figure(figsize=(16, 10))  
sns.barplot(x='state', y='State_HCB', data=state_hcb_sorted, palette="Purples")
plt.title('State-Level Housing Cost Burden (HCB)', fontsize=16)
plt.xlabel('State', fontsize=14)
plt.ylabel('Housing Cost Burden (%)', fontsize=14)
plt.xticks(rotation=90)
plt.ylim(0, 60) #limit for clearer view
plt.yticks(np.arange(2, 60, 4))  #step
plt.tight_layout()

plt.show()
# <---------------------------------------------------------------------------->

# <--------------------------------------Price to Income Ratio-------------------------------------->

# median of house expenses: state [ as median of median ]
state_income_median = area_data.groupby('state')['Median_Income_Area'].median().reset_index(name='Median_Income_state')

# median of house price: state
state_house_price_median = df_house_listings.groupby('state')['property_price'].median().reset_index(name='Median_House_Price_state')

# new dataframe
state_data = pd.merge(state_income_median, state_house_price_median, on='state', how='inner')

# calculation of PIR
state_data['Price_to_Income_Ratio'] = state_data['Median_House_Price_state'] / state_data['Median_Income_state']

# print(state_data)

# pie chart details
range = [0, 3, 4, 5, float('inf')]
category = ['Low (0-3)', 'Moderate (3-4)', 'Serious (4-5)', 'Severe (>5)']

state_data['Price_to_Income_Category'] = pd.cut(state_data['Price_to_Income_Ratio'], bins=range, labels=category)  #cut in ranges

category_counts = state_data['Price_to_Income_Category'].value_counts().reindex(category)

category_counts.plot(kind='pie', 
                    autopct='%1.1f%%', 
                    startangle=90, 
                    colors=['#D3CCE3', '#A9A9C9', '#786D89', '#5E3A69'], #shades of purple
                    wedgeprops={'edgecolor': 'black'}, 
                    explode=(0, 0.1, 0.1, 0.1)) #sliced out

# visualization: pie chart
plt.figure(figsize=(8, 8))
plt.title('Housing Price-to-Income Ratio')
plt.ylabel('')
plt.legend(labels=category, loc='lower right')
plt.axis('equal') #no x axis

plt.show()
 
# visualization: line chart

plt.figure(figsize=(12, 6))
plt.plot(state_data['state'], 
         state_data['Price_to_Income_Ratio'], 
         marker='^', 
         color='#483D8B', 
         linestyle='-', 
         linewidth=2, 
         markersize=8, 
         markerfacecolor='white', 
         markeredgewidth=2)


plt.title('Price-to-Income Ratio Across U.S.', fontsize=18, fontweight='bold', color = '#483D8B')
plt.xlabel('State', fontsize=12)
plt.ylabel('Price-to-Income Ratio', fontsize=12)
plt.xticks(rotation=90, fontsize=10)
# include grid: clear view
plt.grid(True, linestyle=':', alpha=0.7, color = "black")
plt.tight_layout()
plt.show()
# <---------------------------------------------------------------------------->
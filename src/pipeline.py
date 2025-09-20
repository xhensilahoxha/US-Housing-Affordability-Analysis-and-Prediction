import os
import pandas as pd
import sqlalchemy as sql
from kaggle.api.kaggle_api_extended import KaggleApi

# Side Functions Blocks

def download_kaggle_datasets(url, _path=''):
    """ Kaggle API Initialization """
    api = KaggleApi()
    api.authenticate()
    
    # The expected URL format is: https://www.kaggle.com/datasets/owner_slug/dataset_name
    url_parts = url.split('/datasets/') 
    if len(url_parts) < 2:
        raise ValueError("Invalid URL format.") 
    
    dataset_info = url_parts[1].split('/')  
    if len(dataset_info) < 2:
        raise ValueError("Could not extract! ") 
    
    owner_slug = dataset_info[0] 
    dataset_name = dataset_info[1].split('/')[0]  

    api.dataset_download_files(f"{owner_slug}/{dataset_name}", path=_path, unzip=True)

    csv_files = [file for file in os.listdir(_path) if file.endswith('.csv')] 
    if not csv_files:
        raise ValueError("Couldn't find CSV format file!") 

    dfs = {} #dictionary of dataframes
    for csv_file in csv_files:
        csv_path = os.path.join(_path, csv_file)
        print(f"Loading CSV: {csv_file}")
        dfs[csv_file] = pd.read_csv(csv_path)

    return dfs

def initialize_sqlite_db(db_name):
    """ SQLITE Initialization """
    files_dir = './data'
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
        print(f"Created directory: {files_dir}")
    db_path = os.path.join(files_dir, db_name)
 
    if os.path.exists(db_path):
        os.remove(db_path)  # Remove existing file
        print(f"Removed outdated database file: {db_path}")   
    #SQLAlchemy engine for the SQLite database
    engine = sql.create_engine(f'sqlite:///{db_path}')
    print(f"Initialized SQLite database at: {db_path}")
    return engine
    
# Main Function Block

def main():

    sqlite_db_path = 'train_data.sqlite'

    """ Data Extracting """
    # Data source 1: US Households Cost of Living dataset
    url_cost_of_living_us = "https://www.kaggle.com/datasets/asaniczka/us-cost-of-living-dataset-3171-counties"
    dfs = download_kaggle_datasets(url_cost_of_living_us,'data')
    
    """ Data Transformation """
    dfs['cost_of_living_us.csv'].columns = dfs['cost_of_living_us.csv'].columns.str.strip()
    
    cost_of_living_df = dfs['cost_of_living_us.csv']
    cost_of_living_df['parents_per_household'] = cost_of_living_df['family_member_count'].str.extract(r'(\d+)p')[0].astype('int64') 
    cost_of_living_df['children_per_household'] = cost_of_living_df['family_member_count'].str.extract(r'p(\d+)c')[0].astype('int64')

    columns_to_drop_1 = ['isMetro', 'county','family_member_count' ] #irrelevant
    
    #edit: re-adding the areaname column for the analysis file
    
    dfs['cost_of_living_us.csv'].drop(columns=columns_to_drop_1, inplace=True)
    
    # rename columns for calculation convenience for the next #Issues
    dfs['cost_of_living_us.csv'].rename(columns={
                                            'case_id': 'household_id',
                                            'housing_cost': 'housing_expenses', 
                                            'food_cost': 'food_expenses', 
                                            'transportation_cost': 'transport_expenses',
                                            'healthcare_cost': 'healthcare_expenses',
                                            'other_necessities_cost': 'other_necessities_expenses',
                                            'childcare_cost': 'childcare_expenses',
                                            'taxes': 'household_taxes',
                                            'total_cost': 'total_household_expenses',
                                              }, 
                                            inplace=True)
    """
    Data Cleaning
    During data cleaning there were 10 missing values for overall dataframe. 
    During filtering the missing values were part of 'MO' state.
    Since there are 1161 values for that state, we will use imputation median fill method.
        
        #median_family_income column!
    """
    median_expenses = dfs['cost_of_living_us.csv'][dfs['cost_of_living_us.csv']['state'] == 'MO']['median_family_income'].median()
    dfs['cost_of_living_us.csv'].loc[dfs['cost_of_living_us.csv']['state'] == 'MO', 'median_family_income'] = \
    dfs['cost_of_living_us.csv'].loc[dfs['cost_of_living_us.csv']['state'] == 'MO', 'median_family_income'].fillna(median_expenses)
    


    """ Data Loading """
    engine = initialize_sqlite_db(sqlite_db_path)
    if 'cost_of_living_us.csv' in dfs:
        dfs['cost_of_living_us.csv'].to_sql('cost_of_living', engine, if_exists='replace', index=False)
        print("Households' cost of living data is now inserted into SQLite database.")
    else:
        print("File is not found!")
    
    # print(dfs['cost_of_living_us.csv'].head())

    """ Data Extracting """
    # Data source 2: US House Listings Prices dataset
    url_house_listings = "https://www.kaggle.com/datasets/febinphilips/us-house-listings-2023"
    dfs = download_kaggle_datasets(url_house_listings, 'data')

    """ Data Transformation """
    columns_to_drop_2 = ['City', 'Street', 'Zipcode',  #irrelevant (for now)
                         'Bedroom', 'Bathroom', 'LotArea',  #too many nan and missing values
                         'MarketEstimate', 'RentEstimate',  #irrelevant 
                         'ConvertedLot', 'LotUnit', #irrelevant 
                         'Latitude', 'Longitude'] #irrelevant

    dfs['original_extracted_df.csv'].drop(columns=columns_to_drop_2, inplace=True)
    
    dfs['original_extracted_df.csv'].rename(columns={
                                            'State': 'state',
                                            'Area': 'property_area_meters',
                                            'PPSq': 'price_per_sq_meter', 
                                            'Price': 'property_price', 
                                              },
                                            inplace=True)
    
    """
    Data Cleaning
    During data cleaning there were around 5k missing values out of 24k rows of data.
    We will drop rows with missing values in all columns to avoid reducing variance.
    We will drop logical incorrect data rows per columns.

    """
    
    dfs['original_extracted_df.csv'].dropna(how='all', inplace=True)
    
    dfs['original_extracted_df.csv'] = dfs['original_extracted_df.csv'][~dfs['original_extracted_df.csv']['property_price'].isin([0, 1])
                                                                         & dfs['original_extracted_df.csv']['property_price'].notna()]
    dfs['original_extracted_df.csv'] = dfs['original_extracted_df.csv'][~dfs['original_extracted_df.csv']['property_area_meters'].isin([0, 1])
                                                                        & dfs['original_extracted_df.csv']['property_area_meters'].notna()]

    
    
    # print(dfs['original_extracted_df.csv'].isnull().sum())

    """ Data Loading """
    if 'original_extracted_df.csv' in dfs:
        dfs['original_extracted_df.csv'].to_sql('house_listings', engine, if_exists='replace', index=False)
        print("House listings data is now inserted into SQLite database.")
    else:
        print("File is not found!")    

    # print(dfs['original_extracted_df.csv'].head())

if __name__ == "__main__":
    main()

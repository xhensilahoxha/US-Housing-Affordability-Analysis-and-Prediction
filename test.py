""" This document includes automated tests for the pipeline.

    Automated tests: These tests are automatically validated while tests.sh script is running.

    Dynamic: This setup performs checks at runtime.

    Functional: This setup focuses on behavior and features.

    Test Levels:
    1. Component tests: Testing one component
    2. Integration tests: Testing collaboration of components
    3. System tests: Testing End-to-end

    """

import os
import subprocess
import pytest
import sqlite3
import pandas as pd

# Fixture
@pytest.fixture
def database_full_path():
    db_path = '../data/train_data.sqlite'
    script_file_path = __file__  # File's path
    script_files_dir = os.path.dirname(script_file_path)  # Directory of the file
    database_path = os.path.join(script_files_dir, db_path) # Absolute path
    return database_path

# Component Tests
def data_loading(database_full_path):

    try: 
        with sqlite3.connect(database_full_path) as database_connection:

            loaded_query_c = "SELECT COUNT(*) FROM cost_of_living"
            count_query_c = database_connection.execute(loaded_query_c).fetchone()[0]
            assert count_query_c > 0, "There is no data in the 'cost_of_living' table."

            loaded_query_h = "SELECT COUNT(*) FROM house_listings"
            count_query_h = database_connection.execute(loaded_query_h).fetchone()[0]
            assert count_query_h > 0, "There is no data in the 'house_listing' table."
      
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()

def test_null_values_in_columns(database_full_path):

    try:
        with sqlite3.connect(database_full_path) as database_connection:

            columns_to_check = ['household_id', 'housing_expenses','total_household_expenses', 
                                'food_expenses', 'transport_expenses', 'healthcare_expenses', 
                                'other_necessities_expenses', 'childcare_expenses',
                                'household_taxes', 'parents_per_household', 'children_per_household']
            
            for column in columns_to_check:
                query_c = f"SELECT COUNT(*) FROM cost_of_living WHERE {column} IS NULL"
                null_count = database_connection.execute(query_c).fetchone()[0]
                assert null_count == 0, f"There are {null_count} null values in {column} column."

            columns_to_check = ['state', 'property_area_meters', 'price_per_sq_meter', 'property_price']
            
            for column in columns_to_check:
                query_h = f"SELECT COUNT(*) FROM house_listings WHERE {column} IS NULL"
                null_count = database_connection.execute(query_h).fetchone()[0]
                assert null_count == 0, f"There are {null_count} null values in {column} column."
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()

    # print("Null values check passed successfully!")

def test_imputation_method(database_full_path):

    try:
        with sqlite3.connect(database_full_path) as database_connection:
            median_query = "SELECT state, total_household_expenses FROM cost_of_living WHERE state = 'MO'"
            df = pd.read_sql_query(median_query, database_connection)

            # Check if filled with median
            no_null = df['total_household_expenses'].isnull().sum() == 0
            assert no_null, f"State 'MO' still has null values."
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()

# Integration Tests
def test_table_creation_duplicated(database_full_path):

    try: 
        with sqlite3.connect(database_full_path) as database_connection:

            # Get all table names from the database
            fetch_table_names_query = "SELECT name FROM sqlite_master WHERE type='table';"
            fetched_table_data = database_connection.execute(fetch_table_names_query).fetchall()

            actual_table_names = {row[0] for row in fetched_table_data}
        expected_table_names = {"cost_of_living", "house_listings"}

        missing_table_names = expected_table_names - actual_table_names
        assert not missing_table_names, f"Table:{missing_table_names} is not created."

        assert len(actual_table_names) == len(fetched_table_data), "Attention: Tables with the same name are detected!"

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()

def test_column_renaming(database_full_path):

    try:

        with sqlite3.connect(database_full_path) as database_connection:
            
            # Validate column renaming for 'house_listings' table
            expected_columns_cost_of_living = [
                'household_id', 'housing_expenses', 'food_expenses', 'transport_expenses', 
                'healthcare_expenses', 'other_necessities_expenses', 'childcare_expenses', 
                'household_taxes', 'total_household_expenses', 'parents_per_household', 
                'children_per_household', 'state'
            ]
            pragma_query_table = "PRAGMA table_info(cost_of_living);"
            columns_cost_of_living = [row[1] for row in database_connection.execute(pragma_query_table).fetchall()]
            
            missing_columns = set(expected_columns_cost_of_living) - set(columns_cost_of_living)
            assert not missing_columns, f"{missing_columns} column is missing."
            
            # Validate column renaming for 'house_listings' table
            expected_columns_house_listings = [
                'state', 'property_area_meters', 'price_per_sq_meter', 'property_price'
            ]
            pragma_query_table = "PRAGMA table_info(house_listings);"
            columns_house_listings = [row[1] for row in database_connection.execute(pragma_query_table).fetchall()]
            
            missing_columns = set(expected_columns_house_listings) - set(columns_house_listings)
            assert not missing_columns, f"{missing_columns} column is missing."
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()
    
        

def test_table_and_column_format(database_full_path):

    try:
    
        with sqlite3.connect(database_full_path) as database_connection:

            expected_format_cost_of_living = [
                ('household_id', 'BIGINT'), ('housing_expenses', 'FLOAT'), ('food_expenses', 'FLOAT'),
                ('transport_expenses', 'FLOAT'), ('healthcare_expenses', 'FLOAT'), ('other_necessities_expenses', 'FLOAT'),
                ('childcare_expenses', 'FLOAT'), ('household_taxes', 'FLOAT'), ('total_household_expenses', 'FLOAT'),
                ('parents_per_household', 'INTEGER'), ('children_per_household', 'INTEGER'), ('state', 'TEXT')
            ]
            pragma_query_format = "PRAGMA table_info(cost_of_living);"
            name_type_cost_of_living = [(row[1], row[2]) for row in database_connection.execute(pragma_query_format).fetchall()]
            
            # Match column names and types
            mismatching_columns = set(expected_format_cost_of_living) - set(name_type_cost_of_living)
            assert not mismatching_columns, f"Columns mismatch: {mismatching_columns}"


            expected_columns_house_listings = [
                ('state', 'TEXT'), ('property_area_meters', 'FLOAT'), ('price_per_sq_meter', 'FLOAT'), ('property_price', 'FLOAT')
            ]
            pragma_query_format = "PRAGMA table_info(house_listings);"
            name_type_house_listings = [(row[1], row[2]) for row in database_connection.execute(pragma_query_format).fetchall()]
            
            # Match column names and types
            mismatching_columns = set(expected_columns_house_listings) - set(name_type_house_listings)
            assert not mismatching_columns, f"Columns mismatch: {mismatching_columns}"

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close database connection
        if database_connection:
            database_connection.close()

# System Test
def test_end_to_end(database_full_path):
    # Pipeline Execution
    # result = subprocess.run(["bash", "pipeline.sh"], capture_output=True, text=True)
    result = subprocess.run(["python", "./project/pipeline.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"{result.stderr}: Pipeline execution failed!"

    # Output Files validation
    assert os.path.exists(database_full_path), f"Output file {database_full_path} was not found."

if __name__ == '__main__':
    pytest.main()

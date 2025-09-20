# __Project Plan__
## __Title__
The living-cost crisis in the U.S. and its effect on households' ability to afford house prices.

## Main Question
How do essential living expenses impact housing affordability for households across the U.S.?

## Description
This projects focuses on one of the biggest problems affecting the quality of life of the U.S. inhabitants, which is the high prices across various life necessities' directions, like transport prices, childcare costs, healthcare costs, etc. Due to the increased prices these latest years, the U.S. households are facing difficulties in maintaining a good quality of life index. _A living-cost crisis may affect people in various forms, considering mental health conditions, low investment rates, etc._ This project suggests that households' basic-life expenses are fraining them from the possibility of affording a house in various U.S. regions. This project aims to find the connection between essential life expenses and the U.S. inhabitants ability to buy a home.

# Datasources
### Datasource 1: Kaggle Dataset Page
- Metadata URL: [Kaggle Dataset Page](https://www.kaggle.com/datasets/asaniczka/us-cost-of-living-dataset-3171-counties)
- Data URL: [U.S. Cost of Living Data (Kaggle)](https://www.kaggle.com/datasets/asaniczka/us-cost-of-living-dataset-3171-counties/data?select=cost_of_living_us.csv)
- Data Type: CSV

#### _Description_
This dataset offers wide information about 50 U.S. states and families' essential expenses, including here: healthcare, transportation, food, taxes, etc. _We will consider a **typical** family when doing the calculations._ This dataset offers information about the families' incomes. _We need this data for further **cost of living** calculations._

### Datasource 2: Kaggle Dataset Page
- Metadata URL: [Kaggle Dataset Page](https://www.kaggle.com/datasets/febinphilips/us-house-listings-2023)
- Data URL: [U.S. House Listings Data (Kaggle)](https://www.kaggle.com/datasets/febinphilips/us-house-listings-2023?select=original_extracted_df.csv)
- Data Type: CSV

#### _Description_
This dataset is inherited from the Zillow platform, which is one of the biggest online services in the U.S. for sharing real estate and market data. The columns include: state, market prices for various houses, rental prices, and other property details (bedrooms, area, etc). We will focus on property _buying_ prices for this project.

## Work Packages
### Issue 1: Collect Data
It is important in this step to find quantitative and qualitative datasets for complementing the project's aim and answering the main question at the very last issue.
_Dependencies_ : Kaggle Datasets.

### Issue 2: Clean Data and Create an ETL Pipeline
In this step, we must create a script that introduces an automated pipeline for extracting, transforming, and loading the data.
_Dependencies_ : Collected datasets. 

### Issue 3: Automatically Test the Pipeline
We must focus on leveraging a clean structured code, and a very good model pipeline that is able to test data. We must be able to do calculations and sub-tasks that train the pipeline in this step.
_Dependencies_ : ETL Pipeline.

### Issue 4: Continuously integrate the pipeline
In this step, we should be able to integrate the pipeline and focus on the details.
_Dependencies_ : ETL Pipeline Model.

### Issue 5: An engineering pipeline 
This is the last step; we want to make sure that everything is working properly and we are able to derive conclusions.
_Dependencies_ : The integrated ETL Pipeline.
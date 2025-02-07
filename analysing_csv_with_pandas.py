"""
This script performs the technical tasks outlined in the assignment, including:
- Loading and exploring datasets.
- Documenting table structures and relationships.
- Performing analytical tasks, such as identifying top products and customer segments.
- Generating key performance indicators (KPIs) for business insights.
- Exporting results to Excel for reporting.
"""

import pandas as pd
import os 

#load csv
product = pd.read_csv("../../Downloads/Python Test/product.csv", delimiter=';')
product_category = pd.read_csv("../../Downloads/Python Test/product_category.csv", delimiter=';')
product_subcategory = pd.read_csv("../../Downloads/Python Test/product_subcategory.csv", delimiter=';')
sales = pd.read_csv("../../Downloads/Python Test/sales.csv", delimiter=';')
sales_details = pd.read_csv("../../Downloads/Python Test/sales_details.csv", delimiter=';')
special_offer = pd.read_csv("../../Downloads/Python Test/special_offer.csv", delimiter=';')

#exollore tables
#pritn out first 5 rows of each dataset to understand ts structure
print(product.head())
print(product_category.head())
print(product_subcategory.head())
print(sales.head())
print(sales_details.head())
print(special_offer.head())

#gives us the productid whci in our case would be the column would serve as primary key, and as such each needs to be unique
print(product['ProductID'].is_unique)
print(product['ProductSubcategoryID'].isin(product_subcategory['ProductSubcategoryID']).all())

#a function to identify primary keys
def identify_primary_keys(df, table_name):
    """
    Identifies and prints columns that can act as primary keys in a DataFrame.
    args:
        df (DataFrame): The DataFrame to analyze.
        table_name (str): Name of the table for display purposes.
    """
    print(f"Primary Key Check for Table: {table_name}")
    for column in df.columns:
        if df[column].is_unique:
            print(f"- {column} is a primary key.")
        else:
            print(f"- {column} is NOT a primary key.")
    print("\n")

#primary keys identifier for each table
identify_primary_keys(product, "product")
identify_primary_keys(product_category, "product_category")
identify_primary_keys(product_subcategory, "product_subcategory")
identify_primary_keys(sales, "sales")
identify_primary_keys(sales_details, "sales_details")
identify_primary_keys(special_offer, "special_offer")


#a function to validate potential foreign key rlation
def validate_foreign_keys(foreign_df, foreign_key, primary_df, primary_key, relationship_name):

    """
    Validates foreign key relationships between two tables.
    args:
        foreign_df (DataFrame): The DataFrame containing the foreign key.
        foreign_key (str): The foreign key column name.
        primary_df (DataFrame): The DataFrame containing the primary key.
        primary_key (str): The primary key column name.
        relationship_name (str): Description of the relationship being validated.
    """

    print(f"Foreign Key Validation for: {relationship_name}")
    is_valid = foreign_df[foreign_key].isin(primary_df[primary_key]).all()
    if is_valid:
        print(f"- All values in {foreign_key} are valid keys in {primary_key}.")
    else:
        print(f"- There are invalid/missing values in {foreign_key} referencing {primary_key}.")
    print("\n")
#validate relationships for fks
validate_foreign_keys(product, "ProductSubcategoryID", product_subcategory, "ProductSubcategoryID", "Product → Product Subcategory")
validate_foreign_keys(product_subcategory, "ProductCategoryID", product_category, "ProductCategoryID", "Product Subcategory → Product Category")
validate_foreign_keys(sales_details, "SalesOrderID", sales, "SalesOrderID", "Sales Details → Sales")



#count total record
print("Count total records:")
print("\n")
print("Total Records:")
print("product:", len(product))
print("product_category:", len(product_category))
print("product_subcategory:", len(product_subcategory))
print("sales:", len(sales))
print("sales_details:", len(sales_details))
print("special_offer:", len(special_offer))


#print column names
print("\n")
print("Column Names")
print("product:", list(product.columns))
print("\n")
print("product_category:", list(product_category.columns))
print("\n")
print("product_subcategory:", list(product_subcategory.columns))
print("\n")
print("sales:", list(sales.columns))
print("\n")
print("sales_details:", list(sales_details.columns))
print("\n")
print("special_offer:", list(special_offer.columns))


#data type:
print("\n")
print("Data types for special offers:")
print("special_offer:", special_offer.dtypes)
#########################################################################################################################################################



#task 9 total quantity of sold product, most and least sold prods
total_sold = sales_details.groupby('ProductID')['OrderQty'].sum().reset_index()
total_sold = total_sold.merge(product[['ProductID', 'Name']], on='ProductID')
total_sold = total_sold.sort_values(by='OrderQty', ascending=False)

most_sold = total_sold.iloc[0]
least_sold = total_sold.iloc[-1]

print("\n")
print("Most Sold Product:", most_sold['Name'], "with quantity", most_sold['OrderQty'])
print("Least Sold Product:", least_sold['Name'], "with quantity", least_sold['OrderQty'])
print("\n")
# Most Sold Product: AWC Logo Cap with quantity 8311
# Least Sold Product: LL Touring Frame - Blue, 58 with quantity 4
#########################################################################################################################################################



#task 10 calc orders for products on spec offer
sales_on_offer = sales_details[sales_details['SpecialOfferID'] > 1]
sales_on_offer = sales_on_offer.groupby('ProductID')['SalesOrderID'].nunique().reset_index()
sales_on_offer = sales_on_offer.merge(product[['ProductID', 'Name']], on='ProductID')
sales_on_offer = sales_on_offer.sort_values(by='SalesOrderID', ascending=False)
#prod with highest sales on special offer
top_offer_product = sales_on_offer.iloc[0]
print("\n")
print("Product with Highest Sales on Offer:", top_offer_product['Name'], "with orders", top_offer_product['SalesOrderID'])
print("\n")
#Product with Highest Sales on Offer: Patch Kit/8 Patches with orders 844
#########################################################################################################################################################



#task 11 add discount sales
#add unit_discount and total_discount columns to sales_details
sales_details['unit_discount'] = sales_details['UnitPrice'] * sales_details['UnitPriceDiscount']
sales_details['total_discount'] = sales_details['unit_discount'] * sales_details['OrderQty']
print("\n")
print(sales_details[['UnitPrice', 'unit_discount', 'total_discount']].head())
print("\n")
#    UnitPrice  unit_discount  total_discount
# 0   2024.994            0.0             0.0
# 1   2024.994            0.0             0.0
# 2   2024.994            0.0             0.0
# 3   2039.994            0.0             0.0
# 4   2039.994            0.0             0.0
#########################################################################################################################################################


#task 12 fidn custmrs with most orders 
customer_orders = sales.groupby('CustomerID')['SalesOrderID'].nunique().reset_index()
max_orders = customer_orders['SalesOrderID'].max()
top_customers = customer_orders[customer_orders['SalesOrderID'] == max_orders]
print("\n")
print("Customer(s) with Most Orders:")
print(top_customers)
print("\n")
# Customer(s) with Most Orders:
#      CustomerID  SalesOrderID
# 91        11091            28
# 176       11176            28
#########################################################################################################################################################

#task 13 classify customers based on frequency and spending
#gatehr customer data
customer_data = sales.groupby('CustomerID').agg(
    frequency=('SalesOrderID', 'nunique'),
    monetary_value=('TotalDue', 'sum')
).reset_index()

#addclassifications
customer_data['frequency_class'] = customer_data['frequency'].apply(
    lambda x: 'New' if x == 1 else 'Repeated' if x <= 3 else 'Fan')
customer_data['monetary_class'] = customer_data['monetary_value'].apply(
    lambda x: 'Frugal Spender' if x < 100 else 'Medium Spender' if x < 10000 else 'High Spender')

#crate a matrix
matrix = customer_data.groupby(['frequency_class', 'monetary_class']).size().unstack(fill_value=0)
print(matrix)
# monetary_class   Frugal Spender  High Spender  Medium Spender
# frequency_class
# Fan                           3           499             291
# New                        6633             0            5016
# Repeated                    724             6            5947
#########################################################################################################################################################

#task14 Create a piece of code that returns all product categories, total sales amount, total discounted
#amount, and total number of orders per category
#gather data by product category
category_sales = sales_details.merge(product[['ProductID', 'ProductSubcategoryID']], on='ProductID')
category_sales = category_sales.merge(product_subcategory[['ProductSubcategoryID', 'ProductCategoryID']], on='ProductSubcategoryID')
category_sales = category_sales.merge(product_category[['ProductCategoryID', 'Name']], on='ProductCategoryID')

category_summary = category_sales.groupby('Name').agg(
    total_sales=('LineTotal', 'sum'),
    total_discount=('total_discount', 'sum'),
    total_orders=('SalesOrderID', 'nunique')
).reset_index()

print("\n")
print("Category with Highest Sales:")
print(category_summary.sort_values(by='total_sales', ascending=False).head(1))
print("Category with Highest Orders:")
print(category_summary.sort_values(by='total_orders', ascending=False).head(1))
print("\n")
# Category with Highest Sales:
#     Name   total_sales  total_discount  total_orders
# 1  Bikes  9.465117e+07   494640.647169         18368
# Category with Highest Orders:
#           Name   total_sales  total_discount  total_orders
# 0  Accessories  1.272073e+06     6688.028574         19524
#########################################################################################################################################################


#task 15  Mr. Smith
#KPIS ill choose -> 
# KPI1 - Total revenue by year - Reason behind my choise: to show yearly revenue trends to identify growth or decline over time.
# KPi2 - Top Selling product- Reason behind my choise:to find the product with the highest quantity sold to focus marketing efforts or inventory.
# Kpi3 - most profitable category of products - Reason behind my choise: to determine the product category generating the highest revenue

#KPI1
sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])
sales['Year'] = sales['OrderDate'].dt.year
yearly_revenue = sales.groupby('Year')['SubTotal'].sum().reset_index()
print("KPI1 - Yearly revenue:  ", yearly_revenue)
print("\n")
#KPI2
total_sold = sales_details.groupby('ProductID')['OrderQty'].sum().reset_index()
total_sold = total_sold.merge(product[['ProductID', 'Name']], on='ProductID')
top_product = total_sold.sort_values(by='OrderQty', ascending=False).iloc[0]
print("KPI2 - Top-Selling Product:  ", top_product['Name'], "with", top_product['OrderQty'], "units sold.")
print("\n")
#KPI3
category_sales = sales_details.merge(product[['ProductID', 'ProductSubcategoryID']], on='ProductID')
category_sales = category_sales.merge(product_subcategory[['ProductSubcategoryID', 'ProductCategoryID']], on='ProductSubcategoryID')
category_sales = category_sales.merge(product_category[['ProductCategoryID', 'Name']], on='ProductCategoryID')
category_revenue = category_sales.groupby('Name')['LineTotal'].sum().reset_index()
top_category = category_revenue.sort_values(by='LineTotal', ascending=False).iloc[0]
print("KPI3 - Most Profitable Category:  ", top_category['Name'], "with revenue of", top_category['LineTotal'])
print("\n")


#Exporting key points of interest info for client
kpi_data = {
    'KPI': [
        ' 1 - Total Revenue by Year',
        ' 2 - Top-Selling Product',
        ' 3 - Most Profitable Category'
    ],
    'Value': [
        '2005: 11,331,810.00 | 2006: 30,674,770.00 | 2007: 42,011,040.00 | 2008: 25,828,760.00',
        'AWC Logo Cap (8,311 units sold)',
        'Bikes (94,651,172.70 revenue)'
    ]
}
#########################################################################################################################################################


# Create a DataFrame
kpi_df = pd.DataFrame(kpi_data)

#save as xlsx in current dir
print("Current Directory:", os.getcwd())

file_path = os.path.join(os.getcwd(), "Insights.xlsx")
kpi_df.to_excel(file_path, index=False)
print("KPI report successfully saved to:", file_path)
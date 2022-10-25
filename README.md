# ImmoELiza - FullProject
## API to predict the price of real estate sales in Belgium.

Project created in the Bootcamp AI Operator at BeCode. October - 2022

The project in 4 steps: (1) Scraping data from the immoweb.com website, (2) clean data and exploratory analysis, (3) explore machine learning models to select the best performance and finally (4) deploy the API in docker render.


1.	Collecting Data

Dataset gathering information about at least 10.000 properties all over Belgium.

Libraries: BeautifulSoup, Selenium and Pandas 

The dataset have following infos:
•	Locality
•	Type of property (House/apartment)
•	Price
•	Number of rooms
•	Area
•	Fully equipped kitchen (Yes/No)
•	Furnished (Yes/No)
•	Open fire (Yes/No)
•	Terrace (and terrace surface)
•	Garden (and garden surface)
•	Surface of the land
•	Number of facades
•	Swimming pool (Yes/No)
•	State of the building (New, to be renovated, ...)

2.	Data Cleaning and exploratory analysis

Step 1 : Data Cleaning

A dataset that doesn't contain any duplicates, blank spaces or error-free. No duplicates
Extra: a dataset with latitude and longitude was collected and merged into the main database to have a more accurate model.

Step 2 : Exploratory Data Analysis

On this step the following points were explored with vizualization when appropriate:
•	Structure of the data (rows and columns)
•	Correlation between the variables to each other and to price.
•	Which variables have the greatest and least influence on the price.
•	Percentage of missing values per column and resolve this problem

Libraries:  matplotlib, seaborn, plotly, pandas, numpy

3.	Machine Learning Models

Machine learning models to predict prices on Belgium's real estate sales.
With the dataset that was previously scraped, preprocessed and analyzed, preprocess the data to be used with machine learning. Handle NANs, handle categorical data, select features and remove features that have too strong correlation.

Step 1 : Data formatting

Dataset was divided for training and testing. (X_train, y_train, X_test, y_test) to apply the models, and to try a better performance the dataset was also divided with only Houses or Apartments.

Step 2: Model evaluation

The following algorithms were tested: Random Forest Regression (0.82), Gradient Boosting Regressor (0.81), Decision Tree (0.66), Support Vector Regressor (0.52), Lasso model (0.44), Ridge Model (0.44), Bayesian Model (0.44), Elastic Net model (0.44), Multiple Linear Regression (0.37) and Suport Vector Machine Model (0.035).

Random forest Regression and the Gradient Boosting Regressor are the models with best Scores. Gradient Boosting Regressor was chosen to be used in the API.

4.	API deployment

Deploy an API to Render with Docker that web-developers could create a website around it. Get data in JSON format and to return the data in the same format and provide an error if something went wrong.

Step 1: Create a API to process the input and output data

This module contains all the code to preprocess the data and the ML model to predict the price of a house, a route with GET request and return "alive" if the server is alive and a route with POST request that receives the data of a house in JSON format.

Input
{
  "data": {
    "area": int,
    "property_type": "apartment" | "house" | "others",
    "rooms_number": int,
    "zip_code": int,
    "land_area": int | None,
    "garden": bool | None,
    "garden_area": int | None,
    "equipped_kitchen": bool | None,
    "full_address": str | None,
    "swimming_pool": bool | None,
    "furnished": bool | None,
    "open_fire": bool | None,
    "terrace": bool | None,
    "terrace_area": int | None,
    "facades_number": int | None,
    "building_state": "new" | "good" | "to renovate" | "just renovated" | "to rebuild" | none
    ]
  }
}
Output
{
  "prediction": float | None,
  "status_code": int | None
}

Step 2: Create a Dockerfile to wrap your API and deploy your Docker image in Render.com



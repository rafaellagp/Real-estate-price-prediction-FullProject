API deployment

Deploy an API to Render with Docker that web-developers could create a website around it. Get data in JSON format and to return the data in the same format and provide an error if something went wrong.

Step 1: Create a API to process the input and output data

This module contains all the code to preprocess the data and the ML model to predict the price of a house, a route with GET request and return "alive" if the server is alive and a route with POST request that receives the data of a house in JSON format.

Input { "data": { "area": int, "property_type": "apartment" | "house" | "others", "rooms_number": int, "zip_code": int, "land_area": int | None, "garden": bool | None, "garden_area": int | None, "equipped_kitchen": bool | None, "full_address": str | None, "swimming_pool": bool | None, "furnished": bool | None, "open_fire": bool | None, "terrace": bool | None, "terrace_area": int | None, "facades_number": int | None, "building_state": "new" | "good" | "to renovate" | "just renovated" | "to rebuild" | none ] } } Output { "prediction": float | None, "status_code": int | None }

Step 2: Create a Dockerfile to wrap your API and deploy your Docker image in Render.com


libraries: 

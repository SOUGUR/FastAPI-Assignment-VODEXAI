**FastAPI Project**
Table of Contents
1. Overview
2. Prerequisites
3. Setup and Installation
4. Running the Project Locally
5. Endpoints
6. Items Endpoints
7. Clock-in Records Endpoints

1. Overview
This FastAPI project provides a RESTful API for managing items and clock-in records. It allows users to create, read, update, and delete that is perform CRUD operations
on the items and clock-in records hosted on Mongo DB database and also filtering data based on specific criteria.

2. Prerequisites
Before you begin, ensure you have the following installed on your machine:
Python 3.7 or higher
pip (Python package installer)
MongoDB atlas account (for data storage and database connection)

3. Setup and Installation
   
3.1 Clone the Repository
git clone <repository-url>
cd <project-directory>

3.2 Create a Virtual Environment
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`

3.3 Install Dependencies
pip install -r requirements.txt

3.4 Start MongoDB Ensure your MongoDB service is running. You can do this using:
mongod

4. Running the Project Locally
4.1 Run the FastAPI Application using:
uvicorn fast_api_assigmnet.main:app --reload
The --reload flag will automatically reload the server when you make changes to the code.

4.2 Access the API Open your web browser and go to http://127.0.0.1:8000/docs to view the automatically generated API documentation and test the endpoints.

5. Endpoints
5.1 Items Endpoints
   
5.1.a Create Item: POST /items/
Description: Creates a new item.
Request Body:
json
Copy code
{
  "_id": 1,
  "name": "Sample Name",
  "email": "example@example.com",
  "item_name": "Sample Item",
  "quantity": 10,
  "expiry_date": "2024-12-31"
  "insert_date": "2024-10-11"
}
you can omit or leave the insert_date field as it is with current date.

5.1.b Get Item by ID: GET /items/{id}
Description: Retrieves an item by its ID.
Path Parameter: id (integer)

5.1.c Update Item: PUT /items/{id}
Description: Updates an existing item. Only fields that you provide in the request will be updated.
Request Body:
json
Copy code
{
  "email": "newemail@example.com"
}

5.1.d Delete Item: DELETE /items/{id}
Description: Deletes an item by its ID.
Path Parameter: id (integer)

5.1.e Filter Items: GET /items/filter
Description: Filters items based on optional query parameters.
Query Parameters:
email (string, optional)
expiry_date (date, optional, format: YYYY-MM-DD)
quantity (integer, optional)

5.1.f Aggregate Items: GET /items/aggregate
Description: Aggregates items by email.

5.2 Clock-in Records Endpoints
5.2.a Create Clock-in Record: POST /clock-in
Description: Creates a new clock-in record.
Request Body:
json
Copy code
{
  "email": "example@example.com",
  "location": "Office"
}

5.2.b Get Clock-in Record by ID: GET /clock-in/{id}
Description: Retrieves a clock-in record by its ID.
Path Parameter: id (integer)

5.2.c Update Clock-in Record: PUT /clock-in/{id}
Description: Updates an existing clock-in record. Only fields provided in the request will be updated.
Request Body:
json
Copy code
{
  "location": "US"
}

5.2.d Delete Clock-in Record: DELETE /clock-in/{id}
Description: Deletes a clock-in record by its ID.
Path Parameter: id (integer)
Filter Clock-in Records: GET /clock-in/filter

Description: Filters clock-in records based on optional query parameters.
Query Parameters:
email (string, optional)
location (string, optional)

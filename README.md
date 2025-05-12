# Project Title

RESTful Movies API

=================

## Author

by <sp223kz@student.lnu.se>

## Implementation type

REST API

## Links

- Github repository [https://github.com/SabrinaPL/rest-api/]
- RESTful Movies API [https://rest-api-design-a17625cba941.herokuapp.com/api/v1/]
- RESTful Movies API documentation [https://rest-api-design-a17625cba941.herokuapp.com/apidocs/]

## Description

This RESTful Movies API provides access to a movie database, allowing users to retrieve and manage movie, actor, and ratings information. The API also provides aggregated and computed data that can be used for data analysis and to visualize gender distribution based on movie production country, production company, movie genre, department and production year. The main features include:

    Movies Management: Fetch all movies, retrieve a specific movie by ID, and delete movies by ID (with JWT authentication).

    Actors and Credits: Get a list of all actors, fetch actors associated with a specific movie, and manage actor-related information.

    HATEOAS Links: Each response includes relevant navigation links for related resources, like movies, ratings, and credits.

    JWT Authentication & User Management: Register and delete users, with JWT authentication for secure actions like deleting user and movies.

    Data analysis: The API provides endpoints for data analysis and visualization of gender distribution based on movie production country, production company, movie genre, department and production year.

The API supports pagination and structured data, ensuring easy integration with movie-related applications.

## Technologies Used

Python
Flask
MongoEngine
MongoDB
Docker

## Local Installation Instructions

### Clone the Repository:

        Clone the repository from GitHub:

    git clone https://github.com/SabrinaPL/rest-api/

### Navigate to the Project Directory:

    Change directory into the cloned repository:

    cd <repository-directory>

### Set Up the Python Environment:

    Ensure you have Python 3.8+ installed. Then, create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # For Windows, use: venv\Scripts\activate

### Install Dependencies:

    Install required dependencies from requirements.txt:

    pip install -r requirements.txt

### Configure Environment Variables:

    Create a .env file in the project root directory and set the following variables:

        PORT=
        FLASK_ENV=development
        MONGO_HOST=localhost:
        MONGO_PORT=
        MONGO_DB=DBName
        MONGO_USER=username
        MONGO_PASS=password
        JWT_SECRET_KEY=
        JWT_ACCESS_TOKEN_EXPIRES=3600
        JWT_REFRESH_TOKEN_EXPIRES=604800
        JWT_COOKIE_SECURE=False
        HEROKU_APP_NAME=rest-api-design

### Testing the API with Postman

    Step 1:
    Download the Postman collection from: https://github.com/SabrinaPL/rest-api/blob/master/tests/postman/RESTful%20MOVIE%20API.postman_collection.json

    Step 2:
    Open Postman and import the collection to your workspace.

    Step 3:
    Select the downloaded Postman collection .json file and click on "Import".

    Step 4:
    Select the imported collection from the left sidebar.

    Step 5:
    Navigate to Runs and click on "Run" to execute the collection.

### CI/CD Pipeline

    The CI/CD pipeline is set up to automatically deploy the application to Heroku whenever changes are pushed to the main branch. The pipeline includes steps for building, testing and deploying the application.

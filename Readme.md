# Weather API with fastAPI.
There are 3 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/docs`

# Project Setup and Installation.
1. Clone the git repository.
2. Create and activate a virtual environment using the below commands:-
```bash
  python -m venv env
  source env/bin/activate #(For Mac and Linux)
  env\Scripts\activate #(For Windows)
```


3. Run the below command to install the required packages:-
```bash 
  pip install -r requirements.txt
  ```
4. Move to project directory using below command:-
```bash
cd weather_application
```

# Database Setup and Installation.
1. Download and Install PostgreSQL in your computer using this link `https://www.postgresql.org/download/`.
2. Create a database using below command:-
```bash
CREATE DATABASE database_name;
```

# Setup environment variables.
Create a .env file and store your database credentials in below format:-
```bash
USERNAME='name_of_db'
PASSWORD='password_of_db'
DB_HOST='host_of_db'
DB_PORT='port_number_of_db'
DB_NAME='name_of_db'
TESTING_DATABASE_URL='f"postgresql://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"'
 ```

# Run project.

1. Do data ingestion for the given data.
```bash
python ingest.py
```

2. Run the below command to load the data and run the project:-
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 
```
![Alt text](static/server.png?raw=true "weather")


#### This step will take few minutes as it will dump the data in the initial setup.

# To access the API endpoints:
```bash
/api/weather/  #for weather records
/api/weather/stats/  #for weather stats
/docs #for swagger documentation
```
# Testing.
To run the testcases use this command:-
```bash
pytest
```

### For Code Coverage you can refer to this command
```bash
pytest --cov
```
![Alt text](static/pytestcov.png?raw=true "weather")

# Screenshots of Postman Collection

![Alt text](static/postman1.png?raw=true "weather")

<br><br>
![Alt text](static/postman2.png?raw=true "weather")

<br><br>
![Alt text](static/swagger2.png?raw=true "weather")

# AWS Deployment Approach
#### Please refer to aws_approach.md for more elaboration
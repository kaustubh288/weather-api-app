# AWS Approach

# Tools used:
```
AWS Lambda
AWS S3
AWS Aurora Serverless
AWS API Gateway
```
## Use case:
```
AWS Lambda:
Utilize Lambda for implementing data ingestion process, access fastapi endpoints and process input files and finally store data into output database.   

AWS S3:
Utilize AWS S3 for storing input text files.

AWS Aurora Serverless:
Utilize AWS Aurora (Postgresql DB) for storing processed output obtained from Lambda.

AWS API Gateway:
Utilize Amazon API Gateway for accessing fastapi application endpoints.
```
# Approach for deploying application:

## Step 1: Install Dependencies:
In your terminal, navigate to the project directory and install the add-on required dependencies for AWS Deployment:

```
pip install fastapi-lambda
```

## Step 2: Create a Lambda Function Handler:
Create a file named lambda_weather_app.py in your project directory with content:

```
from app import app
from fastapi_lambda import FastAPILambda, api

api = FastAPILambda(app)
handler = api.handler
```

## Step 3: Bundle our application:
Create a ZIP package of all files used.

## Step 4: Create an AWS Lambda Function in AWS:
Go to the AWS Lambda console.
Click "Create function."
Choose "Author from scratch."
Create a function by giving any name for lambda function, select appropriate runtime (Python 3.8+).

## Step 5: Upload ZIP File to Lambda:
Upload Zip file to AWS Lambda service.

## Step 6: Configure Handler Function:
Go to "Function code" section and set the "Handler" to lambda_weather_app.handler .

## Step 7: Configure and Deploy API Gateway:
Configure API Gateway in Lambda, select "API Gateway" as trigger, and set settings. In API Gateway console, deploy API, choose or create a stage. 

Finally, Access FastAPI app via provided endpoint urls.


## Data Ingestion and Data Processing:
1. Create S3 to store input files and Aurora serverless Postgres DB.
2. Configure S3 event notification to trigger lambda function(ingest.py) to trigger this function whenever input files are uploaded to S3 bucket.
3. The Lambda function will process the input data files and generate the desired output into Aurora DB.
4. This ensures the data ingestion occurs in real time and avoids stale data.
5. If we need scheduled data ingestion process:
    1. We can use a CRON job based mechanism which ensures data is loaded at desired intervals.
   2. The drawback of the CRON job could be: if the difference between two jobs is large enough we may get stale data.

## Optimization:
1. Since CRON job can lead to stale data we can opt for real time data ingestion process.
2. When dealing with huge amount of data during the data processing during ingestion process, we can opt AWS Glue Service for faster processing of data.
3. We should use AWS Cognito for Authenticated and authorized API calls for data ingestion.
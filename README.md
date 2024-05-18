# steel-plant industry-Load-Prediction-

A brief description of what this project does and who it's for


## Problem Statement
"Develop a predictive model to forecast energy consumption load for an industry based on historical data including date, industry energy consumption, reactive power, CO2 levels, time of day, week status, day of the week, and load type. The model aims to predict load variations for different load types (light, medium, maximum) and provide insights for optimizing electricity usage."

## Aim
"The aim is to develop a predictive model that accurately forecasts the energy consumption load of an industry, considering various factors such as date, reactive power, CO2 levels, and load type. This model will enable better management and optimization of electricity usage, ultimately leading to improved efficiency and cost savings."


## Dataset Attributes :

Content
This company produces several types of coils, steel plates, and iron plates. The information on electricity consumption is held in a cloud-based system. The information on energy consumption of the industry is stored on the website of the Korea Electric Power Corporation (pccs.kepco.go.kr), and the perspectives on daily, monthly, and annual data are calculated and shown.

## Attribute Information:
Date Continuous-time data taken on the first of the month
Usage_kWh Industry Energy Consumption Continuous kWh
Lagging Current reactive power Continuous kVarh
Leading Current reactive power Continuous kVarh
CO2 Continuous ppm
NSM Number of Seconds from midnight Continuous S
Week status Categorical (Weekend (0) or a Weekday(1))
Day of week Categorical Sunday, Monday : Saturday
Load Type Categorical Light Load, Medium Load, Maximum Load


## Approach

## DVC (Data Version Control):
DVC is a version control system for data and machine learning models. It helps track changes to data, pipelines, and models, facilitating reproducibility and collaboration in ML projects. DVC uses Git-like commands to manage data and integrates with Git for versioning.

## Evidently AI:
Evidently AI is a tool for monitoring machine learning models. It provides insights into model performance, data drift, feature importance, and other metrics crucial for maintaining model health over time. It generates reports comparing current and reference data, helping detect issues and assess model stability.

## Data Life Cycle Stages for Steel Plant Load Prediction:

## Data Ingestion:
Data ingestion involves downloading and unzipping the steel plant dataset from a specified URL. The data is saved locally and extracted into the artifacts/data_ingestion directory for further processing.

## Data Validation:
Data validation checks the ingested data against a schema defined in schema.yaml. It ensures all expected columns are present in the dataset. Validation status is stored in artifacts/data_validation/status.txt.

## Data Transformation:
Data transformation involves preprocessing the validated dataset for model training. It includes renaming columns, oversampling to handle class imbalance, and feature engineering. Processed data is stored in artifacts/data_transformation.

## Model Training:
Model training uses the transformed data to train a machine learning model, specifically an Extra Trees Classifier. The trained model is evaluated on training and test sets, and various metrics such as accuracy, precision, recall, and F1-score are computed. The trained model and evaluation results are saved in artifacts/model_trainer.

## Evidently AI Model Monitoring:
Evidently AI is used to monitor the trained Extra Trees Classifier model. It compares model predictions and key metrics between the training and test sets to detect any data drift or model degradation. Reports including data drift, classification performance, data quality, and target drift are generated and saved in artifacts/model_trainer.



## Prediction pipeline:
Input data is passed through the loaded model to generate predictions. Predicted outputs are logged, and the results are returned.

## Airflow DAG for Single Value Prediction:
An Airflow DAG automates the execution of the training pipeline on a weekly basis. It consists of the following tasks:

Data Ingestion: Downloads and extracts the dataset.
Data Validation: Validates the ingested data against a schema.
Data Transformation: Prepares the data for model training.
Model Training: Trains an Extra Trees Classifier model.
Scheduling: The DAG is scheduled to run weekly, starting from a specified date.
Docker Configuration:
The project is containerized using Docker for portability and reproducibility.

Base Image: Uses apache/airflow:2.8.3 and python:3.8.
Application Setup: Copies all necessary files into the container and sets the working directory to /app.
Dependencies: Installs Python dependencies from requirements.txt.
Execution: Configures Airflow tasks and sets up the DAG for execution.
This setup ensures the ML pipeline's scalability, reproducibility, and scheduled periodic training and deployment.


# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/mahendra867/End-to-End-sentimental-analysis-with-NLP.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n mlproj python=3.8 -y
```

```bash
conda activate mlproj
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up you local host and port
```






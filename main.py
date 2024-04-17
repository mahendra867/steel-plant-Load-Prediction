from src.PROJECTML import logger # although i have src folder when you click the explorar we can see that src but iam directly calling this mlproject_with_mlflow because i have initlizied my login functionality inside the __init__.py constructor thats why i dont need to call this src seperatly  you can call src folder by like this from src.mlproject_with_mlflow import logger , but if we want to ingore a folder like this to import that src folder , we can mention that inside the __init__.py constructor to ignore of calling the src folder 
from src.PROJECTML.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.PROJECTML.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from src.PROJECTML.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.PROJECTML.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
import  pandas as pd

STAGE_NAME = "Data Ingestion stage" 
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") # my data ingestion is started
    obj = DataIngestionTrainingPipeline() # here iam initilizing this DataIngestionTrainingPipeline()
    obj.main() # here iam calling this main
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x") # then iam telling that this data ingestion stage is successfully running completed 
except Exception as e:  # if there are any errors found this will get rise 
    logger.exception(e)
    raise e




# now here in main.py iam defining the data_validation stage name 
STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataValidationTrainingPipeline() # logging is started calling the class DataValidationTrainingPipeline
    obj.main() # here calling this main method from this class
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:  # if anything error in this code then we are telling this part of code to raise exception
    logger.exception(e)
    raise e



STAGE_NAME = "Data Transformation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataTransformationTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e





STAGE_NAME = "Model Trainer stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = ModelTrainerTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


# Set display options to show all rows and columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

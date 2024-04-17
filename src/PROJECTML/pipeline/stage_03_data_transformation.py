from PROJECTML.config.configuration import ConfigurationManager
from PROJECTML.components.data_transformation import DataTransformation
from PROJECTML import logger
from pathlib import Path




STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f: # here iam reading the status.txt file status of data_validation
                status = f.read().split(" ")[-1]

            if status == "True":  # here if the status.txt file status found true then iam running the data_transformation pipeline
               
                config = ConfigurationManager() # here iam initlizing my ConfigurationManager
                data_transformation_config = config.get_data_transformation_config() # and here iam getting my get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config) # here iam passing my data_transformation_config it means iam calling this data_transformation_config
                data_transformation.creating_new_renamed_columns_dataset()
                data_transformation.pipeline_creation()
                data_transformation.find_constant_features()
                data_transformation.find_quasi_constant_features()
                data_transformation.perform_anova_test()
                #data_transformation.selecting_the_best_features()
                data_transformation.train_test_spliting() # here performing the train_test_split()

            else: # else if i status.txt file status shows as false iam rasing the exception
                raise Exception("You data schema is not valid")

        except Exception as e:
            print(e)





if __name__ == '__main__': # here i have initlized the main fucntion 
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
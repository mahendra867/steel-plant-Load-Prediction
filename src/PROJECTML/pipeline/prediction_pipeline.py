import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from PROJECTML import logger
from PROJECTML.utils.common import load_bin

        

class PredictionPipeline:
        def __init__(self):
            
            #self.model = joblib.load('artifacts\model_trainer\ExtraTreesClassifier_model.pkl')
            self.model = joblib.load(Path('artifacts/model_trainer/ExtraTreesClassifier_model.joblib'))
            logger.info("Model object loaded successfully: %s", self.model)

            print(self.model)
            
            

            logger.info("Model object loaded successfully")

                 
    
        def predict(self,data):
            
            prediction = self.model.predict(data)
            logger.info("Model predicted the Data")
            logger.info(f"Input data: {data}")
            logger.info(f"Predicted output: {prediction}")
            return prediction

# Set display options to show all rows and columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)



    

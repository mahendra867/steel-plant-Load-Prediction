# these packages i need in order to create my Model Trainer components 
import pandas as pd
import os
from PROJECTML import logger
import joblib # here iam saving the model because i want to save the data
from sklearn.model_selection import train_test_split
from src.PROJECTML.config.configuration import ConfigurationManager
from src.PROJECTML.components.data_transformation import DataTransformation
from sklearn.metrics import accuracy_score
import pickle
from PROJECTML.entity.config_entity import ModelTrainerConfig
from lightgbm import LGBMClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.ensemble import  ExtraTreesClassifier
from pathlib import Path
# these packages i need in order to create my Model Trainer components 




class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def train(self):
        self.train_data = pd.read_csv(self.config.train_data_path)
        self.test_data = pd.read_csv(self.config.test_data_path)

        self.x_train = self.train_data.drop(columns=['Load_Type'])
        self.y_train = self.train_data['Load_Type']
        self.x_test = self.test_data.drop(columns=['Load_Type'])
        self.y_test = self.test_data['Load_Type']

    def model(self):
        clf = [
            ExtraTreesClassifier()
        ]

        scores = []

        for model in clf:
            model.fit(self.x_train, self.y_train)
            
            train_pred = model.predict(self.x_train)
            test_pred = model.predict(self.x_test)

            train_accuracy = accuracy_score(self.y_train, train_pred)
            test_accuracy = accuracy_score(self.y_test, test_pred)

            train_cm = confusion_matrix(self.y_train, train_pred)
            test_cm = confusion_matrix(self.y_test, test_pred)

            train_precision = precision_score(self.y_train, train_pred, average='weighted')
            test_precision = precision_score(self.y_test, test_pred, average='weighted')

            train_recall = recall_score(self.y_train, train_pred, average='weighted')
            test_recall = recall_score(self.y_test, test_pred, average='weighted')

            train_f1 = f1_score(self.y_train, train_pred, average='weighted')
            test_f1 = f1_score(self.y_test, test_pred, average='weighted')

            scores.append({
                'Model': type(model).__name__,
                'Training Accuracy': train_accuracy,
                'Testing Accuracy': test_accuracy,
                'Training Precision': train_precision,
                'Testing Precision': test_precision,
                'Training Recall': train_recall,
                'Testing Recall': test_recall,
                'Training F1-score': train_f1,
                'Testing F1-score': test_f1
            })

            print("Model:", type(model).__name__)
            print("Training Accuracy:", train_accuracy)
            print("Testing Accuracy:", test_accuracy)
            print("Training Precision:", train_precision)
            print("Testing Precision:", test_precision)
            print("Training Recall:", train_recall)
            print("Testing Recall:", test_recall)
            print("Training F1-score:", train_f1)
            print("Testing F1-score:", test_f1)

            joblib.dump(model, os.path.join(self.config.root_dir, f"{type(model).__name__}_model.joblib"))


                # Load the trained model  and test model 
            model = joblib.load("artifacts\model_trainer\ExtraTreesClassifier_model.joblib")  # Replace "path_to_saved_model.pkl" with the actual path

            #self.preprocessor = joblib.load('artifacts\data_transformation\categorical_preprocessor_obj.joblib')
            # Prepare input data for prediction (a single sample row)
            # Replace the feature values with the values of your unseen test data
            single_sample = {
            'Usage_kWh': 104.62,
            'Lagging_Reactive_Power_kVarh': 34.96,
            'Leading_Reactive_Power_kVarh': 0,
            'CO2': 0.18,
            'Lagging_Power_Factor': 0.05,
            'Leading_Power_Factor': 100,
            'NSM': 63000,
            'WeekStatus_Weekday': 1,
            'WeekStatus_Weekend': 0,
            'hour': 17
            
        }
                    
        #8.46,0,25.92,0,100,31.03,45000,Weekday,Tuesday,Medium_Load

        #40.25,8.82,0.5,0,97.68,99.99,67500,Weekday,Tuesday,Maximum_Load

        # Convert the dictionary to a DataFrame
        input_data = pd.DataFrame([single_sample])
        input_data.info()
        input_data.shape
        #preprocessed_input_data = self.preprocessor.transform(input_data)

        # Ensure that the columns of input_data match the order of features used during training
        # You might need to rearrange the columns or add missing columns
        input_data = input_data[self.x_train.columns]
        print(input_data)

        # Perform prediction
        prediction = model.predict(input_data)

        print("Predicted class label:", prediction)


        return pd.DataFrame(scores)

    

    def overall_score(self,score):

        print(score)







# these packages i need in order to create my Model Trainer components 
import pandas as pd
import os
from PROJECTML import logger
import joblib # here iam saving the model because i want to save the data
from sklearn.model_selection import train_test_split
from PROJECTML.config.configuration import ConfigurationManager
from PROJECTML.components.data_transformation import DataTransformation
from sklearn.metrics import accuracy_score
import pickle
from PROJECTML.entity.config_entity import ModelTrainerConfig
#from lightgbm import LGBMClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.ensemble import  ExtraTreesClassifier
from pathlib import Path
# these packages i need in order to create my Model Trainer components 


# imported necessary libraries for model monitoring with evidently ai
import pandas as pd
import numpy as np
import requests
import zipfile
import io

import evidently
from datetime import datetime, time
from sklearn import datasets, ensemble
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset import DataQualityPreset
from evidently.metric_preset import TargetDriftPreset
from evidently.metric_preset import ClassificationPreset



class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def train(self):
        self.train_data = pd.read_csv(self.config.train_data_path)
        self.test_data = pd.read_csv(self.config.test_data_path)

        self.x_train = self.train_data.drop(columns=['Load_Type'])
        print(f'this is the self.x_train dataset {self.x_train.columns}')
        self.y_train = self.train_data['Load_Type']
        self.x_test = self.test_data.drop(columns=['Load_Type'])
        self.y_test = self.test_data['Load_Type']

    # model monitering by evidently ai open source tool
    def model_monitering(self):  
        
        self.target = 'Load_Type'   # target variable # Recording the prediction values so for that i have create a  column name prediction
        # Reference data means historical data we train the model ,Current data means upcoming or new data that we are going to train the model
        # All features are numerical (assuming this is correct)
        self.prediction = 'prediction'  
        
        self.numerical_features = ['WeekStatus_Weekday', 'WeekStatus_Weekend', 'Usage_kWh',
                                  'Lagging_Reactive_Power_kVarh', 'Leading_Reactive_Power_kVarh',
                                  'CO2', 'Lagging_Power_Factor', 'Leading_Power_Factor', 'NSM', 'hour']

        self.model = ExtraTreesClassifier()
        self.model.fit(self.x_train, self.y_train)

        self.train_data['prediction'] = self.model.predict(self.x_train) # iam considering this self.train_data as historical data or reference data 
        self.test_data['prediction'] = self.model.predict(self.x_test)   # iam considering this self.test_data as upcoming data or current new data to compare performance with reference 

        self.train_pred=self.train_data['prediction']
        self.test_pred=self.test_data['prediction']



        column_mapping = ColumnMapping()
        column_mapping.target = self.target
        column_mapping.prediction = self.prediction
        column_mapping.numerical_features = self.numerical_features


        data_drift_report = Report(metrics=[
            DataDriftPreset(),
        ])

        classification_performance_report = Report(metrics=[
            ClassificationPreset(),
        ])


        multiclass_cat_target_drift_report = Report(metrics=[
            TargetDriftPreset(),
        ])

        data_quality_report = Report(metrics=[
            DataQualityPreset(),
        ])

        classification_performance_report.run(reference_data=self.train_data, current_data=self.test_data, column_mapping=column_mapping)  
        data_drift_report.run(current_data=self.test_data, reference_data=self.train_data, column_mapping=None)
        data_quality_report.run(current_data=self.test_data, reference_data=self.train_data, column_mapping=None)
        multiclass_cat_target_drift_report.run(current_data=self.test_data, reference_data=self.train_data, column_mapping=None)

        data_drift_report.save_html(os.path.join(self.config.root_dir, "data_drift_file.html"))
        classification_performance_report.save_html(os.path.join(self.config.root_dir, "Classification_report.html"))
        data_quality_report.save_html(os.path.join(self.config.root_dir, "Data_quality_report.html"))
        multiclass_cat_target_drift_report.save_html(os.path.join(self.config.root_dir, "target_drift_report.html"))
        
        #data_drift_report.save_html("data_drift_file.html")
        #classification_performance_report.save_html('Classification report.html')
        #data_quality_report.save_html("Data_quality_report.html")
        #multiclass_cat_target_drift_report.save_html("target_drift_report.html")

    def evaluate_model(self):  # Renamed method to evaluate_model
        model=self.model
        train_accuracy = accuracy_score(self.y_train, self.train_pred)
        test_accuracy = accuracy_score(self.y_test, self.test_pred)

        train_cm = confusion_matrix(self.y_train, self.train_pred)
        test_cm = confusion_matrix(self.y_test, self.test_pred)

        train_precision = precision_score(self.y_train, self.train_pred, average='weighted')
        test_precision = precision_score(self.y_test, self.test_pred, average='weighted')

        train_recall = recall_score(self.y_train, self.train_pred, average='weighted')
        test_recall = recall_score(self.y_test, self.test_pred, average='weighted')

        train_f1 = f1_score(self.y_train, self.train_pred, average='weighted')
        test_f1 = f1_score(self.y_test, self.test_pred, average='weighted')

        scores={
                'Model': type(model).__name__,
                'Training Accuracy': train_accuracy,
                'Testing Accuracy': test_accuracy,
                'Training Precision': train_precision,
                'Testing Precision': test_precision,
                'Training Recall': train_recall,
                'Testing Recall': test_recall,
                'Training F1-score': train_f1,
                'Testing F1-score': test_f1
                }

        for metric, value in scores.items():
            print(f"{metric}: {value}")

        joblib.dump(model, os.path.join(self.config.root_dir, f"{type(model).__name__}_model.joblib"))

        model = joblib.load("artifacts\model_trainer\ExtraTreesClassifier_model.joblib")  

        single_sample = {
            'Usage_kWh': 8.46,
            'Lagging_Reactive_Power_kVarh': 0,
            'Leading_Reactive_Power_kVarh': 25.92,
            'CO2': 0,
            'Lagging_Power_Factor': 100,
            'Leading_Power_Factor': 31.03,
            'NSM': 45000,
            'WeekStatus_Weekday': 1,
            'WeekStatus_Weekend': 0,
            'hour': 20
        }
                    
        input_data = pd.DataFrame([single_sample])
        input_data = input_data[self.x_train.columns]

        prediction = model.predict(input_data)

        print("Predicted class label:", prediction)

        return pd.DataFrame(scores, index=[0])

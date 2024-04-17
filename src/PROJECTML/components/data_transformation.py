import os
from PROJECTML import logger
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.preprocessing import OrdinalEncoder

import numpy as np
from sklearn.compose import make_column_transformer
from PROJECTML.config.configuration import DataTransformationConfig
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler

from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import OneHotEncoder








# here i defined the component of DataTransformationConfig below
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        

    def creating_new_renamed_columns_dataset(self):
        self.dataset=self.config.data_path
        self.new_data=pd.read_csv(self.dataset)
        logger.info("loaded the dataset successfully")
        #Rename some columns
        self.new_data= self.new_data.rename(columns={'Lagging_Current_Reactive.Power_kVarh': 'Lagging_Reactive_Power_kVarh',
                                'Leading_Current_Reactive_Power_kVarh': 'Leading_Reactive_Power_kVarh',
                                'Lagging_Current_Power_Factor': 'Lagging_Power_Factor',
                                'Leading_Current_Power_Factor': 'Leading_Power_Factor',
                                'CO2(tCO2)':'CO2'})
        logger.info("renamed the dataset columns successfully")


        # Assuming self.new_data is your DataFrame containing the target feature column 'Load_Type'

        # Define the oversampler
        oversampler = RandomOverSampler(random_state=42)

        # Separate features and target
        X = self.new_data.drop(columns=['Load_Type'])  # Features
        y = self.new_data['Load_Type']  # Target

        # Perform random oversampling
        X_resampled, y_resampled = oversampler.fit_resample(X, y)

        # Convert back to DataFrame if needed
        self.new_data = pd.DataFrame(X_resampled, columns=X.columns)
        self.new_data['Load_Type'] = y_resampled

        # Check the distribution after oversampling
        print(self.new_data['Load_Type'].value_counts())
        print(self.new_data.head())


        #self.new_data.to_csv(os.path.join(self.config.root_dir, "renamed_columns_dataset.csv"),index = False)
        
        self.new_data.head()
        self.new_data['date'] = pd.to_datetime(self.new_data['date'], format='%d/%m/%Y %H:%M')
        #self.new_data['date_year'] = self.new_data['date'].dt.year  # iam dropping it because it is a constant feature 
        #self.new_data['date_month_no'] = self.new_data['date'].dt.month # iam dropping this feature because annova test suggested me to give the least for this feature because it got very less value of annova test
        #self.new_data['date_day'] = self.new_data['date'].dt.day # same applies here
        self.new_data['hour'] = self.new_data['date'].dt.hour
        #self.new_data['min'] = self.new_data['date'].dt.minute  # same applies here 
        self.new_data.drop(columns='date', inplace=True)# we got extract the imp features from this date so thatsy iam dropping this date column]
        self.new_data.drop(columns='Day_of_week', inplace=True) # iam removing this i already performed the annova test there it suggest me to not select this feature based on statistical measure thatsy iam dropping this feature
        self.new_data.info()
        

    def pipeline_creation(self):
        self.new_data1 = self.new_data.copy()
        self.new_data1.drop(columns='Load_Type', inplace=True)

        # Numerical columns
        numerical_columns = self.new_data1.select_dtypes(include=[np.number]).columns.tolist()

        # Categorical columns
        categorical_columns = ['WeekStatus']

        # Apply One-Hot Encoding for categorical columns
        categorical_pipeline = make_column_transformer(
            (OneHotEncoder(), categorical_columns),
            remainder='passthrough'
        )

        # Fit and transform the categorical pipeline
        X_transformed = categorical_pipeline.fit_transform(self.new_data1)

        # Save the preprocessor object for categorical features
        joblib.dump(categorical_pipeline, os.path.join(self.config.root_dir, "categorical_preprocessor_obj.joblib"))

        # Label encode the target variable
        le = LabelEncoder()
        self.new_data['Load_Type'] = le.fit_transform(self.new_data['Load_Type'])

        # Save the label encoder object for the target variable
        joblib.dump(le, os.path.join(self.config.root_dir, "label_encoder_obj.joblib"))

        # Get the feature names after one-hot encoding
        transformed_columns = categorical_pipeline.named_transformers_['onehotencoder'].get_feature_names_out(input_features=categorical_columns).tolist()

        # Combine transformed features with numerical columns
        transformed_columns += numerical_columns

        # Convert X_transformed to DataFrame
        X_transformed_df = pd.DataFrame(X_transformed, columns=transformed_columns)

        # Combine transformed features with target variable
        self.new_data = pd.concat([X_transformed_df, self.new_data['Load_Type']], axis=1)

        # Print transformed dataset info
        logger.info("Transformed Dataset Info:")
        logger.info(self.new_data.info())

        # Print shape and head of the transformed dataset
        logger.info("Shape of Transformed Dataset:")
        logger.info(self.new_data.shape)
        logger.info("Head of Transformed Dataset:")
        logger.info(self.new_data.head())



    def find_constant_features(self):
        # Assuming self.new_data is your DataFrame containing all features

        # Initialize VarianceThreshold with the threshold
        vt = VarianceThreshold(threshold=0)

        # Fit the VarianceThreshold to identify constant features
        vt.fit(self.new_data)

        # Get boolean mask of features that are not constant
        mask = vt.get_support()

        # Get the list of constant features
        constant_features = self.new_data.columns[~mask].tolist()

        # Print or log the constant features
        logger.info("Constant Features:")
        logger.info(constant_features)

        return constant_features

    def find_quasi_constant_features(self):
        # Assuming self.new_data is your DataFrame containing all features

        # Remove the constant features before identifying quasi-constant features
        self.new_data = self.new_data.drop(columns=self.find_constant_features())

        # Initialize VarianceThreshold with the threshold
        vt = VarianceThreshold(threshold=0.01)

        # Fit the VarianceThreshold to identify quasi-constant features
        vt.fit(self.new_data)

        # Get boolean mask of features that are not quasi-constant
        mask = vt.get_support()

        # Get the list of quasi-constant features
        quasi_constant_features = self.new_data.columns[~mask].tolist()

        # Print or log the quasi-constant features
        logger.info("Quasi-Constant Features:")
        logger.info(quasi_constant_features)

        return quasi_constant_features
    
    def perform_anova_test(self):
        # Assuming self.new_data is your DataFrame containing the target feature column 'Load_Type'
        # and independent numerical features

        # Select numerical columns
        numerical_columns = self.new_data.select_dtypes(include=[np.number]).columns.tolist()
        print(numerical_columns)

        # Perform ANOVA test for each numerical feature
        f_values, p_values = f_classif(self.new_data[numerical_columns], self.new_data['Load_Type'])

        # Create a DataFrame to store results
        anova_results = pd.DataFrame({'Feature': numerical_columns, 'F-value': f_values, 'p-value': p_values})

        # Sort the results based on F-values
        anova_results.sort_values(by='F-value', ascending=False, inplace=True)

        # Print or log ANOVA results
        logger.info("ANOVA Test Results:")
        logger.info(anova_results)

        return anova_results
    
    #def selecting_the_best_features(self):
    #   features_to_drop = ['date_day', 'date_month_no', 'min']
    #   self.new_data.drop(columns=features_to_drop, inplace=True)
            
        
    def train_test_spliting(self):
       
        transformed_dataset=self.new_data
        
        train, test = train_test_split(transformed_dataset,test_size=0.25,random_state=42) # this line splits the data into train_test_split

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False) # here it saves the train and test data in csv format inisde the artifacts-> transformation folder
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape) # this logs the information about that how many training and testing samples i have 
        logger.info(test.shape)

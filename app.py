from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from PROJECTML.pipeline.prediction_pipeline import PredictionPipeline
from PROJECTML import logger
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId  # Import ObjectId for handling MongoDB ObjectIds

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://Mahendra:JTx5FZA7parBernO@cluster0.klmitxd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(app.config["MONGO_URI"])

# Now iam creating database in my MongoDB
database_name='steel'
steel_database=client[database_name]

# creating a collection
collection='steel_database'

# storing the created database which is student_database in 1 file which 
steel_details_collection=steel_database[collection]

mongo = client

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET']) 
def predict_datapoint():
    if request.method == 'POST':
            #return render_template("index.html")
        try:
            WeekStatus_Weekday = int(request.form.get('WeekStatus_Weekday'))
            WeekStatus_Weekend = int(request.form.get('WeekStatus_Weekend'))
            Usage_kWh = float(request.form.get('Usage_kWh'))
            Lagging_Reactive_Power_kVarh = float(request.form.get('Lagging_Reactive_Power_kVarh'))
            Leading_Reactive_Power_kVarh = float(request.form.get('Leading_Reactive_Power_kVarh'))
            CO2 = float(request.form.get('CO2'))
            Lagging_Power_Factor = float(request.form.get('Lagging_Power_Factor'))
            Leading_Power_Factor = float(request.form.get('Leading_Power_Factor'))
            NSM = int(request.form.get('NSM'))
            hour = int(request.form.get('hour'))


            # Create a dictionary to store the data
            data = {
                'WeekStatus_Weekday': WeekStatus_Weekday,
                'WeekStatus_Weekend': WeekStatus_Weekend,
                'Usage_kWh': Usage_kWh,
                'Lagging_Reactive_Power_kVarh': Lagging_Reactive_Power_kVarh,
                'Leading_Reactive_Power_kVarh': Leading_Reactive_Power_kVarh,
                'CO2': CO2,
                'Lagging_Power_Factor': Lagging_Power_Factor,
                'Leading_Power_Factor': Leading_Power_Factor,
                'NSM': NSM,
                'hour': hour
            }

            # Insert the data into MongoDB and inserting the created document in MongoDB
            collected_data=steel_details_collection.insert_one(data) # for inserting 1 document 

            # Convert the ObjectId to a string to use it as an identifier
            object_id_str = str(collected_data.inserted_id)

            data = pd.DataFrame([data], columns=['WeekStatus_Weekday', 'WeekStatus_Weekend', 'Usage_kWh', 'Lagging_Reactive_Power_kVarh', 'Leading_Reactive_Power_kVarh', 'CO2', 'Lagging_Power_Factor', 'Leading_Power_Factor', 'NSM', 'hour'])

            logger.info("The data collected from user is %s",data)
            predict_pipeline = PredictionPipeline()
            prediction = predict_pipeline.predict(data)
            final_result = int(prediction[0])
            logger.info("The prediction is %s",prediction)
            logger.info('Made prediction and returning to result.html')


            # Save prediction along with corresponding target feature name
            predicted_column_name = 'Load_Type'  # Replace with actual target column name
            prediction_data = {'Load_Type': final_result }
            
            #steel_details_collection.update_one({'_id': collected_data(ObjectId())}, {'$set': prediction_data}, upsert=True)
            steel_details_collection.update_one({'_id': ObjectId(object_id_str)}, {'$set': prediction_data}, upsert=True)
            
            
            return render_template("result.html", final_result=final_result)
                            
            
        except Exception as e:
                print('The Exception message is: ',e)
                return 'something is wrong'

    else:
        return render_template('index.html')
    
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9092)
            

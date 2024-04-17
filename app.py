from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from PROJECTML.pipeline.prediction_pipeline import PredictionPipeline
from PROJECTML import logger

app = Flask(__name__)
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
            data=[WeekStatus_Weekday,WeekStatus_Weekend,Usage_kWh,Lagging_Reactive_Power_kVarh,Leading_Reactive_Power_kVarh,CO2,Lagging_Power_Factor,Leading_Power_Factor,NSM,hour]
            data = pd.DataFrame([data], columns=['WeekStatus_Weekday', 'WeekStatus_Weekend', 'Usage_kWh', 'Lagging_Reactive_Power_kVarh', 'Leading_Reactive_Power_kVarh', 'CO2', 'Lagging_Power_Factor', 'Leading_Power_Factor', 'NSM', 'hour'])
            logger.info("The data collected from user is %s",data)
            predict_pipeline = PredictionPipeline()
                #logger.info("The prediction is %s",prediction)
            prediction = predict_pipeline.predict(data)
            final_result = int(prediction[0])
            logger.info("The prediction is %s",prediction)
            logger.info('Made prediction and returning to result.html')
            return render_template("result.html", final_result=final_result)
                            
            
        except Exception as e:
                print('The Exception message is: ',e)
                return 'something is wrong'

    else:
        return render_template('index.html')
    
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9092)
            

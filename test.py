from src.PROJECTML import logger  # although i have src folder when you click the explorar we can see that src but iam directly calling this mlproject_with_mlflow because i have initlizied my login functionality inside the __init__.py constructor thats why i dont need to call this src seperatly  you can call src folder by like this from src.mlproject_with_mlflow import logger , but if we want to ingore a folder like this to import that src folder , we can mention that inside the __init__.py constructor to ignore of calling the src folder 


logger.info('welcome to our custom logging')


'''print(data.get_data_as_dataframe())

        dataframe = data.get_data_as_dataframe()
        logger.info("This is the data frame we passing to the model: %s", dataframe)
        logger.info('Initiated prediction')
        predict_pipeline = PredictionPipeline()
        logger.info("Done with initilizing the object to the predictionnpipeline() class")

        data = np.array(dataframe).reshape(1,9)  # Exclude target column
        #logger.info(" this is array of the user data: %s",data)
        #logger.info("Done with dataframe converted to array now iam passing that to my preprocessor and model object")
        prediction = predict_pipeline.predict(data)
        logger.info("The prediction is %s",prediction)
        logger.info("done with prediction ")
        final_result = str(int(prediction[0]))  # Convert numpy array to integer first, then to string
        logger.info('Made prediction and final result %s',final_result)
        logger.info('Made prediction and returning to result.html')
        return render_template("result.html", final_result=final_result)

logger.info('done with prediction')'''




'''class CustomData:
    def __init__(
        self,
        Usage_kWh: float,
        Lagging_Reactive_Power_kVarh: int,
        Leading_Reactive_Power_kVarh: float,
        CO2: int,
        Lagging_Power_Factor: int,
        Leading_Power_Factor: float,
        NSM: int,
        WeekStatus_Weekday: int,
        WeekStatus_Weekend: int,
        hour: int,

    ):
        

        
        self.Usage_kWh = Usage_kWh
        self.Lagging_Reactive_Power_kVarh = Lagging_Reactive_Power_kVarh
        self.Leading_Reactive_Power_kVarh = Leading_Reactive_Power_kVarh
        self.CO2 = CO2
        self.Lagging_Power_Factor = Lagging_Power_Factor
        self.Leading_Power_Factor = Leading_Power_Factor
        self.NSM = NSM
        self.WeekStatus_Weekday= WeekStatus_Weekday
        self.WeekStatus_Weekend= WeekStatus_Weekend
        self.hour= hour
        

        logger.info("user data stored inside the CustomerData class")

    def get_data_as_dataframe(self):

        #self.preprocessor = joblib.load(Path('artifacts/data_transformation/preprocessor_object_file.joblib'))
        #logger.info("This is the preprocessor pipeline: %s", self.preprocessor)

        try:
            customer_data_dict = {
                "Usage_kWh": [self.Usage_kWh],
                "Lagging_Reactive_Power_kVarh": [self.Lagging_Reactive_Power_kVarh],
                "Leading_Reactive_Power_kVarh": [self.Leading_Reactive_Power_kVarh],
                "CO2": [self.CO2],
                "Lagging_Power_Factor": [self.Lagging_Power_Factor],
                "Leading_Power_Factor": [self.Leading_Power_Factor],
                "NSM": [self.NSM],
                "WeekStatus_Weekday": [self.WeekStatus_Weekday],
                "WeekStatus_Weekend": [self.WeekStatus_Weekend],
                "hour": [self.hour]
                
            }




            self.df = pd.DataFrame(customer_data_dict)

            logger.info("Dataframe created")
            logger.info(f"user data got stored in Dataframe values: {self.df}")

            # Print input data features
            print(f"Input Data Features: {self.df}")
            

            return self.df

        except Exception as e:
            logger.error("Exception occurred in creating dataframe")
            raise e '''
'pswd=JTx5FZA7parBernO'


'''{% if final_result == '0' %}
          Based on the provided information, the analysis suggests that the load is categorized as a Light Load. A Light Load indicates minimal energy consumption and low production activity. This may correspond to periods of downtime or reduced operations, resulting in lower electricity usage and reduced strain on equipment.
        {% elif final_result == '1' %}
          Based on the provided information, the analysis suggests that the load is categorized as a Maximum Load. A Maximum Load indicates high energy consumption and peak production activity. This typically occurs during periods of high demand or intensive manufacturing processes, where the steel plant operates at full capacity to meet production targets.
        {% else %}
          Based on the provided information, the analysis suggests that the load is categorized as a Medium Load. A Medium Load signifies moderate energy consumption and production activity. This may occur during regular production cycles or when the steel plant is operating at a standard level of output, neither at minimum nor maximum capacity.
        {% endif %}'''
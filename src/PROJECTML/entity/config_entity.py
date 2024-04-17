# This is called the entity 
from dataclasses import dataclass # here i imported the dataclass from the dataclasses
from pathlib import Path  # here i imported path from pathlib

# here entity means DataIngestionConfig which it returns all the variables like root_dir,source_URL  and etc 
@dataclass(frozen=True) # here i declared the dataclass decorator
class DataIngestionConfig:  # here i have created a class and named as DataIngestionConfig ,and it is not a python class because we need to declare the self to the variables if it is a python class, it is data class  and whenever i define the configuration fucntion , this class should my return function , the below are the varaible it do return 
    root_dir: Path    # these are variable which i have declared inside the class 
    source_URL: str
    local_data_file: Path
    unzip_dir: Path




@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict # here all_Schema just read all the data and install inside the all_schema varaible as a dictionary formate



@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path  # these are variables which are present inside the config.yaml file data_transformation code part and here iam mentioning inside the entity of the class
    data_path: Path
    preprocessor_obj: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    target_column: str  # this target column is present inside the Schema.yaml file which it tells us the quality of the Wine based on the value it returns
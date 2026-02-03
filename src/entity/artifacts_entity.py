from dataclasses import dataclass 

@dataclass
class DataIngestionArtifact:
    trained_file_path: str  
    test_file_path: str     


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str 
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    
    
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
        

@dataclass
class RegressionMetricArtifact:
    r2_score: float
    mae: float
    rmse: float



@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str # The physical location of the trained brain (.pkl file)
    
    # We store two scorecards: one for data it saw, and one for data it never saw.
    train_metric_artifact: RegressionMetricArtifact
    test_metric_artifact: RegressionMetricArtifact 
    

    
    
    
    
    
    
    
    
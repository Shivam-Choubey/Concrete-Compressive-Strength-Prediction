import os, sys
from src.logging.logger import logging
from src.exception.exception import ConcreteStrengthException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

from src.entity.config_entity import (
    DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig,
)

if __name__=='__main__':
    trainingpipelineconfig = TrainingPipelineConfig()
    
    # DATA INGESTION (Raw Materials)
    dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
    data_ingestion = DataIngestion(dataingestionconfig)
    
    logging.info("Initiate the data ingestion")
    
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    
    logging.info("Data Initiation Completed")
    
    print(dataingestionartifact)
    
    data_validation_config = DataValidationConfig(trainingpipelineconfig)
    data_validation = DataValidation(dataingestionartifact, data_validation_config)
        
    logging.info("Initiate the data Validation")
    
    data_validation_artifact = data_validation.initiate_data_validation()
    
    logging.info("data Validation Completed")
    
    print(data_validation_artifact)
    
    
    
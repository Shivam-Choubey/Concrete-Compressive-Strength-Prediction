import os
import sys
import numpy as np

# Standard error handling and logging
from src.exception.exception import ConcreteStrengthException
from src.logging.logger import logging

# Artifacts (inputs from transformation) and Configs (output settings)
from src.entity.artifacts_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from src.entity.config_entity import ModelTrainerConfig

# Utilities for saving/loading and evaluation
from src.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models
)

from src.utils.ml_utils.model.estimator import ConcreteStrengthModel
from src.utils.ml_utils.metric.regression_metric import get_regression_score

# THE CANDIDATES: Regression Algorithms
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            # STEP 1: Define candidate regression models
            models = {
                "Linear Regression": LinearRegression(),
                "Ridge": Ridge(),
                "ElasticNet": ElasticNet(),
                "KNN Regressor": KNeighborsRegressor(),
                "SVR": SVR(),
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBoost": XGBRegressor(objective="reg:squarederror"),
                "LightGBM": LGBMRegressor()
            }

            # STEP 2: Hyperparameter grids (tuning knobs)
            params = {
                "Linear Regression": {},
                "Ridge": {
                    "alpha": [0.1, 1.0, 10.0]
                },
                "ElasticNet": {
                    "alpha": [0.1, 1.0],
                    "l1_ratio": [0.2, 0.5, 0.8]
                },
                "KNN Regressor": {
                    "n_neighbors": [3, 5, 7]
                },
                "SVR": {
                    "C": [0.1, 1, 10],
                    "kernel": ["rbf"]
                },
                "Random Forest": {
                    "n_estimators": [50, 100, 200]
                },
                "Gradient Boosting": {
                    "learning_rate": [0.05, 0.1],
                    "n_estimators": [100, 200]
                },
                "XGBoost": {
                    "learning_rate": [0.05, 0.1],
                    "n_estimators": [100, 200]
                },
                "LightGBM": {
                    "learning_rate": [0.05, 0.1],
                    "n_estimators": [100, 200]
                },
            }

            # STEP 3: Evaluate all models
            # evaluate_models trains, tunes, and returns a scorecard
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # STEP 4: Select the best-performing model
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logging.info(f"Best model selected: {best_model_name}")

            # STEP 5: Calculate regression metrics
            y_train_pred = best_model.predict(X_train)
            
            train_metric = get_regression_score(y_true=y_train,y_pred=y_train_pred)

            y_test_pred = best_model.predict(X_test)
            
            test_metric = get_regression_score(y_true=y_test,y_pred=y_test_pred)

            # STEP 6: Package for Production
            # Load the preprocessor (RobustScaler) from transformation stage
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

            # Combine preprocessing + model into one deployable object
            final_model = ConcreteStrengthModel(preprocessor=preprocessor,model=best_model)

            # Save final model
            save_object(self.model_trainer_config.trained_model_file_path,obj=final_model)

            save_object("final_model/model.pkl",best_model)

            # STEP 7: Create the artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_metric,
                test_metric_artifact=test_metric
            )

            return model_trainer_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            # STEP 1: Load transformed numpy arrays
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(train_file_path)
            
            test_arr = load_numpy_array_data(test_file_path)

            # STEP 2: Split features and target
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # STEP 3: Start model training
            return self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

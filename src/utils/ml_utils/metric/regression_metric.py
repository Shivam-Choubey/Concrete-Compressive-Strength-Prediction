from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
from src.entity.artifacts_entity import RegressionMetricArtifact
from src.exception.exception import ConcreteStrengthException
import sys

def get_regression_score(y_true, y_pred) -> RegressionMetricArtifact:
    try:
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        regression_metric = RegressionMetricArtifact(
            r2_score=r2,
            mae=mae,
            rmse=rmse
        )
        return regression_metric

    except Exception as e:
        raise ConcreteStrengthException(e, sys)

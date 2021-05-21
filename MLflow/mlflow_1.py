import os
import warnings
import sys

import numpy as np
from dask_cuda import LocalCUDACluster
from dask.distributed import Client

import cudf
from cuml import make_regression, train_test_split
from cuml.linear_model import ElasticNet as cuEN
from cuml.metrics.regression import r2_score, mean_squared_error, mean_absolute_error
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def evaluation_metric(actual, pred):
    rmse = float(np.sqrt(mean_squared_error(actual, pred)))
    mae = float(mean_absolute_error(actual, pred))
    r2 = float(r2_score(actual, pred))

    return rmse, mae, r2

if __name__=='__main__':
    n_samples = 2 ** 10
    n_features = 100
    random_state = 23

    cluster = LocalCUDACluster()
    client = Client(cluster)

    X, y = make_regression(n_samples=n_samples, n_features=n_features, random_state=random_state)
    X = cudf.DataFrame(X)
    y = cudf.DataFrame(y)[0]
    X_cudf, X_cudf_test, y_cudf, y_cudf_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        ols_cu = cuEN(alpha=alpha, l1_ratio=l1_ratio)
        ols_cu.fit(X_cudf, y_cudf)
        predict_cuml = ols_cu.predict(X_cudf_test)
        (rmse, mae, r2) = evaluation_metric(y_cudf_test, predict_cuml)
        print(f'ElasticNet Model: alpha={alpha}, l1_ratio={l1_ratio}')
        print(f'RMSE: {rmse}')
        print(f'MAE: {mae}')
        print(f'R2 Score: {r2}')

        mlflow.log_param('alpha', alpha)
        mlflow.log_param('l1_ratio', l1_ratio)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('mae', mae)
        mlflow.log_metric('r2', r2)

        tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != 'file':
            mlflow.sklearn.log_model(cuEN, 'model', registered_model_name ='ElasticNet')
        else:
            mlflow.sklearn.log_model(cuEN, 'model')

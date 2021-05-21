## Tracking ML Experiments Using MLflow

![MLflow Experiment Tracker](images/mlflow_experiment_tracker.png)

### Install

```python
pip install -r requirements.txt
```

### Run

```python
# P refers parameter with alpha as hyperparameter of the ElasticNet Model.

mlflow run MLflow/ -P alpha=0.45
```

### Steps

* Creating Conda Environment
* Installing Necessary Libraries
* Creating Conda.yaml using 
  ```python
  conda env export > conda.yaml
  ```

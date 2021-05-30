## MLops - Interaction between Celery & ML

### Objective

With MLops taking main stream for deploying ML Models into production, the purpose of the repo to get an beginner level understanding 
of ML interaction with Celery, a task distributor with help brokers.

Consider there are multiple request comes to an model for prediction and each data is preprocessed & then sent for prediction. So the
with celery is run tasks (data preprocessing) in a function and then performing prediction using model. So asynchronously handle multiple 
request while one image is transformed and other earlier image is predicted.

[Celery](https://docs.celeryproject.org/en/stable/) is a simple, flexible, and reliable distributed system to process vast amounts
of messages, while providing operations with the tools required to maintain such a system.It’s a task queue with focus on real-time 
processing, while also supporting task scheduling.

### Installation
```python
pip install -r requirements.txt
```

### Run Flask Server
```python
python flask_server.py
```

### Run Celery Task
```python
celery -A tasks.celery worker --loglevel=info
```

**Note** Try out with Multiple workers and Bulk request to check how it works out.

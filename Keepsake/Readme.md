# Playing-with-Keepsake

Keepsake is a version control tool for Machine Learning. It's a beginner lesson on how to use keepsake and store result in AWS and in Local.

# Blog

* 📑 [Keepsake - A Version Control For Machine Learning](mayurji.github.io/machine-learning/keepsake)

### Installation

```
pip install -r requirements.txt
```

### Setting Up AWS

* Create a aws account (**Use Free Tier**)
* Get the access and secret key

### My Credentials From AWS Account

![acces_key](images/access_and_secret_key.png)

* Create S3 bucket
* Install aws cli
* Type the below command in the terminal

```
aws configure
```

* Pass the access and secret key
* From S3 bucket get the region.
* For last option, default is JSON

### My Credentials From AWS Account

![acces_key](images/access_and_secret_key.png)

### AWS Configure

![aws_configure](images/aws_configure.png)

### Run Experiment

```
python main.py
```

![run_experiment](images/run_experiment.png)

### Creating Checkpoint and storing in AWS S3 bucket

![save_checkpoint](images/creating_checkpoint.png)

### Listing All ML Experiments using ls

![ls command](images/ls_command.png)

### Show each ML Experiments using experiment id and show command

![id and show](images/show_command.png)

### Show each ML Checkpoint using checkpoint id and show command

![id and show](images/keepsake_checkpoint.png)

### Show difference between ML experiments (checkpoint) using diff command

![id and diff](images/diff_checkpoint.png)

### End Result of Experiment is stored in AWS Bucket (keepsake-trial)

![aws_bucket_result](images/aws_s3_bucket.png)

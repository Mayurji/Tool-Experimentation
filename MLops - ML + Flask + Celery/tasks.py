from celery import Celery, current_task
from celery.result import AsyncResult
from model.model import NN_Model_K
import torch
import json
import numpy as np
from io import BytesIO
from PIL import Image
from torchvision import transforms
from celery.utils.log import get_task_logger
import time

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
celery = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
celery.conf.accept_content = ['pickle', 'application/json']
celery.conf.result_serializer = 'json'
celery.conf.task_serializer='pickle'
LOGGER = get_task_logger(__name__)

model = NN_Model_K(n_channel=32) #Model takes the output channel for first Conv Layer from user.
model.load_state_dict(torch.load("model/" + 'birds_vs_airplanes.pt', map_location='cpu'))
model.eval()
class_names = ['airplane', 'bird']

"""
Setting up the transformation to be applied to each image, the transformation should be same as what was applied while during training model.
"""
def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.ToTensor(),
    									transforms.Resize((32, 32)),
                                        transforms.Normalize(
                                            [0.5, 0.5, 0.5],
                                            [0.5, 0.5, 0.5])])
    image = Image.open(BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

@celery.task()
def run_inference(image):
	jobid = current_task.request.id
	current_task.update_state(state='PROGRESS', meta={'current':0.1})
	LOGGER.info('JobId: %s, Status: PROGRESS, Meta: prediction started', jobid)
	in_tensor = transform_image(image_bytes=image)
	time.sleep(3)
	LOGGER.info('JobId: %s, Status: PROGRESS, Meta: Image Transformed', jobid)
	current_task.update_state(state='PROGRESS', meta={'current': 0.2})
	
	with torch.no_grad():
		output = model(in_tensor)
		_, predicted = torch.max(output, dim=1)
		out = predicted.item()
	LOGGER.info('JobId: %s, Status: Predicted, Meta: Image Classification is done.', jobid)    

	return {"class_name": class_names[out]}

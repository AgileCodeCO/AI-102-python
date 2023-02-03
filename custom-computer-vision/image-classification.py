# pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time

import sys
sys.path.insert(0, '../')
from resource_credentials import (endpoint, 
    subscription_key, 
    custom_vision_endpoint, 
    custom_vision_training_key, 
    custom_vision_prediction_endpoint,
    custom_vision_prediction_key,
    custom_vision_prediction_resource_id)

# Training credentials
credentials = ApiKeyCredentials(in_headers={"Training-key": subscription_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

# TODO: Upload images
projects = trainer.get_projects()
project = None

for item in projects:
    if item.name == "Sports":
        project = item

print(project.id)

print("Training...")
iteration = None
try:
    iteration = trainer.train_project(project.id, force_train=False)
    while iteration.status != "Completed":
        iteration = trainer.get_iteration(project.id, iteration.id)
        print("Training status: " + iteration.status)
        time.sleep(1)
    print("Training done!")
except:
  print("Model already trained")
  iteration = trainer.get_iterations(project.id)[0]

publish_iteration_name = "Iteration from Python"
if iteration.publish_name == "":    
    trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, custom_vision_prediction_resource_id)
    print("Publish done!")

# Prediction credentials
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": custom_vision_prediction_key})
predictor = CustomVisionPredictionClient(custom_vision_prediction_endpoint, prediction_credentials)

image_to_test = "images/football_test.jpg"
with open(image_to_test, "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    print(f"Predictions on {image_to_test}")
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))



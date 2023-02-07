# pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import pandas as pd
import time
import os
import sys
sys.path.insert(0, '../')
from resource_credentials import (endpoint, 
    subscription_key, 
    custom_vision_endpoint, 
    custom_vision_training_key, 
    custom_vision_prediction_endpoint,
    custom_vision_prediction_key,
    custom_vision_prediction_resource_id)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def find_image_in_batch(batch, image_name):
    for image in batch:
        if image.name == image_name:
            return image

    return None


# Training credentials
credentials = ApiKeyCredentials(in_headers={"Training-key": subscription_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)


train_dataset = pd.read_csv(f"detection-images/train_labels.csv")

tags = train_dataset['class'].unique()

print("Creating project...")

object_detection_domain = next(
    domain for domain in trainer.get_domains() if domain.type == "ObjectDetection" and domain.name == "General")

project = trainer.create_project("Microcontrollers Detection",  domain_id=object_detection_domain.id)

image_list = []

print("Adding images...")

for tag in tags:
    # create tag in project
    project_tag = trainer.create_tag(project.id, tag)

    # upload images
    for index, file in train_dataset[train_dataset["class"]==tag].iterrows():
        # Build region with normalized coordinates***
        region = Region(tag_id=project_tag.id, 
            left=float(file['xmin'])/float(file['width']), 
            top=float(file['ymin'])/float(file['height']), 
            width=float(file['xmax'] - file['xmin'])/float(file['width']), 
            height=float(file['ymax'] - file['ymin'])/float(file['height']))

        filename = file['filename']
        previous_image = find_image_in_batch(image_list, filename)

        if previous_image:
            previous_image.regions.append(region)
        else:
            with open(f"detection-images/train/{filename}", "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=filename, contents=image_contents.read(), regions=[region]))

for batch in chunker(image_list, 64):
    print("Uploading batch...")
    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=batch))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status, image.source_url)
        exit(-1)

print("Training...")

iteration = trainer.train_project(project.id, force_train=False)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    time.sleep(1)
print("Training done!")

publish_iteration_name = "Iteration from Python"

trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, custom_vision_prediction_resource_id)
print("Publish done!")

# Prediction credentials
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": custom_vision_prediction_key})
predictor = CustomVisionPredictionClient(custom_vision_prediction_endpoint, prediction_credentials)

image_to_test = "detection-images/test/IMG_20181228_102636.jpg"
with open(image_to_test, "rb") as image_contents:
    results = predictor.detect_image(
        project.id, publish_iteration_name, image_contents.read())

    print(f"Predictions on {image_to_test}")
    
    # Display the results.
    for prediction in results.predictions:
        print(
            "\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(
                prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top,
                prediction.bounding_box.width, prediction.bounding_box.height))



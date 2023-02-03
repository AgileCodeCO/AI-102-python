# pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
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

# Training credentials
credentials = ApiKeyCredentials(in_headers={"Training-key": subscription_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

print("Creating project...")

project = trainer.create_project("Sports Full")

tags = ["baseball", "basketball", "bmx", "boxing", "football", "formula1", "table-tennis", "tennis", "ultimate", "volleyball"]

image_list = []

print("Adding images...")

for tag in tags:
    # create tag in project
    project_tag = trainer.create_tag(project.id, tag)

    # upload images
    for filename in os.listdir(f"images/train/{tag}"):
        with open(f"images/train/{tag}/{filename}", "rb") as image_contents:
            image_list.append(ImageFileCreateEntry(name=filename, contents=image_contents.read(), tag_ids=[project_tag.id]))


for batch in chunker(image_list, 64):
    print("Uploading batch...")
    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=batch))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
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

image_to_test = "images/football_test.jpg"
with open(image_to_test, "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    print(f"Predictions on {image_to_test}")
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))



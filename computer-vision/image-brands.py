from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


# BRANDS
local_image_path = "images/nfl-teams.jpeg"
local_image = open(local_image_path, "rb")

# Call API with image and features
detect_brands_results_local = computervision_client.analyze_image_in_stream(local_image, [VisualFeatureTypes.brands])

# Print detection results with bounding box and confidence score
print("\nDetecting brands in local image: \n")
if len(detect_brands_results_local.brands) == 0:
    print("No brands detected.")
else:    
    for item in detect_brands_results_local.brands:
        print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format(
            item.name, item.confidence * 100, item.rectangle.x, item.rectangle.x + item.rectangle.w,
            item.rectangle.y, item.rectangle.y + item.rectangle.h))
print()

#local_image_path = "images/sofi-stadium.jpeg"
local_image = open(local_image_path, "rb")

# Call API with image and features
features_result = computervision_client.analyze_image_in_stream(local_image, [VisualFeatureTypes.categories, 
    VisualFeatureTypes.objects, 
    VisualFeatureTypes.adult, 
    VisualFeatureTypes.faces,
    VisualFeatureTypes.color,
    VisualFeatureTypes.image_type])

# Print detection results with bounding box and confidence score
print("\nDetecting categories in local image: \n")
if len(features_result.categories) == 0:
    print("No categories detected.")
else:    
    for item in features_result.categories:
        print(item.name)
print()

print("\nDetecting objects in local image: \n")
if len(features_result.objects) == 0:
    print("No objects detected.")
else:    
    for item in features_result.objects:
        print("'{}' object detected with confidence {:.1f}% at location {}, {}, {}, {}".format(
            item.object_property, item.confidence * 100, item.rectangle.x, item.rectangle.x + item.rectangle.w,
            item.rectangle.y, item.rectangle.y + item.rectangle.h))
print()

print("\nDetecting adult in local image: \n")
print("Is adult content:", features_result.adult.is_adult_content)
print("Is racy content:", features_result.adult.is_racy_content)
print("Is gory content:", features_result.adult.is_gory_content)
print()


print("\nDetecting faces in local image: \n")
if len(features_result.faces) == 0:
    print("No faces detected.")
else:    
    for item in features_result.faces:        
        print("'{}' face detected with age {} at location {}, {}, {}, {}".format(
            item.gender, item.age, item.face_rectangle.left, item.face_rectangle.top ,item.face_rectangle.width,
            item.face_rectangle.height))
print()

print("\nDetecting colors in local image: \n")
if len(features_result.color.dominant_colors) == 0:
    print("No colors detected.")
else:    
    for item in features_result.color.dominant_colors:
        print(item)
print()
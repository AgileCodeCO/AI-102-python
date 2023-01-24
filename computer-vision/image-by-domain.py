from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# List domain models
models = computervision_client.list_models()

print("\nDomain models:")
for x in models.models_property:
    print(x)

local_image_path = "images/eiffel-tower.jpeg"
local_image = open(local_image_path, "rb")

domain = "landmarks"
detect_domain_results_landmark_local = computervision_client.analyze_image_by_domain_in_stream(domain,
                                                                                               local_image)

# Print results of landmark detected
print("\nLandmarks in the local image:")
if len(detect_domain_results_landmark_local.result["landmarks"]) == 0:
    print("No landmarks detected.")
else:
    for landmark in detect_domain_results_landmark_local.result["landmarks"]:        
        print("'{}' with confidence {:.2f}%".format(landmark["name"], landmark["confidence"] * 100))
print()
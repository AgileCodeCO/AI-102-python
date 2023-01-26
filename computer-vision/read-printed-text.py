from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

local_image_path = "images/printed_text.jpg"
local_image = open(local_image_path, "rb")


readed_text_result = computervision_client.recognize_printed_text_in_stream(local_image)

for region in readed_text_result.regions:   
    for line in region.lines:
        print("****LINE****")
        for word in line.words:
            print(f"{word.text} ({word.bounding_box})")

print()
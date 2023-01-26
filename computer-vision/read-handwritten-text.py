from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

local_image_path = "images/handwritten-text.png"
local_image = open(local_image_path, "rb")


readed_text_result = computervision_client.read_in_stream(local_image, raw=True)

operation_location_remote = readed_text_result.headers["Operation-Location"]
operation_id = operation_location_remote.split("/")[-1]

while True:
    get_handw_text_results = computervision_client.get_read_result(operation_id)
    if get_handw_text_results.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)

print()
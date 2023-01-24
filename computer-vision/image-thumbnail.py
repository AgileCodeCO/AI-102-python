from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

local_image_path = "images/sofi-stadium.jpeg"
local_image = open(local_image_path, "rb")

print("Generating thumbnail from a local image...")
thumb_local = computervision_client.generate_thumbnail_in_stream(100, 100, local_image, True)

# Write the image binary to file
with open("images/thumb_local.png", "wb") as f:
    for chunk in thumb_local:
        f.write(chunk)

print("Thumbnail saved to local folder.")
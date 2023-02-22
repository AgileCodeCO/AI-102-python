# pip install azure-ai-textanalytics

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(subscription_key))

try:
    documents = [       
        {"id": "1", "language": "en", "text": "My cat might need to see a veterinarian because is feeling sick."},
        {"id": "2", "language": "es", "text": "A mi me encanta el fútbol americano y la formula 1!"}
    ]

    response = text_analytics_client.extract_key_phrases(documents=documents)

    for document in response:
        print("Document Id: ", document.id)
        print("\tKey Phrases:")
        for phrase in document.key_phrases:
            print("\t\t", phrase)

except Exception as err:
    print("Encountered exception. {}".format(err))

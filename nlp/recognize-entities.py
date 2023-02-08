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

    for document in documents:
        print(
            "Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

    response = text_analytics_client.recognize_entities(documents=documents)
    print(response)
    for result in response:
        print("Document Id: ", result.id)
        print("\tEntities:")
        for entity in result.entities:
            print("\t\t", entity.text, f"- category: {entity.category}", f"- score: {entity.confidence_score}")

except Exception as err:
    print("Encountered exception. {}".format(err))

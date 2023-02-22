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
        {"id": "1", "text": "My cat might need to see a veterinarian because is feeling sick."},
        {"id": "2", "country_hint": "co", "text": "A mi me encanta el fútbol americano y la formula 1!"},
        {"id": "3", "text": "I'm happy and sad"}
    ]

    response = text_analytics_client.detect_language(documents=documents)
    
    for result in response:
        print("Document Id: ", result.id)
        print("\tPrimary language:", result.primary_language.name, "score:", result.primary_language.confidence_score)
        

except Exception as err:
    print("Encountered exception. {}".format(err))

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
        {"id": "2", "language": "es", "text": "A mi me encanta el fútbol americano y la formula 1!"},
        {"id": "3", "language": "en", "text": "I'm happy and sad"}
    ]

    response = text_analytics_client.analyze_sentiment(documents=documents)
    
    for result in response:
        print("Document Id: ", result.id)
        print("\tSentiment:", result.sentiment)
        for sentence in result.sentences:
            print("\tSentence:", sentence.text)
            print("\tSentence sentiment:", sentence.sentiment)
            print("\t\t", "positive:", sentence.confidence_scores.positive, "neutral:", sentence.confidence_scores.neutral, "negative:", sentence.confidence_scores.negative)

except Exception as err:
    print("Encountered exception. {}".format(err))

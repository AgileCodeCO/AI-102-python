from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Read credentials from common file
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key

credential = AzureKeyCredential(subscription_key)
document_analysis_client = DocumentAnalysisClient(endpoint, credential)

with open("docs/invoice.pdf", "rb") as fd:
    document = fd.read()

poller = document_analysis_client.begin_analyze_document("prebuilt-layout", document)

result = poller.result()
for page in result.pages:
    print("----Analyzing layout from page #{}----".format(page.page_number))
    print(
        "Page has width: {} and height: {}, measured with unit: {}".format(
            page.width, page.height, page.unit
        )
    )

    for line_idx, line in enumerate(page.lines):
        print(
            "...Line # {} has content '{}' within bounding polygon '{}'".format(
                line_idx,
                line.content,
                line.polygon,
            )
        )

    for word in page.words:
        print(
            "...Word '{}' has a confidence of {}".format(
                word.content, word.confidence
            )
        )

    for selection_mark in page.selection_marks:
        print(
            "...Selection mark is '{}' within bounding polygon '{}' and has a confidence of {}".format(
                selection_mark.state,
                selection_mark.polygon,
                selection_mark.confidence,
            )
        )

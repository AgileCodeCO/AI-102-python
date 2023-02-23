# pip install azure.cognitiveservices.speech
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region="eastus")

speech_config.speech_synthesis_voice_name = "es-CO-SalomeNeural"

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

while True:
    print("Type some text that you want to speak or 'quit' to exit...")
    text = input()

    if text == "quit":
        break

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech played for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
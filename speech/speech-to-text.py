# pip install azure.cognitiveservices.speech
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region="eastus")

audio_filename = "audio/text-to-speech.wav"
audio_input = speechsdk.AudioConfig(filename=audio_filename)

speech_synthesizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input, language="es-CO")

result = speech_synthesizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
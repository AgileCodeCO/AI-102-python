# pip install azure.cognitiveservices.speech
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region="eastus")

speech_config.speech_synthesis_voice_name = "es-CO-SalomeNeural"

audio_filename = "audio/text-to-speech.wav"
audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_filename)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

print("Type some text that you want to speak and save in an audio file...")
text = input()

result = speech_synthesizer.speak_text_async(text).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech audio saved for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
    print("Did you update the subscription info?")
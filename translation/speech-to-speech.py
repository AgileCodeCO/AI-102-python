# pip install azure.cognitiveservices.speech
import sys
sys.path.insert(0, '../')
from resource_credentials import endpoint, subscription_key
import azure.cognitiveservices.speech as speechsdk

speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=subscription_key,
                                                                          region="eastus")

speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region="eastus")

# From language configuration
fromLanguage = 'es-CO'
speech_translation_config.speech_recognition_language = fromLanguage

# Target languages
speech_translation_config.add_target_language("fr")
speech_translation_config.add_target_language("en-US")

# Input audio... could be with microphone as well
audio_filename = "audio/text-to-speech.wav"
audio_input = speechsdk.AudioConfig(filename=audio_filename)
recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config,
                                                         audio_config=audio_input)

result = recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.TranslatedSpeech:
    print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))

    # Translations
    for key in result.translations:
        print("TRANSLATED into {}: {}".format(key, result.translations[key]))
        print("Speech played for language [{}]".format(key))
        if key == "fr":
            speech_config.speech_synthesis_voice_name = "fr-FR-CelesteNeural"
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            speech_synthesizer.speak_text_async(result.translations[key]).get()
        else:
            speech_config.speech_synthesis_voice_name = "en-US-ElizabethNeural"
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            speech_synthesizer.speak_text_async(result.translations[key]).get()
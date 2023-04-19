import hug
import requests
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import azure.cognitiveservices.speech as speechsdk
import os
import json
import uuid


# # Add your Computer Vision subscription key and endpoint to your environment variables.
# subscription_key = "eeaf3e3ab15b45f697be75bc5df5130b"
# endpoint = "https://tic-clo2-vision.cognitiveservices.azure.com/vision/v3.2/analyze"

# Instantiate a client object
#computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


@hug.post('/image')
def process_image(image):
    print(image)
    subscription_key = 'eeaf3e3ab15b45f697be75bc5df5130b'
    endpoint = 'https://tic-clo2-vision.cognitiveservices.azure.com/vision/v3.2/analyze'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    # Envoie l'image à l'API Computer Vision
    response = requests.post(endpoint, headers=headers, params={'visualFeatures': 'Objects'},
                             files={'image': image})
    response.raise_for_status()
    analysis = response.json()

    # Compte le nombre de personnes détectées dans l'image
    objects = analysis['objects']
    person_count = sum(obj['object'] == 'person' for obj in objects)

    with open('config.json', 'r') as f:

        data = json.load(f)

    return {'personCount': person_count, 'personAllowed': data['NumberOfPerson']}


@hug.post('/config')
def config(body):
        # Add your key and endpoint
    key = "13bbdefa382f40a7a68a79a05754a0f1"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "francecentral"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'fr',
        'to': ['en']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    bodyEn = [{
        'text': body['textToSpeech']
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=bodyEn)
    response = request.json()

    print(response[0]['translations'][0]['text'])
    body['textToSpeechEN'] = response[0]['translations'][0]['text']
    with open('config.json', 'w') as f:
        json.dump(body, f)
    audioFr()
    audioEn()
    return body


@hug.get('/fr')
def audioFr():
    speech_config = speechsdk.SpeechConfig(subscription="8fbc3d2068dd47cebfad7e2d95730d39", region="francecentral")
    audio_config = speechsdk.audio.AudioOutputConfig(filename="fr.wav")

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='fr-CA-JeanNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    with open('config.json', 'r') as f:

        data = json.load(f)

    # Accéder à la donnée souhaitée
    text = data['textToSpeech']

    print(text)
    speech_synthesizer.speak_text_async(text).get()
    return 'OK'

@hug.get('/En')
def audioEn():
    speech_config = speechsdk.SpeechConfig(subscription="8fbc3d2068dd47cebfad7e2d95730d39", region="francecentral")
    audio_config = speechsdk.audio.AudioOutputConfig(filename="en.wav")

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-AshleyNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    with open('config.json', 'r') as f:

        data = json.load(f)

    # Accéder à la donnée souhaitée
    text = data['textToSpeechEN']

    print(text)
    speech_synthesizer.speak_text_async(text).get()
    return 'OK'



@hug.get("/fr.wav", output=hug.output_format.file)
def image():
    return "./fr.wav"
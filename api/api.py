import hug
import requests
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import hug

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

    return {'person_count': person_count}


@hug.post('/config')
def config(body):
    with open('config.json', 'w') as f:
        json.dump(body, f)
    return body


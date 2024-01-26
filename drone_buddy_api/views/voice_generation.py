import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from dronebuddylib import IntentRecognitionEngine, TextRecognitionEngine
from dronebuddylib.models import EngineConfigurations
from dronebuddylib.models.enums import IntentRecognitionAlgorithm, TextRecognitionAlgorithm
from dronebuddylib.utils.logger import Logger
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from drone_buddy_api.utils.serializers import IntentRecognitionSerializer, ImageAndConfigurationsSerializer, \
    TextRecognitionSerializer, VoiceGenerationSerializer

logger = Logger()

import pyttsx3


# Apply csrf_exempt to the entire CBV
@method_decorator(csrf_exempt, name='dispatch')
class VoiceGenerationView(APIView):

    # Define the POST method
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: openapi.Response('Intent recognition successful')}
    )
    def post(self, request, *args, **kwargs):
        voice_gen_engine = pyttsx3.init()

        serializer = VoiceGenerationSerializer(data=request.data)
        if serializer.is_valid():

            text = serializer.validated_data['text']
            logger.log_info("voice generation", 'Received text: ' + text)
            voice_gen_engine.say(text)
            voice_gen_engine.runAndWait()
            voice_gen_engine.stop()

            if voice_gen_engine._inLoop:
                voice_gen_engine.endLoop()

            # Your logic here...
            return Response({'message': 'VOice played ',
                             'result': []})
        else:
            return Response(serializer.errors, status=400)


def convert_text_recognition_result_to_serializable(data):
    serializable_data = []

    for item in data.full_information:
        text_data = {
            "description": item.description,
            "bounding_poly": {
                "vertices": [{"x": vertex.x, "y": vertex.y} for vertex in item.bounding_poly.vertices]
            }
        }
        serializable_data.append(text_data)
    result = {
        "text": data.text,
        "locale": data.locale,
        "full_information": serializable_data}
    return result

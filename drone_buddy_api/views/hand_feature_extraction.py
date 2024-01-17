import json

import cv2
import numpy as np
from dronebuddylib import ObjectDetectionEngine
from dronebuddylib.atoms.bodyfeatureextraction import HandFeatureExtractionImpl
from dronebuddylib.models import EngineConfigurations
from dronebuddylib.models.enums import VisionAlgorithm
from dronebuddylib.utils.logger import Logger
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from drone_buddy_api.utils.serializers import ImageAndConfigurationsSerializer

# Define the serializer

logger = Logger()


# Apply csrf_exempt to the entire CBV
@method_decorator(csrf_exempt, name='dispatch')
class HandFeatureExtractionView(APIView):

    # Define the POST method
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Image file to upload'),
                'engine_configurations': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING)
                )
            },
        ),
        responses={200: openapi.Response('Object detection successful')}
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageAndConfigurationsSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            # Read the image data into a memory buffer
            image_data = image.read()
            # Convert the image data to a numpy array
            numpy_array = np.frombuffer(image_data, np.uint8)
            # Decode the image data into a format that OpenCV understands
            cv_image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

            # Now you can use the cv_image with OpenCV for processing
            # For example, let's just save it to the server

            try:
                engine_configurations = json.loads(serializer.validated_data['engine_configurations'])
            except:
                engine_configurations = serializer.validated_data['engine_configurations']

            logger.log_info("object_ detection", 'Received image: ' + image.name)
            engine_configs = EngineConfigurations(engine_configurations)
            engine = HandFeatureExtractionImpl(engine_configs)
            detected_gesture = engine.get_gesture(image_rgb)

            # Your logic here...
            return Response({'message': 'Hand feature completed ',
                             'result': convert_to_serializable(detected_gesture)})
        else:
            return Response(serializer.errors, status=400)


def convert_to_serializable(gesture_result):
    def category_to_dict(category):
        return {
            'index': category.index,
            'score': category.score,
            'display_name': category.display_name,
            'category_name': category.category_name
        }

    def landmark_to_dict(landmark):
        return {
            'x': landmark.x,
            'y': landmark.y,
            'z': landmark.z,
            'visibility': landmark.visibility,
            'presence': landmark.presence
        }

    result_dict = {
        'gestures': [[category_to_dict(cat) for cat in gesture_list] for gesture_list in gesture_result.gestures],
        'handedness': [[category_to_dict(cat) for cat in handedness_list] for handedness_list in
                       gesture_result.handedness],
        'hand_landmarks': [[landmark_to_dict(lm) for lm in lm_list] for lm_list in gesture_result.hand_landmarks],
        'hand_world_landmarks': [[landmark_to_dict(lm) for lm in lm_list] for lm_list in
                                 gesture_result.hand_world_landmarks]
    }

    return result_dict

# Usage

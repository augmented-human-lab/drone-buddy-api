import json

import cv2
import numpy as np
from dronebuddylib import ObjectDetectionEngine
from dronebuddylib.atoms.objectdetection.detected_object import DetectedCategories, ObjectDetectionResult
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
class DetectObjectsView(APIView):

    # Define the POST method
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'algorithm_name', in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=[algo.value for algo in VisionAlgorithm],  # Enum values for the dropdown
                description='The name of the algorithm to use for detection',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Image file to upload'),
                'engine_configurations': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Assuming it's a JSON string
                    description='JSON string of engine configurations'
                )
            }
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

            # Now you can use the cv_image with OpenCV for processing
            # For example, let's just save it to the server

            try:
                engine_configurations = json.loads(serializer.validated_data['engine_configurations'])
            except:
                engine_configurations = serializer.validated_data['engine_configurations']

            logger.log_info("object_ detection", 'Received image: ' + image.name)
            algorithm_name = request.query_params['algorithm_name']
            engine_configs = EngineConfigurations(engine_configurations)
            engine = ObjectDetectionEngine(algorithm_name, engine_configs)
            detected_objects = engine.get_detected_objects(cv_image)

            # Your logic here...
            return Response({'message': 'Detection started using ' + algorithm_name,
                             'result': detected_objects.to_json()})
        else:
            return Response(serializer.errors, status=400)

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
    TextRecognitionSerializer

logger = Logger()


# Apply csrf_exempt to the entire CBV
@method_decorator(csrf_exempt, name='dispatch')
class TextRecognitionView(APIView):

    # Define the POST method
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'algorithm_name', in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=[algo.value for algo in TextRecognitionAlgorithm],  # Enum values for the dropdown
                description='The name of the algorithm to use for text recognition',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image_path': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='path of the image to be analysed'),
                'engine_configurations': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING)
                )
            },
        ),
        responses={200: openapi.Response('Intent recognition successful')}
    )
    def post(self, request, *args, **kwargs):
        serializer = TextRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                engine_configurations = json.loads(serializer.validated_data['engine_configurations'])
            except:
                engine_configurations = serializer.validated_data['engine_configurations']

            algorithm_name = request.query_params['algorithm_name']
            image_path = serializer.validated_data['image_path']
            logger.log_info("Text recognition", 'Received image at : ' + image_path)
            engine_configs = EngineConfigurations(engine_configurations)
            engine = TextRecognitionEngine(algorithm_name, engine_configs)
            detected_objects = engine.recognize_text(image_path)

            # Your logic here...
            return Response({'message': 'Intent Recognition completed using ' + algorithm_name,
                             'result': convert_text_recognition_result_to_serializable(detected_objects)})
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

import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from dronebuddylib import IntentRecognitionEngine
from dronebuddylib.models import EngineConfigurations
from dronebuddylib.models.enums import IntentRecognitionAlgorithm
from dronebuddylib.utils.logger import Logger
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from drone_buddy_api.utils.serializers import IntentRecognitionSerializer

logger = Logger()


# Apply csrf_exempt to the entire CBV
@method_decorator(csrf_exempt, name='dispatch')
class IntentRecognitionView(APIView):

    # Define the POST method
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'algorithm_name', in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=[algo.value for algo in IntentRecognitionAlgorithm],  # Enum values for the dropdown
                description='The name of the algorithm to use for intent recognition',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'engine_configurations': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING)
                )
            },
        ),
        responses={200: openapi.Response('Intent recognition successful')}
    )
    def post(self, request, *args, **kwargs):
        serializer = IntentRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                engine_configurations = json.loads(serializer.validated_data['engine_configurations'])
            except:
                engine_configurations = serializer.validated_data['engine_configurations']

            algorithm_name = request.query_params['algorithm_name']
            text = serializer.validated_data['text']
            logger.log_info("intent recognition", 'Received text: ' + text)
            engine_configs = EngineConfigurations(engine_configurations)
            engine = IntentRecognitionEngine(algorithm_name, engine_configs)
            recognized_intent = engine.recognize_intent(text)

            return Response({'message': 'Intent Recognition completed using ' + algorithm_name,
                             'result': recognized_intent.to_json()})
        else:
            return Response(serializer.errors, status=400)

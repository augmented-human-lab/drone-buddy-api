from rest_framework import serializers


class ImageAndConfigurationsSerializer(serializers.Serializer):
    image = serializers.ImageField()  # Add an image field
    engine_configurations = serializers.CharField()  # Temporarily change this to a CharField


class FaceRecognitionSerializer(serializers.Serializer):
    # image = serializers.ImageField()  # Add an image field
    image_path = serializers.CharField()  # Temporarily change this to a CharField
    engine_configurations = serializers.CharField()  # Temporarily change this to a CharField
    person_name = serializers.CharField()  # Temporarily change this to a CharField


class TextRecognitionSerializer(serializers.Serializer):
    image_path = serializers.CharField()  # Temporarily change this to a CharField
    engine_configurations = serializers.CharField()  # Temporarily change this to a CharField


class VoiceGenerationSerializer(serializers.Serializer):
    text = serializers.CharField()  # Temporarily change this to a CharField


class IntentRecognitionSerializer(serializers.Serializer):
    engine_configurations = serializers.CharField()  # Temporarily change this to a CharField
    text = serializers.CharField()  # Temporarily change this to a CharField

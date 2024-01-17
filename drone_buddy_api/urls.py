"""
URL configuration for drone_buddy_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drone_buddy_api.views.face_recognition import FaceRecognitionView, FaceRecognitionRememberView
from drone_buddy_api.views.hand_feature_extraction import HandFeatureExtractionView
from drone_buddy_api.views.intent_recognition import IntentRecognitionView
from drone_buddy_api.views.object_detection import DetectObjectsView
from drone_buddy_api.views.text_recognition import TextRecognitionView

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation for your project",
        # Terms of service URL, contact, and license information can be added here
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    path('atoms/object-detection/detect-objects/', DetectObjectsView.as_view(), name='detect_objects'),

    path('atoms/face-recognition/recognize-face/', FaceRecognitionView.as_view(),
         name='recognize_face'),
    path('atoms/face-recognition/remember-face/', FaceRecognitionRememberView.as_view(),
         name='remember_face'),
    path('atoms/intent-recognition/recognize-intent/', IntentRecognitionView.as_view(),
         name='recognize_intent'),
    path('atoms/text-recognition/recognize-text/', TextRecognitionView.as_view(),
         name='recognize_text'),
    path('atoms/feature-recognition/recognize-hand-gesture/', HandFeatureExtractionView.as_view(),
         name='recognize_hand_gesture'),

    # path('atoms/object-detection/detect-objects', detect_objects, name='detect_objects'),
]

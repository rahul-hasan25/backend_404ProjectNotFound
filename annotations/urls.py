from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageSeriesViewSet, MedicalImageViewSet, AnnotationViewSet, LabelClassViewSet

router = DefaultRouter()
router.register(r'label-classes', LabelClassViewSet)
router.register(r'series', ImageSeriesViewSet)
router.register(r'images', MedicalImageViewSet)
router.register(r'annotations', AnnotationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
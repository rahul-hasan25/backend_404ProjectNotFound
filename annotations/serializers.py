from rest_framework import serializers
from .models import ImageSeries, MedicalImage, Annotation, LabelClass

class LabelClassSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LabelClass
        fields = ['id', 'name']

class AnnotationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model  = Annotation
        fields = ['id', 'image', 'label_class', 'points']

class MedicalImageSerializer(serializers.ModelSerializer):
    annotations = AnnotationSerializer(many=True, read_only=True)

    class Meta:
        model  = MedicalImage
        fields = ['id', 'series', 'image_file', 'order', 'annotations']

class ImageSeriesSerializer(serializers.ModelSerializer):
    images     = MedicalImageSerializer(many=True, read_only=True)
    class_name = serializers.CharField(source='label_class.name', read_only=True)

    class Meta:
        model  = ImageSeries
        fields = ['id', 'name', 'view_type', 'label_class', 'class_name', 'images']
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import ImageSeries, MedicalImage, Annotation, LabelClass
from .serializers import ImageSeriesSerializer, MedicalImageSerializer, AnnotationSerializer, LabelClassSerializer

class LabelClassViewSet(viewsets.ModelViewSet):
    queryset           = LabelClass.objects.all()
    serializer_class   = LabelClassSerializer
    permission_classes = [AllowAny]

class ImageSeriesViewSet(viewsets.ModelViewSet):
    queryset           = ImageSeries.objects.all().prefetch_related('images__annotations')
    serializer_class   = ImageSeriesSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset   = ImageSeries.objects.all().prefetch_related('images__annotations')
        view_type  = self.request.query_params.get('view_type')
        class_name = self.request.query_params.get('class_name')
        
        if view_type:
            queryset = queryset.filter(view_type=view_type)
        if class_name:
            queryset = queryset.filter(label_class__name__iexact=class_name)
            
        return queryset

class MedicalImageViewSet(viewsets.ModelViewSet):
    queryset           = MedicalImage.objects.all()
    serializer_class   = MedicalImageSerializer
    permission_classes = [AllowAny]

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset           = Annotation.objects.all()
    serializer_class   = AnnotationSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='bulk-save')
    def bulk_save(self, request):
        image_id         = request.data.get('image_id')
        annotations_data = request.data.get('annotations', [])
        
        Annotation.objects.filter(image_id=image_id).delete()
        
        created_annotations = []
        for ann in annotations_data:
            new_ann = Annotation.objects.create(
                image_id    = image_id,
                label_class = ann.get('label_class', 'Tumor'),
                points      = ann.get('points', [])
            )
            created_annotations.append(AnnotationSerializer(new_ann).data)
        return Response(created_annotations, status=status.HTTP_201_CREATED)
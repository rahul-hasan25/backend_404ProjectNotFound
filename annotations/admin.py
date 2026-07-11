from django.contrib import admin
from .models import ImageSeries, MedicalImage, Annotation, LabelClass

class MedicalImageInline(admin.TabularInline):
    model  = MedicalImage
    extra  = 3 
    fields = ('image_file', 'order')

class AnnotationInline(admin.TabularInline):
    model = Annotation
    extra = 0

@admin.register(LabelClass)
class LabelClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ImageSeries)
class ImageSeriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'view_type', 'label_class', 'get_image_count', 'created_at')
    list_filter   = ('view_type', 'label_class')
    search_fields = ('name',)
    inlines       = [MedicalImageInline]

    def get_image_count(self, obj):
        return obj.images.count()
    get_image_count.short_description = 'Total Images'

@admin.register(MedicalImage)
class MedicalImageAdmin(admin.ModelAdmin):
    list_display  = ('id', 'series', 'image_file', 'order')
    list_filter   = ('series__view_type', 'series__label_class')
    search_fields = ('series__name',)
    inlines       = [AnnotationInline]

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'image', 'label_class', 'created_at')
    list_filter   = ('label_class', 'image__series__view_type')
    search_fields = ('label_class', 'image__id')
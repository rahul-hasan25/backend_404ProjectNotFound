from django.db import models

class LabelClass(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "Tumor", "Cyst"

    def __str__(self):
        return self.name

class ImageSeries(models.Model):
    VIEW_CHOICES = [
        ('axial', 'Axial'),
        ('sagittal', 'Sagittal'),
    ]
    name = models.CharField(max_length=255, help_text="e.g., Axial Tumor Series")
    view_type   = models.CharField(max_length=10, choices=VIEW_CHOICES, default='axial')
    label_class = models.ForeignKey(LabelClass, on_delete=models.CASCADE, related_name='series')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_view_type_display()} - {self.label_class.name})"

class MedicalImage(models.Model):
    series     = models.ForeignKey(ImageSeries, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image {self.order} - {self.series.name}"

class Annotation(models.Model):
    image       = models.ForeignKey(MedicalImage, related_name='annotations', on_delete=models.CASCADE)
    label_class = models.CharField(max_length=100, default='Tumor')
    points      = models.JSONField() 
    created_at  = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kanban_tasks')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority    = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    task_date   = models.DateField(db_index=True, help_text="The core dashboard control date")
    due_date    = models.DateField(blank=True, null=True, help_text="Deadline timestamp")
    tags        = models.JSONField(default=list, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} ({self.task_date})"
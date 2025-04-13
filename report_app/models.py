from django.db import models
from django.contrib.auth.models import User

class ReportConfig(models.Model):
    name = models.CharField(max_length=100)
    config_file = models.FileField(upload_to='configs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Report(models.Model):
    name = models.CharField(max_length=100)
    input_file = models.FileField(upload_to='input_files/')
    reference_file = models.FileField(upload_to='reference_files/')
    output_file = models.FileField(upload_to='output_files/', null=True, blank=True)
    config = models.ForeignKey(ReportConfig, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 
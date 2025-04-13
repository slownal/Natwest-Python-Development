from rest_framework import serializers
from .models import Report, ReportConfig

class ReportConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportConfig
        fields = ['id', 'name', 'config_file', 'created_at', 'updated_at']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name', 'input_file', 'reference_file', 'output_file', 
                 'config', 'status', 'created_at', 'updated_at'] 
from django.contrib import admin
from .models import Report, ReportConfig

@admin.register(ReportConfig)
class ReportConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'config', 'created_at', 'created_by')
    list_filter = ('status', 'created_at', 'created_by', 'config')
    search_fields = ('name',) 
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from .models import Report, ReportConfig
from .serializers import ReportSerializer, ReportConfigSerializer
import pandas as pd
import json
import os
from django.conf import settings

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root showing available endpoints
    """
    return Response({
        'reports': reverse('report-list', request=request, format=format),
        'configs': reverse('reportconfig-list', request=request, format=format),
    })

class ReportConfigViewSet(viewsets.ModelViewSet):
    queryset = ReportConfig.objects.all()
    serializer_class = ReportConfigSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_report(self, request, pk=None):
        report = self.get_object()
        
        try:
            # Read input and reference files
            input_df = pd.read_csv(report.input_file.path)
            reference_df = pd.read_csv(report.reference_file.path)
            
            # Read transformation rules from config
            with open(report.config.config_file.path, 'r') as f:
                rules = json.load(f)
            
            # Apply transformations
            output_df = pd.DataFrame()
            
            # Rule 1: outfield1 = field1 + field2
            output_df['outfield1'] = input_df['field1'] + input_df['field2']
            
            # Rule 2: outfield2 = refdata1
            output_df['outfield2'] = reference_df['refdata1']
            
            # Rule 3: outfield3 = refdata2 + refdata3
            output_df['outfield3'] = reference_df['refdata2'] + reference_df['refdata3']
            
            # Rule 4: outfield4 = field3 * max(field5, refdata4)
            output_df['outfield4'] = input_df['field3'].astype(float) * pd.concat([input_df['field5'], reference_df['refdata4']], axis=1).max(axis=1)
            
            # Rule 5: outfield5 = max(field5, refdata4)
            output_df['outfield5'] = pd.concat([input_df['field5'], reference_df['refdata4']], axis=1).max(axis=1)
            
            # Save output file
            output_path = os.path.join(settings.MEDIA_ROOT, 'output_files', f'report_{report.id}.csv')
            output_df.to_csv(output_path, index=False)
            
            # Update report status and save output file
            report.output_file = f'output_files/report_{report.id}.csv'
            report.status = 'completed'
            report.save()
            
            return Response({'status': 'success', 'message': 'Report generated successfully'})
            
        except Exception as e:
            report.status = 'failed'
            report.save()
            return Response({'status': 'error', 'message': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
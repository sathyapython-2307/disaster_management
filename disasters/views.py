from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, NumberFilter
from .models import DisasterEvent, DisasterData, RiskModel, HistoricalDisaster
from .serializers import DisasterEventSerializer, DisasterDataSerializer, RiskModelSerializer, HistoricalDisasterSerializer
from core.models import AuditLog
import logging

logger = logging.getLogger(__name__)


class DisasterEventFilterSet(FilterSet):
    """
    Custom FilterSet for DisasterEvent to support range filtering
    """
    disaster_type = CharFilter(field_name='disaster_type', lookup_expr='iexact')
    status = CharFilter(field_name='status', lookup_expr='iexact')
    risk_score_min = NumberFilter(field_name='risk_score', lookup_expr='gte')
    risk_score_max = NumberFilter(field_name='risk_score', lookup_expr='lte')
    
    class Meta:
        model = DisasterEvent
        fields = ['disaster_type', 'status', 'risk_score_min', 'risk_score_max']

@login_required
def disasters_map_view(request):
    context = {
        'user_role': request.user.role,
    }
    return render(request, 'disasters/disasters_map.html', context)


@login_required
def disaster_details_view(request, disaster_id):
    try:
        disaster = DisasterEvent.objects.get(id=disaster_id)
        context = {
            'disaster': disaster,
            'user_role': request.user.role,
        }
        return render(request, 'disasters/disaster_details.html', context)
    except DisasterEvent.DoesNotExist:
        return render(request, 'errors/404.html', status=404)


class DisasterEventViewSet(viewsets.ModelViewSet):
    queryset = DisasterEvent.objects.all()
    serializer_class = DisasterEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DisasterEventFilterSet
    search_fields = ['location_name']
    ordering_fields = ['predicted_time', 'risk_score']
    ordering = ['-predicted_time']
    
    @action(detail=False, methods=['get'])
    def active_events(self, request):
        events = DisasterEvent.objects.filter(status__in=['predicted', 'active'])
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        threshold = float(request.query_params.get('threshold', 70))
        events = DisasterEvent.objects.filter(risk_score__gte=threshold)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        disaster = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(DisasterEvent.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = disaster.status
        disaster.status = new_status
        disaster.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='update',
            resource_type='DisasterEvent',
            resource_id=str(disaster.id),
            description=f"Updated status from {old_status} to {new_status}",
            old_values={'status': old_status},
            new_values={'status': new_status},
        )
        
        return Response({'status': 'updated'})
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        disaster = self.get_object()
        data_points = DisasterData.objects.filter(event=disaster).order_by('timestamp')
        
        analytics = {
            'total_data_points': data_points.count(),
            'avg_value': sum(d.value for d in data_points) / max(data_points.count(), 1),
            'data_types': list(set(d.data_type for d in data_points)),
        }
        
        return Response(analytics)


class DisasterDataViewSet(viewsets.ModelViewSet):
    queryset = DisasterData.objects.all()
    serializer_class = DisasterDataSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['event', 'data_type', 'source']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class RiskModelViewSet(viewsets.ModelViewSet):
    queryset = RiskModel.objects.all()
    serializer_class = RiskModelSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['disaster_type', 'is_active']
    search_fields = ['name']
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        model = self.get_object()
        RiskModel.objects.filter(disaster_type=model.disaster_type).update(is_active=False)
        model.is_active = True
        model.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='model_change',
            resource_type='RiskModel',
            resource_id=str(model.id),
            description=f"Activated risk model: {model.name}",
        )
        
        return Response({'status': 'activated'})


class HistoricalDisasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricalDisaster.objects.all()
    serializer_class = HistoricalDisasterSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['disaster_type']
    search_fields = ['location_name']
    ordering_fields = ['occurrence_date']
    ordering = ['-occurrence_date']

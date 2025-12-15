from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert, AlertDispatch, AlertThreshold, NotificationPreference
from .serializers import AlertSerializer, AlertDispatchSerializer, AlertThresholdSerializer, NotificationPreferenceSerializer
from core.models import AuditLog
import logging

logger = logging.getLogger(__name__)

@login_required
def alerts_view(request):
    context = {
        'user_role': request.user.role,
    }
    return render(request, 'alerts/alerts.html', context)


@login_required
def alert_details_view(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        context = {
            'alert': alert,
            'user_role': request.user.role,
        }
        return render(request, 'alerts/alert_details.html', context)
    except Alert.DoesNotExist:
        return render(request, 'errors/404.html', status=404)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['severity', 'status', 'disaster_event']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        alerts = Alert.objects.filter(status='pending')
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        alerts = Alert.objects.filter(severity='critical')
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'acknowledged'
        alert.acknowledged_by = request.user
        alert.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='alert_dispatch',
            resource_type='Alert',
            resource_id=str(alert.id),
            description=f"Acknowledged alert: {alert.title}",
        )
        
        return Response({'status': 'acknowledged'})
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'resolved'
        alert.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='alert_dispatch',
            resource_type='Alert',
            resource_id=str(alert.id),
            description=f"Resolved alert: {alert.title}",
        )
        
        return Response({'status': 'resolved'})


class AlertDispatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertDispatch.objects.all()
    serializer_class = AlertDispatchSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['alert', 'recipient', 'channel', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return AlertDispatch.objects.all()
        return AlertDispatch.objects.filter(recipient=self.request.user)


class AlertThresholdViewSet(viewsets.ModelViewSet):
    queryset = AlertThreshold.objects.all()
    serializer_class = AlertThresholdSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['disaster_type', 'is_active']
    
    def perform_create(self, serializer):
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='AlertThreshold',
            resource_id=str(serializer.instance.id),
            description=f"Created alert threshold for {serializer.instance.disaster_type}",
            new_values=serializer.data,
        )
    
    def perform_update(self, serializer):
        old_values = AlertThreshold.objects.get(id=serializer.instance.id).__dict__
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='AlertThreshold',
            resource_id=str(serializer.instance.id),
            description=f"Updated alert threshold for {serializer.instance.disaster_type}",
            old_values=old_values,
            new_values=serializer.data,
        )


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return NotificationPreference.objects.all()
        return NotificationPreference.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put'])
    def my_preferences(self, request):
        try:
            preference = NotificationPreference.objects.get(user=request.user)
        except NotificationPreference.DoesNotExist:
            preference = NotificationPreference.objects.create(user=request.user)
        
        if request.method == 'PUT':
            serializer = self.get_serializer(preference, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        serializer = self.get_serializer(preference)
        return Response(serializer.data)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DisasterAnalytics, AlertAnalytics, UserActivityLog, SystemMetrics
from .serializers import DisasterAnalyticsSerializer, AlertAnalyticsSerializer, UserActivityLogSerializer, SystemMetricsSerializer
from django.db.models import Sum, Avg, Count
from datetime import timedelta
from django.utils import timezone

@login_required
def analytics_dashboard_view(request):
    context = {
        'user_role': request.user.role,
    }
    return render(request, 'analytics/analytics_dashboard.html', context)


class DisasterAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DisasterAnalytics.objects.all()
    serializer_class = DisasterAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['disaster_type', 'date']
    ordering_fields = ['date']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        analytics = DisasterAnalytics.objects.filter(date__gte=start_date)
        
        summary = {
            'total_events': analytics.aggregate(Sum('total_events'))['total_events__sum'] or 0,
            'high_risk_events': analytics.aggregate(Sum('high_risk_events'))['high_risk_events__sum'] or 0,
            'avg_risk_score': analytics.aggregate(Avg('avg_risk_score'))['avg_risk_score__avg'] or 0,
            'total_affected_population': analytics.aggregate(Sum('total_affected_population'))['total_affected_population__sum'] or 0,
            'total_estimated_damage': analytics.aggregate(Sum('total_estimated_damage'))['total_estimated_damage__sum'] or 0,
        }
        
        return Response(summary)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        analytics = DisasterAnalytics.objects.filter(date__gte=start_date).values('disaster_type').annotate(
            total_events=Sum('total_events'),
            high_risk_events=Sum('high_risk_events'),
            avg_risk_score=Avg('avg_risk_score'),
        )
        
        return Response(analytics)


class AlertAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertAnalytics.objects.all()
    serializer_class = AlertAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['date']
    ordering_fields = ['date']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        analytics = AlertAnalytics.objects.filter(date__gte=start_date)
        
        summary = {
            'total_alerts': analytics.aggregate(Sum('total_alerts'))['total_alerts__sum'] or 0,
            'critical_alerts': analytics.aggregate(Sum('critical_alerts'))['critical_alerts__sum'] or 0,
            'high_alerts': analytics.aggregate(Sum('high_alerts'))['high_alerts__sum'] or 0,
            'avg_response_time': analytics.aggregate(Avg('avg_response_time_minutes'))['avg_response_time_minutes__avg'] or 0,
            'avg_acknowledgment_rate': analytics.aggregate(Avg('acknowledgment_rate'))['acknowledgment_rate__avg'] or 0,
        }
        
        return Response(summary)


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'activity_type']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return UserActivityLog.objects.all()
        return UserActivityLog.objects.filter(user=self.request.user)


class SystemMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_metrics = SystemMetrics.objects.latest('timestamp')
        serializer = self.get_serializer(latest_metrics)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        latest = SystemMetrics.objects.latest('timestamp')
        
        health = {
            'status': 'healthy' if latest.cpu_usage_percent < 80 and latest.memory_usage_percent < 80 else 'warning',
            'cpu_usage': latest.cpu_usage_percent,
            'memory_usage': latest.memory_usage_percent,
            'api_response_time': latest.api_response_time_ms,
            'active_users': latest.active_users,
        }
        
        return Response(health)

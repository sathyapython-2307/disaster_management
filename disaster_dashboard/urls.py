from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.views import CustomUserViewSet, AuditLogViewSet, GeofenceViewSet, DataSourceViewSet, login_view, register_view, logout_view, dashboard_view, governance_view
from disasters.views import DisasterEventViewSet, DisasterDataViewSet, RiskModelViewSet, HistoricalDisasterViewSet, disasters_map_view, disaster_details_view
from alerts.views import AlertViewSet, AlertDispatchViewSet, AlertThresholdViewSet, NotificationPreferenceViewSet, alerts_view, alert_details_view
from analytics.views import DisasterAnalyticsViewSet, AlertAnalyticsViewSet, UserActivityLogViewSet, SystemMetricsViewSet, analytics_dashboard_view
from governance.views import RolePermissionViewSet, PolicyConfigurationViewSet, ComplianceLogViewSet, DataRetentionPolicyViewSet, governance_dashboard_view
from core.csrf_views import csrf_failure

# API Router
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'geofences', GeofenceViewSet, basename='geofence')
router.register(r'data-sources', DataSourceViewSet, basename='data-source')
router.register(r'disasters', DisasterEventViewSet, basename='disaster')
router.register(r'disaster-data', DisasterDataViewSet, basename='disaster-data')
router.register(r'risk-models', RiskModelViewSet, basename='risk-model')
router.register(r'historical-disasters', HistoricalDisasterViewSet, basename='historical-disaster')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'alert-dispatches', AlertDispatchViewSet, basename='alert-dispatch')
router.register(r'alert-thresholds', AlertThresholdViewSet, basename='alert-threshold')
router.register(r'notification-preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'disaster-analytics', DisasterAnalyticsViewSet, basename='disaster-analytics')
router.register(r'alert-analytics', AlertAnalyticsViewSet, basename='alert-analytics')
router.register(r'user-activity', UserActivityLogViewSet, basename='user-activity')
router.register(r'system-metrics', SystemMetricsViewSet, basename='system-metrics')
router.register(r'role-permissions', RolePermissionViewSet, basename='role-permission')
router.register(r'policies', PolicyConfigurationViewSet, basename='policy')
router.register(r'compliance-logs', ComplianceLogViewSet, basename='compliance-log')
router.register(r'retention-policies', DataRetentionPolicyViewSet, basename='retention-policy')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard_alt'),
    
    # Disasters
    path('disasters/', disasters_map_view, name='disasters_map'),
    path('disasters/<uuid:disaster_id>/', disaster_details_view, name='disaster_details'),
    
    # Alerts
    path('alerts/', alerts_view, name='alerts'),
    path('alerts/<uuid:alert_id>/', alert_details_view, name='alert_details'),
    
    # Analytics
    path('analytics/', analytics_dashboard_view, name='analytics'),
    
    # Governance
    path('governance/', governance_dashboard_view, name='governance'),
    path('governance/admin/', governance_view, name='admin_governance'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Custom error handlers for JSON responses
handler403 = 'core.csrf_views.handle_403'
handler404 = 'core.csrf_views.handle_404'
handler500 = 'core.csrf_views.handle_500'
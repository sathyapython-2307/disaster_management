from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import RolePermission, PolicyConfiguration, ComplianceLog, DataRetentionPolicy
from .serializers import RolePermissionSerializer, PolicyConfigurationSerializer, ComplianceLogSerializer, DataRetentionPolicySerializer
from core.models import AuditLog
from core.permissions import require_role, IsAdmin, ADMIN
import logging

logger = logging.getLogger(__name__)

@login_required
@require_role(ADMIN)
def governance_dashboard_view(request):
    context = {
        'user_role': request.user.role,
    }
    return render(request, 'governance/governance_dashboard.html', context)


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['role']
    search_fields = ['permission']
    
    def perform_create(self, serializer):
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            resource_type='RolePermission',
            resource_id=str(serializer.instance.id),
            description=f"Created permission: {serializer.instance.permission} for {serializer.instance.role}",
            new_values=serializer.data,
        )


class PolicyConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PolicyConfiguration.objects.all()
    serializer_class = PolicyConfigurationSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['policy_type', 'is_active']
    search_fields = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='PolicyConfiguration',
            resource_id=str(serializer.instance.id),
            description=f"Created policy: {serializer.instance.name}",
            new_values=serializer.data,
        )
    
    def perform_update(self, serializer):
        old_values = PolicyConfiguration.objects.get(id=serializer.instance.id).__dict__
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='PolicyConfiguration',
            resource_id=str(serializer.instance.id),
            description=f"Updated policy: {serializer.instance.name}",
            old_values=old_values,
            new_values=serializer.data,
        )


class ComplianceLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComplianceLog.objects.all()
    serializer_class = ComplianceLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'status']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ComplianceLog.objects.all()
        return ComplianceLog.objects.filter(user=self.request.user)


class DataRetentionPolicyViewSet(viewsets.ModelViewSet):
    queryset = DataRetentionPolicy.objects.all()
    serializer_class = DataRetentionPolicySerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['data_type', 'is_active']
    
    def perform_create(self, serializer):
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='DataRetentionPolicy',
            resource_id=str(serializer.instance.id),
            description=f"Created retention policy for {serializer.instance.data_type}",
            new_values=serializer.data,
        )
    
    def perform_update(self, serializer):
        old_values = DataRetentionPolicy.objects.get(id=serializer.instance.id).__dict__
        serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='config_change',
            resource_type='DataRetentionPolicy',
            resource_id=str(serializer.instance.id),
            description=f"Updated retention policy for {serializer.instance.data_type}",
            old_values=old_values,
            new_values=serializer.data,
        )

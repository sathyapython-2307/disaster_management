from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, AuditLog, SystemConfiguration, Geofence, DataSource
from .serializers import CustomUserSerializer, AuditLogSerializer, GeofenceSerializer, DataSourceSerializer
from .permissions import require_role, require_permission, IsAdmin, ADMIN, ANALYST, RESPONDER, PUBLIC
import logging

logger = logging.getLogger(__name__)

# Authentication Views
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in successfully")
            return redirect('dashboard')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'auth/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Username already exists'})
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='public'
        )
        logger.info(f"New user registered: {username}")
        return redirect('login')
    
    return render(request, 'auth/register.html')


@login_required
def logout_view(request):
    logger.info(f"User {request.user.username} logged out")
    logout(request)
    return redirect('login')


# Dashboard Views
@login_required
def dashboard_view(request):
    context = {
        'user_role': request.user.role,
    }
    
    if request.user.role == 'admin':
        return render(request, 'dashboard/admin_dashboard.html', context)
    elif request.user.role == 'analyst':
        return render(request, 'dashboard/analyst_dashboard.html', context)
    elif request.user.role == 'responder':
        return render(request, 'dashboard/responder_dashboard.html', context)
    else:
        return render(request, 'dashboard/public_dashboard.html', context)


@login_required
@require_role(ADMIN)
def governance_view(request):
    users = CustomUser.objects.all()
    geofences = Geofence.objects.all()
    data_sources = DataSource.objects.all()
    
    context = {
        'users': users,
        'geofences': geofences,
        'data_sources': data_sources,
    }
    return render(request, 'governance/admin_governance.html', context)


# REST API ViewSets
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == ADMIN:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'change_role']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        user = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            resource_type='User',
            resource_id=str(user.id),
            description=f"Created user: {user.username}",
            new_values={'username': user.username, 'email': user.email, 'role': user.role},
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_update(self, serializer):
        old_values = CustomUser.objects.get(id=serializer.instance.id).__dict__
        user = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='update',
            resource_type='User',
            resource_id=str(user.id),
            description=f"Updated user: {user.username}",
            old_values={'role': old_values.get('role')},
            new_values={'role': user.role},
            ip_address=self.get_client_ip(self.request)
        )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def change_role(self, request, pk=None):
        
        user = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in dict(CustomUser.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = new_role
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='update',
            resource_type='User',
            resource_id=str(user.id),
            description=f"Changed role to {new_role}",
            new_values={'role': new_role},
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'status': 'role changed'})
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['action', 'resource_type', 'user']
    search_fields = ['description', 'resource_id']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return AuditLog.objects.all()
        return AuditLog.objects.filter(user=self.request.user)


class GeofenceViewSet(viewsets.ModelViewSet):
    queryset = Geofence.objects.all()
    serializer_class = GeofenceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            resource_type='Geofence',
            resource_id=str(serializer.instance.id),
            description=f"Created geofence: {serializer.instance.name}",
            new_values=serializer.data,
        )


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['source_type', 'is_active']
    search_fields = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            resource_type='DataSource',
            resource_id=str(serializer.instance.id),
            description=f"Created data source: {serializer.instance.name}",
            new_values=serializer.data,
        )
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Handle file uploads for data sources"""
        import os
        import uuid
        from django.conf import settings
        
        try:
            # Check if file is provided
            if 'file' not in request.FILES:
                logger.warning("File upload attempted without file")
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            uploaded_file = request.FILES['file']
            source_type = request.data.get('source_type', 'file')
            
            logger.info(f"Processing file upload: {uploaded_file.name}, type: {source_type}")
            
            # Validate file type
            allowed_extensions = ['.csv', '.json', '.xml', '.txt']
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext not in allowed_extensions:
                logger.warning(f"Invalid file type: {file_ext}")
                return Response(
                    {'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'data_sources')
            os.makedirs(upload_dir, exist_ok=True)
            logger.info(f"Upload directory ready: {upload_dir}")
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}{file_ext}"
            file_full_path = os.path.join(upload_dir, filename)
            
            # Save file directly to disk
            logger.info(f"Saving file to: {file_full_path}")
            with open(file_full_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            # Store relative path for database
            file_path = os.path.join('uploads', 'data_sources', filename)
            logger.info(f"File saved successfully: {file_path}")
            
            # Log the upload - wrap in try-except to not fail if audit log fails
            try:
                AuditLog.objects.create(
                    user=request.user,
                    action='create',
                    resource_type='FileUpload',
                    resource_id=filename,
                    description=f"Uploaded file: {uploaded_file.name}",
                    new_values={'original_name': uploaded_file.name, 'file_path': file_path},
                    ip_address=self.get_client_ip(request)
                )
                logger.info(f"Audit log created for file: {filename}")
            except Exception as audit_error:
                logger.warning(f"Failed to create audit log: {str(audit_error)}")
            
            return Response({
                'file_path': file_path,
                'original_name': uploaded_file.name,
                'size': uploaded_file.size
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"File upload error: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Sync a specific data source"""
        from core.data_sync import DataSyncManager
        
        try:
            data_source = self.get_object()
            
            if not data_source.file_path:
                return Response(
                    {'error': 'This data source has no file path'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.info(f"Syncing data source: {data_source.name}")
            processed, errors = DataSyncManager.sync_data_source(data_source, request.user)
            
            if errors:
                return Response({
                    'status': 'partial',
                    'processed': processed,
                    'errors': errors,
                    'message': f'Synced {processed} records with {len(errors)} errors'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'success',
                    'processed': processed,
                    'message': f'Successfully synced {processed} records'
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error syncing data source: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def sync_all(self, request):
        """Sync all active data sources"""
        from core.data_sync import DataSyncManager
        
        try:
            logger.info("Starting sync of all active data sources")
            results = DataSyncManager.sync_all_active_sources(request.user)
            
            return Response({
                'status': 'completed',
                'results': results
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error syncing all data sources: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

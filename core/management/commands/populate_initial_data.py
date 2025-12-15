from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from alerts.models import AlertThreshold
from governance.models import RolePermission, DataRetentionPolicy

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate initial data for the disaster dashboard'

    def handle(self, *args, **options):
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create sample users
        roles = ['analyst', 'responder', 'public']
        for role in roles:
            if not User.objects.filter(username=f'{role}_user').exists():
                User.objects.create_user(
                    username=f'{role}_user',
                    email=f'{role}@example.com',
                    password='password123',
                    role=role,
                    first_name=role.capitalize(),
                    last_name='User'
                )
                self.stdout.write(self.style.SUCCESS(f'Created {role} user'))

        # Create alert thresholds
        thresholds = [
            {'disaster_type': 'flood', 'risk_score_threshold': 60, 'confidence_threshold': 70},
            {'disaster_type': 'earthquake', 'risk_score_threshold': 70, 'confidence_threshold': 75},
            {'disaster_type': 'cyclone', 'risk_score_threshold': 65, 'confidence_threshold': 72},
            {'disaster_type': 'wildfire', 'risk_score_threshold': 55, 'confidence_threshold': 68},
        ]

        for threshold in thresholds:
            if not AlertThreshold.objects.filter(disaster_type=threshold['disaster_type']).exists():
                AlertThreshold.objects.create(
                    disaster_type=threshold['disaster_type'],
                    risk_score_threshold=threshold['risk_score_threshold'],
                    confidence_threshold=threshold['confidence_threshold'],
                    notification_channels=['email', 'push', 'in_app'],
                    recipient_roles=['admin', 'analyst', 'responder']
                )
                self.stdout.write(self.style.SUCCESS(f'Created alert threshold for {threshold["disaster_type"]}'))

        # Create role permissions
        permissions = [
            {'role': 'admin', 'permission': 'manage_users'},
            {'role': 'admin', 'permission': 'manage_system'},
            {'role': 'admin', 'permission': 'view_audit_logs'},
            {'role': 'analyst', 'permission': 'view_disasters'},
            {'role': 'analyst', 'permission': 'view_analytics'},
            {'role': 'analyst', 'permission': 'export_reports'},
            {'role': 'responder', 'permission': 'view_disasters'},
            {'role': 'responder', 'permission': 'acknowledge_alerts'},
            {'role': 'responder', 'permission': 'manage_incidents'},
            {'role': 'public', 'permission': 'view_public_alerts'},
        ]

        for perm in permissions:
            if not RolePermission.objects.filter(role=perm['role'], permission=perm['permission']).exists():
                RolePermission.objects.create(
                    role=perm['role'],
                    permission=perm['permission']
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))

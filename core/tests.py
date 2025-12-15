from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AuditLog, Geofence, DataSource

User = get_user_model()

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='analyst'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'analyst')

    def test_user_str(self):
        self.assertIn('Analyst', str(self.user))

class AuditLogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            user=self.user,
            action='create',
            resource_type='TestResource',
            resource_id='123',
            description='Test action'
        )
        self.assertEqual(log.action, 'create')
        self.assertEqual(log.resource_type, 'TestResource')

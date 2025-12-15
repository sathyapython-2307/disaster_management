"""
Management command to sync uploaded data sources
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from core.models import DataSource
from core.data_sync import DataSyncManager
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync uploaded data sources to disaster events'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source-id',
            type=str,
            help='Sync specific data source by ID'
        )
        parser.add_argument(
            '--source-name',
            type=str,
            help='Sync specific data source by name'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sync all active data sources (respects sync intervals)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync regardless of sync interval'
        )
        parser.add_argument(
            '--user',
            type=str,
            default='admin',
            help='Username to attribute sync action to (default: admin)'
        )
    
    def handle(self, *args, **options):
        # Get user for audit logging
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"User {options['user']} not found, syncing without audit logging")
            )
            user = None
        
        # Determine what to sync
        if options['all']:
            self.stdout.write(self.style.SUCCESS('Syncing all active data sources...'))
            results = DataSyncManager.sync_all_active_sources(user)
            self._print_results(results)
        
        elif options['source_id']:
            try:
                source = DataSource.objects.get(id=options['source_id'])
                self.stdout.write(f"Syncing: {source.name}")
                processed, errors = DataSyncManager.sync_data_source(source, user)
                self._print_sync_result(source.name, processed, errors)
            except DataSource.DoesNotExist:
                raise CommandError(f"Data source with ID {options['source_id']} not found")
        
        elif options['source_name']:
            try:
                source = DataSource.objects.get(name=options['source_name'])
                self.stdout.write(f"Syncing: {source.name}")
                processed, errors = DataSyncManager.sync_data_source(source, user)
                self._print_sync_result(source.name, processed, errors)
            except DataSource.DoesNotExist:
                raise CommandError(f"Data source with name {options['source_name']} not found")
        
        else:
            # Show available sources
            sources = DataSource.objects.filter(is_active=True)
            if not sources.exists():
                self.stdout.write(self.style.WARNING('No active data sources found'))
                return
            
            self.stdout.write(self.style.SUCCESS('Available data sources:'))
            self.stdout.write('-' * 80)
            for source in sources:
                sync_status = 'Never' if not source.last_sync else source.last_sync.strftime('%Y-%m-%d %H:%M:%S')
                self.stdout.write(
                    f"  {source.name:<40} | Type: {source.source_type:<10} | Last sync: {sync_status}"
                )
            self.stdout.write('-' * 80)
            self.stdout.write(
                self.style.WARNING('Use --source-id, --source-name, or --all to sync specific sources')
            )
    
    def _print_sync_result(self, name: str, processed: int, errors: list):
        """Print sync result for a single source"""
        if errors:
            self.stdout.write(
                self.style.ERROR(f"Sync failed for {name}: {len(errors)} errors")
            )
            for error in errors[:5]:  # Show first 5 errors
                self.stdout.write(f"  - {error}")
            if len(errors) > 5:
                self.stdout.write(f"  ... and {len(errors) - 5} more errors")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully synced {name}: {processed} records processed")
            )
    
    def _print_results(self, results: dict):
        """Print overall sync results"""
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('SYNC RESULTS'))
        self.stdout.write('=' * 80)
        self.stdout.write(f"Total sources: {results['total_sources']}")
        self.stdout.write(f"Synced: {self.style.SUCCESS(str(results['synced']))}")
        self.stdout.write(f"Failed: {self.style.ERROR(str(results['failed']))}")
        self.stdout.write(f"Skipped: {results['skipped']}")
        
        if results['details']:
            self.stdout.write('\nDetails:')
            self.stdout.write('-' * 80)
            for detail in results['details']:
                if detail['status'] == 'success':
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ {detail['source']}: {detail['processed']} records")
                    )
                elif detail['status'] == 'failed':
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ {detail['source']}: {detail['processed']} records, {len(detail['errors'])} errors")
                    )
                elif detail['status'] == 'skipped':
                    self.stdout.write(f"  - {detail['source']}: {detail['reason']}")
                else:
                    self.stdout.write(f"  ? {detail['source']}: {detail.get('error', 'Unknown error')}")
        
        self.stdout.write('=' * 80 + '\n')

from django.core.management.base import BaseCommand
from django.db import transaction
from web.models import WebFarsl, WebMcust, WebPcust
import os


class Command(BaseCommand):
    help = 'Migrate data from backup SQL file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', 
            type=str, 
            default='backup.sql',
            help='Path to backup SQL file'
        )

    def handle(self, *args, **options):
        backup_file = options['file']
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'Backup file {backup_file} not found')
            )
            return

        self.stdout.write('Starting data migration...')
        
        try:
            with transaction.atomic():
                self.migrate_farsl_data()
                self.migrate_mcust_data()
                self.migrate_pcust_data()
                
            self.stdout.write(
                self.style.SUCCESS('Data migration completed successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Migration failed: {str(e)}')
            )

    def migrate_farsl_data(self):
        """Migrate web_farsl data"""
        # This data would be migrated based on the SQL dump
        farsl_data = [
            (-6800, '__INT on LOAN-FINANCIAL ASSISTANCE'),
            (-6750, '__INT on LOAN-TRAVEL'),
            (-6700, '__INT on LOAN-AGRICULTURAL'),
            # Add more data from your backup.sql
        ]
        
        self.stdout.write('Migrating FARSL data...')
        for fid, fname in farsl_data:
            WebFarsl.objects.get_or_create(
                fID=fid,
                defaults={'fname': fname}
            )

    def migrate_mcust_data(self):
        """Migrate web_mcust data"""
        self.stdout.write('Migrating MCUST data...')
        # Add logic based on your web_mcust table structure

    def migrate_pcust_data(self):
        """Migrate web_pcust data"""
        self.stdout.write('Migrating PCUST data...')
        # Add logic based on your web_pcust table structure

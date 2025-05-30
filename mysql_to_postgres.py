#!/usr/bin/env python
"""
MySQL to PostgreSQL data migration script
"""
import os
import json
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from web.models import WebFarsl, WebMcust, WebPcust
from django.db import transaction

def migrate_mysql_to_postgres():
    """
    Migrate data from MySQL fixtures to PostgreSQL
    """
    print("Starting MySQL to PostgreSQL migration...")
    
    # List of fixture files to load
    fixture_files = [
        "farsl_fixtures.json",
        "mcust_fixtures.json",
        "pcust_fixtures_1.json",
        "pcust_fixtures_2.json",
        "pcust_fixtures_3.json",
        "pcust_fixtures_4.json",
        "pcust_fixtures_5.json",
        "pcust_fixtures_6.json",
        "pcust_fixtures_7.json",
        "pcust_fixtures_8.json",
        "pcust_fixtures_9.json",
    ]
    
    total_objects = 0
    
    with transaction.atomic():
        for fixture_file in fixture_files:
            if os.path.exists(fixture_file):
                print(f"Loading {fixture_file}...")
                
                with open(fixture_file, 'r', encoding='utf-8') as f:
                    fixtures = json.load(f)
                
                for fixture in fixtures:
                    model_name = fixture['model']
                    pk = fixture['pk']
                    fields = fixture['fields']
                    
                    try:
                        if model_name == 'web.webfarsl':
                            obj, created = WebFarsl.objects.get_or_create(
                                fid=pk,
                                defaults=fields
                            )
                            if created:
                                total_objects += 1
                                
                        elif model_name == 'web.webmcust':
                            obj, created = WebMcust.objects.get_or_create(
                                fid=pk,
                                defaults=fields
                            )
                            if created:
                                total_objects += 1
                                
                        elif model_name == 'web.webpcust':
                            # Handle foreign key references
                            if fields.get('fcust'):
                                try:
                                    fields['fcust'] = WebMcust.objects.get(fid=fields['fcust'])
                                except WebMcust.DoesNotExist:
                                    print(f"Warning: WebMcust with fid={fields['fcust']} not found")
                                    fields['fcust'] = None
                                    
                            if fields.get('fsl'):
                                try:
                                    fields['fsl'] = WebFarsl.objects.get(fid=fields['fsl'])
                                except WebFarsl.DoesNotExist:
                                    print(f"Warning: WebFarsl with fid={fields['fsl']} not found")
                                    fields['fsl'] = None
                            
                            obj, created = WebPcust.objects.get_or_create(
                                fauto=pk,
                                defaults=fields
                            )
                            if created:
                                total_objects += 1
                                
                    except Exception as e:
                        print(f"Error processing {model_name} with pk={pk}: {e}")
                        continue
                
                print(f"✓ Completed {fixture_file}")
            else:
                print(f"⚠ {fixture_file} not found, skipping...")
    
    print(f"\n✅ Migration completed successfully!")
    print(f"Total objects migrated: {total_objects}")
    print(f"Final counts:")
    print(f"  WebFarsl: {WebFarsl.objects.count()}")
    print(f"  WebMcust: {WebMcust.objects.count()}")
    print(f"  WebPcust: {WebPcust.objects.count()}")

if __name__ == "__main__":
    migrate_mysql_to_postgres()

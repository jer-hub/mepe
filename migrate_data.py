#!/usr/bin/env python
"""
Data migration script for Render deployment
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a command and return True if successful"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Starting data migration...")
    
    # Run migrations
    if not run_command("python manage.py migrate"):
        sys.exit(1)
    
    # Check if data already exists
    result = subprocess.run(
        "python manage.py shell -c \"from web.models import WebFarsl; print(WebFarsl.objects.count())\"",
        shell=True, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        count = result.stdout.strip().split('\n')[-1]
        if int(count) > 0:
            print(f"Data already exists ({count} WebFarsl objects). Skipping migration.")
            return
      # Load data fixtures from repository
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
    
    for filename in fixture_files:
        if os.path.exists(filename):
            print(f"Loading {filename}...")
            if not run_command(f"python manage.py loaddata {filename}"):
                print(f"Failed to load {filename}")
                sys.exit(1)
        else:
            print(f"Warning: {filename} not found, skipping...")
    
    print("Data migration completed successfully!")

if __name__ == "__main__":
    main()

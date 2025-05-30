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
            return    # Load data fixtures using custom migration script
    print("Running data migration from fixtures...")
    if not run_command("python mysql_to_postgres.py"):
        print("Data migration failed")
        sys.exit(1)
    
    print("PostgreSQL data migration completed successfully!")

if __name__ == "__main__":
    main()

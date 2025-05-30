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
    
    # Load data fixtures
    fixture_urls = [
        "https://your-storage-url/farsl_fixtures.json",
        "https://your-storage-url/mcust_fixtures.json",
        "https://your-storage-url/pcust_fixtures_1.json",
        "https://your-storage-url/pcust_fixtures_2.json",
        # Add more URLs as needed
    ]
    
    for url in fixture_urls:
        filename = url.split('/')[-1]
        print(f"Downloading {filename}...")
        
        if run_command(f"curl -o {filename} {url}"):
            print(f"Loading {filename}...")
            if run_command(f"python manage.py loaddata {filename}"):
                run_command(f"rm {filename}")  # Clean up
            else:
                print(f"Failed to load {filename}")
                sys.exit(1)
        else:
            print(f"Failed to download {filename}")
            sys.exit(1)
    
    print("Data migration completed successfully!")

if __name__ == "__main__":
    main()

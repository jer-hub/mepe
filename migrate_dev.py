"""
Development migration script from MySQL to PostgreSQL
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and check for errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting MySQL to PostgreSQL migration")
    
    # Check if PostgreSQL is running
    print("\n📋 Pre-migration checklist:")
    print("1. Ensure PostgreSQL is installed and running")
    print("2. Create database 'mepecoop_web_postgres'")
    print("3. Ensure PostgreSQL user 'postgres' exists with password '1234'")
    
    input("\nPress Enter when ready to continue...")
    
    # Copy environment file
    if not run_command("copy .env.postgres .env", "Setting PostgreSQL environment"):
        return
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running Django migrations"):
        return
    
    # Run data migration
    if not run_command("python mysql_to_postgres.py", "Migrating data from MySQL fixtures"):
        return
    
    # Test the application
    print("\n🧪 Testing the migrated application...")
    result = subprocess.run(
        "python manage.py shell -c \"from web.models import WebFarsl, WebMcust, WebPcust; print(f'WebFarsl: {WebFarsl.objects.count()}'); print(f'WebMcust: {WebMcust.objects.count()}'); print(f'WebPcust: {WebPcust.objects.count()}')\"",
        shell=True, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print("✅ Migration verification successful:")
        print(result.stdout)
    else:
        print("❌ Migration verification failed:")
        print(result.stderr)
        return
    
    print("\n🎉 MySQL to PostgreSQL migration completed successfully!")
    print("\nNext steps:")
    print("1. Test your application: python manage.py runserver")
    print("2. Commit changes: git add . && git commit -m 'Migrate from MySQL to PostgreSQL'")
    print("3. Deploy to Render: git push origin main")

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Test database connection before starting the application
"""
import os
import sys

def test_database():
    print("🗄️  Testing Database Connection...")
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uevent.settings')
        django.setup()
        
        from django.db import connection
        
        # Test connection
        connection.ensure_connection()
        
        # Get database info
        db_name = connection.settings_dict.get('NAME', 'unknown')
        db_user = connection.settings_dict.get('USER', 'unknown')
        db_host = connection.settings_dict.get('HOST', 'unknown')
        
        print(f"✅ Connected to: {db_name}")
        print(f"   User: {db_user}")
        print(f"   Host: {db_host}")
        
        # Test query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Database query test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
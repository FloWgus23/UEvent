#!/bin/bash
set -e

echo "🚀 Starting UEvent Application..."
echo "📊 Environment Check:"
echo "   PORT: ${PORT}"
echo "   RAILWAY_ENVIRONMENT: ${RAILWAY_ENVIRONMENT}"
echo "   DATABASE_URL: ${DATABASE_URL:0:30}..."

echo ""
echo "🔧 Running Django Checks..."

# Test Django configuration
python manage.py check --deploy || {
    echo "❌ Django check failed!"
    exit 1
}

echo "✅ Django configuration OK"

echo ""
echo "🗄️  Testing Database Connection..."

# Test database connection
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uevent.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('✅ Database connection successful')
" || {
    echo "❌ Database connection failed!"
    exit 1
}

echo ""
echo "🌐 Starting Gunicorn..."
echo "   Binding to: 0.0.0.0:${PORT}"
echo "   Workers: 2"
echo "   Timeout: 120s"

exec gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    uevent.wsgi:application
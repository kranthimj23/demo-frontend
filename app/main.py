from flask import Flask, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

# Configuration from environment variables
BACKEND_URL = os.getenv('BACKEND_URL', 'http://demo-backend:8080')
APP_NAME = os.getenv('APP_NAME', 'Demo Frontend')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

# Simple HTML template for the frontend
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .healthy { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .info { background: #d1ecf1; color: #0c5460; }
        .env-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .dev { background: #ffc107; color: #000; }
        .sit { background: #17a2b8; color: #fff; }
        .uat { background: #28a745; color: #fff; }
        .prod { background: #dc3545; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ app_name }}</h1>
        <span class="env-badge {{ environment }}">{{ environment | upper }}</span>
        <div class="status info">
            <strong>Frontend Status:</strong> Running
        </div>
        <div class="status {{ backend_status_class }}">
            <strong>Backend Status:</strong> {{ backend_status }}
        </div>
        <div class="status {{ db_status_class }}">
            <strong>Database Status:</strong> {{ db_status }}
        </div>
        <hr>
        <p><strong>Backend URL:</strong> {{ backend_url }}</p>
        <p><strong>Version:</strong> 1.0.0</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page showing system status"""
    backend_status = "Unknown"
    backend_status_class = "error"
    db_status = "Unknown"
    db_status_class = "error"
    
    try:
        # Check backend health
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            backend_status = "Healthy"
            backend_status_class = "healthy"
    except Exception as e:
        backend_status = f"Unreachable: {str(e)}"
    
    try:
        # Check database status via backend
        response = requests.get(f"{BACKEND_URL}/db/status", timeout=5)
        if response.status_code == 200:
            db_status = "Connected"
            db_status_class = "healthy"
    except Exception as e:
        db_status = f"Unreachable: {str(e)}"
    
    return render_template_string(
        HTML_TEMPLATE,
        app_name=APP_NAME,
        environment=ENVIRONMENT,
        backend_url=BACKEND_URL,
        backend_status=backend_status,
        backend_status_class=backend_status_class,
        db_status=db_status,
        db_status_class=db_status_class
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "demo-frontend"})

@app.route('/ready')
def ready():
    """Readiness check endpoint"""
    return jsonify({"status": "ready", "service": "demo-frontend"})

@app.route('/api/users')
def get_users():
    """Proxy endpoint to get users from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/users", timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items')
def get_items():
    """Proxy endpoint to get items from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/items", timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

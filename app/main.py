from flask import Flask, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

# Configuration from environment variables
BACKEND_URL = os.getenv('BACKEND_URL', 'http://demo-backend:8080')
APP_NAME = os.getenv('APP_NAME', 'Demo Frontend')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

# UI Configuration - These can be changed per environment/release
THEME_COLOR = os.getenv('THEME_COLOR', '#3498db')  # Primary theme color
THEME_NAME = os.getenv('THEME_NAME', 'Blue Theme')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
BUILD_NUMBER = os.getenv('BUILD_NUMBER', '1')

# Banner Configuration
BANNER_ENABLED = os.getenv('BANNER_ENABLED', 'true').lower() == 'true'
BANNER_TEXT = os.getenv('BANNER_TEXT', 'Welcome to Demo Application')
BANNER_COLOR = os.getenv('BANNER_COLOR', '#2c3e50')

# Feature Flags - Toggle features on/off per environment
FEATURE_USER_MANAGEMENT = os.getenv('FEATURE_USER_MANAGEMENT', 'true').lower() == 'true'
FEATURE_ITEM_CATALOG = os.getenv('FEATURE_ITEM_CATALOG', 'true').lower() == 'true'
FEATURE_ANALYTICS = os.getenv('FEATURE_ANALYTICS', 'false').lower() == 'true'
FEATURE_DARK_MODE = os.getenv('FEATURE_DARK_MODE', 'false').lower() == 'true'
FEATURE_NOTIFICATIONS = os.getenv('FEATURE_NOTIFICATIONS', 'false').lower() == 'true'

# Footer Configuration
FOOTER_TEXT = os.getenv('FOOTER_TEXT', 'Demo 3-Tier Application')
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Demo Corp')

# Enhanced HTML template with configurable features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }} - {{ environment | upper }}</title>
    <style>
        :root {
            --theme-color: {{ theme_color }};
            --banner-color: {{ banner_color }};
        }
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 0;
            background: {% if feature_dark_mode %}#1a1a2e{% else %}#f0f2f5{% endif %}; 
            color: {% if feature_dark_mode %}#eee{% else %}#333{% endif %};
            min-height: 100vh;
        }
        .banner {
            background: var(--banner-color);
            color: white;
            padding: 12px 20px;
            text-align: center;
            font-size: 14px;
            display: {% if banner_enabled %}block{% else %}none{% endif %};
        }
        .header {
            background: var(--theme-color);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { margin: 0; font-size: 24px; }
        .header-info { text-align: right; font-size: 12px; }
        .env-badge { 
            display: inline-block; 
            padding: 6px 16px; 
            border-radius: 20px; 
            font-size: 11px; 
            font-weight: bold;
            text-transform: uppercase;
            margin-left: 15px;
        }
        .dev { background: #f39c12; color: #000; }
        .sit { background: #3498db; color: #fff; }
        .uat { background: #27ae60; color: #fff; }
        .prod { background: #e74c3c; color: #fff; }
        .container { 
            max-width: 1200px; 
            margin: 30px auto; 
            padding: 0 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        .card { 
            background: {% if feature_dark_mode %}#16213e{% else %}white{% endif %}; 
            padding: 25px; 
            border-radius: 12px; 
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }
        .card h2 { 
            margin-top: 0; 
            color: var(--theme-color);
            border-bottom: 2px solid var(--theme-color);
            padding-bottom: 10px;
        }
        .status-item { 
            padding: 12px 15px; 
            margin: 10px 0; 
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .healthy { background: {% if feature_dark_mode %}#1e4620{% else %}#d4edda{% endif %}; color: {% if feature_dark_mode %}#7dcea0{% else %}#155724{% endif %}; }
        .error { background: {% if feature_dark_mode %}#4a1c1c{% else %}#f8d7da{% endif %}; color: {% if feature_dark_mode %}#e74c3c{% else %}#721c24{% endif %}; }
        .info { background: {% if feature_dark_mode %}#1a3a4a{% else %}#d1ecf1{% endif %}; color: {% if feature_dark_mode %}#5dade2{% else %}#0c5460{% endif %}; }
        .feature-list { list-style: none; padding: 0; margin: 0; }
        .feature-list li { 
            padding: 10px 15px; 
            margin: 8px 0; 
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {% if feature_dark_mode %}#1a1a2e{% else %}#f8f9fa{% endif %};
        }
        .feature-enabled { color: #27ae60; font-weight: bold; }
        .feature-disabled { color: #95a5a6; }
        .version-info {
            background: {% if feature_dark_mode %}#1a1a2e{% else %}#f8f9fa{% endif %};
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .version-info p { margin: 8px 0; }
        .theme-preview {
            width: 100%;
            height: 40px;
            background: var(--theme-color);
            border-radius: 8px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .config-table {
            width: 100%;
            border-collapse: collapse;
        }
        .config-table td {
            padding: 8px 12px;
            border-bottom: 1px solid {% if feature_dark_mode %}#2c3e50{% else %}#eee{% endif %};
        }
        .config-table td:first-child {
            font-weight: bold;
            width: 40%;
        }
        .footer {
            background: var(--banner-color);
            color: white;
            padding: 20px;
            text-align: center;
            margin-top: 40px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: var(--theme-color);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            margin: 5px;
        }
        .btn:hover { opacity: 0.9; }
        .api-section { margin-top: 20px; }
    </style>
</head>
<body>
    {% if banner_enabled %}
    <div class="banner">
        {{ banner_text }}
    </div>
    {% endif %}
    
    <div class="header">
        <div>
            <h1>{{ app_name }} <span class="env-badge {{ environment }}">{{ environment }}</span></h1>
        </div>
        <div class="header-info">
            <div>Version: {{ app_version }} (Build #{{ build_number }})</div>
            <div>Theme: {{ theme_name }}</div>
        </div>
    </div>
    
    <div class="container">
        <div class="grid">
            <!-- System Status Card -->
            <div class="card">
                <h2>System Status</h2>
                <div class="status-item info">
                    <span><strong>Frontend</strong></span>
                    <span>Running</span>
                </div>
                <div class="status-item {{ backend_status_class }}">
                    <span><strong>Backend</strong></span>
                    <span>{{ backend_status }}</span>
                </div>
                <div class="status-item {{ db_status_class }}">
                    <span><strong>Database</strong></span>
                    <span>{{ db_status }}</span>
                </div>
                
                <div class="api-section">
                    <h3>Quick Actions</h3>
                    {% if feature_user_management %}
                    <a href="/api/users" class="btn">View Users</a>
                    {% endif %}
                    {% if feature_item_catalog %}
                    <a href="/api/items" class="btn">View Items</a>
                    {% endif %}
                </div>
            </div>
            
            <!-- Feature Flags Card -->
            <div class="card">
                <h2>Feature Flags</h2>
                <ul class="feature-list">
                    <li>
                        <span>User Management</span>
                        <span class="{% if feature_user_management %}feature-enabled{% else %}feature-disabled{% endif %}">
                            {% if feature_user_management %}ENABLED{% else %}DISABLED{% endif %}
                        </span>
                    </li>
                    <li>
                        <span>Item Catalog</span>
                        <span class="{% if feature_item_catalog %}feature-enabled{% else %}feature-disabled{% endif %}">
                            {% if feature_item_catalog %}ENABLED{% else %}DISABLED{% endif %}
                        </span>
                    </li>
                    <li>
                        <span>Analytics Dashboard</span>
                        <span class="{% if feature_analytics %}feature-enabled{% else %}feature-disabled{% endif %}">
                            {% if feature_analytics %}ENABLED{% else %}DISABLED{% endif %}
                        </span>
                    </li>
                    <li>
                        <span>Dark Mode</span>
                        <span class="{% if feature_dark_mode %}feature-enabled{% else %}feature-disabled{% endif %}">
                            {% if feature_dark_mode %}ENABLED{% else %}DISABLED{% endif %}
                        </span>
                    </li>
                    <li>
                        <span>Notifications</span>
                        <span class="{% if feature_notifications %}feature-enabled{% else %}feature-disabled{% endif %}">
                            {% if feature_notifications %}ENABLED{% else %}DISABLED{% endif %}
                        </span>
                    </li>
                </ul>
            </div>
            
            <!-- Theme & Configuration Card -->
            <div class="card">
                <h2>Theme & Configuration</h2>
                <div class="theme-preview">{{ theme_name }}</div>
                <table class="config-table">
                    <tr><td>Theme Color</td><td>{{ theme_color }}</td></tr>
                    <tr><td>Banner Color</td><td>{{ banner_color }}</td></tr>
                    <tr><td>Banner Enabled</td><td>{% if banner_enabled %}Yes{% else %}No{% endif %}</td></tr>
                    <tr><td>Company</td><td>{{ company_name }}</td></tr>
                </table>
            </div>
            
            <!-- Version & Build Info Card -->
            <div class="card">
                <h2>Release Information</h2>
                <div class="version-info">
                    <table class="config-table">
                        <tr><td>Application</td><td>{{ app_name }}</td></tr>
                        <tr><td>Version</td><td>{{ app_version }}</td></tr>
                        <tr><td>Build Number</td><td>{{ build_number }}</td></tr>
                        <tr><td>Environment</td><td>{{ environment | upper }}</td></tr>
                        <tr><td>Backend URL</td><td>{{ backend_url }}</td></tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>{{ footer_text }} | {{ company_name }} | Environment: {{ environment | upper }}</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page showing system status and configuration"""
    backend_status = "Unknown"
    backend_status_class = "error"
    db_status = "Unknown"
    db_status_class = "error"
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            backend_status = "Healthy"
            backend_status_class = "healthy"
    except Exception as e:
        backend_status = f"Unreachable"
    
    try:
        response = requests.get(f"{BACKEND_URL}/db/status", timeout=5)
        if response.status_code == 200:
            db_status = "Connected"
            db_status_class = "healthy"
    except Exception as e:
        db_status = f"Unreachable"
    
    return render_template_string(
        HTML_TEMPLATE,
        app_name=APP_NAME,
        environment=ENVIRONMENT,
        backend_url=BACKEND_URL,
        backend_status=backend_status,
        backend_status_class=backend_status_class,
        db_status=db_status,
        db_status_class=db_status_class,
        # Theme configuration
        theme_color=THEME_COLOR,
        theme_name=THEME_NAME,
        banner_color=BANNER_COLOR,
        # Banner configuration
        banner_enabled=BANNER_ENABLED,
        banner_text=BANNER_TEXT,
        # Version info
        app_version=APP_VERSION,
        build_number=BUILD_NUMBER,
        # Feature flags
        feature_user_management=FEATURE_USER_MANAGEMENT,
        feature_item_catalog=FEATURE_ITEM_CATALOG,
        feature_analytics=FEATURE_ANALYTICS,
        feature_dark_mode=FEATURE_DARK_MODE,
        feature_notifications=FEATURE_NOTIFICATIONS,
        # Footer
        footer_text=FOOTER_TEXT,
        company_name=COMPANY_NAME
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "demo-frontend",
        "version": APP_VERSION,
        "build": BUILD_NUMBER,
        "environment": ENVIRONMENT
    })

@app.route('/ready')
def ready():
    """Readiness check endpoint"""
    return jsonify({"status": "ready", "service": "demo-frontend"})

@app.route('/config')
def config():
    """Return current configuration"""
    return jsonify({
        "app_name": APP_NAME,
        "environment": ENVIRONMENT,
        "version": APP_VERSION,
        "build_number": BUILD_NUMBER,
        "theme": {
            "color": THEME_COLOR,
            "name": THEME_NAME,
            "banner_color": BANNER_COLOR
        },
        "banner": {
            "enabled": BANNER_ENABLED,
            "text": BANNER_TEXT
        },
        "features": {
            "user_management": FEATURE_USER_MANAGEMENT,
            "item_catalog": FEATURE_ITEM_CATALOG,
            "analytics": FEATURE_ANALYTICS,
            "dark_mode": FEATURE_DARK_MODE,
            "notifications": FEATURE_NOTIFICATIONS
        }
    })

@app.route('/api/users')
def get_users():
    """Proxy endpoint to get users from backend"""
    if not FEATURE_USER_MANAGEMENT:
        return jsonify({"error": "User Management feature is disabled"}), 403
    try:
        response = requests.get(f"{BACKEND_URL}/api/users", timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items')
def get_items():
    """Proxy endpoint to get items from backend"""
    if not FEATURE_ITEM_CATALOG:
        return jsonify({"error": "Item Catalog feature is disabled"}), 403
    try:
        response = requests.get(f"{BACKEND_URL}/api/items", timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
import mysql.connector
from mysql.connector import Error
import os
import time

app = Flask(__name__, static_folder='../static', template_folder='../Template')
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database Configuration for Docker
db_host = os.getenv("DB_HOST", "mysql")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "rootpassword")
db_name = os.getenv("DB_NAME", "mywebsite")

print("="*50)
print("🔧 DATABASE CONFIGURATION")
print("="*50)
print(f"Host: {db_host}")
print(f"User: {db_user}")
print(f"Database: {db_name}")
print("="*50)

# Global database connection
db = None
cursor = None

def init_database(max_retries=10, retry_delay=5):
    """Initialize database connection with retry logic for Docker startup"""
    global db, cursor
    
    for attempt in range(max_retries):
        try:
            print(f"\n🔄 Connection Attempt {attempt + 1}/{max_retries}")
            print(f"   Connecting to: {db_user}@{db_host}")
            
            # Connect to MySQL server (without database first)
            db = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                connect_timeout=30,
                autocommit=True
            )
            
            cursor = db.cursor(buffered=True)
            print("✅ Connected to MySQL server!")
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            print(f"✅ Database '{db_name}' created/verified")
            
            # Close and reconnect with database selected
            cursor.close()
            db.close()
            
            # Reconnect with database
            db = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                connect_timeout=30,
                autocommit=True
            )
            cursor = db.cursor(buffered=True)
            print(f"✅ Connected to database '{db_name}'")
            
            # Create table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contact_queries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Table 'contact_queries' created/verified")
            
            # Test query
            cursor.execute("SELECT COUNT(*) FROM contact_queries")
            count = cursor.fetchone()[0]
            print(f"✅ Database ready! Current submissions: {count}")
            print("="*50)
            
            return True
            
        except Error as e:
            print(f"❌ Connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print("❌ All connection attempts exhausted!")
                return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                return False
    
    return False

# Initialize database on startup
print("\n🚀 Starting Flask Application...")
if not init_database():
    print("\n⚠️  WARNING: Database initialization failed!")
    print("⚠️  Application will start but database features won't work.")
else:
    print("\n🎉 Application started successfully!")

# Routes
@app.route('/')
def index():
    """Serve the main landing page"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"❌ Error serving index.html: {e}")
        return f"Error: {e}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        if db and db.is_connected():
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.execute("SELECT COUNT(*) FROM contact_queries")
            count = cursor.fetchone()[0]
            return {
                "status": "healthy",
                "database": "connected",
                "submissions": count
            }, 200
        else:
            return {"status": "unhealthy", "database": "disconnected"}, 503
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503

@app.route('/submit', methods=['POST'])
def submit():
    """Handle contact form submission"""
    if not db or not db.is_connected():
        print("❌ Database not connected")
        flash('Service temporarily unavailable. Please try again later.', 'error')
        return redirect('/')
    
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        
        print(f"\n📝 New submission received:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Phone: {phone}")
        
        # Validation
        if not name or not email or not message:
            print("❌ Validation failed: Missing required fields")
            flash('Please fill in all required fields.', 'error')
            return redirect('/')
        
        if '@' not in email or '.' not in email:
            print("❌ Validation failed: Invalid email")
            flash('Please enter a valid email address.', 'error')
            return redirect('/')
        
        # Insert into database
        sql = "INSERT INTO contact_queries (name, email, phone, message) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, message)
        
        cursor.execute(sql, values)
        db.commit()
        
        print(f"✅ Submission saved successfully! ID: {cursor.lastrowid}")
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect('/')
        
    except Error as e:
        print(f"❌ Database error: {e}")
        db.rollback()
        flash('Error submitting form. Please try again.', 'error')
        return redirect('/')
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect('/')

@app.route('/admin')
def admin():
    """Admin panel to view submissions"""
    if not db or not db.is_connected():
        return "Database not connected", 503
    
    try:
        cursor.execute("""
            SELECT name, email, phone, message, created_at 
            FROM contact_queries 
            ORDER BY created_at DESC
        """)
        results = cursor.fetchall()
        print(f"✅ Admin panel loaded: {len(results)} submissions")
        return render_template('admin.html', queries=results)
    except Error as e:
        print(f"❌ Error loading admin panel: {e}")
        return f"Database error: {str(e)}", 500

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Cleanup
@app.teardown_appcontext
def close_connection(exception):
    """Close database connection on shutdown"""
    global db, cursor
    if cursor:
        cursor.close()
    if db and db.is_connected():
        db.close()
        print("🔌 Database connection closed")



if __name__ == '__main__':
    print("\n🌐 Starting Flask server on http://0.0.0.0:5000")
    print("📊 Admin panel: http://localhost:5000/admin")
    print("❤️  Health check: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=True)
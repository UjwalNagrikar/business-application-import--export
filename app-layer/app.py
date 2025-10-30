from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error
import os 

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

db_host = os.getenv("DB_HOST", "mysql")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "rootpassword")
db_name = os.getenv("DB_NAME", "mywebsite")

try:
    # Connect to MySQL server
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )
    cursor = db.cursor()
    print("✅ Connected to MySQL container successfully!")

    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"✅ Database '{db_name}' is ready!")

    # Switch to database
    db.database = db_name
    print(f"✅ Connected to DB '{db_name}'")

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_queries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(50),
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Table 'contact_queries' ready!")

except Error as e:
    print("❌ MySQL connection or setup failed:", e)

# Flask routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
            return redirect("/")

        sql = "INSERT INTO contact_queries (name, email, phone, message) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, message)

        cursor.execute(sql, values)
        db.commit()

        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect("/")
    except Exception as e:
        flash(f'Error submitting form: {str(e)}', 'error')
        return redirect("/")

@app.route('/admin')
def admin():
    cursor.execute("SELECT name, email, phone, message FROM contact_queries ORDER BY id DESC")
    results = cursor.fetchall()
    return render_template("admin.html", queries=results)

if __name__ == '__main__':
    app.run(debug=True)

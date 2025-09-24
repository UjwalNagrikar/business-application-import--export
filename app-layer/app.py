from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# RDS MySQL details
rds_host = "database-1.c58kc82qa65f.ap-south-1.rds.amazonaws.com"  # Replace with your RDS endpoint
rds_user = "admin"                             # RDS username
rds_password = "Ujwal9494"                     # RDS password
database = "database-1"

try:
    # Step 1: Connect to RDS without specifying a database
    db = mysql.connector.connect(
        host=rds_host,
        user=rds_user,
        password=rds_password
    )
    cursor = db.cursor()
    print("✅ Connected to RDS MySQL instance successfully!")

    # Step 2: Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    print(f"✅ Database '{database}' is ready!")

    # Step 3: Connect to the newly created database
    db.database = database
    print(f"✅ Connected to database '{database}' successfully!")

    # Step 4: Create table if not exists
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
    print("✅ Table 'contact_queries' is ready!")

except Error as e:
    print("❌ RDS connection or setup failed:", e)


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

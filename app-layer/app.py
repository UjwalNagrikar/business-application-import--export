from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Connect to MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="un_trade"
    )
    cursor = db.cursor()
    print("✅ MySQL connection successful!")
except Error as e:
    print("❌ MySQL connection failed:", e)

# Routes
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

        # Basic validation
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
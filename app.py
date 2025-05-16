from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# === DATABASE CONFIGURATION ===
DB_CONFIG = {
    'host': 'orionhealthdb.cdl8ve71qmkj.us-east-1.rds.amazonaws.com',
    'database': 'postgres',
    'user': 'Rimisha',
    'password': 'qQJ=Wv*{5|61'
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# === ROUTES ===

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients;")
    patients = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['date_of_birth']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (first_name, last_name, dob, gender, address, phone, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['date_of_birth']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']

        cur.execute("""
            UPDATE patients SET first_name = %s, last_name = %s, date_of_birth = %s,
                             gender = %s, address = %s, phone = %s, email = %s
            WHERE id = %s;
        """, (first_name, last_name, dob, gender, address, phone, email, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home'))

    cur.execute("SELECT * FROM patients WHERE id = %s;", (id,))
    patient = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit.html', patient=patient)

@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
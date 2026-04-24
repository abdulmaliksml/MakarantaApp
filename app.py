import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

# Tabbatar Python yana aiki a folder din MakarantaApp
os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)

def saita_database():
    conn = sqlite3.connect('makaranta.db')
    cursor = conn.cursor()
    # Table din dalibai
    cursor.execute('''CREATE TABLE IF NOT EXISTS dalibai 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, suna TEXT, reg_no TEXT, level TEXT)''')
    
    # Saka bayanan ka na asali idan babu su
    cursor.execute("SELECT * FROM dalibai WHERE reg_no='UG24/CSED/1021'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO dalibai (suna, reg_no, level) VALUES (?, ?, ?)", 
                       ("ABDULMALIK MUHAMMAD ABBAS", "UG24/CSED/1021", "200L"))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html', admin_name="Abdulmalik Muhammad Abbas")

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    suna = request.form.get('full_name').upper()
    reg = request.form.get('reg_no').upper()
    lvl = request.form.get('level')
    
    conn = sqlite3.connect('makaranta.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dalibai (suna, reg_no, level) VALUES (?, ?, ?)", (suna, reg, lvl))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/duba', methods=['POST'])
def duba():
    reg = request.form.get('reg_number').upper()
    conn = sqlite3.connect('makaranta.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dalibai WHERE reg_no=?", (reg,))
    student = cursor.fetchone()
    conn.close()
    
    courses = [
        {"code": "PHY102", "title": "General Physics II"},
        {"code": "CSC201", "title": "Computer Programming I"},
        {"code": "CSC203", "title": "Discrete Structures"},
        {"code": "CSC211", "title": "Introduction to Software Engineering"},
        {"code": "EDU2201", "title": "Introduction To Educational Psychology"},
        {"code": "ENT211", "title": "Entrepreneurship and Innovation"},
        {"code": "ICT211", "title": "Digital Logic Design"},
        {"code": "ICT212", "title": "Computer Architecture and Organisation"},
        {"code": "MTH2301", "title": "Mathematical Methods"}
    ]
    
    if student:
        return render_template('dashboard.html', student=student, courses=courses)
    return "<h1>User Not Found!</h1><a href='/'>Go Back</a>"

if __name__ == '__main__':
    saita_database()
    app.run(host='0.0.0.0', port=5000, debug=True)

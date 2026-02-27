from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def setup_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    
    cursor.execute('''
        CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            secret_key TEXT
        )
    ''')
    
    userdata = [
        ('admin', 'password123', 'B93CCR45TGG'),
        ('user123', 'dontlookatme123', 'B92RC44YT71'),
        ('basea41', 'asdasd2003', 'B94EFR4BT6G')
    ] 
    
    cursor.executemany("INSERT INTO users (username, password, secret_key) VALUES (?, ?, ?)", userdata)
    connection.commit()
    connection.close()
    
setup_database()

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Secure Login Portal</title></head>
<body style="text-align:center; padding-top:50px; font-family:sans-serif;">
    <h2>System Login Panel</h2>
    <form action="/login" method="POST" style="border:1px solid #ccc; display:inline-block; padding:20px;">
        Username: <br><input type="text" name="username"><br><br>
        Password: <br><input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    <p style="color:gray;"><i>Tip: Try to login as 'admin' using an injection payload!</i></p>
</body>
</html>
"""

@app.route('/')
def home():
    return LOGIN_PAGE

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            return f"""
                <h2 style='color:green;'>Login Successful!</h2>   
                <p>Welcome, <b>{user[1]}</b></p>
                <p><b>Your Secret Key:</b> {user[3]}</p>
                <a href='/'Log Out</a>
                """
        else:
            return "<h2 style='color:red;'>Incorrect username or password!</h2><a href='/'>TRY AGAIN</a>"

    except Exception as exc:    
        return f"<h3>Database Error:</h3><p>{str(exc)}</p><a href='/'>Go Back</a>"
    finally:
        connection.close()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)           
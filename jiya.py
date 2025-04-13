from flask import Flask, request, jsonify
import mysql.connector
import hashlib
# import Login
import logging


from flask import Flask, request, jsonify, make_response
import mysql.connector
import bcrypt
import jwt
import datetime
import logging
import hashlib
import psycopg2
# import AddUser
# import Login
import requests
# import UpdateImage

app = Flask(__name__)

# Configure DB connection
db_config_g1 = {
    'host': '10.0.116.125',        # Use your DB server IP
    'user': 'cs432g1',             # Your DB username
    'password': '1234',        # Your DB password
    'database': 'cs432g1'          # Your DB name
}

db_config_cims = {
    'host': '10.0.116.125',        # Use your DB server IP
    'user': 'cs432g1',             # Your DB username
    'password': '1234',        # Your DB password
    'database': 'cs432cims'          # Your DB name
}

app.config['SECRET_KEY'] = "CS"

def get_db_connection(cims = True):
    """Establish a database connection."""
    if cims:
        return mysql.connector.connect(**db_config_cims)
    else:
        return mysql.connector.connect(**db_config_g1)

@app.route('/addMember', methods=['POST'])
def add_member():
    data = request.get_json()
    print("hello")
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')

    if not username or not email or not dob:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = mysql.connector.connect(**db_config_cims)

        cursor = conn.cursor()

        # 1. Insert into members
        insert_member = """
            INSERT INTO members (UserName, emailID, DoB)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_member, (username, email, dob))
        conn.commit()

        # 2. Get the new member's ID
        member_id = cursor.lastrowid

        # 3. Insert into Login with default password
        insert_login = """
            INSERT INTO Login (MemberID, Password, Role)
            VALUES (%s, %s, %s)
        """
        default_password = hashlib.md5(data.get('password', '').encode()).hexdigest()  # You can hash this later
        # default_password = data.get('password', '')  # You can hash this later
        cursor.execute(insert_login, (member_id, default_password, 'member'))
        conn.commit()

        return jsonify({
            'message': 'Member and login created successfully',
            'member_id': member_id
        }), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = mysql.connector.connect(**db_config_cims)
        cursor = conn.cursor(dictionary=True)

        # Hash the password
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Check credentials

        # Fetch MemberID from members table using the username
        cursor.execute("SELECT ID FROM members WHERE UserName = %s", (username,))
        member = cursor.fetchone()

        if not member:
            return jsonify({'error': 'User not found'}), 404

        member_id = member['ID']

        # Check credentials in Login table
        cursor.execute("SELECT * FROM Login WHERE MemberID = %s AND Password = %s", (member_id, hashed_password))
        user = cursor.fetchone()

        if user:
            token = jwt.encode({
                'user_id': str(user['MemberID']),
                # 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Test route
@app.route('/', methods=['GET'])
def hello():
    return 'API is running!'

if __name__ == '__main__':
    # conn = mysql.connector.connect(**db_config)
    # print("connected to DB")
    app.run(host='0.0.0.0', port=5000)

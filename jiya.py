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

# import logging

# Set up logging configuration
# logging.basicConfig(level=logging.DEBUG)

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


# add member endpoint: creates entry  in the main cims member table also creates a login table entry
@app.route('/addMember', methods=['POST'])
def add_member():
    data = request.get_json()
    # print("hello")
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')
    password = data.get('password')
    contact_no = data.get('contact_no')
    age = data.get('age')
    profile_image = data.get('profile_image')
    role = data.get('role')

    if not username or not email or not dob:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = mysql.connector.connect(**db_config_cims)
        conn2 = mysql.connector.connect(**db_config_g1)

        cursor = conn.cursor()
        cursor2 = conn2.cursor()

        # 1. Insert into members
        insert_member = """
            INSERT INTO members (UserName, emailID, DoB)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_member, (username, email, dob))
        conn.commit()
        
        # 2. Get the new member's ID
        member_id = cursor.lastrowid

        insert_member_ext = """
            INSERT INTO memberExt (Name, Member_ID, Email, Password, Contact_No, Age, Role) VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor2.execute(insert_member_ext, (username, member_id, email, password, contact_no, age, role))
        conn2.commit()

        insert_mapping = """
            INSERT INTO MemberGroupMapping (MemberId, GroupId)
            VALUES (%s, %s)
        """
        cursor.execute(insert_mapping, (member_id, 1))
        conn.commit()

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
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()


@app.route('/addAdmin', methods=['POST'])
def add_admin():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')
    password = data.get('password')

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
        cursor.execute(insert_login, (member_id, default_password, 'admin'))
        conn.commit()

        return jsonify({
            'message': 'Admin and login created successfully',
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

# login endpoint: checks the credentials of the user and returns a token
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
            # Generate token
            token = jwt.encode({
                'user_id': str(user['MemberID']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            # Update session and expiry in the Login table
            session_expiry = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()
            cursor.execute(
                "UPDATE Login SET Session = %s, Expiry = %s WHERE MemberID = %s",
                (token, session_expiry, member_id)
            )
            conn.commit()

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

@app.route('/deleteMember', methods=['DELETE'])
def delete_member():
    print("here")
    token = request.headers.get('Authorization')  # Bearer <token>
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Authorization token missing or malformed'}), 401

    token = token.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        admin_id = decoded['user_id']  # This is the admin's ID, not the member to be deleted

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validate session and role for the admin (not the member being deleted)
        cursor.execute("SELECT Role, Session FROM Login WHERE MemberID = %s", (admin_id,))
        login_info = cursor.fetchone()

        print("login_info", login_info["Session"])
        print("token", token)

        if not login_info or login_info['Session'] != token or login_info['Role'] != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        member_to_delete = data.get('member_id')

        if not member_to_delete:
            return jsonify({'error': 'member_id is required'}), 400
        
        # Fetch email of the member to delete
        cursor.execute("SELECT emailID FROM members WHERE ID = %s", (member_to_delete,))
        user_row = cursor.fetchone()

        if not user_row:
            return jsonify({'error': 'Member not found'}), 404

        email_to_delete = user_row['emailID']

        # Delete from memberExt using email
        conn2 = get_db_connection(cims=False)
        cursor2 = conn2.cursor()
        cursor2.execute("DELETE FROM memberExt WHERE Email = %s", (email_to_delete,))
        conn2.commit()

        # Delete from Login table
        cursor.execute("DELETE FROM Login WHERE MemberID = %s", (member_to_delete,))
        conn.commit()

        # Delete from members table
        cursor.execute("DELETE FROM members WHERE ID = %s", (member_to_delete,))
        conn.commit()

        return jsonify({'message': 'Member deleted successfully'}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()



# Test route
@app.route('/', methods=['GET'])
def hello():
    return 'API is running!'

if __name__ == '__main__':
    # conn = mysql.connector.connect(**db_config)
    # print("connected to DB")
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)

import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (username, email, password_hash))
    conn.commit()

    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """ select * from users where email = %s """
    
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return user
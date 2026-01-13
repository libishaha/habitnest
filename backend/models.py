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

def create_task(user_id, task_text, task_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
                INSERT INTO daily_tasks(user_id, task_text, task_date, completed)
                VALUES(%s, %s, %s, FALSE)
            """
    
    cursor.execute(query, (user_id, task_text, task_date))
    conn.commit()
    
    task_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    
    return task_id

def get_tasks_by_date(user_id, task_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """ select id, task_text, task_date, completed, created_at
                from daily_tasks
                where user_id = %s and task_date = %s
                order by created_at desc
            """
    
    cursor.execute(query, (user_id, task_date))
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return tasks

def toggle_task_complete(task_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    check_query = """ select completed from daily_tasks where id = %s and user_id = %s """
    cursor.execute(check_query,(task_id, user_id))
    result = cursor.fetchone()
    
    if not result:
        cursor.close()
        conn.close()
        return False
    
    current_status = result[0]
    new_status = not current_status
    
    query = """update daily_tasks set completed = %s where id = %s and user_id = %s"""
    cursor.execute(query, (new_status, task_id, user_id))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return True